from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import localtime
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User,on_delete=models.CASCADE)
    start_time= models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toLocaleString(self, key):
        return datetime.fromisoformat(localtime(key).isoformat()).strftime('%Y/%m/%d %H:%M')