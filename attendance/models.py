from django.db import models
from participant.models import Participant


# Create your models here.
class Attendance(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    entry_1 = models.TimeField()
    leave_1 = models.TimeField()
    entry_2 = models.TimeField()
    leave_2 = models.TimeField()
    date = models.DateField()
    cmd = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
