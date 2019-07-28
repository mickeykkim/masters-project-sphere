from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation
from .forms import WearableAnnotationForm, CameraAnnotationForm

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


class PatientDataListView(LoginRequiredMixin,generic.ListView):
   model = PatientData
   paginate_by = 10


class PatientDataDetailView(LoginRequiredMixin,generic.DetailView):
   model = PatientData


class WearableDataListView(LoginRequiredMixin,generic.ListView):
   model = WearableData
   paginate_by = 10


class WearableDataDetailView(LoginRequiredMixin,generic.DetailView):
   model = WearableData


class WearableAnnotationDetailView(LoginRequiredMixin,generic.DetailView):
   model = WearableAnnotation


class CameraDataListView(LoginRequiredMixin,generic.ListView):
   model = CameraData
   paginate_by = 10


class CameraDataDetailView(LoginRequiredMixin,generic.DetailView):
   model = CameraData


class CameraAnnotationDetailView(LoginRequiredMixin,generic.DetailView):
   model = CameraAnnotation


class CreateWearableAnnotationView(LoginRequiredMixin,generic.CreateView):
   model = WearableAnnotation
   form_class = WearableAnnotationForm
   template_name = 'sensors/wearabledata_detail.html'
   success_url = 'sensors/wearabledata_detail.html'


class CreateAnnotationView(LoginRequiredMixin,generic.CreateView):
   model = CameraAnnotation
   form_class = CameraAnnotationForm
   template_name = 'sensors/cameradata_detail.html'
   success_url = 'sensors/cameradata_detail.html'
