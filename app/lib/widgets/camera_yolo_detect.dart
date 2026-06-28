import 'package:flutter/material.dart';
import 'package:my_project/models/detection.dart';
import 'package:ultralytics_yolo/ultralytics_yolo.dart';
import 'package:provider/provider.dart';

import '../providers/detect_provider.dart';

import '../providers/track_provider.dart';
import '../trackers/centroid_tracker.dart';
import '../utils/permission_utils.dart';
import 'custom_overlay.dart';

class CameraYoloDetect extends StatefulWidget {
  const CameraYoloDetect({super.key});

  @override
  State<CameraYoloDetect> createState() => _CameraYoloDetectState();
}

class _CameraYoloDetectState extends State<CameraYoloDetect> {
  bool isPermissionGranted = false;
  final tracker = CentroidTracker();

  @override
  void initState() {
    super.initState();
    _initPermissionsAndModel();
  }

  Future<void> _initPermissionsAndModel() async {
    final granted = await PermissionUtils.requestCameraPermission();
    if (granted) {
      setState(() => isPermissionGranted = true);
    } else {
      setState(() => isPermissionGranted = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final detect = context.watch<DetectProvider>();
    final track = context.read<TrackProvider>();
    final model = detect.selectedYoloModel;


    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (detect.ocrSuccess) {
        showCustomOverlay(
          context,
          message: "檢測到違規",
        );

        detect.clearOcrSuccess(); // 一定要清掉
      }
    });

    return Stack(
      children: [
        if (!isPermissionGranted)
          Center(child: CircularProgressIndicator())
        else
             YOLOView(
               modelPath: model,
              task: YOLOTask.detect,
              controller: detect.controller,
              showOverlays: false,
              onResult: (results) {

                debugPrint('Found ${results.length} objects!');
                final detections = results.map<Detection>((r) {
                  final box = r.normalizedBox;
                  return Detection(
                    label: r.className,
                    score: (r.confidence).toDouble(),
                    left: box.left.toDouble(),
                    top: box.top.toDouble(),
                    right: box.right.toDouble(),
                    bottom: box.bottom.toDouble(),
                  );
                }).toList();

                final trackIds = track.updateDetections(detections); //更新物件追中

                for (final result in results) {
                  debugPrint('${result.className}: ${result.confidence}');
                  debugPrint('this is bounding box: ${result.boundingBox}');

                }
                detect.getResult(results, trackIds);
              },
              ),

      ]);


  }
}



