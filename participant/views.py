from django.shortcuts import render
from .models import Participant  
from event.models import Event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def participant(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        seat_no = request.POST.get('seat_no')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2')
        memo = request.POST.get('memo')
        address = request.POST.get('address')

        # Create and save the Participant object
        participant = Participant(
            name=name,
            email=email,
            seat_no=seat_no,
            dob=dob,
            gender=gender,
            role=role,
            phone1=phone1,
            phone2=phone2,
            memo=memo,
            address=address
        )
        participant.save()

        return JsonResponse({'status': 'success', 'message': 'Participant registered successfully!'})

    elif request.method == 'GET':
        participants = Participant.objects.all()
        events = Event.objects.all()
        
        return render(request, 'participant/participant.html', context={'participants': participants, 'events': events})

