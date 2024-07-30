from django.db import models
from event.models import Event
from django.utils import timezone


# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    seat_no = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    facial_feature = models.TextField(default=None, null=True)
    face = models.BooleanField(default=False)
    role = models.CharField(max_length=50)
    phone_1 = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.TextField(blank=True, null=True)

    def is_event_over(self):
        return timezone.now() > self.event.end_time

    def __str__(self):
        return self.name
