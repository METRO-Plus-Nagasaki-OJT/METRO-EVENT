from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    
    # if request.method=="POST":
    #     name=request.POST.get("name")
    #     venue=request.POST.get("venue")
    #     organizer=request.POST.get("organizer")
    #     memo=request.POST.get("memo")
    #     event=Event.objects.create(name=name,venue=venue,organizer=organizer,memo=memo)
    context={
        "event":Event.objects.all()
    }

    return render(request,"event/index.html",context)