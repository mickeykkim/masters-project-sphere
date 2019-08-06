from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import UPDRS_TASK, ANNOTATION_STATUS


class AnnotationForm(forms.ModelForm):
    timestamp = forms.CharField(help_text='hh:mm:ss:ff')
    annotator = forms.ModelChoiceField(queryset=User.objects.all())
    annotation = forms.ChoiceField(choices=UPDRS_TASK)
    status = forms.ChoiceField(choices=ANNOTATION_STATUS)
    note = forms.CharField(help_text='Note regarding annotation', required=False)

    def clean_annotation(self):
        data = self.cleaned_data['annotation']

        if not data:
            raise ValidationError(_('Annotation cannot be blank.'))

        return data
