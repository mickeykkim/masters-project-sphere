from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation
from .forms import WearableAnnotationForm, CameraAnnotationForm
import xlwt


def download_excel_data(request):
	# content-type of response
	response = HttpResponse(content_type='application/ms-excel')

	#decide file name
	response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xls"'

	#creating workbook
	wb = xlwt.Workbook(encoding='utf-8')

	#adding sheet
	ws = wb.add_sheet("sheet1")

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	# headers are bold
	font_style.font.bold = True

	#column header names, you can use your own headers here
	columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4', ]

	#write column headers in sheet
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	#get your data, from database or from a text file...
	data = get_data() #dummy method to fetch data.
	for my_row in data:
		row_num = row_num + 1
		ws.write(row_num, 0, my_row.name, font_style)
		ws.write(row_num, 1, my_row.start_date_time, font_style)
		ws.write(row_num, 2, my_row.end_date_time, font_style)
		ws.write(row_num, 3, my_row.notes, font_style)

	wb.save(response)
	return response


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


class CreateWearableAnnotationView(generic.CreateView):
   model = WearableAnnotation
   form_class = WearableAnnotationForm
   template_name = 'sensors/wearabledata_detail.html'
   success_url = 'sensors/wearabledata_detail.html'


class CreateAnnotationView(generic.CreateView):
   model = CameraAnnotation
   form_class = CameraAnnotationForm
   template_name = 'sensors/cameradata_detail.html'
   success_url = 'sensors/cameradata_detail.html'
