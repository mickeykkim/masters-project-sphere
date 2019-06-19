from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation


def index(request):
   """View function for sensor index site."""

   # Generate counts of some of the main objects
   num_patients = PatientData.objects.all().count()
   num_wearables = WearableData.objects.all().count()
   num_cameras = CameraData.objects.all().count()
   num_wearable_annotations = WearableAnnotation.objects.all().count()
   num_camera_annotations = CameraAnnotation.objects.all().count()

   context = {
      'num_patients': num_patients,
      'num_wearables': num_wearables,
      'num_cameras': num_cameras,
      'num_wearable_annotations': num_wearable_annotations,
      'num_camera_annotations': num_camera_annotations,
   }

   # Render the HTML template index.html with the data in the context variable
   return render(request, 'index.html', context=context)


class PatientDataListView(generic.ListView):
   model = PatientData
   paginate_by = 10


class PatientDataDetailView(generic.DetailView):
   model = PatientData


class WearableDataListView(generic.ListView):
   model = WearableData
   paginate_by = 10


class WearableDataDetailView(generic.DetailView):
   model = WearableData


class WearableAnnotationDetailView(generic.DetailView):
   model = WearableAnnotation


class CameraDataListView(generic.ListView):
   model = CameraData
   paginate_by = 10


class CameraDataDetailView(generic.DetailView):
   model = CameraData


class CameraAnnotationDetailView(generic.DetailView):
   model = CameraAnnotation
