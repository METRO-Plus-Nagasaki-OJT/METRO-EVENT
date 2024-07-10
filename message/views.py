from django.shortcuts import render
from .models import Message
from django.http import JsonResponse

# Create your views here.
def message_view(request):
    if request.method == "POST":
        sender = request.POST.get('sender')
        subject = request.POST.get('subject')
        period = request.POST.get('period')
        situation = request.POST.get('situation')

        message = Message(
            sender = sender,
            subject = subject,
            period = period,
            situation = situation
        )
        message.save()
        
        return JsonResponse({'stauts': 'success', 'message': "Message have been created successfully!"})
    
    elif request.method == "GET":
        messages = Message.objects.all()

    return render(request, 'message/message.html')