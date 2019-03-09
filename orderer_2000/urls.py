from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^all_rooms/', views.RoomList.as_view()),
    url(r'^room/new$', views.add_room),
    url(r'^room/delete/(?P<id>\d+)$', views.delete_room)

]
