# Generated by Django 2.0.3 on 2018-05-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0007_auto_20180518_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridgeitemhistory',
            name='message',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
