from django.shortcuts import render, redirect
from django.urls import reverse
from coordenacao.models import User

def view_perfil(request):
    if request.method == 'GET' and request.session['user_id']:
        try:
            user = User.objects.get(cpf=request.session['user_id'])
            if request.session['user_type'] == 1:
                perfil_name = 'coordenador/perfil-coordenador'
            elif request.session['user_type'] == 2:
                perfil_name = 'professor/perfil-professor'
            else:
                perfil_name = 'aluno/perfil-aluno'
            print(f'coordenacao/{perfil_name}.html')
            return render(request, f'coordenacao/{perfil_name}.html', {'user':user})
        except:
            return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))

def form_editar_perfil(request):
    if request.session['user_id']:
        try:
            user = User.objects.get(cpf=request.session['user_id'])
            return render(request, 'coordenacao/editar-dados.html', {'user':user})
        except:
            return redirect(reverse('index'))
    return redirect(reverse('index'))

def edit_user(request):
    if request.method == 'POST' and request.session['user_id']:
        try:
            User.objects.filter(pk=request.session['user_id']).update(
                nome = request.POST['nome'],
                email = request.POST['email'],
                telefone = request.POST['telefone'],
                endereco = request.POST['endereco'],
                bairro = request.POST['bairro'],
                cidade = request.POST['cidade'],
                estado = request.POST['estado'])
            return redirect(reverse('view_perfil'))
        except:
            return redirect(reverse('index'))
    return redirect(reverse('index'))

def edit_password(request):
    if request.method == 'POST' and request.session['user_id']:
        try:
            user = User.objects.get(cpf=request.session['user_id'])
            if request.POST['password'] == user.password:
                user = User.objects.filter(cpf=request.session['user_id']).update(
                    password = request.POST['password2'])
                return redirect(reverse('view_perfil'))
            return redirect(reverse('form_perfil'))
        except:
            return redirect(reverse('index'))
    return redirect(reverse('index'))