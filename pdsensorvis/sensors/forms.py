from django import forms
from .models import WearableAnnotation, CameraAnnotation, UPDRS_TASK


class WearableAnnotationForm(forms.ModelForm):
    class Meta:
        model = WearableAnnotation
        fields = ['annotation']


class CameraAnnotationForm(forms.ModelForm):
    class Meta:
        model = CameraAnnotation
        fields = ['annotation']
