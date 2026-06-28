import 'dart:io';

import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';
import 'package:flutter/cupertino.dart';
import 'package:my_project/providers/photo_provider.dart';
import 'package:my_project/utils/current_time_utils.dart';
import 'package:ultralytics_yolo/ultralytics_yolo.dart';
import 'package:ultralytics_yolo/widgets/yolo_controller.dart';

import '../models/photo_model.dart';
import '../utils/capture_util.dart';
import '../utils/detect_validator.dart';
import '../utils/flashlight_util.dart';
import '../utils/image_crop_util.dart';
import '../utils/location_utils.dart';
import '../utils/ocr_util.dart';

class DetectProvider with ChangeNotifier {
  PhotoProvider? _photoProvider;
  void setPhotoProvider(PhotoProvider provider) {
    _photoProvider = provider;
  }

  final controller = YOLOViewController();

  bool _isDevMode = false;
  bool get isDevMode => _isDevMode;

  String _selectedYoloModel = ''; // 預設值
  String get selectedYoloModel => _selectedYoloModel;

  bool _isCameraActive = false; //  新增相機狀態
  bool get isCameraActive => _isCameraActive;

  bool _ocrSuccess = false;
  bool get ocrSuccess => _ocrSuccess;

  // 記錄已經成功捕捉過並完成 5 秒序列的物件 ID
  final Set<int> _capturedTrackIds = {};

  void changeModel(String modelPath) {
    controller.switchModel(modelPath, YOLOTask.detect);
  }

  void toggleDevMode() {
    _isDevMode = !_isDevMode;
    notifyListeners();
  }

  // 📷 切換相機按鈕狀態
  void toggleCamera() {
    _isCameraActive = !_isCameraActive;
    debugPrint("📸 Camera active: $_isCameraActive");

    if (_isCameraActive) {
      // ✅ 啟用 YOLO 模型
      changeModel("redline_plus_int8");
      debugPrint("🚀 啟用 YOLO 模型：$_selectedYoloModel");
    } else {
      // ❌ 關閉模型或停止動作
      debugPrint("🛑 停止 YOLO 模型");
      changeModel("");
    }

    notifyListeners();
  }

  void setYoloModel(String model) {
    _selectedYoloModel = model;
    debugPrint("🧠 已選擇 YOLO 模型：$_selectedYoloModel");
    changeModel(_selectedYoloModel);
    notifyListeners();
  }

  // 取得 GPS 跟地址
  String? latString;
  String? lngString;
  String? address;
  Future<void> fetchLocation() async {
    try {
      Position pos = await LocationUtils.getCurrentPosition();
      latString = pos.latitude.toString();
      lngString = pos.longitude.toString();
      debugPrint("📍 取得經緯度：lat: $latString, lng: $lngString");
      notifyListeners(); // 先顯示經緯度

      // 再去查地址
      List<Placemark> placemarks = await placemarkFromCoordinates(
        pos.latitude,
        pos.longitude,
      );
      Placemark place = placemarks.first;
      address = "${place.street}, ${place.locality}";
      notifyListeners(); // 更新地址
    } catch (e) {
      debugPrint("⚠️ 取得定位失敗 或 地址失敗：$e");
    }
  }

  String dateTimeString = "";
  // 取得時間
  Future<void> getCurrentTime() async {
    final currentTime = CurrentTimeUtils().getCurrentDateTime();
    dateTimeString = currentTime;
    notifyListeners();
  }

  // 開關手電筒
  bool isFlashlightOn = false;
  Future<void> toggleFlashlight() async {
    try {
      await FlashlightUtil.toggle(controller);
      isFlashlightOn = FlashlightUtil.isOn;
      notifyListeners(); // 通知 UI 更新
    } catch (e) {
      debugPrint("Flashlight toggle error: $e");
    }
  }

  List<YOLOResult> _results = [];
  List<YOLOResult> get results => _results;

  // 更新即時偵測結果
  Future<void> getResult(List<YOLOResult> results, List<int> trackIds) async {
    _results = results;
    notifyListeners();

    // 只要成功檢測到且不在捕捉中，就嘗試開始 5 秒序列
    if (!_isCapturing) {
      final validator = DetectValidator(selectedYoloModel);
      final groups = validator.getValidGroups(results);
      
      if (groups.isNotEmpty) {
        bool shouldTrigger = false;
        int? targetTrackId;

        for (var group in groups) {
          final car = group[1];
          final carIdx = results.indexOf(car);
          if (carIdx != -1 && carIdx < trackIds.length) {
            targetTrackId = trackIds[carIdx];
            // 檢查這個 ID 是否已經完成過 5 秒捕捉
            if (!_capturedTrackIds.contains(targetTrackId)) {
              shouldTrigger = true;
              break;
            }
          }
        }

        if (shouldTrigger) {
          debugPrint("🎯 偵測到有效目標 (ID: $targetTrackId)，開始 5 秒序列...");
          captureImage(targetTrackId);
        }
      }
    }
  }

  // 📸 拍照序列狀態
  bool _isCapturing = false;
  bool get isCapturing => _isCapturing;

  // 📸 執行 5 秒捕捉序列（每秒一張，共 5 張時間序列照片）
  Future<void> captureImage([int? trackId]) async {
    if (_isCapturing) return;
    _isCapturing = true;
    notifyListeners();

    List<File> capturedImages = [];
    List<List<YOLOResult>> resultsSequence = [];

    debugPrint("🎬 開始 5 秒序列捕捉...");
    await fetchLocation(); // 捕捉前先抓位置
    await getCurrentTime();

    for (int i = 0; i < 5; i++) {
      final file = await CaptureUtil.getCapture(controller);
      if (file != null) {
        capturedImages.add(file);
        // 儲存當下的偵測結果副本，確保影像與結果對應
        resultsSequence.add(List.from(_results));
        debugPrint("📸 捕捉第 ${i + 1} 張照片, 偵測到 ${_results.length} 個物件");
      } else {
        debugPrint("⚠️ 第 ${i + 1} 張照片捕捉失敗");
      }
      if (i < 4) {
        await Future.delayed(const Duration(seconds: 1));
      }
    }

    if (capturedImages.isNotEmpty) {
      bool success = await _processSequence(capturedImages, resultsSequence);
      if (success && trackId != null) {
        // 5 秒捕捉並處理成功後，才將 ID 加入跳過清單 (實作「5秒才做物件追蹤的清單跳過」)
        _capturedTrackIds.add(trackId);
        debugPrint("✅ 序列捕捉成功，標記 ID $trackId 為已處理，之後將跳過此物件");
      }
    } else {
      debugPrint("⚠️ 未能捕捉到任何照片");
    }

    _isCapturing = false;
    notifyListeners();
  }

  // 處理捕捉到的 5 秒序列
  Future<bool> _processSequence(List<File> images, List<List<YOLOResult>> resultsList) async {
    final validator = DetectValidator(selectedYoloModel);

    // 1. 尋找所有影格中，車牌 BBox 最大的一張進行 OCR 處理
    double maxPlateArea = -1;
    File? bestImageForOcr;
    YOLOResult? bestPlateResult;

    for (int i = 0; i < images.length; i++) {
      final groups = validator.getValidGroups(resultsList[i]);
      for (final group in groups) {
        final plate = group[0];
        // 使用歸一化寬高計算面積
        final area = plate.normalizedBox.width * plate.normalizedBox.height;
        if (area > maxPlateArea) {
          maxPlateArea = area;
          bestImageForOcr = images[i];
          bestPlateResult = plate;
        }
      }
    }

    if (bestImageForOcr == null || bestPlateResult == null) {
      debugPrint("⚠️ 序列中未發現符合條件的車牌組合 (car + MIU + plate)");
      return false;
    }

    debugPrint("🏆 找到最大車牌 (面積: $maxPlateArea)，進行 OCR 辨識...");

    // 2. 僅對車牌 BBox 最大的一張進行 OCR 處理
    final plateCropForOcr = await ImageCropUtil.cropByNormalizedBox(
      imageFile: bestImageForOcr,
      normalizedBox: bestPlateResult.normalizedBox,
      index: 99, // OCR 專用臨時索引
      expandRatio: 0.25,
    );

    final finalOcrText = await OcrUtil.recognizeText(plateCropForOcr);
    debugPrint("📝 OCR 辨識結果: $finalOcrText");

    if (!OcrUtil.isOcrTextValid(finalOcrText)) {
      debugPrint("❌ OCR 辨識結果無效，不進行後續存檔");
      return false;
    }

    _triggerOcrSuccess();

    // 3. 將序列中的照片存入 PhotoProvider (時間序列照片)
    List<File> allImages = [];
    List<File> allCarImages = [];
    List<File> allPlateImages = [];

    for (int i = 0; i < images.length; i++) {
      final groups = validator.getValidGroups(resultsList[i]);
      if (groups.isNotEmpty) {
        final plate = groups[0][0];
        final car = groups[0][1];

        final plateFile = await ImageCropUtil.cropByNormalizedBox(
          imageFile: images[i],
          normalizedBox: plate.normalizedBox,
          index: i + 1,
          expandRatio: 0.25,
        );

        final carFile = await ImageCropUtil.cropByNormalizedBox(
          imageFile: images[i],
          normalizedBox: car.normalizedBox,
          index: i + 1,
          expandRatio: 0.1,
        );

        allImages.add(images[i]);
        allCarImages.add(carFile);
        allPlateImages.add(plateFile);
      }
    }

    if (allImages.isNotEmpty) {
      final photo = PhotoModel(
        imagePaths: allImages,
        cutCarImagePaths: allCarImages,
        cutLicensePlateImagePaths: allPlateImages,
        date: dateTimeString.isNotEmpty ? dateTimeString : DateTime.now().toString().split('.')[0],
        address: address ?? '未知地點',
        longitude: lngString ?? '',
        latitude: latString ?? '',
        licensePlate: finalOcrText,
      );

      _photoProvider?.addPhoto(photo);
      debugPrint("✅ 已新增序列照片紀錄: $finalOcrText, 共 ${allImages.length} 張照片");
      return true;
    }
    return false;
  }

  void _triggerOcrSuccess() {
    _ocrSuccess = true;
    notifyListeners();
  }

  void clearOcrSuccess() {
    _ocrSuccess = false;
  }
}
