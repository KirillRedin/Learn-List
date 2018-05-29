from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^login/$', views.LogIn.as_view(), name='LogIn'),
    url(r'^LearnList/$', views.PlaylistList.as_view(), name='MainPage'),
    url(r'^LearnList/user/(?P<id>[0-9]+)/$', views.UserDetail.as_view(), name='UserProfile'),
    url(r'^LearnList/playlist/(?P<id>[0-9]+)/$', views.PlaylistDetail.as_view(), name='PlaylistPage'),
]