# Generated by Django 2.0.3 on 2018-05-04 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180407_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='location.Office'),
        ),
    ]
