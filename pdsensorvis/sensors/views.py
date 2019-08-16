from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation
from .forms import CameraAnnotationCreateForm, CameraAnnotationEditForm

User = get_user_model()


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


def edit_camera_annotation(request, uuid, pk):
    """View function for editing an existing camera annotation."""

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


class CameraAnnotationDetailView(LoginRequiredMixin, generic.DetailView):
    model = CameraAnnotation


class CameraAnnotationByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing annotations by current user."""
    model = CameraAnnotation
    template_name = 'sensors/cameraannotation_list_annotated_user.html'
    paginate_by = 10

    def get_queryset(self):
        return CameraAnnotation.objects.filter(annotator=self.request.user).order_by('id')
