# Generated by Django 2.2.2 on 2019-09-16 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sensors', '0013_auto_20190905_1210'),
    ]

    operations = [
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
    ]
