# Generated by Django 2.2.6 on 2019-11-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensors", "0006_auto_20191118_1220"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cameraannotation",
            name="annotation",
            field=models.CharField(
                choices=[
                    ("asm", "Asymmetry"),
                    ("dst", "Dystonia"),
                    ("dsk", "Dyskensia"),
                    ("ebt", "En Bloc Turning"),
                    ("mov", "Slow/Hesitant Movement"),
                    ("str", "Short Stride Length"),
                    ("pos", "Stooped Posture"),
                    ("trm", "Tremor"),
                    ("oth", "Other/Activity"),
                ],
                default="oth",
                help_text="PD Symptom",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="wearableannotation",
            name="annotation",
            field=models.CharField(
                choices=[
                    ("asm", "Asymmetry"),
                    ("dst", "Dystonia"),
                    ("dsk", "Dyskensia"),
                    ("ebt", "En Bloc Turning"),
                    ("mov", "Slow/Hesitant Movement"),
                    ("str", "Short Stride Length"),
                    ("pos", "Stooped Posture"),
                    ("trm", "Tremor"),
                    ("oth", "Other/Activity"),
                ],
                default="oth",
                help_text="PD Symptom",
                max_length=3,
            ),
        ),
    ]
