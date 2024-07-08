from django.shortcuts import render
from .models import Participant  

def participant(request):
    participants = Participant.objects.all()  
    context = {
        'participants': participants,
    }
    return render(request, 'participant/participant.html', context)
