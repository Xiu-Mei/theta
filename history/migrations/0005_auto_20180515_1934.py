# Generated by Django 2.0.3 on 2018-05-15 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20180515_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridgeitemhistory',
            name='cartridge_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='printer_spares.CartridgeItem'),
        ),
    ]