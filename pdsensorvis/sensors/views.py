import csv
import xlwt

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views import generic
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation, CameraAnnotationComment
from .forms import CameraAnnotationCreateForm, CameraAnnotationEditForm, CameraAnnotationCommentCreateForm
from uuid import UUID

User = get_user_model()


def is_valid_uuid(uuid_to_test, version=4):
    """Check if uuid_to_test is a valid UUID."""
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def index(request):
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


def search_results(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query is not None:
            if is_valid_uuid(query, 4):
                lookups = Q(pk=query)
            else:
                lookups = Q(patient__first_name__icontains=query) | Q(patient__last_name__icontains=query)
            camera_results = CameraData.objects.filter(lookups)
            wearable_results = WearableData.objects.filter(lookups)
            context = {'cameradata': camera_results, 'wearabledata': wearable_results}
            return render(request, "sensors/search_results.html", context)
        else:
            return render(request, "sensors/search_results.html")

    else:
        return render(request, "sensors/search_results.html")


def edit_camera_annotation(request, uuid, pk):
    existing_annotation = get_object_or_404(CameraAnnotation, pk=pk)

    if request.method == 'POST':
        form = CameraAnnotationEditForm(request.POST, instance=existing_annotation)
        if form.is_valid():
            existing_annotation = form.save(commit=False)
            existing_annotation.annotation = form.cleaned_data['annotation']
            existing_annotation.save()
            return redirect('cameradata-detail', pk=uuid)
    else:
        form = CameraAnnotationEditForm(instance=existing_annotation)

    context = {
        'form': form,
        'cameraannotation': existing_annotation,
    }

    return render(request, 'sensors/edit_camera_annotation.html', context)


def delete_camera_annotation(request, uuid, pk):
    existing_annotation = get_object_or_404(CameraAnnotation, pk=pk)

    if request.method == 'POST':
        existing_annotation.delete()
        return redirect('cameradata-detail', pk=uuid)
    else:
        form = CameraAnnotationEditForm(instance=existing_annotation)

    context = {
        'form': form,
        'cameraannotation': existing_annotation,
    }

    return render(request, 'sensors/edit_camera_annotation.html', context)


def export_annotations_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="annotations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Session ID:', pk])
    writer.writerow(['Timestamp', 'Annotation', 'Status', 'Annotation Note', 'Annotator', 'Comments'])

    annotations = CameraAnnotation.objects.filter(camera_id=pk)

    for annotation in annotations:
        comment_list = CameraAnnotationComment.objects.filter(annotation_id=annotation.id)
        discussion = ""

        for comment in comment_list:
            discussion += comment.author.username + " (" + comment.timestamp.strftime('%d/%m/%Y') + "): " + \
                          comment.text + "\n"

        writer.writerow([annotation.timestamp, annotation.get_annotation_display(), annotation.get_status_display(),
                         annotation.note, annotation.annotator.username, discussion, ])

    return response


def export_annotations_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="annotations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Session ID:', pk, ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet headers
    row_num = 1
    columns = ['Timestamp', 'Annotation', 'Status', 'Annotation Note', 'Annotator', 'Comments', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    annotations = CameraAnnotation.objects.filter(camera_id=pk)

    for annotation in annotations:
        row_num += 1
        comment_list = CameraAnnotationComment.objects.filter(annotation_id=annotation.id)
        discussion = ""

        for comment in comment_list:
            discussion += comment.author.username + " (" + comment.timestamp.strftime('%d/%m/%Y') + "): " + \
                          comment.text + "\n"

        items = [annotation.timestamp, annotation.get_annotation_display(), annotation.get_status_display(),
                 annotation.note, annotation.annotator.username, discussion, ]

        for col_num in range(len(items)):
            ws.write(row_num, col_num, items[col_num], font_style)

    wb.save(response)
    return response


class CameraDataDetailGet(LoginRequiredMixin, generic.DetailView):
    model = CameraData

    def get_context_data(self, **kwargs):
        context = super(CameraDataDetailGet, self).get_context_data(**kwargs)
        context['form'] = CameraAnnotationCreateForm(initial=self.request.session.get('form_data'))
        return context


class CameraDataDetailView(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        view = CameraDataDetailGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, pk):
        current_camera = get_object_or_404(CameraData, pk=pk)

        form = CameraAnnotationCreateForm(request.POST)

        if form.is_valid():
            self.request.session['form_data'] = form.cleaned_data
            new_annotation = form.save(commit=False)
            new_annotation.camera = current_camera
            new_annotation.annotator = request.user
            new_annotation.annotation = form.cleaned_data['annotation']
            new_annotation.save()
            return redirect('cameradata-detail', pk=pk)
        else:
            print(form.errors)

        context = {
            'form': form,
            'cameradata': current_camera
        }

        return render(request, 'sensors/cameradata_detail.html', context)


class PatientDataListView(LoginRequiredMixin, generic.ListView):
    model = PatientData
    paginate_by = 10


class PatientDataDetailView(LoginRequiredMixin, generic.DetailView):
    model = PatientData


class WearableDataListView(LoginRequiredMixin, generic.ListView):
    model = WearableData
    paginate_by = 10


class WearableDataDetailView(LoginRequiredMixin, generic.DetailView):
    model = WearableData


class WearableAnnotationDetailView(LoginRequiredMixin, generic.DetailView):
    model = WearableAnnotation


class CameraDataListView(LoginRequiredMixin, generic.ListView):
    model = CameraData
    paginate_by = 10


class CameraAnnotationByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing annotations by current user."""
    model = CameraAnnotation
    template_name = 'sensors/cameraannotation_list_annotated_user.html'
    paginate_by = 10

    def get_queryset(self):
        return CameraAnnotation.objects.filter(annotator=self.request.user).order_by('camera', 'timestamp')


class CameraAnnotationDetailGet(LoginRequiredMixin, generic.DetailView):
    """View to get annotations."""
    model = CameraAnnotation

    def get_context_data(self, **kwargs):
        context = super(CameraAnnotationDetailGet, self).get_context_data(**kwargs)
        context['form'] = CameraAnnotationCommentCreateForm()
        return context


class CameraAnnotationDetailView(LoginRequiredMixin, generic.View):
    """Combined get and post for camera annotations and comments."""
    def get(self, request, *args, **kwargs):
        view = CameraAnnotationDetailGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, uuid, pk):
        current_annotation = get_object_or_404(CameraAnnotation, pk=pk)

        form = CameraAnnotationCommentCreateForm(request.POST)

        if form.is_valid():
            # self.request.session['form_data'] = form.cleaned_data
            new_comment = form.save(commit=False)
            new_comment.annotation = current_annotation
            new_comment.author = request.user
            new_comment.text = form.cleaned_data['text']
            new_comment.save()
            return redirect('cameraannotation-detail', uuid=uuid, pk=pk)
        else:
            print(form.errors)

        context = {
            'form': form,
            'cameraannotation': current_annotation
        }

        return render(request, 'sensors/cameraannotation_detail.html', context)
