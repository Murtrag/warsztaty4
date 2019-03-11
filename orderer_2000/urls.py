from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^all_rooms/', views.RoomList.as_view()),
    url(r'^room/new$', views.add_room, name="room_new"),
    url(r'^room/delete/(?P<id>\d+)$', views.delete_room, name="room_delete"),
    url(r"^room/(?P<pk>\d+)", views.DetailRoom.as_view(), name="room_detail"),
    url(r'^room/modify/(?P<id>\d+)$', views.edit_room, name="room_modify"),
]
