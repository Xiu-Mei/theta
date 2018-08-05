# Generated by Django 2.0.3 on 2018-03-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0010_auto_20180326_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='image',
            field=models.ImageField(default='images/buildings/default_building.png', upload_to='images/buildings'),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ImageField(default='images/locations/default_location.png', upload_to='images/locations'),
        ),
    ]
