from django.db import models
from event.models import Event


# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=255)
    seat_no = models.CharField(max_length=255)
    gender = models.BooleanField()
    profile = models.TextField(default=None)
    dob = models.DateField()
    email = models.EmailField()
    face = models.BooleanField()
    facial_feature = models.TextField(default=None)
    memo = models.TextField()
    status = models.PositiveSmallIntegerField()
    role = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event_Participant(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_1 = models.CharField(max_length=30)
    phone_2 = models.CharField(max_length=30, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
