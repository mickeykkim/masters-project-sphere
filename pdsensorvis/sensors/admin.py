from django.contrib import admin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation


# Register your models here.
@admin.register(PatientData)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'notes')


class WearableAnnotationInline(admin.TabularInline):
    model = WearableAnnotation
    extra = 0


@admin.register(WearableData)
class WearableDataAdmin(admin.ModelAdmin):
    list_display = ('patient', 'time', 'id')
    inlines = [WearableAnnotationInline]
    extra = 0


class CameraAnnotationInline(admin.TabularInline):
    model = CameraAnnotation
    extra = 0


@admin.register(CameraData)
class CameraDataAdmin(admin.ModelAdmin):
    list_display = ('patient', 'time', 'id')
    inlines = [CameraAnnotationInline]
    extra = 0


@admin.register(WearableAnnotation)
class WearableAnnotationAdmin(admin.ModelAdmin):
    list_display = ('wearable', 'timestamp', 'annotation', 'id')


@admin.register(CameraAnnotation)
class CameraAnnotationAdmin(admin.ModelAdmin):
    list_display = ('camera', 'timestamp', 'annotation', 'id')
