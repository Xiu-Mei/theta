# Generated by Django 2.0.3 on 2018-04-29 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('image',
                 models.ImageField(default='images/buildings/default_building.png', upload_to='images/buildings')),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('plan', models.ImageField(default='images/plans/default_plan.png', upload_to='images/plans')),
                ('building',
                 models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='location.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('left', models.IntegerField(default=0, verbose_name='coordinate left')),
                ('top', models.IntegerField(default=0, verbose_name='coordinate top')),
                ('comment', models.TextField(blank=True, null=True)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.Floor')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('additional_name', models.CharField(blank=True, max_length=512, null=True)),
                ('image', models.ImageField(default='images/rooms/default_room.png', upload_to='images/rooms')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.Floor')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='location.Room'),
        ),
        migrations.AddField(
            model_name='building',
            name='office',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='location.Office'),
        ),
    ]
