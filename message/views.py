from django.shortcuts import render

# Create your views here.
def message_view(request):
    return render(request, 'message/message.html')