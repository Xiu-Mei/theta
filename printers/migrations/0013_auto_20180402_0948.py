# Generated by Django 2.0.3 on 2018-04-02 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0012_auto_20180401_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printer',
            name='image',
            field=models.ImageField(default='/images/printers/printer.png', upload_to='images/printers'),
        ),
    ]
