from orders.models import *
from orders.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


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

    def get_object(self, id):
        try:
            return Playlist.objects.get(id=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        playlist = self.get_object(id)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        playlist = self.get_object(id)
        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        playlist = self.get_object(id)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
