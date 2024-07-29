from django.shortcuts import render
from .models import Message
from django.http import JsonResponse
from event.models import Event
from django.shortcuts import get_object_or_404

# Create your views here.
def message_view(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        sender = request.POST.get('sender')
        content = request.POST.get('content')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        # message_type = request.POST.get('type', None)

        try:
            message = Message(  
                subject = subject,
                sender = sender,
                content = content,
                startDate = startDate,
                endDate = endDate,
                # type = message_type

            )
            message.save()
        
            return JsonResponse({'status': 'success', 'message': "Message have been created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    elif request.method == "GET":
        messages = Message.objects.all()
        events = Event.objects.all()

    return render(request, 'message/message.html', context = {'messages': messages, 'events': events})

def get_message_details(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(Message, id = message_id)
        detailsubject = request.POST.get('detailsubject')
        detailcontent = request.POST.get('detailcontent')
        detailstartDate = request.POST.get('detailstartDate')
        detailendDate = request.POST.get('detailendDate')

        try:
            message.subject = detailsubject
            message.content = detailcontent
            message.startDate = detailstartDate
            message.endDate = detailendDate
            message.save()
        
            return JsonResponse({'status': 'success', 'message': "Message have been created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    if request.method == 'GET':
        message = get_object_or_404(Message, id = message_id)
        #event = get_object_or_404(Event, id = event_id)
        detail = {
            "id": message.id,
            "subject": message.subject,
            "content": message.content,
            "startDate": message.startDate,
            "endDate": message.endDate,
            #"type": message.type,
            #"createdDate": event.created_at.isoformat(),
            #"finishedDate": event.updated_at.isoformat()
        }
        return JsonResponse(detail)