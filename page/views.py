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


class SearchView(View):
    def get(self, request):
        if len(request.GET) == 0:
            return render(request, "search_room.html")

        else:
            least_capacity = request.GET.get("least_capacity", False) or False
            projector = request.GET.get("projector", False)
            date = request.GET.get("date", False) or False
            filters = {"projector": False}
            if least_capacity is not False:
                filters.update({"capacity__gte": int(least_capacity)})

            if projector is not False:
                filters.update({"projector": True})

            if date is not False:
                filters.update({"date": datetime.strptime(date, "%Y-%m-%d")})

            return render(
                request,
                "list_available_rooms.html",
                {"results": Room.objects.filter(**filters)},
            )


class ReservationView(View):
    def post(self, request, pk):
        pk = self.kwargs["pk"]
        room = Room.objects.get(pk=pk)
        date_string = request.POST.get("date")
        client = request.POST.get("client")
        if date_string != "":
            date = datetime.strptime(date_string, "%Y-%m-%d")
            if date < datetime.today().replace(
                hour=0, minute=0, second=0, microsecond=0
            ):
                print(
                    "old date",
                )
                pass
                # @TODO django message about old date
            elif len(Reservation.objects.filter(rooms=room, date=date)) > 0:
                print("date reserver")
                pass
                # @TODO django message about already booked date
            else:
                # @TODO django message about success
                r = Reservation.objects.create(rooms=room, date=date, client=client)
                r.save()
        else:
            print("no date")
            pass
            # @TODO django message about no date
        return redirect("room_detail", pk=pk)


class DeleteReservation(edit.DeleteView):
    model = Reservation
    template_name = "remove_reservation.html"

    def get_success_url(self):
        return reverse_lazy("room_detail", kwargs={"pk": self.object.rooms.pk})
