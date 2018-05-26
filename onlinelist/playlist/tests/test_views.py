from ..models import *
from ..serializers import *
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


# initialize the APIClient app
client = Client()

class GetAllPlaylists(TestCase):

    """ Test module for GET all playlists API """

    def setUp(self):
        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        self.playlist1 = Playlist.objects.create(
            user=user,
            name='Playlist1',
            description='playlist description',
            picture='picture link'
        )

        self.playlist2 = Playlist.objects.create(
            user=user,
            name='Playlist2',
            description='playlist description',
            picture='picture link'
        )

    def test_get_all_playlists(self):
        # get API response
        response = client.get(reverse('PlaylistList'))
        # get data from db
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
