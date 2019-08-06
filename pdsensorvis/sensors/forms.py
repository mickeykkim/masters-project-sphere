from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CameraAnnotation


class CameraAnnotationForm(forms.ModelForm):
    class Meta:
        model = CameraAnnotation
        fields = ('timestamp', 'annotation', 'status', 'note')

    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data
