# Generated by Django 2.0.4 on 2018-05-27 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0005_data_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='name',
            field=models.CharField(default='Name', max_length=45),
            preserve_default=False,
        ),
    ]
