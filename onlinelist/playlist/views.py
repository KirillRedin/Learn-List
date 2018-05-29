from playlist.models import *
from playlist.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User


# Create your views here.

class LogIn(APIView):
    """ Login in page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        return Response(template_name='login.html')

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
                return Response({'message': messaage}, template_name='login.html')
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
            return Response({'message': messaage}, template_name='login.html')


class LogOut(APIView):
    """ Login in page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        logout(request)
        return Response(template_name='login.html')


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
        user_pictures = UserPicture.objects.all()
        parts = Part.objects.filter(playlist=playlist).order_by('number')
        data = Data.objects.filter(playlist=playlist).order_by('number')
        comments = Comment.objects.filter(playlist=playlist)
        users = []
        for comment in comments:
            users.append(User.objects.get(id=comment.user.id))
        return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')


    def post(self, request, id, format=None):
        playlist = self.get_object(id)
        user_pictures = UserPicture.objects.all()
        parts = Part.objects.filter(playlist=playlist).order_by('number')
        data = Data.objects.filter(playlist=playlist).order_by('number')
        comments = Comment.objects.filter(playlist=playlist)
        users = []
        for comment in comments:
            users.append(User.objects.get(id=comment.user.id))

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
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('add_part') != None:
            print("Add part")
            name = request.POST['addPartName']
            description = request.POST['addPartDescription']
            number = request.POST['addPartNumber']
            try:
                greaterParts = Part.objects.filter(playlist=playlist, number__gte=number)
                Part.increase_number(self, greaterParts)
            except Part.DoesNotExist:
                print('Greater parts does not exitst')

            Part.objects.create(user=request.user, playlist=playlist, name=name, description=description, number=number)
            parts = Part.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('add_data') != None:
            print("Add data")
            name = request.POST['addDataName']
            link = request.POST['addDataLink']
            description = request.POST['addDataDescription']
            number = request.POST['addDataNumber']
            part = Part.objects.get(id=request.POST['addDataPartId'])
            try:
                greaterData = Data.objects.filter(part=part, number__gte=number)
                Data.increase_number(self, greaterData)
            except Data.DoesNotExist:
                print('Greater data does not exitst')

            Data.objects.create(user=request.user, playlist=playlist, part=part, name=name, link=link, description=description, number=number)
            data = Data.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('delete_part') != None:
            print("Delete part")
            part = Part.objects.get(id=request.POST['deletePartId'])
            try:
                greaterParts = Part.objects.filter(playlist=playlist, number__gte=part.number)
                Part.decrease_number(self, greaterParts)
            except Part.DoesNotExist:
                print('Greater parts does not exitst')
            part.delete()
            parts = Part.objects.filter(playlist=playlist).order_by('number')
            data = Data.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('delete_data') != None:
            print("Delete data")
            data = Data.objects.get(id=request.POST['deleteDataId'])
            try:
                greaterData = Data.objects.filter(playlist=playlist, part=data.part, number__gte=data.number)
                Data.decrease_number(self, greaterData)
            except Data.DoesNotExist:
                print('Greater data does not exitst')
            data.delete()
            data = Data.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('edit_part') != None:
            print('Edit part')
            name = request.POST['editPartName']
            description = request.POST['editPartDescription']
            number = request.POST['editPartNumber']
            part = Part.objects.get(id=request.POST['editPartId'])
            try:
                greaterPart = Part.objects.filter(playlist=playlist, number__gte=part.number + 1)
                Part.decrease_number(self, greaterPart)
            except Part.DoesNotExist:
                print('Greater part does not exitst')

            try:
                greaterPart = Part.objects.filter(playlist=playlist, number__gte=number)
                Part.increase_number(self, greaterPart)
            except Part.DoesNotExist:
                print('Greater part does not exitst')

            part.name = name
            part.description = description
            part.number = number
            part.save()
            parts = Part.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')


        elif request.POST.get('edit_data') != None:
            print('Edit data')
            name = request.POST['editDataName']
            description = request.POST['editDataDescription']
            link = request.POST['editDataLink']
            number = request.POST['editDataNumber']
            data = Data.objects.get(id=request.POST['editDataId'])
            part = data.part
            try:
                greaterData = Data.objects.filter(part=part, number__gte=data.number + 1)
                Data.decrease_number(self, greaterData)
            except Data.DoesNotExist:
                print('Greater data does not exitst')

            try:
                greaterData = Data.objects.filter(part=part, number__gte=number)
                Data.increase_number(self, greaterData)
            except Data.DoesNotExist:
                print('Greater data does not exitst')

            data.name = name
            data.description = description
            data.number = number
            data.link = link
            data.save()
            data = Data.objects.filter(playlist=playlist).order_by('number')
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('add_comment') != None:
            print('Add comment')
            content = request.POST['addCommentContent']
            Comment.objects.create(content=content, playlist=playlist, user=request.user)
            parts = Part.objects.filter(playlist=playlist).order_by('number')
            data = Data.objects.filter(playlist=playlist).order_by('number')
            comments = Comment.objects.filter(playlist=playlist)
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        elif request.POST.get('delete_comment') != None:
            print('Delete comment')
            comment = Comment.objects.get(id=request.POST['deleteCommentId'])
            comment.delete()
            comments = Comment.objects.filter(playlist=playlist)
            return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments, 'user_pictures': user_pictures, 'users': users}, template_name='playlist.html')

        print("Operation selection error")
        return Response(template_name='playlist.html')
