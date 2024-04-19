from django.shortcuts import render, redirect 
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get('confirmar_senha')
        
        users = User.objects.filter(username=email)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Email já existe!!')
            return redirect('/usuarios/cadastro')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'A senha e o confirmar senha deve ser iguais')
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        try:
    # Criar um novo usuário com o email fornecido como username e email
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, 'Usuario criado com sucesso !!')
            return redirect('/usuarios/login/')

        except IntegrityError as e:
            messages.add_message(request, constants.ERROR, 'Err: erro interno do sistema')
            return redirect('/usuarios/cadastro')
        
def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            return redirect('/pacientes/home')
        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
        return redirect('/usuarios/login/')
    
def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')