# Generated by Django 2.0.3 on 2018-04-27 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0024_auto_20180427_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='left',
            field=models.IntegerField(default=0, verbose_name='coordinate left'),
        ),
        migrations.AlterField(
            model_name='place',
            name='top',
            field=models.IntegerField(default=0, verbose_name='coordinate top'),
        ),
    ]
