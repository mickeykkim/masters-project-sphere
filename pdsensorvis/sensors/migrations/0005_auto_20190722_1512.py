# Generated by Django 2.2.2 on 2019-07-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0004_auto_20190722_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameraannotation',
            name='note',
            field=models.CharField(help_text='Note regarding annotation', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='wearableannotation',
            name='note',
            field=models.CharField(help_text='Note regarding annotation', max_length=500, null=True),
        ),
    ]