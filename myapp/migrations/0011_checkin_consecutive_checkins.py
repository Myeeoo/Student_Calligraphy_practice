# Generated by Django 3.2.18 on 2023-05-22 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_like_checkin_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='consecutive_checkins',
            field=models.IntegerField(default=0),
        ),
    ]
