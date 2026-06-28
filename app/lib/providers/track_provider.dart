import 'package:flutter/material.dart';
import 'package:my_project/providers/detect_provider.dart';
import '../models/detection.dart';
import '../trackers/centroid_tracker.dart';

class TrackProvider with ChangeNotifier {

  DetectProvider? _detectProvider;
  void setDetect(DetectProvider detectProvider) {
    _detectProvider = detectProvider;
  }



  final CentroidTracker _tracker = CentroidTracker();
  // 用來記錄目前畫面上的 Track IDs
  final Set<int> _currentTrackIds = {};
  List<Track> get tracks => _tracker.tracks;

  List<int> updateDetections(List<Detection> detections) {
    final assignedIds = _tracker.update(detections);
    notifyListeners();
    return assignedIds;
  }

  /// 當偵測到新物件出現時觸發
  void _onNewObjectDetected(Track track) async {
    // 觸發邏輯已移至 DetectProvider，根據驗證結果決定是否捕捉
  }

  void reset() {
    _tracker.reset();
    _currentTrackIds.clear();
    notifyListeners();
  }
}

