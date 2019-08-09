from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CameraAnnotation


class CameraAnnotationCreateForm(forms.ModelForm):
    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data

    class Meta:
        model = CameraAnnotation
        fields = ['timestamp', 'annotation', 'status', 'note']
        widgets = {
            'timestamp': forms.TextInput(attrs={
                'id': 'form-timestamp',
                'required': True,
                'placeholder': '00:00:00:00',
                'readonly': True,
                'style': 'font-family: "Roboto Mono", serif; text-align: center; display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 3px; height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 15%; min-width: 120px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 3px; height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 22%;',
            }),
        }


class CameraAnnotationEditForm(forms.ModelForm):
    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data

    class Meta:
        model = CameraAnnotation
        fields = ['timestamp', 'annotation', 'status', 'note']
