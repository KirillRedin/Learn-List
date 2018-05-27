from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey('Part', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    number = models.IntegerField()
    link = models.CharField(max_length=200)
    picture = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'data'
        unique_together = (('id', 'part'),)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playlist'

class Part(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=45)
    number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=200, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'part'


class Privilege(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING)
    access_num = models.IntegerField()

    class Meta:
        db_table = 'privilege'
        unique_together = (('id', 'user', 'playlist'),)

