from playlist.models import *
from playlist.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User


# Create your views here.

class SignIn(APIView):
    """ Sing in page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        return Response(template_name='signin.html')

    def post(self, request, format=None):
        messaage = messaage = {
            'text': '',
            'color': ''
        }
        if request.POST.get('signin') != None:

            user = authenticate(request, username=request.POST['login'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return Response({'message': messaage}, template_name='playlist.html')
            else:
                messaage = {
                    'text': 'Невірний Логін або Пароль',
                    'color': 'Red'
                }
                return Response({'message': messaage}, template_name='signin.html')
        else:
            print('Registration')
            user = User.objects.create_user(
                username=request.POST['login'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name']
            )
            picturename = ""
            if request.FILES.get('userPicture') != None:
                print('Uploading picture')
                picture = request.FILES['userPicture']
                img_fs = FileSystemStorage(base_url='/playlist/static/playlist/images', location="playlist/static/playlist/images")
                picturename = img_fs.save(picture.name, picture)
            UserPicture.objects.create(user=user, picture=picturename)
            messaage = {
                'text': 'Користувач успішно зареєстрований',
                'color': 'Green'
            }
            return Response({'message': messaage}, template_name='signin.html')

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

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
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
        user_picture = UserPicture.objects.get(user = request.user)
        playlistSerializer = PlaylistSerializer(playlist)
        parts = Part.objects.filter(playlist=playlist).order_by('number')
        data = Data.objects.filter(playlist=playlist).order_by('number')
        return Response({'playlist': playlistSerializer.data, 'user_picture': user_picture, 'parts': parts, 'data':data}, template_name='playlist.html')


    def post(self, request, id, format=None):
        playlist = self.get_object(id)
        user_picture = UserPicture.objects.get(user = request.user)
        if request.POST.get('edit_playlist') != None:
            print("Editing playlist")
            name = request.POST['playlistName']
            description = request.POST['playlistDescription']
            picturename = playlist.picture

            if request.FILES.get('playlistPicture') != None:
                print("Changing picture")
                picture = request.FILES['playlistPicture']
                img_fs = FileSystemStorage(base_url='/playlist/static/playlist/images', location="playlist/static/playlist/images")
                picturename = img_fs.save(picture.name, picture)
                print(picturename)

            playlist.name = name
            playlist.description = description
            playlist.picture = picturename
            playlist.save()
            parts = Part.objects.filter(playlist=playlist).order_by('number')
            data = Data.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'user_picture': user_picture, 'parts': parts, 'data':data}, template_name='playlist.html')

        elif request.POST.get('add_part') != None:
            print("Add part")
            name = request.POST['addPartName']
            description = request.POST['addPartDescription']
            number = request.POST['addPartNumber']
            try:
                greaterParts = Part.objects.filter(playlist=playlist.id, number__gte=number)
                Part.increase_number(self, greaterParts)
            except Part.DoesNotExist:
                print('Part does not exitst')
            data = {
                'user': 1,
                'playlist': playlist.id,
                'name': name,
                'description': description,
                'number': number,
            }
            partSerializer = PartSerializer(data=data)

            if partSerializer.is_valid():
                partSerializer.save()
                parts = Part.objects.filter(playlist=playlist).order_by('number')
                data = Data.objects.filter(playlist=playlist).order_by('number')
                return Response({'playlist': playlist, 'user_picture': user_picture, 'parts': parts, 'data':data}, template_name='playlist.html')

            print("Add part error ")
            return Response(template_name='playlist.html')

        print("Operation selection error")
        return Response(template_name='playlist.html')

    # def put(self, request, id, format=None):
    #     playlist = self.get_object(id)
    #     playlistSerializer = PlaylistSerializer(playlist, data=request.data)
    #     parts = Part.objects.filter(playlist=playlist).order_by('number')
    #     data = Data.objects.filter(playlist=playlist).order_by('number')
    #     if playlistSerializer.is_valid():
    #         playlistSerializer.save()
    #         return Response({'playlist': playlistSerializer.data, 'parts': parts, 'data':data}, status=status.HTTP_204_NO_CONTENT)
    #     return Response(playlistSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, id, format=None):
    #     playlist = self.get_object(id)
    #     playlist.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #

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
