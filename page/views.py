from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from page.models import Room, Reservation
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, edit
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator


class RoomList(ListView):
    paginate_by = 7
    model = Room
    template_name = "list_room.html"


class DetailRoom(DetailView):
    model = Room
    template_name = "detail_room.html"


class AddRoom(SuccessMessageMixin, edit.CreateView):
    model = Room
    success_message = "Pomyslnie dodano salkę"
    template_name = "add_room.html"
    success_url = reverse_lazy("all_rooms")
    fields = ("name", "capacity", "projector", "tv", "air_conditioning")


class DeleteRoom(edit.DeleteView):
    model = Room
    success_message = "Pomyslnie usunięto salkę"
    success_url = reverse_lazy("all_rooms")
    template_name = "remove_room.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class EditRoom(SuccessMessageMixin, edit.UpdateView):
    model = Room
    success_message = "Pomyslnie zmodyfikowano dane"
    template_name = "edit_room.html"
    fields = ("name", "capacity", "projector", "tv", "air_conditioning")
    success_url = reverse_lazy("edit_room")

    def get_success_url(self):
        return reverse_lazy("room_edit", kwargs={"pk": self.kwargs["pk"]})


class SearchView(View):
    paginate_by = 7

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

            page_number = request.GET.get("page")
            paginator = Paginator(Room.objects.filter(**filters), self.paginate_by)
            page_obj = paginator.get_page(page_number)

            return render(
                request,
                "list_available_rooms.html",
                {"page_obj": page_obj},
            )


class ReservationView(View):
    warning_message = "Nie dokonano rezerwacji z powodu: {}"

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
                messages.warning(
                    self.request,
                    self.warning_message.format("nie można planować przeszłości!"),
                )
            elif len(Reservation.objects.filter(rooms=room, date=date)) > 0:
                messages.warning(
                    self.request,
                    self.warning_message.format(
                        "Salka na ten dzień została już zarezerwowana wcześniej!"
                    ),
                )
            else:
                r = Reservation.objects.create(rooms=room, date=date, client=client)
                r.save()
        else:
            messages.warning(
                self.request, self.warning_message.format("nie podano daty!")
            )
        return redirect("room_detail", pk=pk)


class DeleteReservation(edit.DeleteView):
    model = Reservation
    template_name = "remove_reservation.html"
    success_message = "Pomyslnie usunięto termin"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("room_detail", kwargs={"pk": self.object.rooms.pk})
