from django.shortcuts import render
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

# def edit(request,id):
#     if request.method == 'POST':
#         event = Event.objects.get(pk=id)
#         event.name = request.POST.get('name')
#         event.starttime = request.POST.get('starttime')
#         event.endtime = request.POST.get('endtime')
#         event.venue = request.POST.get('venue')
#         event.organizer = request.POST.get('organizer')
#         event.memo = request.POST.get('memo')
#         event.save()
#         return JsonResponse({'message': 'Event updated successfully.'})
#     else:
#         event = Event.objects.get(pk=id)
#         context = {'event': event}
#         return render(request, 'edit_event.html', context)