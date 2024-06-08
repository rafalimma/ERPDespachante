from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.

def home(request):
    return render(
        request,
        'home.html',
    )

# def clientes(request):
#     return redirect(reverse('cadastro_clientes'))
