from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class PatientData(models.Model):
   """Fields and Functions related to each patient"""

   # Fields
   id = models.AutoField(primary_key=True)
   first_name = models.CharField(max_length=50, help_text='Patient first name')
   last_name = models.CharField(max_length=50, help_text='Patient last name')
   notes = models.CharField(max_length=500, help_text='Notes regarding patient')

   # Metadata
   class Meta: 
      ordering = ['last_name']

   # Methods
   def get_absolute_url(self):
      return reverse('model-detail-view', args=[str(self.id)])
   
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
      return reverse('model-detail-view', args=[str(self.id)])
   
   def __str__(self):
      return f'{self.patient} - {self.time}'


class CameraData(models.Model):
   """Data related to silhouette camera"""

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
      return reverse('model-detail-view', args=[str(self.id)])
   
   def __str__(self):
      return f'{self.patient} - {self.time}'


class WearableAnnotation(models.Model):
   """Fields and Functions related to wearable annotations"""

   # Fields
   id = models.AutoField(primary_key=True)
   wearable = models.ForeignKey('WearableData', on_delete=models.SET_NULL, null=True)
   timestamp = models.TimeField()

   UPDRS_TASK = (
      ('a', 'Task A'),
      ('b', 'Task B'),
      ('c', 'Task C'),
      ('d', 'Task D'),
   )

   annotation = models.CharField(
      max_length=1,
      choices=UPDRS_TASK,
      blank=True,
      default='a',
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

   UPDRS_TASK = (
      ('a', 'Task A'),
      ('b', 'Task B'),
      ('c', 'Task C'),
      ('d', 'Task D'),
   )

   annotation = models.CharField(
      max_length=1,
      choices=UPDRS_TASK,
      blank=True,
      default='a',
      help_text='UPDRS Task',
   )

   class Meta:
      ordering = ['-timestamp']

   def __str__(self):
      """String for representing the Model object."""
      return f'{self.camera} - {self.timestamp} - {self.annotation}'
