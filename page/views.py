from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from page.models import Room, Reservation
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, edit
from datetime import datetime


class RoomList(ListView):
    model = Room
    template_name = "list_room.html"


class DetailRoom(DetailView):
    model = Room
    template_name = "detail_room.html"


class AddRoom(edit.CreateView):
    model = Room
    template_name = "add_room.html"
    success_url = reverse_lazy("all_rooms")
    fields = ("name", "capacity", "projector", "tv", "air_conditioning")


class DeleteRoom(edit.DeleteView):
    model = Room
    success_url = reverse_lazy("all_rooms")
    template_name = "remove_room.html"


class EditRoom(edit.UpdateView):
    model = Room
    template_name = "edit_room.html"
    fields = ("name", "capacity", "projector", "tv", "air_conditioning")
    success_url = reverse_lazy("edit_room")

    def get_success_url(self):
        return reverse_lazy("room_edit", kwargs={"pk": self.kwargs["pk"]})

    # @TODO message with info that it was successfully modified


def form(request):
    rooms = Room.objects.all()
    return render(request, "form.html", {"rooms": rooms})


def search(request):
    if request.method == "GET":

        id = int(request.GET["id"])
        least_capacity = request.GET.get("least_capacity", False)
        projector = request.GET.get("projector", False)
        date = request.GET.get("date", False)

        rooms = list(range(4))

        if id != -1:
            rooms[0] = Room.objects.filter(id=id)
        else:
            rooms[0] = Room.objects.all()

        if least_capacity:
            rooms[1] = Room.objects.filter(capacity__gte=int(least_capacity))
        else:
            rooms[1] = Room.objects.all()

        if projector:
            rooms[2] = Room.objects.filter(projector=True)
        else:
            rooms[2] = Room.objects.all()

        if date:
            date = datetime.strptime(date, "%Y-%m-%d")
            booked_rooms = [
                room
                for room in Room.objects.all()
                if Reservation.objects.filter(date=date).filter(rooms=room)
            ]
            rooms[3] = [room for room in Room.objects.all() if room not in booked_rooms]
        else:
            rooms[3] = Room.objects.all()

        for i in range(4):
            rooms[i] = set(rooms[i])

        results = rooms[0]

        for i in range(1, 4):
            results = results.intersection(rooms[i])

        results = list(results)

        if results:
            return render(request, "list_available_rooms.html", {"results": results})
        else:
            return HttpResponse("Brak wolnych sal dla podanych kryteriów wyszukiwania")


def reservation(request, id):
    """rezerwacja sali, widok dostępny tylko metodą POST (formularz w widoku sali)"""
    if request.method == "POST":

        id = int(id)
        room = Room.objects.get(id=id)

        date = request.POST.get("date", False)
        if not date:
            return HttpResponse("Proszę podać datę rezerwacji")
        date = datetime.strptime(date, "%Y-%m-%d")
        if date < datetime.today():
            return HttpResponse("Błąd! Data rezerwacji jest datą przeszłą!")
        if Reservation.objects.filter(rooms=room).filter(date=date):
            return HttpResponse("Błąd! Sala jest już zarezerwowana na wybrany dzień!")
        reservation = Reservation.objects.create(rooms=room, date=date)
        reservation.save()
        return redirect("room_detail", pk=id)
