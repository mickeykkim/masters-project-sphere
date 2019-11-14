from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import WearableAnnotation, CameraAnnotation, CameraAnnotationComment, WearableData, CameraData, PatientData


class PatientDataCreateForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = ['first_name', 'last_name', 'date_of_birth', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 50%; min-width: 350px;',
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 50%; min-width: 350px;',
            }),
            'date_of_birth': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'required': True,
                'data-target': '#datetimepicker1',
            }),
            'notes': forms.Textarea(attrs={
                'id': 'form-text',
                'required': False,
                'style': 'border: 1px solid #D3D3D3; border-radius: 3px; margin: 2px 0 0 0; '
                         'height: 100px; width: 100%; box-sizing: border-box;'
            }),
        }


class PatientDataEditForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = ['first_name', 'last_name', 'date_of_birth', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 70%; min-width: 350px;'
                         'background-color: #f8f8f8;',
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 70%; min-width: 350px;'
                         'background-color: #f8f8f8;',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 70%; min-width: 350px;'
                         'background-color: #f8f8f8;',
            }),
            'notes': forms.Textarea(attrs={
                'id': 'form-text',
                'required': False,
                'style': 'border: 1px solid #D3D3D3; border-radius: 3px; margin: 3px 0 0 0; width: 100%; '
                         'min-width: 190px; height: 100px; box-sizing: border-box; background-color: #f8f8f8;',
            }),
        }


class WearableDataCreateForm(forms.ModelForm):
    class Meta:
        model = WearableData
        fields = ['filename', 'note', 'time']
        widgets = {
            'note': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #D3D3D3; border-radius: 3px; margin: 3px 0 0 0; '
                         'height: 100px; width: 100%; box-sizing: border-box; ',
            }),
            'time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'required': True,
                'data-target': '#datetimepicker1',
            })
        }


class WearableDataEditForm(forms.ModelForm):
    class Meta:
        model = WearableData
        fields = ['note', 'time']
        widgets = {
            'note': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #D3D3D3; border-radius: 3px; margin: 3px 0 0 0; height: 100px; '
                         'width: 100%; min-width: 190px; box-sizing: border-box; background-color: #f8f8f8;',
            }),
            'time': forms.DateTimeInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 100%; min-width: 190px;'
                         'background-color: #f8f8f8;',
            }),
        }


class CameraDataCreateForm(forms.ModelForm):
    class Meta:
        model = CameraData
        fields = ['filename', 'note', 'time', 'framerate']
        widgets = {
            'note': forms.Textarea(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'border: 1px solid #D3D3D3; border-radius: 3px; margin: 3px 0 0 0; '
                         'height: 100px; width: 100%; box-sizing: border-box; ',
            }),
            'time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'required': True,
                'data-target': '#datetimepicker1',
            }),
            'framerate': forms.Select(attrs={
                'id': 'form-framerate',
                'default': 'Film',
                'required': True,
                'style': 'display: table-cell; vertical-align: middle; border: 1px solid #D3D3D3; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 5%; min-width: 45px;',
            }),
        }


class CameraDataEditForm(forms.ModelForm):
    class Meta:
        model = CameraData
        fields = ['note', 'time', 'framerate']
        widgets = {
            'note': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #D3D3D3; border-radius: 3px; margin: 3px 0 0 0; width: 50%; '
                         'min-width: 190px; height: 100px; box-sizing: border-box; background-color: #f8f8f8;',
            }),
            'time': forms.DateTimeInput(attrs={
                'id': 'form-note',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 50%; min-width: 190px;'
                         'background-color: #f8f8f8;',
            }),
            'framerate': forms.Select(attrs={
                'id': 'form-framerate',
                'default': 'Film',
                'required': True,
                'style': 'display: table-cell; vertical-align: middle; border: 1px solid #D3D3D3; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 5%; min-width: 45px;',
            }),
        }


class CameraAnnotationCreateForm(forms.ModelForm):
    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data

    class Meta:
        model = CameraAnnotation
        fields = ['time_begin', 'time_end', 'annotation', 'note', ] # 'frame_begin', 'frame_end', 'ms_time_begin', 'ms_time_end']
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
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 26%; min-width: 190px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 36%; min-width: 250px;',
            })
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
        widgets = {
            'time_begin': forms.TextInput(attrs={
                'id': 'form-time-begin',
                'required': True,
                'style': 'text-align: left; display: table-cell; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 14%; min-width: 190px; '
                         'background-color: #f8f8f8;',
            }),
            'time_end': forms.TextInput(attrs={
                'id': 'form-time-end',
                'required': True,
                'style': 'text-align: left; display: table-cell; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 14%; min-width: 190px; '
                         'background-color: #f8f8f8;',
            }),
            'annotation': forms.Select(attrs={
                'id': 'form-annotation',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25.5%; min-width: 190px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 190px;'
                         'background-color: #f8f8f8;',
            })
        }


class WearableAnnotationCreateForm(forms.ModelForm):
    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data

    class Meta:
        model = WearableAnnotation
        fields = ['frame_begin', 'frame_end', 'annotation', 'note']
        widgets = {
            'frame_begin': forms.TextInput(attrs={
                'id': 'form-time-begin',
                'required': True,
                'style': 'text-align: left; display: table-cell; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 250px; '
                         'background-color: #f8f8f8;',
            }),
            'frame_end': forms.TextInput(attrs={
                'id': 'form-time-end',
                'required': True,
                'style': 'text-align: left; display: table-cell; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 250px; '
                         'background-color: #f8f8f8;',
            }),
            'annotation': forms.Select(attrs={
                'id': 'form-annotation',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 250px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 250px;'
                         'background-color: #f8f8f8;',
            })
        }


class WearableAnnotationEditForm(forms.ModelForm):
    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data

    class Meta:
        model = WearableAnnotation
        fields = ['frame_begin', 'frame_end', 'annotation', 'note']
        widgets = {
            'frame_begin': forms.TextInput(attrs={
                'id': 'form-time-begin',
                'required': True,
                'style': 'text-align: left; display: table-cell; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 190px; '
                         'background-color: #f8f8f8;',
            }),
            'frame_end': forms.TextInput(attrs={
                'id': 'form-time-end',
                'required': True,
                'style': 'text-align: left; display: table-cell; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 190px; '
                         'background-color: #f8f8f8;',
            }),
            'annotation': forms.Select(attrs={
                'id': 'form-annotation',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 190px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #D3D3D3; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 25%; min-width: 190px;'
                         'background-color: #f8f8f8;',
            })
        }


class CameraAnnotationCommentCreateForm(forms.ModelForm):
    class Meta:
        model = CameraAnnotationComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 150px; width: 70%; box-sizing: border-box; background-color: #f8f8f8;',
            }),
        }


class CameraAnnotationCommentEditForm(forms.ModelForm):
    class Meta:
        model = CameraAnnotationComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'form-text',
                'required': True,
                'style': 'border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 150px; width: 100%; box-sizing: border-box; background-color: #f8f8f8;',
            }),
        }


class UploadFileForm(forms.Form):
    filename = forms.FileField(help_text='Filename (.csv only; max size: 42MB)')

