import os
from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(
        default=False,
    )
    tv = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    images = models.ManyToManyField("Image")

    @property
    def is_booked(self):
        return datetime.today().date() in self.reservation_set.all().values_list(
            "date", flat=True
        )

    def __str__(self):
        return self.name


class Reservation(models.Model):
    client = models.CharField(
        max_length=50,
        help_text="Name and Last name of the client who is making this order",
    )
    date = models.DateField()
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()


class Image(models.Model):
    image = models.ImageField(upload_to="galery")

    def __str__(self):
        return os.path.splitext(os.path.basename(self.image.name))[0]
