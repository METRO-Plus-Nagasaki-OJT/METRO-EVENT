from django.db import models
from participant.models import Participant


# Create your models here.
class Attendance(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    entry_1 = models.TimeField(null=True)
    leave_1 = models.TimeField(null=True)
    entry_2 = models.TimeField(null=True)
    leave_2 = models.TimeField(null=True)
    date = models.DateField()
    cmd = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
