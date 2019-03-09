from django.db import models

# Create your dick bigger

class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateField()
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()
