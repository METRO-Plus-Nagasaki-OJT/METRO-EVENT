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
            try:
                organizer = User.objects.get(id=organizer_id) 
            except User.DoesNotExist:
                return JsonResponse({"error": "Organizer user does not exist."}, status=400)
            Event.objects.create(name=name,start_time=start,end_time=end,venue=venue,admin=organizer,memo=memo,)
            return JsonResponse({"success":"True"})
    context={
        "event":Event.objects.all()
    }

    return render(request,"event/index.html",context)