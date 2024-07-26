from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': "Invalid credentials"})        
    return render(request, 'p_hub_admin/login.html')

def menu(request):
    return render(request,"p_hub_admin/menu.html")