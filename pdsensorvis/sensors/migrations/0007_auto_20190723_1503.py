# Generated by Django 2.2.2 on 2019-07-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0006_auto_20190722_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameraannotation',
            name='timestamp',
            field=models.CharField(help_text='hh:mm:ss:ff', max_length=11),
        ),
        migrations.AlterField(
            model_name='wearableannotation',
            name='timestamp',
            field=models.CharField(help_text='hh:mm:ss:ff', max_length=11),
        ),
    ]
