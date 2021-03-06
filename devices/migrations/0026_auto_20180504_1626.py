# Generated by Django 2.0.3 on 2018-05-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180504_1626'),
        ('devices', '0025_auto_20180427_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryNumberPrefix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=512, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='building',
            name='office',
        ),
        migrations.RemoveField(
            model_name='floor',
            name='building',
        ),
        migrations.RemoveField(
            model_name='place',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='place',
            name='room',
        ),
        migrations.RemoveField(
            model_name='room',
            name='floor',
        ),
        migrations.DeleteModel(
            name='Building',
        ),
        migrations.DeleteModel(
            name='Floor',
        ),
        migrations.DeleteModel(
            name='Office',
        ),
        migrations.DeleteModel(
            name='Place',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
