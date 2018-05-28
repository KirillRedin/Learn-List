from playlist.models import *
from playlist.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User


# Create your views here.


class PlaylistList(APIView):

    """ List of Playlists, or create a new playlist """

    # renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistDetail(APIView):

    """ Retrieve, update or delete a playlist instance """

    renderer_classes = (TemplateHTMLRenderer,)

    def get_object(self, id):
        try:
            return Playlist.objects.get(id=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        playlist = self.get_object(id)
        playlistSerializer = PlaylistSerializer(playlist)
        parts = Part.objects.filter(playlist=playlist).order_by('number')
        data = Data.objects.filter(playlist=playlist).order_by('number')
        return Response({'playlist': playlistSerializer.data, 'parts': parts, 'data':data}, template_name='playlist.html')


    def post(self, request, id, format=None):
        name = request.POST['playlistName']
        description = request.POST['playlistDescription']
        picture = request.FILES['playlistPicture']
        img_fs = FileSystemStorage(base_url='/playlist/static/playlist/images', location="playlist/static/playlist/images")
        picturename = img_fs.save(picture.name, picture)
        playlist = self.get_object(id)
        data = {
            'id': id,
            'user': 1,
            'name': name,
            'description': description,
            'picture': picturename,
            'creation_date': playlist.creation_date
        }
        playlistSerializer = PlaylistSerializer(playlist, data=data)
        if playlistSerializer.is_valid():
            print('Hello world')
            playlistSerializer.save()
            playlist = Playlist.objects.get(id=id)
            playlistSerializer2 = PlaylistSerializer(playlist)
            parts = Part.objects.filter(playlist=playlist).order_by('number')
            data = Data.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlistSerializer2.data, 'parts': parts, 'data':data}, template_name='playlist.html')
        print('Hello world2')
        return Response(playlistSerializer.errors, template_name='playlist.html')

    def put(self, request, id, format=None):
        playlist = self.get_object(id)
        playlistSerializer = PlaylistSerializer(playlist, data=request.data)
        parts = Part.objects.filter(playlist=playlist).order_by('number')
        data = Data.objects.filter(playlist=playlist).order_by('number')
        if playlistSerializer.is_valid():
            playlistSerializer.save()
            return Response({'playlist': playlistSerializer.data, 'parts': parts, 'data':data}, status=status.HTTP_204_NO_CONTENT)
        return Response(playlistSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        playlist = self.get_object(id)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PlaylistPartsList(APIView):
#
#
#     """ List of Parts, or create a new part """
#
#     # renderer_classes = (TemplateHTMLRenderer,)
#
#     def get(self, request, playlist_id, format=None):
#         playlist = Plalylist.objects.get(id=playlist_id)
#         parts = Part.objects.get(playlist=playlist)
#         serializer = PartSerializer(parts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
