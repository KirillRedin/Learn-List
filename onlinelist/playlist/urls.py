from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^login/$', views.LogIn().as_view(), name='LogIn'),
    url(r'^playlists/$', views.PlaylistList().as_view(), name='PlaylistList'),
    url(r'^playlists/(?P<id>[0-9]+)/$', views.PlaylistDetail.as_view(), name='PlaylistDetail'),
]