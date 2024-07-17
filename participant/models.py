from django.db import models
from event.models import Event


# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=255)
    seat_no = models.CharField(max_length=255)
    gender = models.BooleanField()
    profile = models.TextField(default=None, null=True)
    dob = models.DateField()
    email = models.EmailField()
    face = models.BooleanField(default=False)
    facial_feature = models.TextField(default=None,null=True)
    memo = models.TextField(default=None,null=True)
    status = models.PositiveSmallIntegerField(default=0)
    role = models.PositiveSmallIntegerField()
    phone_1 = models.CharField(max_length=30)
    phone_2 = models.CharField(max_length=30, default=None,null=True)
    address = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
