from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from event.models import Event
from django.utils import timezone
from participant.models import Participant

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': "Invalid credentials"})        
    return render(request, 'p_hub_admin/login.html')

def monitoring(request):
    current_time = timezone.now()
    active_events = Event.objects.filter(end_time__gte=current_time)
    
    events_with_status = [
        {
            'id': event.id,
            'name': event.name,
        }
        for event in active_events
    ]
    
    return render(request, 'p_hub_admin/monitoring.html', {'events': events_with_status})

def participants_list(request, event_id):
    participants = Participant.objects.filter(event__id=event_id)
    participants_data = [
        {
            'name': participant.name,
            'seat_no': participant.seat_no
        }
        for participant in participants
    ]
    return JsonResponse({'participants': participants_data})
def menu(request):
    return render(request,"p_hub_admin/menu.html")
