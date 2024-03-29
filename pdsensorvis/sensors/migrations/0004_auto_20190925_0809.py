# Generated by Django 2.2.2 on 2019-09-25 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensors", "0003_auto_20190924_2227"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cameradata",
            name="filename",
            field=models.FileField(help_text="Camera video file", upload_to="camera/"),
        ),
        migrations.AlterField(
            model_name="cameradata",
            name="framerate",
            field=models.CharField(
                choices=[
                    ("NTSC_Film", 23.98),
                    ("Film", 24),
                    ("PAL", 25),
                    ("NTSC", 29.97),
                    ("Web", 30),
                    ("PAL_HD", 50),
                    ("NTSC_HD", 59.94),
                    ("High", 60),
                ],
                default="Film",
                help_text="Video framerate",
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="wearabledata",
            name="filename",
            field=models.FileField(
                help_text="Wearable data file", upload_to="wearable/"
            ),
        ),
    ]
