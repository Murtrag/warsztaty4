import os
from datetime import datetime
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, edit
from page.models import Room, Reservation, Image


class RoomList(ListView):
    paginate_by = 6
    model = Room
    template_name = "list_room.html"


class DetailRoom(DetailView):
    model = Room
    template_name = "detail_room.html"


class AddRoom(SuccessMessageMixin, edit.CreateView):
    model = Room
    success_message = "Pomyslnie dodano salkę, proszę skorzystać z pola pod formularzem aby dołączyć zdjęcia"
    template_name = "add_room.html"
    fields = ("name", "capacity", "projector", "tv", "air_conditioning")

    def get_success_url(self, **kwargs):
        self.request.session["created_room_id"] = self.object.id
        return reverse("room_new")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["created_room_id"] = self.request.session.pop("created_room_id")
        except Exception:
            # created_room_id doas not exist in session, means not any new element were created so skip
            pass
        return context


class UploadImage(View):
    def post(self, request, pk):
        try:
            image_obj = request.FILES["file"]
            assert os.path.splitext(image_obj._name)[1][1:] in [
                "gif",
                "jpg",
            ], "Not an image extension!"
            new_image = Image()
            new_image.image.save(image_obj.name, image_obj)
            new_image.save()
            Room.objects.get(pk=pk).images.add(new_image)
        except Exception as e:
            return HttpResponseBadRequest(f"No Files Attached. {e}")
        return HttpResponse("File Attached.")


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
    paginate_by = 6

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
