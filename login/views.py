from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('senha')
    
        user = authenticate(username=username, password=password)

        if user:
            return redirect(reverse('home'))
        else:
            messages.error(request, "Login inválido")
    return render(request, 'login.html')    


