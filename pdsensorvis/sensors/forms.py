from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import CameraAnnotation, CameraAnnotationComment


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
                'default': '00:00:00:00',
                'readonly': True,
                'style': 'font-family: "Roboto Mono", serif; text-align: center; display: table-cell; vertical-align: '
                         'top; border: 1px solid #a0a0a0; border-radius: 3px; height: 30px; line-height: 30px; '
                         'margin: 0px 0px 0px 0px; width: 14%; min-width: 130px;',
            }),
            'annotation': forms.Select(attrs={
                'id': 'form-annotation',
                'required': True,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 6px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 22%; min-width: 145px;',
            }),
            'note': forms.TextInput(attrs={
                'id': 'form-note',
                'required': False,
                'style': 'display: table-cell; vertical-align: top; border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 30px; line-height: 30px; margin: 0px 0px 0px 0px; width: 17%;',
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
        fields = ['timestamp', 'annotation', 'status', 'note']


class CameraAnnotationCommentCreateForm(forms.ModelForm):
    """
    def clean_text(self):
        data = self.cleaned_data['text']

        if not data:
            raise ValidationError(_('Comment cannot be blank.'))

        return data
    """

    class Meta:
        model = CameraAnnotationComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'form-text',
                'required': False,
                'style': 'border: 1px solid #a0a0a0; border-radius: 3px; '
                         'height: 150px; width: 90%; box-sizing: border-box; background-color: #f8f8f8;',
            }),
        }
