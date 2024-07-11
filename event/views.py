from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import HttpResponseServerError,JsonResponse
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
    context={
        "event":Event.objects.all(),
        "user":User.objects.all()
    }

    return render(request,"event/index.html",context)

def edit(request,id):
    event=get_object_or_404(Event,id=id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.starttime = request.POST.get('starttime')
        event.endtime = request.POST.get('endtime')
        event.venue = request.POST.get('venue')
        event.organizer = request.POST.get('organizer')
        event.memo = request.POST.get('memo')
        event.save()
        return JsonResponse({'message': 'Event updated successfully.'})
    else:
        context = {
         'name': event.name,
        'starttime': event.starttime,
        'endtime': event.endtime,
        'venue': event.venue,
        'memo': event.memo,
        'organizer': event.organizer.id
        }
        return JsonResponse(context)