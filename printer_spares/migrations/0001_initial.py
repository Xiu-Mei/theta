# Generated by Django 2.0.3 on 2018-03-24 07:53

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('printers', '0001_initial'),
        ('devices', '0002_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('image', models.ImageField(default='cartridge.png', storage=django.core.files.storage.FileSystemStorage(location='./media/images/spares'), upload_to='')),
                ('in_stock', models.IntegerField()),
                ('comment', models.CharField(max_length=512)),
                ('contractors', models.ManyToManyField(to='devices.Contractor')),
                ('printers', models.ManyToManyField(to='printers.Printer')),
                ('urls', models.ManyToManyField(to='devices.Url')),
            ],
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=512, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('image', models.ImageField(default='spare.png', storage=django.core.files.storage.FileSystemStorage(location='./media/images/spares'), upload_to='')),
                ('in_stock', models.IntegerField()),
                ('comment', models.CharField(max_length=512)),
                ('contractors', models.ManyToManyField(to='devices.Contractor')),
                ('indexes', models.ManyToManyField(to='printer_spares.Index')),
                ('printers', models.ManyToManyField(to='printers.Printer')),
                ('urls', models.ManyToManyField(to='devices.Url')),
            ],
        ),
    ]