from django.db import models

# Create your models here.
class Message(models.Model):
    subject = models.CharField(max_length = 255)
    sender = models.CharField(max_length = 255)
    content = models.CharField(max_length = 255)
    startDate = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)
    createdDate = models.DateTimeField(blank=True, null=True)
    # type = models.CharField(max_length = 255, blank=True, null=True)

    def __str__(self):
        return self.subject
