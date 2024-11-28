from django.shortcuts import render, redirect
from django.urls import reverse
from coordenacao.models import User, Coordenador, Aluno
from coordenacao.models import Curso, Periodo
from sistema_academico.coordenacao.views.utils import generate_password, send_email_new_user

def list_alunos(request):
    '''
    Retorna html com lista de Alunos Cadastrados
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        request.session['aluno_create_error'] = False
        alunos = Aluno.objects.all()
        return render(request, 
                      'coordenacao/coordenador/coordenador-aba-aluno.html', 
                      {'alunos':alunos})
    return redirect(reverse('index'))

def form_aluno(request):
    '''
    Retorna html com formulário de criação de aluno
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        cursos = Curso.objects.filter(
            created_by=Coordenador.objects.get(
                user_id=request.session['user_id']))
        periodos = Periodo.objects.all()
        return render(request, 'coordenacao/coordenador/create-aluno.html', 
                      {'cursos': cursos,
                      'periodos': periodos})
    return redirect(reverse('index'))

def create_aluno(request):
    '''
    Retorna html com formulário de criação de aluno
    '''
    if request.method == 'POST' and request.session['user_type'] == 1:
        try:
            User.objects.get(cpf=request.POST['cpf'])
            request.session['aluno_create_error'] = True
            return redirect(reverse('form_aluno'))
        except:
            # Gera Senha
            passwrd = generate_password()
            # Cria Usuário
            new_user = User(cpf=request.POST['cpf'],
                            email=request.POST['email'],
                            password=passwrd, nome=request.POST['nome'],
                            telefone=request.POST['telefone'],
                            endereco=request.POST['endereco'],
                            bairro=request.POST['bairro'], 
                            cidade=request.POST['cidade'],
                            estado=request.POST['estado'])
            new_user.save()

            # Cria Aluno com novo Usuário
            new_aluno = Aluno(user=new_user,
                              curso_id=request.POST['curso'],
                              periodo_ingresso_id=request.POST['periodo'])
            new_aluno.save()

            # Envia email com senha gerada
            send_email_new_user(request.POST['email'], 
                                passwrd,
                                request.POST['nome'])
            return redirect(reverse('alunos'))
    return redirect(reverse('index'))