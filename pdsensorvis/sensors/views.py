from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation
from .serializers import * 


def index(request):
   """View function for sensor index site."""

   # Generate counts of some of the main objects
   num_patients = PatientData.objects.all().count()
   num_wearables = WearableData.objects.all().count()
   num_cameras = CameraData.objects.all().count()
   num_wearable_annotations = WearableAnnotation.objects.all().count()
   num_camera_annotations = CameraAnnotation.objects.all().count()

   # Available books (status = 'a')
   # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

   context = {
      'num_patients': num_patients,
      'num_wearables': num_wearables,
      'num_cameras': num_cameras,
      'num_wearable_annotations': num_wearable_annotations,
      'num_camera_annotations': num_camera_annotations,
   }

   # Render the HTML template index.html with the data in the context variable
   return render(request, 'index.html', context=context)


@api_view(['GET', 'POST'])
def patientdata_list(request):
   """
   List or create new patient data.
   """
   if request.method == 'GET':
      data = []
      nextPage = 1
      previousPage = 1
      patients = PatientData.objects.all()
      page = request.GET.get('page', 1)
      paginator = Paginator(patients, 10)
      try:
         data = paginator.page(page)
      except PageNotAnInteger:
         data = paginator.page(1)
      except EmptyPage:
         data = paginator.page(paginator.num_pages)

      serializer = PatientDataSerializer(data,context={'request': request} ,many=True)
      if data.has_next():
         nextPage = data.next_page_number()
      if data.has_previous():
         previousPage = data.previous_page_number()

      return Response({'data': serializer.data, 
                       'count': paginator.count, 
                       'numpages' : paginator.num_pages, 
                       'nextlink': '/patients/?page=' + str(nextPage), 
                       'prevlink': '/patients/?page=' + str(previousPage)})

   elif request.method == 'POST':
      serializer = PatientDataSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def patientdata_detail(request, pk):
   """
   Retrieve, update or delete a patient data instance.
   """
   try:
      patient = PatientData.objects.get(pk=pk)
   except PatientData.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method == 'GET':
      serializer = PatientDataSerializer(patient, context={'request': request})
      return Response(serializer.data)

   elif request.method == 'PUT':
      serializer = PatientDataSerializer(patient, data=request.data, context={'request': request})
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   elif request.method == 'DELETE':
      patient.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
