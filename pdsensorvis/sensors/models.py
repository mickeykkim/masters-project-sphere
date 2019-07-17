from django.db import models
from django.urls import reverse
import uuid
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .preprocess_data import Preprocess

# Create your models here.
class PatientData(models.Model):
   """Fields and Functions related to each patient"""

   # Fields
   id = models.AutoField(primary_key=True)
   first_name = models.CharField(max_length=50, help_text='Patient first name')
   last_name = models.CharField(max_length=50, help_text='Patient last name')
   date_of_birth = models.DateField()
   notes = models.CharField(max_length=500, help_text='Notes regarding patient')

   # Metadata
   class Meta: 
      ordering = ['last_name']

   # Methods
   def get_absolute_url(self):
      return reverse('patientdata-detail', args=[str(self.id)])
   
   def __str__(self):
      return f'{self.last_name}, {self.first_name}'


class WearableData(models.Model):
   """Data related to wristworn wearable"""

   # Fields
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this wearable data')
   patient = models.ForeignKey('PatientData', on_delete=models.SET_NULL, null=True)
   filename = models.FileField(upload_to='wearable/')
   time = models.DateTimeField()

   # Metadata
   class Meta: 
      ordering = ['patient', '-time']

   # Methods
   def get_absolute_url(self):
      return reverse('wearabledata-detail', args=[str(self.id)])
   
   def __str__(self):
      return f'{self.patient} - {self.time}'

class CameraData(models.Model):
   """Data related to silhouette camera"""

   # Fields
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this wearable data')
   patient = models.ForeignKey('PatientData', on_delete=models.SET_NULL, null=True)
   filename = models.FileField(upload_to='camera/')
   time = models.DateTimeField()

   # Metadata
   class Meta: 
      ordering = ['patient', '-time']

   # Methods
   def get_absolute_url(self):
      return reverse('cameradata-detail', args=[str(self.id)])
   
   def __str__(self):
      return f'{self.patient} - {self.time}'

   def media_path(self):
      return settings.MEDIA_ROOT


class WearableAnnotation(models.Model):
   """Fields and Functions related to wearable annotations"""

   # Fields
   id = models.AutoField(primary_key=True)
   wearable = models.ForeignKey('WearableData', on_delete=models.SET_NULL, null=True)
   timestamp = models.TimeField()
   annotator = models.CharField(max_length=50, help_text='Annotator of data')

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

   annotation = models.CharField(
      max_length=3,
      choices=UPDRS_TASK,
      blank=True,
      default='prs',
      help_text='UPDRS Task',
   )

   class Meta:
      ordering = ['-timestamp']

   def __str__(self):
      """String for representing the Model object."""
      return f'{self.wearable} - {self.timestamp} - {self.annotation}'


class CameraAnnotation(models.Model):
   """Fields and Functions related to camera annotations"""

   # Fields
   id = models.AutoField(primary_key=True)
   camera = models.ForeignKey('CameraData', on_delete=models.SET_NULL, null=True)
   timestamp = models.TimeField()
   annotator = models.CharField(max_length=50, help_text='Annotator of data')

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

   annotation = models.CharField(
      max_length=3,
      choices=UPDRS_TASK,
      blank=True,
      default='prs',
      help_text='UPDRS Task',
   )

   class Meta:
      ordering = ['-timestamp']

   def __str__(self):
      """String for representing the Model object."""
      return f'{self.camera} - {self.timestamp} - {self.annotation}'
