from django.shortcuts import render, get_object_or_404
from .models import Participant
from event.models import Event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import binascii
from django.core.paginator import Paginator
from .qr_creator import create_qr, send_qr
from attendance.face_capture import capture_face, get_encode
import numpy as np
import cv2
import pickle as pkl
from django.shortcuts import HttpResponse

@csrf_exempt
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
        event_id = request.POST.get('event') 
        event = get_object_or_404(Event, id=event_id)

        # Handle base64-encoded image data
        if 'fileInput' in request.FILES:
            profile = request.FILES["fileInput"]
            img = base64.b64encode(profile.read())
            profile = img.decode('utf-8')
            np_img = cv2.cvtColor(np.frombuffer(img, dtype=np.uint8), cv2.COLOR_RGB2BGR)
            face, detection_status = capture_face(np_img)
            if detection_status == True:
                
            
        else:
            profile = None

        participant = Participant(
            name=name,
            email=email,
            seat_no=seat_no,
            dob=dob,
            gender=gender,
            role=role,
            phone_1=phone_1,
            phone_2=phone_2,
            memo=memo,
            address=address,
            event=event,
            profile=profile 
        )
        participant.save()
        create_qr(participant.id)
        send_qr(email, "", "", True, 'common/QR.png')
        return JsonResponse({'status': 'success', 'message': 'Participant registered successfully!'})

    elif request.method == 'GET':
        participants = Participant.objects.all().order_by('-created_at')
        events = Event.objects.all()

        # Handling pagination
        per_page = request.GET.get('per_page', 10)
        paginator = Paginator(participants, per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        return render(request, 'participant/participant.html', context={
            'page': page,
            'events': events,
            'per_page': per_page,
        })

@csrf_exempt
def get_participant_data(request, participant_id):
    if request.method == 'GET':
        participant = get_object_or_404(Participant, id=participant_id)

        try:
            profile_data = base64.b64decode(participant.profile)
        except (binascii.Error, TypeError) as e:
            print(f"Error decoding profile data: {e}")
            profile_data = None

        data = {
            'name': participant.name,
            'email': participant.email,
            'seat_no': participant.seat_no,
            'dob': participant.dob,
            'phone_1': participant.phone_1,
            'phone_2': participant.phone_2,
            'memo': participant.memo,
            'address': participant.address,
            'role': participant.role,
            'gender': participant.gender,
            'created_at': participant.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': participant.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'image_data': base64.b64encode(profile_data).decode('utf-8') if profile_data else None,
            'editPf': bool(participant.profile),
        }
        return JsonResponse(data)

def delete_participant(request, participant_id):
    print(request.method)
    if request.method == 'DELETE':
        participant = get_object_or_404(Participant, pk=participant_id)
        participant.delete()
        return JsonResponse({'message': 'Participant deleted successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

def update_participant(request, participant_id):
    if request.method == 'POST':
        participant = get_object_or_404(Participant, id=participant_id)
        
        # Retrieve data from POST request
        name = request.POST.get('editname')
        email = request.POST.get('editemail')
        seat_no = request.POST.get('editseat_no')
        dob = request.POST.get('editdob')
        gender = request.POST.get('editgender')
        role = request.POST.get('editrole')
        phone_1 = request.POST.get('editphone_1')
        phone_2 = request.POST.get('editphone_2')
        memo = request.POST.get('editmemo')
        address = request.POST.get('editaddress')
        event_id = request.POST.get('event') 
        event = get_object_or_404(Event, id=event_id)

        # Handle base64-encoded image data if provided
        if 'editfileInput' in request.FILES:
            profile = request.FILES["editfileInput"]
            img = profile.read()
            profile = base64.b64encode(img).decode('utf-8')  
        else:
            profile = participant.profile  

        # Update 
        participant.name = name
        participant.email = email
        participant.seat_no = seat_no
        participant.dob = dob
        participant.gender = gender
        participant.role = role
        participant.phone_1 = phone_1
        participant.phone_2 = phone_2
        participant.memo = memo
        participant.address = address
        participant.event = event
        participant.profile = profile
        
        participant.save()

        # Prepare response data
        response_data = {
            'status': 'success',
            'updatedInfo': {
                'email': participant.email,
            }
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def send_update_notification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_qr(email)  
        return HttpResponse(status=200)
    return HttpResponse(status=400)