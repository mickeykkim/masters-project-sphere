import csv
import xlwt

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views import generic
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation, \
    CameraAnnotationComment, WearableDataPoint
from .forms import CameraAnnotationCreateForm, CameraAnnotationEditForm, CameraAnnotationCommentCreateForm, \
    CameraAnnotationCommentEditForm, WearableDataCreateForm, CameraDataCreateForm, PatientDataCreateForm, \
    PatientDataEditForm, WearableDataEditForm, WearableAnnotationCreateForm, WearableAnnotationEditForm, \
    CameraDataEditForm
from uuid import UUID

User = get_user_model()

annotation_fields = ['Time Begin (h:m:s:f)', 'Time Begin (h:m:s,ms)', 'Frame Begin', 'Time End (h:m:s:f)',
                     'Time End (h:m:s,ms)', 'Frame End', 'Annotation', 'Note', 'Annotator', 'Comments', ]


def is_valid_uuid(uuid_to_test, version=4):
    """Check if uuid_to_test is a valid UUID. Default to check UUID version 4."""
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def convert_smpte_to_frames(smpte, framerate):
    components = smpte.split(":")
    frames = int(components[0]) * (framerate * 60 * 60) + \
             int(components[1]) * (framerate * 60) + \
             int(components[2]) * framerate + \
             int(components[3])
    return frames


def convert_smpte_to_ms_time(smpte, framerate):
    components = smpte.split(":")
    print(str(int(components[3])))
    ms = str(round(int(components[3]) * 1000 / framerate)).zfill(3)
    ms_time = str(components[0]) + ":" + \
              str(components[1]) + ":" + \
              str(components[2]) + "," + ms
    return ms_time


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

        if query and query.strip():
            if is_valid_uuid(query):
                lookups = Q(pk=query)
            else:
                lookups = Q(patient__first_name__icontains=query) | Q(patient__last_name__icontains=query)

            camera_results = CameraData.objects.filter(lookups)
            wearable_results = WearableData.objects.filter(lookups)

            context = {
                'cameradata': camera_results,
                'wearabledata': wearable_results
            }

            return render(request, "search_results.html", context)
        else:
            return render(request, "search_results.html")

    else:
        return render(request, "search_results.html")


@permission_required('sensors.can_alter_patientdata')
def create_patientdata(request):

    if request.method == 'POST':
        form = PatientDataCreateForm(request.POST)
        if form.is_valid():
            new_patient = form.save(commit=False)
            new_patient.save()
            return redirect('patientdata')
        else:
            print(form.errors)
    else:
        form = PatientDataCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'sensors/patient_upload.html', context)


@permission_required('sensors.can_alter_patientdata')
def edit_patientdata(request, pk):
    existing_patientdata = get_object_or_404(PatientData, pk=pk)

    if request.method == 'POST':
        form = PatientDataEditForm(request.POST, instance=existing_patientdata)
        if form.is_valid():
            existing_patientdata = form.save(commit=False)
            existing_patientdata.save()
            return redirect('patientdata-detail', pk)
        else:
            print(form.errors)
    else:
        form = PatientDataEditForm(instance=existing_patientdata)

    context = {
        'form': form,
        'patientdata': existing_patientdata,
    }

    return render(request, 'sensors/edit_patientdata.html', context)


@permission_required('sensors.can_alter_patientdata')
def delete_patientdata(request, pk):
    existing_patientdata = get_object_or_404(PatientData, pk=pk)

    if request.method == 'POST':
        existing_patientdata.delete()
        return redirect('patientdata')
    else:
        form = PatientDataEditForm(instance=existing_patientdata)

    context = {
        'form': form,
        'patientdata': existing_patientdata,
    }

    return render(request, 'sensors/edit_patientdata.html', context)


@permission_required('sensors.can_alter_wearabledata')
def create_wearabledata(request, pk):
    patient_id = get_object_or_404(PatientData, pk=pk)

    if request.method == 'POST':
        form = WearableDataCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_wearable = form.save(commit=False)
            new_wearable.patient = patient_id
            new_wearable.save()
            import_wearabledata_csv(new_wearable.id, new_wearable.filename.path)
            return redirect('patientdata-detail', pk=pk)
        else:
            print(form.errors)
    else:
        form = WearableDataCreateForm()

    context = {
        'form': form,
        'patientdata': patient_id,
    }

    return render(request, 'sensors/wearable_upload.html', context)


@permission_required('sensors.can_alter_wearabledata')
def edit_wearabledata(request, uuid):
    existing_wearable = get_object_or_404(WearableData, pk=uuid)

    if request.method == 'POST':
        form = WearableDataEditForm(request.POST, instance=existing_wearable)
        if form.is_valid():
            existing_wearable = form.save(commit=False)
            existing_wearable.save()
            return redirect('wearabledata-detail', pk=uuid)
        else:
            print(form.errors)
    else:
        form = WearableDataEditForm(instance=existing_wearable)

    context = {
        'form': form,
        'wearabledata': existing_wearable,
    }

    return render(request, 'sensors/edit_wearabledata.html', context)


@permission_required('sensors.can_alter_wearabledata')
def delete_wearabledata(request, uuid):
    existing_wearable = get_object_or_404(WearableData, pk=uuid)

    if request.method == 'POST':
        existing_wearable.delete()
        return redirect('wearabledata')
    else:
        form = WearableDataEditForm(instance=existing_wearable)

    context = {
        'form': form,
        'wearabledata': existing_wearable,
    }

    return render(request, 'sensors/edit_wearabledata.html', context)


@permission_required('sensors.can_alter_wearableannotation')
def create_wearable_annotation(request, uuid):
    existing_wearable = get_object_or_404(WearableData, pk=uuid)

    if request.method == 'POST':
        form = WearableAnnotationCreateForm(request.POST)
        if form.is_valid():
            new_annotation = form.save(commit=False)
            new_annotation.wearable = existing_wearable
            new_annotation.annotator = request.user
            new_annotation.annotation = form.cleaned_data['annotation']
            new_annotation.save()
            return redirect('wearabledata-detail', pk=uuid)
    else:
        form = WearableAnnotationCreateForm()

    context = {
        'form': form,
        'wearable': existing_wearable,
    }

    return render(request, 'sensors/create_wearable_annotation.html', context)


@permission_required('sensors.can_alter_wearableannotation')
def edit_wearable_annotation(request, uuid, pk):
    existing_annotation = get_object_or_404(WearableAnnotation, pk=pk)
    existing_wearable = get_object_or_404(WearableData, pk=uuid)

    if request.method == 'POST':
        form = WearableAnnotationEditForm(request.POST, instance=existing_annotation)
        if form.is_valid():
            existing_annotation = form.save(commit=False)
            existing_annotation.annotation = form.cleaned_data['annotation']
            return redirect('wearabledata-detail', pk=uuid)
    else:
        form = WearableAnnotationEditForm(instance=existing_annotation)

    context = {
        'form': form,
        'wearableannotation': existing_annotation,
    }

    return render(request, 'sensors/edit_wearable_annotation.html', context)


@permission_required('sensors.can_alter_wearableannotation')
def delete_wearable_annotation(request, uuid, pk):
    existing_annotation = get_object_or_404(WearableAnnotation, pk=pk)

    if request.method == 'POST':
        existing_annotation.delete()
        return redirect('wearabledata-detail', pk=uuid)
    else:
        form = WearableAnnotationEditForm(instance=existing_annotation)

    context = {
        'form': form,
        'cameraannotation': existing_annotation,
    }

    return render(request, 'sensors/edit_wearable_annotation.html', context)


@permission_required('sensors.can_alter_cameradata')
def create_cameradata(request, pk):
    patient_id = get_object_or_404(PatientData, pk=pk)

    if request.method == 'POST':
        form = CameraDataCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_camera = form.save(commit=False)
            new_camera.patient = patient_id
            new_camera.save()
            return redirect('patientdata-detail', pk=pk)
        else:
            print(form.errors)
    else:
        form = CameraDataCreateForm()

    context = {
        'form': form,
        'patientdata': patient_id,
    }

    return render(request, 'sensors/camera_upload.html', context)


@permission_required('sensors.can_alter_cameradata')
def edit_cameradata(request, uuid):
    existing_camera = get_object_or_404(CameraData, pk=uuid)

    if request.method == 'POST':
        form = CameraDataEditForm(request.POST, instance=existing_camera)
        if form.is_valid():
            existing_camera = form.save(commit=False)
            existing_camera.save()
            return redirect('cameradata-detail', pk=uuid)
        else:
            print(form.errors)
    else:
        form = CameraDataEditForm(instance=existing_camera)

    context = {
        'form': form,
        'cameradata': existing_camera,
    }

    return render(request, 'sensors/edit_cameradata.html', context)


@permission_required('sensors.can_alter_cameradata')
def delete_cameradata(request, uuid):
    existing_camera = get_object_or_404(CameraData, pk=uuid)

    if request.method == 'POST':
        existing_camera.delete()
        return redirect('cameradata')
    else:
        form = CameraDataEditForm(instance=existing_camera)

    context = {
        'form': form,
        'cameradata': existing_camera,
    }

    return render(request, 'sensors/edit_cameradata.html', context)


@permission_required('sensors.can_alter_cameraannotation')
def edit_camera_annotation(request, uuid, pk):
    existing_annotation = get_object_or_404(CameraAnnotation, pk=pk)
    existing_camera = get_object_or_404(CameraData, pk=uuid)

    if request.method == 'POST':
        form = CameraAnnotationEditForm(request.POST, instance=existing_annotation)
        if form.is_valid():
            existing_annotation = form.save(commit=False)
            existing_annotation.annotation = form.cleaned_data['annotation']
            fps = existing_camera.get_framerate_display()
            existing_annotation.frame_begin = convert_smpte_to_frames(existing_annotation.time_begin, fps)
            existing_annotation.frame_end = convert_smpte_to_frames(existing_annotation.time_end, fps)
            existing_annotation.ms_time_begin = convert_smpte_to_ms_time(existing_annotation.time_begin, fps)
            existing_annotation.ms_time_end = convert_smpte_to_ms_time(existing_annotation.time_end, fps)
            existing_annotation.save()
            return redirect('cameradata-detail', pk=uuid)
    else:
        form = CameraAnnotationEditForm(instance=existing_annotation)

    context = {
        'form': form,
        'cameraannotation': existing_annotation,
    }

    return render(request, 'sensors/edit_camera_annotation.html', context)


@permission_required('sensors.can_alter_cameraannotation')
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


@permission_required('sensors.can_alter_cameraannotationcomment')
def edit_cameraannotation_comment(request, uuid, pk, cid):
    existing_camera = get_object_or_404(CameraData, pk=uuid)
    existing_annotation = get_object_or_404(CameraAnnotation, pk=pk)
    existing_comment = get_object_or_404(CameraAnnotationComment, pk=cid)

    if request.method == 'POST':
        form = CameraAnnotationCommentEditForm(request.POST, instance=existing_comment)
        if form.is_valid():
            existing_comment = form.save(commit=False)
            existing_comment.save()
            return redirect('cameraannotation-detail', uuid=uuid, pk=pk)
        else:
            print(form.errors)
    else:
        form = CameraAnnotationCommentEditForm(instance=existing_comment)

    context = {
        'form': form,
        'camera': existing_camera,
        'annotation': existing_annotation,
        'comment': existing_comment,
    }

    return render(request, 'sensors/edit_cameraannotation_comment.html', context)


@permission_required('sensors.can_alter_cameraannotationcomment')
def delete_cameraannotation_comment(request, uuid, pk, cid):
    existing_camera = get_object_or_404(CameraData, pk=uuid)
    existing_annotation = get_object_or_404(CameraAnnotation, pk=pk)
    existing_comment = get_object_or_404(CameraAnnotationComment, pk=cid)

    if request.method == 'POST':
        existing_comment.delete()
        return redirect('cameradata-detail', pk=uuid)
    else:
        form = CameraAnnotationCommentEditForm(instance=existing_comment)

    context = {
        'form': form,
        'camera': existing_camera,
        'annotation': existing_annotation,
        'comment': existing_comment,
    }

    return render(request, 'sensors/edit_cameraannotation_comment.html', context)


class CameraDataDetailGet(LoginRequiredMixin, generic.DetailView):
    model = CameraData
    permission_required = 'catalog.sensors.can_alter_cameradata'

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
        return CameraAnnotation.objects.filter(annotator=self.request.user).order_by('camera', 'time_begin')


def export_annotations_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + pk + ".csv"''

    writer = csv.writer(response)
    writer.writerow(['Session ID:', pk])
    writer.writerow(annotation_fields)

    annotations = CameraAnnotation.objects.filter(camera_id=pk)

    for annotation in annotations:
        comment_list = CameraAnnotationComment.objects.filter(annotation_id=annotation.id)
        discussion = ""

        for comment in comment_list:
            discussion += comment.author.username + " (" + comment.timestamp.strftime('%d/%m/%Y %H:%M') + "): " + \
                          comment.text + "\n"

        writer.writerow([annotation.time_begin, annotation.ms_time_begin, annotation.frame_begin, annotation.time_end,
                         annotation.ms_time_end, annotation.frame_end, annotation.get_annotation_display(),
                         annotation.note, annotation.annotator.username, discussion, ])

    return response


def export_annotations_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + pk + ".xls"''

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet title w/Session ID
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Session ID:', pk, ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet headers
    row_num = 1
    columns = annotation_fields
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
            discussion += comment.author.username + " (" + comment.timestamp.strftime('%d/%m/%Y %H:%M') + "): " + \
                          comment.text + "\n"
        items = [annotation.time_begin, annotation.ms_time_begin, annotation.frame_begin, annotation.time_end,
                 annotation.ms_time_end, annotation.frame_end, annotation.get_annotation_display(),
                 annotation.note, annotation.annotator.username, discussion, ]

        for col_num in range(len(items)):
            ws.write(row_num, col_num, items[col_num], font_style)

    wb.save(response)
    return response


def upload_csv_annotation(request, pk):
    context = {}
    if "GET" == request.method:
        return render(request, "sensors/upload_csv.html", context)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    import_wearableannotation_csv(pk, csv_file)

    return render(request, 'sensors/upload_csv.html', context)


def import_wearabledata_csv(pk, path):
    """
    Method for importing wearable data points. Requires csv file with acceleration magnitudes in the first column.
    WARNING: Does not do any validation.
    """
    wearabledata = get_object_or_404(WearableData, pk=pk)
    with open(path) as import_file:
        reader = csv.reader(import_file)
        frame_num = 1
        for row in reader:
            _, created = WearableDataPoint.objects.get_or_create(
                wearable=wearabledata,
                frame=frame_num,
                magnitude=row[0],
            )
            frame_num += 1


def import_wearableannotation_csv(pk, path):
    """
    Method for importing wearable data annotations. Requires csv file with appropriate headers.
    WARNING: Does not do any validation.
    """
    wearabledata = get_object_or_404(WearableData, pk=pk)
    with open(path) as import_file:
        reader = csv.DictReader(import_file, fieldnames=['Frame Begin', 'Frame End', 'Annotation', 'Note'])
        for row in reader:
            _, created = WearableAnnotation.objects.get_or_create(
                wearable=wearabledata,
                annotator=User,
                frame_begin=row['Frame Begin'],
                frame_end=row['Frame End'],
                annotation=row['Annotation'],
                note=row['Note'],
            )
