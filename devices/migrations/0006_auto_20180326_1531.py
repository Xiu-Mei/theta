# Generated by Django 2.0.3 on 2018-03-26 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_auto_20180326_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='image',
            field=models.ImageField(default='device.png', upload_to='images/devices'),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ImageField(upload_to='images/locations'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(default='manufacturer.png', upload_to='images/manufacturers'),
        ),
    ]