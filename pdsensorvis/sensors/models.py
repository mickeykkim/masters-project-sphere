from django.db import models
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .preprocess_data import Preprocess
import uuid

# User-defined UPDRS tasks
UPDRS_TASK = (
    ('prs', 'prone sup'),
    ('toe', 'toe tapping'),
    ('leg', 'leg agility'),
    ('afc', 'arising from chair'),
    ('tug', 'timed up and go'),
    ('nmp', 'normal pace'),
    ('slp', 'slow pace'),
    ('fsp', 'fast pace'),
)


class PatientData(models.Model):
    """Fields and Functions related to each patient"""

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, help_text='Patient first name')
    last_name = models.CharField(max_length=50, help_text='Patient last name')
    date_of_birth = models.DateField()
    notes = models.CharField(max_length=500, help_text='Notes regarding patient')

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('patientdata-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class WearableData(models.Model):
    """Data related to wristworn wearable"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this wearable data')
    patient = models.ForeignKey('PatientData', on_delete=models.CASCADE, null=True)
    filename = models.FileField(upload_to='wearable/')
    time = models.DateTimeField()
    note = models.CharField(max_length=500, help_text='Note regarding wearable')

    class Meta:
        ordering = ['patient', '-time']

    def get_absolute_url(self):
        return reverse('wearabledata-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.patient} ({self.time})'


class CameraData(models.Model):
    """Data related to silhouette camera"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this wearable data')
    patient = models.ForeignKey('PatientData', on_delete=models.CASCADE, null=True)
    filename = models.FileField(upload_to='camera/')
    time = models.DateTimeField()
    note = models.CharField(max_length=500, help_text='Note regarding camera')

    class Meta:
        ordering = ['patient', '-time']

    def get_absolute_url(self):
        return reverse('cameradata-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.patient} ({self.time})'


class WearableAnnotation(models.Model):
    """Fields and Functions related to wearable annotations"""
    id = models.AutoField(primary_key=True)
    note = models.CharField(max_length=500, help_text='Note regarding annotation', null=True, blank=True)
    wearable = models.ForeignKey('WearableData', on_delete=models.CASCADE, null=True)
    timestamp = models.CharField(max_length=11, help_text='hh:mm:ss:ff')
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    annotation = models.CharField(
        max_length=3,
        choices=UPDRS_TASK,
        blank=True,
        default='prs',
        help_text='UPDRS Task',
    )

    class Meta:
        ordering = ['timestamp']

    def get_absolute_url(self):
        return reverse('wearableannotation-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.wearable} - {self.timestamp} - {self.annotation}'


class CameraAnnotation(models.Model):
    """Fields and Functions related to camera annotations"""
    id = models.AutoField(primary_key=True)
    note = models.CharField(max_length=500, help_text='Note regarding annotation', null=True, blank=True)
    camera = models.ForeignKey('CameraData', on_delete=models.CASCADE, null=True)
    timestamp = models.CharField(max_length=11, help_text='hh:mm:ss:ff')
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    annotation = models.CharField(
        max_length=3,
        choices=UPDRS_TASK,
        blank=True,
        default='prs',
        help_text='UPDRS Task',
    )

    class Meta:
        ordering = ['timestamp']

    def get_absolute_url(self):
        return reverse('cameraannotation-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.camera} - {self.timestamp} - {self.annotation}'
