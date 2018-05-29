from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserPicture(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.TextField(max_length=200)

    class Meta:
        db_table = 'user_picture'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.DO_NOTHING)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=45)
    number = models.IntegerField()
    link = models.TextField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def increase_number(self, greaterData):
        for data in greaterData:
            data.number += 1
            data.save()

    def decrease_number(self, greaterParts):
        for part in greaterParts:
            part.number -= 1
            part.save()

    class Meta:
        db_table = 'data'
        unique_together = (('id', 'part'),)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=45)
    type = models.IntegerField()
    picture = models.TextField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'playlist'


class Part(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=45)
    number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def increase_number(self, greaterParts):
        for part in greaterParts:
            part.number += 1
            part.save()

    def decrease_number(self, greaterParts):
        for part in greaterParts:
            part.number -= 1
            part.save()

    # def add_part(self, user_):
    #
    # def update_part(self):

    class Meta:
        db_table = 'part'


class Privilege(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    access_num = models.IntegerField()

    class Meta:
        db_table = 'privilege'
        unique_together = (('id', 'user', 'playlist'),)

