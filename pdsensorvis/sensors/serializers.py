from rest_framework import serializers
from .models import (
    PatientData,
    WearableData,
    CameraData,
    WearableAnnotation,
    CameraAnnotation,
)


class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientData
        fields = ("id", "first_name", "last_name", "notes")


class WearableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WearableData
        fields = ("id", "patient", "filename", "time")


class CameraDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraData
        fields = ("id", "patient", "filename", "time")


class WearableAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WearableAnnotation
        fields = ("id", "wearable", "timestamp", "annotation")


class CameraAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAnnotation
        fields = ("id", "camera", "timestamp", "annotation")
