from django.shortcuts import render
from .models import Message
from django.http import JsonResponse
from event.models import Event

# Create your views here.
def message_view(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        sender = request.POST.get('sender')
        content = request.POST.get('content')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        message_type = request.POST.get('type')

        message = Message(
            subject = subject,
            sender = sender,
            content = content,
            startDate = startDate,
            endDate = endDate,
            type = message_type

        )
        message.save()
        
        return JsonResponse({'status': 'success', 'message': "Message have been created successfully!"})
    
    elif request.method == "GET":
        messages = Message.objects.all()
        events = Event.objects.all()

    return render(request, 'message/message.html', context = {'messages': messages, 'events': events})