# Generated by Django 2.0.3 on 2018-04-09 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0019_auto_20180409_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(default='images/rooms/default_room.png', upload_to='images/rooms'),
        ),
    ]