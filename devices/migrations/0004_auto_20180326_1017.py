# Generated by Django 2.0.3 on 2018-03-26 07:17

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20180326_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(default='manufacturer.png', storage=django.core.files.storage.FileSystemStorage(location='images/manufacturers'), upload_to=''),
        ),
    ]
