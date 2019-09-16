# Generated by Django 2.2.2 on 2019-09-16 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraAnnotation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.CharField(help_text='hh:mm:ss:ff', max_length=11)),
                ('annotation', models.CharField(choices=[('pos', 'Stooped Posture'), ('asm', 'Asymmetry'), ('ebt', 'En Bloc Turning'), ('dys', 'Dystonia/Dyskensia'), ('mov', 'Slow/Hesitant Movement'), ('str', 'Short Stride Length'), ('oth', 'Other')], default='oth', help_text='PD Symptom', max_length=3)),
                ('status', models.CharField(choices=[('b', '+'), ('e', '-')], default='b', help_text='Begin (+) or End (-)', max_length=1)),
                ('note', models.CharField(blank=True, help_text='Note regarding annotation', max_length=500, null=True)),
                ('annotator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['camera', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PatientData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='Patient first name', max_length=50)),
                ('last_name', models.CharField(help_text='Patient last name', max_length=50)),
                ('date_of_birth', models.DateField()),
                ('notes', models.CharField(help_text='Notes regarding patient', max_length=500)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='WearableData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this wearable data', primary_key=True, serialize=False)),
                ('filename', models.FileField(upload_to='wearable/')),
                ('time', models.DateTimeField()),
                ('note', models.CharField(help_text='Note regarding wearable', max_length=500)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensors.PatientData')),
            ],
            options={
                'ordering': ['patient', '-time'],
            },
        ),
        migrations.CreateModel(
            name='WearableAnnotation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.CharField(help_text='hh:mm:ss:ff', max_length=11)),
                ('annotation', models.CharField(choices=[('pos', 'Stooped Posture'), ('asm', 'Asymmetry'), ('ebt', 'En Bloc Turning'), ('dys', 'Dystonia/Dyskensia'), ('mov', 'Slow/Hesitant Movement'), ('str', 'Short Stride Length'), ('oth', 'Other')], default='oth', help_text='PD Symptom', max_length=3)),
                ('status', models.CharField(choices=[('b', '+'), ('e', '-')], default='b', help_text='Begin (+) or End (-)', max_length=1)),
                ('note', models.CharField(blank=True, help_text='Note regarding annotation', max_length=500, null=True)),
                ('annotator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('wearable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensors.WearableData')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CameraData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this wearable data', primary_key=True, serialize=False)),
                ('filename', models.FileField(upload_to='camera/')),
                ('time', models.DateTimeField()),
                ('note', models.CharField(help_text='Note regarding camera', max_length=500)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensors.PatientData')),
            ],
            options={
                'ordering': ['patient', '-time'],
            },
        ),
        migrations.CreateModel(
            name='CameraAnnotationComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='sensors.CameraAnnotation')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddField(
            model_name='cameraannotation',
            name='camera',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensors.CameraData'),
        ),
    ]
