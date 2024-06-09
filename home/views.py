from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
def home(request):
    return render(
        request,
        'home.html',
    )

# def clientes(request):
#     return redirect(reverse('cadastro_clientes'))
