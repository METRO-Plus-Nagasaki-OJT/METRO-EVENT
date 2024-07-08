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
        participant_no = request.POST.get('participant_no')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2')
        memo = request.POST.get('memo')
        address = request.POST.get('address')

        # Create and save the Participant object
        participant = Participant(
            name=name,
            email=email,
            participant_no=participant_no,
            dob=dob,
            gender=gender,
            occupation=occupation,
            phone1=phone1,
            phone2=phone2,
            memo=memo,
            address=address
        )
        participant.save()

        return JsonResponse({'status': 'success', 'message': 'Participant registered successfully!'})

    elif request.method == 'GET':
        events = Event.objects.all()
        return render(request, 'participant/participant.html', {'events': events})

