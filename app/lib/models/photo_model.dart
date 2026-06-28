import 'dart:io';

class PhotoModel {
  final List<File> imagePaths;
  final List<File> cutCarImagePaths;
  final List<File> cutLicensePlateImagePaths;
  final String date;
  final String address;
  final String longitude;
  final String latitude;
  final String licensePlate;

  PhotoModel({
    required this.imagePaths,
    required this.cutCarImagePaths,
    required this.cutLicensePlateImagePaths,
    required this.date,
    required this.address,
    required this.longitude,
    required this.latitude,
    required this.licensePlate,
  });
}
