from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
@login_required
def home(request):
    return render(
        request,
        'home.html',
    )

# def clientes(request):
#     return redirect(reverse('cadastro_clientes'))
