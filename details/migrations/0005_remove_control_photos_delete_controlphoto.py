# Generated by Django 4.2 on 2023-10-06 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0004_controlphoto_control_patient_controls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='control',
            name='photos',
        ),
        migrations.DeleteModel(
            name='ControlPhoto',
        ),
    ]