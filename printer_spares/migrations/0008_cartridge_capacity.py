# Generated by Django 2.0.3 on 2018-04-01 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer_spares', '0007_auto_20180326_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartridge',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
    ]
