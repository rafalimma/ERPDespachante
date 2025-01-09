from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Filial
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('senha')
    
        user = authenticate(username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect(reverse('home') + '?periodo=mensal')
        else:
            messages.error(request, "Usuários ou senha inválidos.")
    return render(request, 'login.html')

def logout_option(request):
    logout(request)
    return redirect('login')

def login_sessao_expirada(request):
    messages.warning(request, 'Sua sessão foi expirada!')
    return redirect('login')

def paginacao(request):
    usuarios = User.objects.all().values('id', 'username', 'first_name', 'last_name')
    servicos_paginados = Paginator(usuarios, 10)
    page_num = request.GET.get('page')
    usuarios = servicos_paginados.get_page(page_num)

    return render(request, 'usuarios.html', {'usuarios': usuarios})

@login_required
def usuarios(request):
    usuarios = User.objects.all().values('id', 'username', 'first_name', 'last_name', 'is_active')
    return render(request, 'usuarios.html', {'usuarios': usuarios})

@login_required
def novo_usuario(request):
    groups = Group.objects.all()
    return render(request, 'novo_usuario.html', {'groups': groups})

def cadastro_usuario(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        nome_usuario = request.POST.get('nome_usuario')
        email = request.POST.get('email')
        group_id = request.POST.get('group')
        status = request.POST.get('status')
        password = request.POST.get('senha')

        if User.objects.filter(username=nome_usuario).exists():
            messages.error(request, "Usuário já existente!")
            return redirect(novo_usuario)
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email do usuário já existente!")
            return redirect(novo_usuario)
        
        if not all([first_name, second_name, nome_usuario, email, group_id]):
            messages.error(request, 'Preencha todos os campos!')
            return redirect(novo_usuario)
        
        usuario = User.objects.create_user(first_name=first_name, last_name=second_name,
                       email=email, username=nome_usuario, is_active=status, password=password)
        
        group = Group.objects.get(id=group_id)
        usuario.groups.add(group)
        
        usuario.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
    return redirect(usuarios)

@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    groups = Group.objects.all()
    return render(request,
                  'editar_usuario.html',
                  {'usuario': usuario,
                   'groups': groups}
                  )

def form_edicao_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('id_usuario')
        usuario = get_object_or_404(User, pk=usuario_id)
        print(usuario)
        usuario.username = request.POST.get('username')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('second_name')
        usuario.email = request.POST.get('email')
        usuario.is_active = True if request.POST.get('status') == 'on' else False
        group = request.POST.get('group')

        if usuario.username == '' or usuario.email == '' or group=='':
            messages.error(request, 'Preencha todos os campos!')
            return redirect(f'editar_usuario/{usuario_id}')
        
        usuario.save()
        usuario.groups.add(group)
        messages.success(request, 'Usuário editado com sucesso!')
    return redirect(usuarios)




