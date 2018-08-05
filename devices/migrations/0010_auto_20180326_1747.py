# Generated by Django 2.0.3 on 2018-03-26 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_auto_20180326_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='images/buildings')),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.RemoveField(
            model_name='location',
            name='office',
        ),
        migrations.AddField(
            model_name='office',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='room',
            field=models.CharField(max_length=512, unique=True),
        ),
        migrations.AddField(
            model_name='building',
            name='office',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='devices.Office'),
        ),
        migrations.AddField(
            model_name='location',
            name='building',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='devices.Building'),
        ),
    ]