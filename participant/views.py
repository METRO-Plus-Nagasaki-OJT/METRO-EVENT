from django.shortcuts import render, get_object_or_404
from .models import Participant
from event.models import Event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import binascii
from django.core.paginator import Paginator
from .qr_creator import create_qr, send_qr
from attendance.face_capture import capture_face, get_encode, load_pickle, save_embeddings, check_modelnembed
from attendance.unknown_training import train_unknown_classifier
import numpy as np
import cv2
import pickle as pkl
from django.shortcuts import HttpResponse
import json

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
        embeddable = False
        if 'fileInput' in request.FILES:
            profile = request.FILES["fileInput"]
            img = base64.b64encode(profile.read())
            profile = img.decode('utf-8')
            embeddable = True
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
        
        if embeddable:
            image_np = np.fromstring(base64.b64decode(img), dtype=np.uint8)
            np_img = cv2.imdecode(image_np, cv2.IMREAD_ANYCOLOR)
            face, detection_status = capture_face(np_img)
            print("Face captured!")
            if detection_status == True:
                encoding = get_encode(face)
                participant.facial_feature = json.dumps(encoding)
                print("Face embedding registered!")
        participant.save()
        train_unknown_classifier()
        create_qr(participant.id)
        send_qr(email, "", "", True, 'common/QR.png')
        return JsonResponse({'status': 'success', 'message': 'Participant registered successfully!'})

    elif request.method == 'GET':
        search_term = request.GET.get('search', '') 
        participants = Participant.objects.all().order_by('-created_at')
        if search_term:
            participants = participants.filter(
                name__icontains=search_term
            ) | participants.filter(
                seat_no__icontains=search_term
            ) | participants.filter(
                email__icontains=search_term
            )
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
            'search_term': search_term 
        })

def participants_view(request):
    per_page = request.GET.get('per_page', 10)
    search_term = request.GET.get('search', '')

    # Filter participants based on search term
    participants = Participant.objects.all()
    if search_term:
        participants = participants.filter(
            name__icontains=search_term
        ) | participants.filter(
            seat_no__icontains=search_term
        ) | participants.filter(
            email__icontains=search_term
        )
    
    paginator = Paginator(participants, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'participants_table_body.html', {'page': page_obj})
    
    return render(request, 'participants.html', {'page': page_obj, 'per_page': per_page, 'search_term': search_term})

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

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Participant
from event.models import Event
from .qr_creator import create_qr, send_qr

@csrf_exempt
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
        email_status = request.POST.get('email_status')

        # Handle base64-encoded image data if provided
        if 'editfileInput' in request.FILES:
            profile = request.FILES["editfileInput"]
            img = profile.read()
            profile = base64.b64encode(img).decode('utf-8')
        else:
            profile = participant.profile

        # Update participant fields
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

        # Save participant object
        participant.save()

        # Send email notification if email_status is true
        if email_status == 'true':
            send_update_notification(email)

        return JsonResponse({'status': 'success', 'message': 'Participant updated successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def send_update_notification(email):
    send_qr(email, 'Your Information is Updated!', 'Your Information is Updated!', False)

def participants_view(request):
    per_page = request.GET.get('per_page', 10)
    participants = Participant.objects.all() 
    paginator = Paginator(participants, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'participants_table_body.html', {'page': page_obj})
    
    return render(request, 'participants.html', {'page': page_obj, 'per_page': per_page})


