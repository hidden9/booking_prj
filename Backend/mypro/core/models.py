from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_room_manager = models.BooleanField(default=False)


class Room(models.Model):
    name = models.TextField(null=True)
    num_days_in_adv = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class TimeSlot(models.Model):
    time_from = models.TimeField(max_length=4)
    time_to = models.TimeField(max_length=4)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)


class Booking(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)


