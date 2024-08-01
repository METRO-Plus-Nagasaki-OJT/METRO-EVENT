from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.http import HttpResponseServerError,JsonResponse
from django.db.models import Count
from django.utils import timezone
# Create your views here.
def index(request):
    
    if request.method=="POST":
            name=request.POST.get("name")
            start=request.POST.get("starttime")
            end=request.POST.get("endtime")
            venue=request.POST.get("venue")
            organizer_id=request.POST.get("organizer")
            memo=request.POST.get("memo")
            organizer = User.objects.get(id=organizer_id) 
            event=Event(name=name,start_time=start,end_time=end,venue=venue,memo=memo,admin=organizer)
            event.save()
            return JsonResponse({"success":"True"})
    current_time=timezone.now()
    events = Event.objects.annotate(participant_count=Count('participant'),attendance_count=Count('participant__attendance')).values('id', 'name', 'start_time', 'end_time', 'participant_count', 'attendance_count').order_by('id')
    for event in events:
        if event['start_time'] <= current_time <= event['end_time']:
            event['status'] = 'Open'
        elif current_time > event['end_time']:
            event['status'] = 'Closed'
        else:
            event['status'] = 'Upcoming'

    context={
        "event":events,
        "user":User.objects.all()
    }

    return render(request,"event/index.html",context)

def edit(request,id):
    event = get_object_or_404(Event, id=id)
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('editname')
        start_time = request.POST.get('editstarttime')
        end_time = request.POST.get('editendtime')
        venue = request.POST.get('editvenue')
        organizer_id = request.POST.get('editorganizer')
        memo = request.POST.get('editmemo')

        # Validate and assign new values to the event instance
        event.name = name if name else event.name
        event.start_time = start_time if start_time else event.start_time
        event.end_time = end_time if end_time else event.end_time
        event.venue = venue if venue else event.venue
        event.memo = memo if memo else event.memo

        # Fetch the user object based on the organizer_id
        if organizer_id:
            try:
                event.admin = User.objects.get(id=organizer_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Organizer does not exist.'}, status=400)
        
        event.save()
        return JsonResponse({'message': 'Event updated successfully.'})
    
    else:
        users = User.objects.all()
        context = {
            'name': event.name,
            'created_at': event.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': event.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'venue': event.venue,
            'memo': event.memo,
            'user_id': event.admin.id
        }
        return JsonResponse(context)

def delete(request,id):
    if request.method == 'POST':
        product = get_object_or_404(Event, id=id)
        product.delete()    
        return redirect('event')  # Redirect to the product list page or another page after deletion
    context={
        "event":Event.objects.all()
    }
    return JsonResponse(context)