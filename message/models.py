from django.db import models
from event.models import Event
from participant.models import Participant
from django.contrib.auth.models import User

# Create your models here.
class MessageRecord(models.Model):
    message = models.ForeignKey('Message', on_delete = models.CASCADE)
    receiver = models.ForeignKey(Participant, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('message', 'receiver')

    def __str__(self):
        return f"Messsage ID: {self.message.id}, Participant ID: {self.receiver.id}"

class Message(models.Model):
    TYPE_CHOICES = [
        ('one', 'One Time'),
        ('many', 'Many Times')
    ]
    subject = models.CharField(max_length = 255)
    sender = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    startDate = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)
    createdDate = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length = 255, choices = TYPE_CHOICES, default='one')
    receivers = models.ManyToManyField(Participant, through ="MessageRecord", related_name = "messages", blank = True)

    def __str__(self):
        return self.subject
