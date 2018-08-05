# Generated by Django 2.0.3 on 2018-04-07 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0014_contractor_office'),
        ('printers', '0015_auto_20180407_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='printeritem',
            name='office',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='devices.Office'),
            preserve_default=False,
        ),
    ]