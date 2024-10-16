from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from event.models import Event
from django.utils import timezone
from participant.models import Participant
from attendance.models import Attendance
from utils.decorators import authenticated_user_exempt
from django.http import HttpResponse
from django.contrib import messages

@authenticated_user_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Your profile was updated.") 
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid credentials"})
    return HttpResponse(render(request, "p_hub_admin/login.html"))


def monitoring(request):
    current_time = timezone.now()
    active_events = Event.objects.filter(end_time__gte=current_time)

    events_with_status = [
        {
            "id": event.id,
            "name": event.name,
        }
        for event in active_events
    ]

    return render(
        request, "p_hub_admin/monitoring.html", {"events": events_with_status}
    )


def participants_list(request, event_id):
    participants = Participant.objects.filter(event__id=event_id)

    attendance_records = Attendance.objects.filter(
        participant__in=participants, date__gte=timezone.now().date()
    )

    attendance_status = {record.participant_id: record for record in attendance_records}

    participants_data = []
    for participant in participants:
        attendance = attendance_status.get(participant.id)

        if attendance:
            if attendance.entry_1 and not attendance.leave_1:
                status = "entry"
            elif attendance.leave_1 and attendance.entry_1:
                status = "leave"
            elif (
                attendance.leave_1
                and attendance.entry_1
                and attendance.entry_2
                and not attendance.leave_2
            ):
                status = "entry"
            elif (
                attendance.leave_1
                and attendance.entry_1
                and attendance.entry_2
                and attendance.leave_2
            ):
                status = "leave"
            else:
                status = "none"
        else:
            status = "none"

        participants_data.append(
            {
                "id": participant.id,
                "name": participant.name,
                "seat_no": participant.seat_no,
                "status": status,
            }
        )

    return JsonResponse({"participants": participants_data})


def menu(request):
    return render(request, "p_hub_admin/menu.html")


def logout_view(request):
    logout(request)
    return  redirect("logout")  
