from django.apps import AppConfig, apps
from django.core.management import call_command
import sys

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
