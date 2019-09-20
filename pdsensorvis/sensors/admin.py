from django.contrib import admin
from .models import PatientData, WearableData, CameraData, WearableAnnotation, CameraAnnotation, \
    CameraAnnotationComment, WearableDataPoint


# Register your models here.
@admin.register(PatientData)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'notes')


class WearableAnnotationInline(admin.TabularInline):
    model = WearableAnnotation
    extra = 0


class WearableDataPointInline(admin.TabularInline):
    model = WearableDataPoint
    extra = 0


@admin.register(WearableData)
class WearableDataAdmin(admin.ModelAdmin):
    def annotations(self):
        return self.w_annotations.count()

    def data_points(self):
        return self.data_point.count()

    list_display = ('patient', 'time', 'id', annotations, data_points)
    inlines = [WearableAnnotationInline, WearableDataPointInline]
    extra = 0


class CameraAnnotationInline(admin.TabularInline):
    model = CameraAnnotation
    extra = 0


@admin.register(CameraData)
class CameraDataAdmin(admin.ModelAdmin):
    def annotations(self):
        return self.c_annotations.count()

    list_display = ('patient', 'time', 'id', annotations)
    inlines = [CameraAnnotationInline]
    extra = 0


@admin.register(WearableAnnotation)
class WearableAnnotationAdmin(admin.ModelAdmin):
    list_display = ('wearable', 'frame_begin', 'frame_end', 'annotation', 'id')


class CameraAnnotationCommentInline(admin.TabularInline):
    model = CameraAnnotationComment
    extra = 0


@admin.register(CameraAnnotation)
class CameraAnnotationAdmin(admin.ModelAdmin):
    def comment(self):
        comments_num = self.comments.count()
        if comments_num > 0:
            return comments_num
        else:
            return ""

    list_display = ('camera', 'timestamp', 'id', 'annotation', 'status', comment)
    inlines = [CameraAnnotationCommentInline]
    extra = 0


@admin.register(CameraAnnotationComment)
class CameraAnnotationCommentAdmin(admin.ModelAdmin):
    list_display = ('annotation', 'author', 'timestamp', 'text')


@admin.register(WearableDataPoint)
class WearableDataPointAdmin(admin.ModelAdmin):
    list_display = ('wearable', 'frame', 'magnitude', 'id')
