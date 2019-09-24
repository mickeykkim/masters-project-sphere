from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CameraAnnotation, CameraAnnotationComment, WearableData


class CameraAnnotationCreateForm(forms.ModelForm):
    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data

    class Meta:
        model = CameraAnnotation
        fields = ['time_begin', 'time_end', 'annotation', 'note',
                  'frame_begin', 'frame_end', 'ms_time_begin', 'ms_time_end']
        widgets = {
            'time_begin': forms.TextInput(attrs={
                'id': 'form-time-begin',
                'required': True,
                'default': '00:00:00:00',
                'readonly': True,
                'style': 'font-family: "Roboto Mono", serif; text-align: center; display: table-cell; vertical-align: '
                         'top; border: 1px solid #a0a0a0; border-radius: 3px; height: 30px; line-height: 30px; '
                         'margin: 0px 0px 0px 0px; width: 14%; min-width: 150px; background-color: #f8f8f8;',
            }),
            'time_end': forms.TextInput(attrs={
                'id': 'form-time-end',
                'required': True,
                'default': '00:00:00:00',
                'readonly': True,
                'style': 'font-family: "Roboto Mono", serif; text-align: center; display: table-cell; vertical-align: '
                         'top; border: 1px solid #a0a0a0; border-radius: 3px; height: 30px; line-height: 30px; '
                         'margin: 0px 0px 0px 0px; width: 14%; min-width: 150px; background-color: #f8f8f8;',
            }),
            'annotation': forms.Select(attrs={
                'id': 'form-annotation',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25.5%; min-width: 190px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 190px;',
            }),
            'status': forms.Select(attrs={
                'id': 'form-annotation',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 5%; min-width: 45px;',
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
        fields = ['time_begin', 'time_end', 'annotation', 'note']


class CameraAnnotationCommentCreateForm(forms.ModelForm):
    class Meta:
        model = CameraAnnotationComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 150px; width: 90%; box-sizing: border-box; background-color: #f8f8f8;',
            }),
        }


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    filename = forms.FileField()


class WearableDataCreateForm(forms.ModelForm):
    class Meta:
        model = WearableData
        fields = ['filename', 'note', 'time']
        widgets = {
            'note': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #a0a0a0; border-radius: 3px; margin: 10px 0 0 0; '
                         'height: 100px; width: 100%; box-sizing: border-box; background-color: #f8f8f8;',
            }),
            'time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'required': True,
                'data-target': '#datetimepicker1',
            }),
        }
