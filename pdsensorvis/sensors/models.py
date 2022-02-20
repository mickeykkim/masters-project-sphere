from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

ANNOTATION = (
    ("asm", "Asymmetry"),
    ("dst", "Dystonia"),
    ("dsk", "Dyskensia"),
    ("ebt", "En Bloc Turning"),
    ("str", "Short Stride Length"),
    ("mov", "Slow/Hesitant Movement"),
    ("pos", "Stooped Posture"),
    ("trm", "Tremor"),
    ("oth", "Other/Activity"),
)

FRAME_RATES = (
    ("NTSC_Film", 23.98),
    ("Film", 24),
    ("PAL", 25),
    ("NTSC", 29.97),
    ("Web", 30),
    ("PAL_HD", 50),
    ("NTSC_HD", 59.94),
    ("High", 60),
)


class PatientData(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, help_text="Patient first name")
    last_name = models.CharField(max_length=50, help_text="Patient last name")
    date_of_birth = models.DateField(help_text="Patient date of birth")
    notes = models.CharField(max_length=500, help_text="Notes regarding patient")

    class Meta:
        ordering = ["last_name"]
        permissions = (
            ("can_alter_patientdata", "Can create or edit patient data entries."),
        )

    def get_absolute_url(self):
        return reverse("patientdata-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class WearableData(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this wearable data",
    )
    patient = models.ForeignKey(
        "PatientData", on_delete=models.CASCADE, null=True, related_name="wearables"
    )
    filename = models.FileField(upload_to="wearable/", help_text="Wearable data file")
    time = models.DateTimeField(help_text="Session date & time")
    note = models.CharField(max_length=500, help_text="Note regarding wearable data")

    class Meta:
        ordering = ["patient", "-time"]
        permissions = (
            ("can_alter_wearabledata", "Can create or edit wearable data entries."),
        )

    def get_absolute_url(self):
        return reverse("wearabledata-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.patient} ({self.time})"


class CameraData(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this wearable data",
    )
    patient = models.ForeignKey(
        "PatientData", on_delete=models.CASCADE, null=True, related_name="cameras"
    )
    filename = models.FileField(upload_to="camera/", help_text="Camera video file")
    framerate = models.CharField(
        max_length=9,
        choices=FRAME_RATES,
        default="Film",
        help_text="Video framerate",
    )
    time = models.DateTimeField(help_text="Session date & time")
    note = models.CharField(max_length=500, help_text="Note regarding camera data")

    class Meta:
        ordering = ["patient", "-time"]
        permissions = (
            ("can_alter_cameradata", "Can create or edit camera data entries."),
        )

    def get_absolute_url(self):
        return reverse("cameradata-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.patient} ({self.time})"

    def get_user_annotations(self):
        return self.c_annotations.filter(annotator=User)


class WearableAnnotation(models.Model):
    id = models.AutoField(primary_key=True)
    wearable = models.ForeignKey(
        "WearableData",
        on_delete=models.CASCADE,
        null=True,
        related_name="w_annotations",
    )
    frame_begin = models.PositiveIntegerField()
    frame_end = models.PositiveIntegerField()
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    annotation = models.CharField(
        max_length=3,
        choices=ANNOTATION,
        default="oth",
        help_text="PD Symptom",
    )
    note = models.CharField(
        max_length=500, help_text="Note regarding annotation", null=True, blank=True
    )

    class Meta:
        ordering = ["frame_begin"]
        permissions = (
            (
                "can_alter_wearableannotation",
                "Can create or edit wearable annotations.",
            ),
        )

    def get_absolute_url(self):
        return reverse(
            "wearableannotation-detail", args=[str(self.wearable.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.wearable} - ({self.frame_begin}-{self.frame_end}) - {self.get_annotation_display()}"


class CameraAnnotation(models.Model):
    id = models.AutoField(primary_key=True)
    camera = models.ForeignKey(
        "CameraData", on_delete=models.CASCADE, null=True, related_name="c_annotations"
    )
    time_begin = models.CharField(max_length=11, help_text="hh:mm:ss:ff")
    time_end = models.CharField(max_length=11, help_text="hh:mm:ss:ff")
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    annotation = models.CharField(
        max_length=3,
        choices=ANNOTATION,
        default="oth",
        help_text="PD Symptom",
    )
    note = models.CharField(
        max_length=500, help_text="Note regarding annotation", null=True, blank=True
    )

    class Meta:
        ordering = ["camera", "time_begin"]
        permissions = (
            ("can_alter_cameraannotation", "Can create or edit camera annotations."),
        )

    def get_absolute_url(self):
        return reverse(
            "cameraannotation-detail", args=[str(self.camera.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.camera} - ({self.time_begin}-{self.time_end}) - {self.get_annotation_display()}"


class CameraAnnotationComment(models.Model):
    id = models.AutoField(primary_key=True)
    annotation = models.ForeignKey(
        "CameraAnnotation", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    class Meta:
        ordering = ["annotation", "timestamp"]
        permissions = (
            (
                "can_alter_cameraannotation_comment",
                "Can create or edit camera annotation comments.",
            ),
        )

    def __str__(self):
        return self.text


class WearableDataPoint(models.Model):
    id = models.AutoField(primary_key=True)
    wearable = models.ForeignKey(
        "WearableData", on_delete=models.CASCADE, null=True, related_name="data_point"
    )
    frame = models.PositiveIntegerField()
    magnitude = models.FloatField()

    class Meta:
        ordering = ["frame"]
        permissions = (
            ("can_alter_wearabledata_point", "Can create or edit wearable data point."),
        )

    def __str__(self):
        return f"{self.wearable.id} - ({self.frame}, {self.magnitude})"
