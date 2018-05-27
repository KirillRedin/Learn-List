from ..models import *
from django.test import TestCase
from django.contrib.auth.models import User


class PlaylistTest(TestCase):

    """ Test module for Playlist model """

    def setUp(self):

        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        self.playlist = Playlist.objects.create(
            user=user,
            name='New Playlist',
            description='playlist description',
            picture='picture link'
        )

    def test_playlist(self):
        playlist = Playlist.objects.get(id=self.playlist.id)
        self.assertEqual(playlist.name, 'New Playlist')


class DataTest(TestCase):

    """ Test module for Data model """

    def setUp(self):
        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        playlist = Playlist.objects.create(
            user=user,
            name='New Playlist',
            description='playlist description',
            picture='picture link'
        )

        part = Part.objects.create(
            playlist=playlist,
            user=user,
            description='data description'
        )

        self.data = Data.objects.create(
            part=part,
            user=user,
            link='data link',
            description='data description'
        )

    def test_data(self):
        data = Data.objects.get(id=self.data.id)
        self.assertEqual(data.link, 'data link')


class CommentTest(TestCase):

    """ Test module for Comment model """

    def setUp(self):
        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        playlist = Playlist.objects.create(
            user=user,
            name='New Playlist',
            description='playlist description',
            picture='picture link'
        )

        self.comment = Comment.objects.create(
            playlist=playlist,
            user=user,
            content='comment content'
        )

    def test_comment(self):
        new_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(new_comment.content, 'comment content')


class PrivilegeTest(TestCase):

    """ Test module for Privilege model """

    def setUp(self):
        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        playlist = Playlist.objects.create(
            user=user,
            name='New Playlist',
            description='playlist description',
            picture='picture link'
        )

        self.privilege = Privilege.objects.create(
            user=user,
            playlist=playlist,
            access_num=1
        )

    def test_privilege(self):
        privilege = Privilege.objects.get(id=self.privilege.id)
        self.assertEqual(privilege.access_num, 1)