from django.shortcuts import render
from django.http import HttpResponse
from main.models import *
# Create your views here.


def add_room(request):
    if request.method == "GET":
        return render(request, "add_room.html")
    if request.method == "POST":
        rooms = Room()
        rooms.name = request.POST['name']
        rooms.capacity = request.POST['capacity']
        rooms.tv = request.POST['tv']
        rooms.air_conditioning = request.POST['air_conditioning']
        rooms.save()
        return HttpResponse("Dodano pokój")

