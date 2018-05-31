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
            type=10,
            description='playlist description',
            picture='picture link'
        )

    def test_playlist(self):
        playlist = Playlist.objects.get(id=self.playlist.id)
        self.assertEqual(playlist.name, 'New Playlist')


class PartTest(TestCase):

    """ Test module for Part model """

    def setUp(self):
        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        playlist = Playlist.objects.create(
            user=user,
            name='New Playlist',
            type=1,
            description='playlist description',
            picture='picture link'
        )

        self.part = Part.objects.create(
            playlist=playlist,
            user=user,
            name='Part name',
            number=1,
            description='data description'
        )

    def test_part(self):
        part = Part.objects.get(id=self.part.id)
        self.assertEqual(part.name, 'Part name')

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
            type=1,
            description='playlist description',
            picture='picture link'
        )

        part = Part.objects.create(
            playlist=playlist,
            user=user,
            name='Part name',
            number=1,
            description='data description'
        )

        self.data = Data.objects.create(
            playlist=playlist,
            part=part,
            user=user,
            name='name',
            number=1,
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
            type=1,
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


class AccessTest(TestCase):

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
            type=1,
            description='playlist description',
            picture='picture link'
        )

        self.privilege = Access.objects.create(
            user=user,
            playlist=playlist,
            read = 1,
            comment = 1,
            edit = 1,
            give_access = 1
        )

    def test_access(self):
        access = Access.objects.get(id=self.privilege.id)
        self.assertEqual(access.read, 1)
        self.assertEqual(access.comment, 1)
        self.assertEqual(access.edit, 1)
        self.assertEqual(access.give_access, 1)


class UserPictureTest(TestCase):

    """ Test module for UserPictureTest model """

    def setUp(self):
        user = User.objects.create_user(
            username='Redin',
            email='email',
            password=123
        )

        self.user_picture = UserPicture.objects.create(
            user=user,
            picture='picture link'
        )

    def test_user_picture(self):
        user_picture = UserPicture.objects.get(id=self.user_picture.id)
        self.assertEqual(user_picture.picture, 'picture link')