from django.shortcuts import render
from django.http import HttpResponse
from main.models import *
from django.views.generic import ListView
from django.http import HttpResponse


def test(request):
    return HttpResponse("test")

class RoomList(ListView):
    pass



def add_room(request):
    if request.method == "GET":
        return render(request, "add_room.html")
    if request.method == "POST":
        rooms = Room()
        rooms.name = request.POST['name']
        rooms.capacity = request.POST['capacity']
        if request.POST['projector'] == "Tak":
            rooms.projector = True
        if request.POST['projector'] == "Nie":
            rooms.projector = False
        if request.POST['tv'] == "Tak":
            rooms.tv = True
        if request.POST['tv'] == "Nie":
            rooms.tv = False
        if request.POST['air_conditioning'] == "Tak":
            rooms.air_conditioning = True
        if request.POST['air_conditioning'] == "Nie":
            rooms.air_conditioning = False
        rooms.save()
        return HttpResponse("Dodano pokój")

