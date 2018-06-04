from playlist.models import *
from playlist.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.

class LogIn(APIView):
    """ Login in page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        if request.user.is_authenticated:
            return redirect('/')
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
                return redirect('/')
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
            picturename = "no-photo.jpg"
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


@method_decorator(login_required, name='dispatch')
class LogOut(APIView):
    """ Logout page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        logout(request)
        return redirect('/login/')


@method_decorator(login_required, name='dispatch')
class UserDetail(APIView):

    """ User Detail page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        user = self.get_object(id)
        try:
            user_picture = UserPicture.objects.get(user=user)
        except UserPicture.DoesNotExist:
            user_picture = UserPicture.objects.create(user=user, picture='no-photo.jpg')
        playlists = Playlist.objects.filter(user=user, type=1)
        playlist_paginator = Paginator(playlists, 6)
        page = request.GET.get('public_page', 1)
        try:
            playlists = playlist_paginator.page(page)
        except PageNotAnInteger:
            playlists = playlist_paginator.page(1)
        except EmptyPage:
            playlists = playlist_paginator.page(playlist_paginator.num_pages)

        if request.user.is_superuser:
            access_list = Access.objects.filter(user=user, playlist__user=user, playlist__type=0)
            print(access_list)
        else:
            access_list = Access.objects.filter(user=request.user, playlist__user=user, playlist__type=0)

        access_paginator = Paginator(access_list, 6)
        page = request.GET.get('private_page', 1)
        try:
            access_list = access_paginator.page(page)
        except PageNotAnInteger:
            access_list = access_paginator.page(1)
        except EmptyPage:
            access_list = access_paginator.page(access_paginator.num_pages)
        return Response({'playlists': playlists, 'user': user, 'user_picture': user_picture, 'access_list': access_list}, template_name='profile.html')

    def post(self, request, id, format=None):
        user = self.get_object(id)
        try:
            user_picture = UserPicture.objects.get(user=user)
        except UserPicture.DoesNotExist:
            user_picture = UserPicture.objects.create(user=user, picture='no-photo.jpg')
        error_message = ''
        if request.POST.get('edit_user') != None:
            username = request.POST['editLogin']
            first_name = request.POST['editFirstName']
            last_name = request.POST['editLastName']
            email = request.POST['editEmail']
            picturename = user_picture.picture

            if request.FILES.get('editPicture') != None:
                picture = request.FILES['editPicture']
                img_fs = FileSystemStorage(base_url='/playlist/static/playlist/images', location="playlist/static/playlist/images")
                picturename = img_fs.save(picture.name, picture)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            user_picture.picture = picturename
            user_picture.save()
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('edit_password') != None:
            old_password = request.POST['oldPassword']
            new_password = request.POST['newPassword']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                error_message = 'Невірний пароль'
                user = self.get_object(id)
                user_picture = UserPicture.objects.get(user=user)
                playlists = Playlist.objects.filter(user=user, type=1)
                if request.user.is_superuser:
                    access_list = Access.objects.filter(playlist__user=user, playlist__type=0)
                else:
                    access_list = Access.objects.filter(user=request.user, playlist__user=user, playlist__type=0)
                return Response({'playlists': playlists, 'user': user, 'user_picture': user_picture,
                                 'access_list': access_list, 'error_message': error_message}, template_name='profile.html')

        elif request.POST.get('profile_search') != None:
            name = request.POST['searchName']
            playlists = Playlist.objects.filter(user=user, type=1, name__icontains=name)
            access_list = Access.objects.filter(user=request.user, playlist__user=user, playlist__type=0, playlist__name__icontains=name)
            return Response({'playlists': playlists, 'user': user, 'user_picture': user_picture, 'access_list': access_list}, template_name='profile.html')

        return HttpResponseRedirect(self.request.path_info)

@method_decorator(login_required, name='dispatch')
class UserList(APIView):

    """User List page"""

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        if request.user.is_superuser != 1:
            return redirect('/')
        users = User.objects.all()
        paginator = Paginator(users, 6)
        page = request.GET.get('page', 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return Response({'users': users}, template_name='users.html')

    def post(self, request, format=None):
        if request.user.is_superuser != 1:
            return redirect('/')
        name = request.POST['searchName']
        users = User.objects.filter(Q(username__icontains=name) | Q(first_name__icontains=name) | Q(last_name__icontains=name))
        paginator = Paginator(users, 6)
        page = request.GET.get('page', 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return Response({'users': users}, template_name='users.html')


@method_decorator(login_required, name='dispatch')
class PlaylistList(APIView):

    """ List of Playlists, or create a new playlist """

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        if request.user.is_superuser:
            playlists = Playlist.objects.all()
        else:
            playlists = Playlist.objects.filter(type=1)
        paginator = Paginator(playlists, 6)
        page = request.GET.get('page', 1)
        try:
            playlists = paginator.page(page)
        except PageNotAnInteger:
            playlists = paginator.page(1)
        except EmptyPage:
            playlists = paginator.page(paginator.num_pages)

        return Response({'playlists': playlists}, template_name='mainpage.html')

    def post(self, request, format=None):
        if request.POST.get('add_playlist') != None:
            name = request.POST['addPlaylistName']
            user = request.user
            type = request.POST['addPlaylistType']
            description = request.POST['addPlaylistDescription']

            picturename = 'no-photo.jpg'

            if request.FILES.get('addPlaylistPicture') != None:
                print("Adding picture")
                picture = request.FILES['addPlaylistPicture']
                img_fs = FileSystemStorage(base_url='/playlist/static/playlist/images', location="playlist/static/playlist/images")
                picturename = img_fs.save(picture.name, picture)

            playlist = Playlist.objects.create(name=name, user=user, type=type, description=description, picture=picturename)
            Access.objects.create(user=user, playlist=playlist, read=1, comment=1, edit=1, give_access=1)
            return redirect('playlist/' + str(playlist.id))

        elif request.POST.get('global_search') != None:
            name = request.POST['searchName']
            if request.user.is_superuser:
                playlists = Playlist.objects.filter(name__icontains=name)
            else:
                playlists = Playlist.objects.filter(type=1, name__icontains=name)
            paginator = Paginator(playlists, 6)
            page = request.GET.get('page', 1)
            try:
                playlists = paginator.page(page)
            except PageNotAnInteger:
                playlists = paginator.page(1)
            except EmptyPage:
                playlists = paginator.page(paginator.num_pages)
            return Response({'playlists': playlists}, template_name='mainpage.html')


@method_decorator(login_required, name='dispatch')
class AccessiblePlaylists(APIView):

    """ List of accessible Playlists """

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        if request.user.is_superuser:
            return redirect('/')
        access_list = Access.objects.filter(~Q(playlist__user=request.user), user=request.user)
        paginator = Paginator(access_list, 6)
        page = request.GET.get('page', 1)
        try:
            access_list = paginator.page(page)
        except PageNotAnInteger:
            access_list = paginator.page(1)
        except EmptyPage:
            access_list = paginator.page(paginator.num_pages)
        return Response({'access_list': access_list}, template_name='accessible_playlists.html')

    def post(self, request, format=None):
        if request.user.is_superuser:
            return redirect('/')
        name = request.POST['searchName']
        access_list = Access.objects.filter(~Q(playlist__user=request.user), user=request.user, playlist__name__icontains=name)
        paginator = Paginator(access_list, 6)
        page = request.GET.get('page', 1)
        try:
            access_list = paginator.page(page)
        except PageNotAnInteger:
            access_list = paginator.page(1)
        except EmptyPage:
            access_list = paginator.page(paginator.num_pages)
        return Response({'access_list': access_list}, template_name='accessible_playlists.html')


@method_decorator(login_required, name='dispatch')
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
        paginator = Paginator(comments, 6)
        page = request.GET.get('page', 1)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        access_list = Access.objects.filter(playlist=playlist)
        user_access = None
        try:
            user_access = Access.objects.get(playlist=playlist, user=request.user)
        except Access.DoesNotExist:
            if request.user != playlist.user and playlist.type != 1 and request.user.is_superuser != 1:
                return redirect('/')
        return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments,
                         'user_pictures': user_pictures, 'access_list': access_list, 'user_access': user_access},
                        template_name='playlist.html',)


    def post(self, request, id, format=None):
        playlist = self.get_object(id)
        user_pictures = UserPicture.objects.all()
        parts = Part.objects.filter(playlist=playlist).order_by('number')
        data = Data.objects.filter(playlist=playlist).order_by('number')
        comments = Comment.objects.filter(playlist=playlist)
        paginator = Paginator(comments, 6)
        page = request.GET.get('page', 1)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        user_access = None
        try:
            user_access = Access.objects.get(playlist=playlist, user=request.user)
        except Access.DoesNotExist:
            if request.user != playlist.user and playlist.type != 1 and request.user.is_superuser != 1:
                return redirect('/')
        access_list = Access.objects.filter(playlist=playlist)

        if request.POST.get('edit_playlist') != None:
            print("Editing playlist")
            name = request.POST['editPlaylistName']
            type = request.POST['editPlaylistType']
            description = request.POST['editPlaylistDescription']
            picturename = playlist.picture

            if request.FILES.get('editPlaylistPicture') != None:
                print("Changing picture")
                picture = request.FILES['editPlaylistPicture']
                img_fs = FileSystemStorage(base_url='/playlist/static/playlist/images', location="playlist/static/playlist/images")
                picturename = img_fs.save(picture.name, picture)

            playlist.name = name
            playlist.type = type
            playlist.description = description
            playlist.picture = picturename
            playlist.save()
            return HttpResponseRedirect(self.request.path_info)

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
            return HttpResponseRedirect(self.request.path_info)

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
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('delete_part') != None:
            print("Delete part")
            part = Part.objects.get(id=request.POST['deletePartId'])
            try:
                greaterParts = Part.objects.filter(playlist=playlist, number__gte=part.number)
                Part.decrease_number(self, greaterParts)
            except Part.DoesNotExist:
                print('Greater parts does not exitst')
            part.delete()
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('delete_data') != None:
            print("Delete data")
            data = Data.objects.get(id=request.POST['deleteDataId'])
            try:
                greaterData = Data.objects.filter(playlist=playlist, part=data.part, number__gte=data.number)
                Data.decrease_number(self, greaterData)
            except Data.DoesNotExist:
                print('Greater data does not exitst')
            data.delete()
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('delete_playlist') != None:
            print("Delete playlist")
            playlist.delete()
            return redirect('/')

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
            return HttpResponseRedirect(self.request.path_info)


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
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('add_comment') != None:
            print('Add comment')
            content = request.POST['addCommentContent']
            Comment.objects.create(content=content, playlist=playlist, user=request.user)
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('delete_comment') != None:
            print('Delete comment')
            comment = Comment.objects.get(id=request.POST['deleteCommentId'])
            comment.delete()
            return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('give_access') != None:
            print('Give access')
            try:
                user = User.objects.get(username = request.POST['addUserName'])
            except User.DoesNotExist:
                print('User does not exist')
                error_message = "Користувача з таким Ім'ям не існує"
                access_list = Access.objects.filter(playlist=playlist)
                return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments,
                                 'user_pictures': user_pictures, 'access_list': access_list, 'error_message': error_message, 'user_access': user_access}, template_name='playlist.html')
            else:
                if user == request.user or user == playlist.user and request.user.is_superuser != 1:
                    error_message = 'Ви не можете редагувати свої права' if user == request.user else 'Ви не можете редагувати права власника'
                    access_list = Access.objects.filter(playlist=playlist)
                    return Response({'playlist': playlist, 'parts': parts, 'data':data, 'comments': comments,
                                 'user_pictures': user_pictures, 'access_list': access_list, 'error_message': error_message, 'user_access': user_access}, template_name='playlist.html')
                read_access = False
                comment_access = False
                edit_access = False
                give_access = False
                if request.POST.get('readAccess') != None:
                    read_access = True
                if request.POST.get('commentAccess') != None:
                    comment_access = True
                if request.POST.get('editAccess') != None:
                    edit_access = True
                if request.POST.get('giveAccess') != None:
                    give_access = True
                try:
                    access = Access.objects.get(user=user, playlist=playlist)
                except Access.DoesNotExist:
                    print('Access does not exist')
                    Access.objects.create(user=user, playlist=playlist, read=read_access, comment=comment_access, edit=edit_access, give_access=give_access)
                else:
                    access.read = read_access
                    access.comment = comment_access
                    access.edit = edit_access
                    access.give_access = give_access
                    access.save()
                finally:
                    return HttpResponseRedirect(self.request.path_info)

        elif request.POST.get('delete_access') != None:
            print('Delete access')
            access = Access.objects.get(id=request.POST['accessId'])
            access.delete()
            return HttpResponseRedirect(self.request.path_info)

        print("Operation selection error")
        return HttpResponseRedirect(self.request.path_info)
