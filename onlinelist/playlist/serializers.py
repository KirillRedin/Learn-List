from rest_framework import serializers
from playlist.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'playlist',
            'user',
            'content',
            'creation_date'
        )


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = (
            'id',
            'playlist',
            'part',
            'user',
            'name',
            'link',
            'description',
            'creation_date'
        )

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = (
            'id',
            'playlist',
            'name',
            'user',
            'number',
            'description',
            'creation_date'
        )
        ordering = ('number',)


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = (
            'id',
            'user',
            'name',
            'type',
            'description',
            'picture',
            'creation_date'
        )


class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilege
        fields = (
            'id',
            'user',
            'playlist',
            'read',
            'comment',
            'edit',
            'give_access',
        )


class UserPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPicture
        fields = (
            'id',
            'user',
            'picture'
        )