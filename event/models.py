from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time= models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
