from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import localtime
from django.utils import timezone

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toLocaleString(self, key):
        return datetime.fromisoformat(localtime(key).isoformat()).strftime(
            "%Y/%m/%d %H:%M"
        )

    @property
    def date(self):
        start_time = datetime.fromisoformat(
            localtime(self.start_time).isoformat()
        ).strftime("%Y/%m/%d %H:%M")
        end_time = datetime.fromisoformat(
            localtime(self.end_time).isoformat()
        ).strftime("%Y/%m/%d %H:%M")
        return f"{start_time} - {end_time}"

    @property
    def locale_format_start_time(self):
        return datetime.fromisoformat(localtime(self.start_time).isoformat()).strftime(
            "%Y-%m-%dT%H:%M"
        )

    @property
    def locale_format_end_time(self):
        return datetime.fromisoformat(localtime(self.end_time).isoformat()).strftime(
            "%Y-%m-%dT%H:%M"
        )

    @property
    def status(self):
        return 1 if self.start_time <= timezone.now() <= self.end_time else 0
