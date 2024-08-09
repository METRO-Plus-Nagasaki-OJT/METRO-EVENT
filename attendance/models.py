from django.db import models
from participant.models import Participant


# Create your models here.
class Attendance(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name="attendances"
    )
    entry_1 = models.TimeField(null=True, blank=True)
    leave_1 = models.TimeField(null=True, blank=True)
    entry_2 = models.TimeField(null=True, blank=True)
    leave_2 = models.TimeField(null=True, blank=True)
    date = models.DateField()
    cmd = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        return {
            "label": "完了" if self.entry_1 and self.leave_1 else "未完了",
            "value": 1 if self.entry_2 and self.leave_2 else 2,
        }

    def __str__(self) -> str:
        return f"{self.participant} - {self.date}"
