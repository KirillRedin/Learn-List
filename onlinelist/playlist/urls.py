from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^login/$', views.LogIn.as_view(), name='LogIn'),
    url(r'^logout/$', views.LogOut.as_view(), name='LogOut'),
    url(r'^LearnList/$', views.PlaylistList.as_view(), name='MainPage'),
    url(r'^LearnList/accessible/', views.AccessiblePlaylists.as_view(), name='AccessiblePlaylists'),
    url(r'^LearnList/user/(?P<id>[0-9]+)/$', views.UserDetail.as_view(), name='UserProfile'),
    url(r'^LearnList/playlist/(?P<id>[0-9]+)/$', views.PlaylistDetail.as_view(), name='PlaylistPage'),
]