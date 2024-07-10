from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length = 255)
    subject = models.CharField(max_length = 255)
    period = models.DateField()
    situation = models.CharField(max_length = 255)
