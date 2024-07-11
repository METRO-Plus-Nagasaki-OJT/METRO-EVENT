from django.shortcuts import render
from .models import Participant  
from event.models import Event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404


def participant(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        seat_no = request.POST.get('seat_no')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        phone_1 = request.POST.get('phone_1')
        phone_2 = request.POST.get('phone_2')
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
            phone1=phone_1,
            phone2=phone_2,
            memo=memo,
            address=address
        )
        participant.save()

        return JsonResponse({'status': 'success', 'message': 'Participant registered successfully!'})

    elif request.method == 'GET':
        participants = Participant.objects.all()
        events = Event.objects.all()
        
        return render(request, 'participant/participant.html', context={'participants': participants, 'events': events})

@csrf_exempt
def get_participant_data(request, participant_id):
    if request.method == 'GET':
        participant = get_object_or_404(Participant, id=participant_id)
        data = {
            'name': participant.name,
            'email': participant.email,
            'seat_no': participant.seat_no,
            'dob': participant.dob,
            'phone1': participant.phone_1,
            'phone2': participant.phone_2,
            'memo': participant.memo,
            'address': participant.address,
            'role': participant.role,
            'gender': participant.gender,
            # 'image_url': participant.image_url,  # Assuming you have this field in your model
        }
        return JsonResponse(data)

