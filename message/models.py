from django.db import models
from event.models import Event

# Create your models here.
class Message(models.Model):
    TYPE_CHOICES = [
        ('one', 'One Time'),
        ('many', 'Many Times')
    ]
    subject = models.CharField(max_length = 255)
    sender = models.CharField(max_length = 255)
    content = models.CharField(max_length = 255)
    startDate = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)
    createdDate = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length = 255, choices = TYPE_CHOICES, default='one')

    def __str__(self):
        return self.subject
