# Generated by Django 2.0.4 on 2018-05-29 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0009_playlist_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=500),
        ),
    ]
