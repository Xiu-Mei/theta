# Generated by Django 2.0.3 on 2018-05-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('printer_spares', '0013_cartridgeitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridge',
            name='name',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]