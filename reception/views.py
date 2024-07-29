from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "reception/index.html")


def client(request):
    return render(request, "reception/client.html")


def client_v2(request):
    return render(request, "reception/client_v2.html")


def settings(request):
    return render(request, "reception/settings.html")
