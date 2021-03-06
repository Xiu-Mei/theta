# Generated by Django 2.0.3 on 2018-03-26 07:12

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='image',
            field=models.ImageField(default='device.png', storage=django.core.files.storage.FileSystemStorage(location='images/devices'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='images/location'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(default='manufacturer.png', storage=django.core.files.storage.FileSystemStorage(location='./images/manufacturers'), upload_to='./images/manufacturers'),
        ),
    ]
