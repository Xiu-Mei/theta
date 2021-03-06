# Generated by Django 2.0.3 on 2018-04-09 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0018_auto_20180409_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('additional_name', models.CharField(blank=True, max_length=512, null=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.Floor')),
            ],
        ),
        migrations.RenameField(
            model_name='place',
            old_name='location',
            new_name='floor',
        ),
        migrations.AddField(
            model_name='room',
            name='places',
            field=models.ManyToManyField(blank=True, to='devices.Place'),
        ),
    ]
