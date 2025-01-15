from django.shortcuts import render

# Create your views here.

def faturamento(request):
    return render(request, 'faturamento.html')