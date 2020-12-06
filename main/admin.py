from django.contrib import admin
from main.models import Room, Reservation, Image


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "projector", "tv", "air_conditioning")


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("client", "rooms", "date")


admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Image)
