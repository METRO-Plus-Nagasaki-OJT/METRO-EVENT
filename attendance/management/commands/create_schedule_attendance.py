from attendance.models import Attendance
from participant.models import Participant
from event.models import Event
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand

def get_event_ids():
    now = timezone.localtime(timezone.now())
    ongoing_events = Event.objects.filter(end_time__gt=now)
    event_ids = list(ongoing_events.values_list('id', flat=True))
    print(event_ids)
    return event_ids

def attendance_scheduling():
    today = datetime.now().date()
    current_weekday = datetime.weekday(today)
    if current_weekday != 4 or current_weekday != 5:
        for event_id in get_event_ids():
            participant_ids = list(Participant.objects.filter(event__id=event_id).values_list("id", flat=True))
            print(participant_ids)
            for participant_id in participant_ids:
                Attendance.objects.create(participant_id=participant_id, date=today)
        print("finished creating")

class Command(BaseCommand):
    help = 'Run Attendance Schedule Automation Code'
    def handle(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        if now.hour >= 12:
            print('Running custom automation code')
            attendance_scheduling()