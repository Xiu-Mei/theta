# Generated by Django 2.0.3 on 2018-04-06 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0013_auto_20180404_1314'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='offices',
            field=models.ManyToManyField(blank=True, to='devices.Office'),
        ),
    ]
