# Generated by Django 2.2.2 on 2019-07-23 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0007_auto_20190723_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cameraannotation',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='wearableannotation',
            options={'ordering': ['id']},
        ),
    ]
