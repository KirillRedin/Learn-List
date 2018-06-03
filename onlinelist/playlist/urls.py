from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^login/$', views.LogIn.as_view(), name='LogIn'),
    url(r'^logout/$', views.LogOut.as_view(), name='LogOut'),
    url(r'^$', views.PlaylistList.as_view(), name='MainPage'),
    url(r'^accessible/$', views.AccessiblePlaylists.as_view(), name='AccessiblePlaylists'),
    url(r'^users/$', views.UserList.as_view(), name='UserList'),
    url(r'^user/(?P<id>[0-9]+)/$', views.UserDetail.as_view(), name='UserProfile'),
    url(r'^playlist/(?P<id>[0-9]+)/$', views.PlaylistDetail.as_view(), name='PlaylistPage'),
]