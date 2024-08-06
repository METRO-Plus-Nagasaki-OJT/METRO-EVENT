from django.shortcuts import render
from .models import Message
from django.http import JsonResponse
from event.models import Event
from participant.models import Participant
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your views here.
def message_view(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        sender = request.POST.get('sender')
        content = request.POST.get('content')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        createdDate = request.POST.get('createdDate')
        event_id = request.POST.get('event')
        type_value = request.POST.get('type')

        print(f"Received data: subject={subject}, sender={sender}, content={content}, startDate={startDate}, endDate={endDate}, createdDate={createdDate}, event_id={event_id}, type_value-{type_value}")
        
        if type_value == '1':
            message_type = 'one'
        elif type_value == "2":
            message_type = 'many'
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid type selected.'}, status = 400)
        try:
            event = get_object_or_404(Event, id=event_id)
            message = Message(
                subject = subject,
                sender = sender,
                content = content,
                startDate = startDate,
                endDate = endDate,
                createdDate = createdDate,
                event = event,
                type = message_type

            )
            message.save()
        
            return JsonResponse({'status': 'success', 'message': "Message have been created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    elif request.method == "GET":
        messages = Message.objects.all().order_by('-id')
        events = Event.objects.all()
        now = timezone.now()
        for message in messages:
            if message.startDate and message.endDate:
                if now < message.startDate:
                    message.status_display = 'Upcoming'
                elif message.startDate <= now <= message.endDate:
                    message.status_display = 'Current'
                else:
                    message.status_display = 'End'

    return render(request, 'message/message.html', context = {'messages': messages, 'events': events})

def get_message_details(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(Message, id = message_id)
        detailsubject = request.POST.get('detailsubject')
        detailcontent = request.POST.get('detailcontent')
        detailstartDate = request.POST.get('detailstartDate')
        detailendDate = request.POST.get('detailendDate')
        detailtype = request.POST.get('detailtype')

        if detailsubject.strip():
            message.subject = detailsubject
        if detailcontent.strip():
            message.content = detailcontent
        if detailstartDate.strip():
            message.startDate = detailstartDate
        if detailendDate.strip():
            message.endDate = detailendDate
        if detailtype:
            if detailtype == '1':
                message.type = 'one'
            elif detailtype == '2':
                message.type = 'many'
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid type provided.'}, status=400)

        try:
            message.save()
        
            return JsonResponse({'status': 'success', 'message': "Message have been created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    if request.method == 'GET':
        message = get_object_or_404(Message, id = message_id)
        
        if message.type:
            if message.type == 'one':
                message.type = '1'
            elif message.type == 'many':
                message.type = '2'
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid type provided.'}, status=400)

        detail = {
            "id": message.id,
            "subject": message.subject,
            "content": message.content,
            "startDate": message.startDate,
            "endDate": message.endDate,
            "createdDate": message.createdDate,
            "type": message.type,
        }
        return JsonResponse(detail)

def autocomplete_suggestions(request):
    query = request.GET.get('q', '')
    event_id = request.GET.get('event_id', '')

    if not query or not event_id:
        return JsonResponse([], safe = False)

    try:
        participants = Participant.objects.filter(
            event_id = event_id,
            name__icontains = query
        ).values('id', 'name') [:10]

        return JsonResponse(list(participants), safe = False)

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status = 500)