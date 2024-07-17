from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.http import HttpResponseServerError,JsonResponse
from django.db.models import Count
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
    events = Event.objects.annotate(participant_count=Count('participant'))
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
            'starttime': event.start_time,
            'endtime': event.end_time,
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