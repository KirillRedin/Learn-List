from rest_framework import serializers
from playlist.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'data',
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
            'user',
            'link',
            'picture',
            'description',
            'creation_date'
        )


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = (
            'id',
            'user',
            'name',
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
            'access_num'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'login',
            'name',
            'surname',
            'status',
            'picture',
            'email',
            'creation_date'
        )