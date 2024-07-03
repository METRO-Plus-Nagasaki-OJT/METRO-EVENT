from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'p_hub_admin/login.html')