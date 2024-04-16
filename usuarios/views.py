from django.shortcuts import render, redirect 
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

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
            print('Erro 1')
            return redirect('/usuarios/cadastro')
        
        if senha != confirmar_senha:
            print('Erro')
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            print('Erro 3')
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
            return redirect('/usuarios/login/')

        except IntegrityError as e:
            print('Err: Erro Interno do sistena', e)
            return redirect('/usuarios/cadastro')