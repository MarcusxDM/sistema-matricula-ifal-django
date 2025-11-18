import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q

from coordenacao.models import User, Coordenador, Professor
from coordenacao.models import Curso, Disciplina, Oferta
from coordenacao.models import Matricula, Atividade, Resposta

def index(request):
    '''
    Página de index
    '''
    request.session.flush()
    versao = "4.0.1"
    print(f'Sistema de Matrícula - Versão {versao}')
    return render(request, 'coordenacao/login.html', {})

def login(request):
    '''
    Recebe POST com CPF e Senha
    efetua o login
    Retorna para o index caso falhe, ou redireciona para o Home caso tenha sucesso
    user_type:
        1 = Coordenador
        2 = Professor
        3 = Aluno
    '''
    if request.method == 'POST':
        try:
            user = User.objects.get(cpf=request.POST['cpf'])
            print(user)
            if user.password == request.POST['password']:
                # Success Login
                request.session['login_error'] = ""
                request.session['user_id'] = user.cpf
                try:
                    Coordenador.objects.get(user_id=request.session['user_id'])
                    request.session['user_type'] = 1
                except Coordenador.DoesNotExist:
                    try:
                        Professor.objects.get(user_id=request.session['user_id'])
                        request.session['user_type'] = 2
                    except Professor.DoesNotExist:
                        request.session['user_type'] = 3
                return redirect('home')
            else:
                request.session['login_error'] = 'Senha incorreta'
                return redirect(reverse('index'))
        except:
            request.session['login_error'] = 'Usuário não encontrado'
            return redirect(reverse('index'))
    return redirect(reverse('index'))

def home(request):
    '''
    Página Home
    '''
    # try:
    user_name = User.objects.get(cpf=request.session['user_id']).nome
    request.session['user_name'] = user_name
    atividades=[] 
    cursos=[]
    if request.session['user_type'] == 1:
        home_name = 'coordenador/home-coordenador'
        cursos = Curso.objects.filter(created_by__pk=request.session['user_id'])
        disciplinas = Disciplina.objects.filter(curso__in=cursos)
        ofertas = Oferta.objects.filter(professor=None, disciplina__in=disciplinas)
    elif request.session['user_type'] == 2:
        home_name = 'professor/home-professor'
        ofertas = Oferta.objects.filter(professor__pk=request.session['user_id'], periodo__end_date__gte=datetime.date.today())
        atividades = Atividade.objects.filter(oferta__in=ofertas)
        respostas = Resposta.objects.filter(atividade__in=atividades, nota=None)
        atividades_sem_nota = []
        for r in respostas:
            atividades_sem_nota.append(r.atividade.id)
        atividades = Atividade.objects.filter(pk__in=atividades_sem_nota).order_by('entrega_date')

    else:
        home_name = 'aluno/home-aluno'
        matriculas = Matricula.objects.filter(aluno__pk=request.session['user_id'], oferta__periodo__end_date__gte=datetime.date.today())
        ofertas = []
        for m in matriculas:
            ofertas.append(m.oferta)
        atividades = Atividade.objects.filter(oferta__in=ofertas, entrega_date__gte=datetime.date.today())
        respostas = Resposta.objects.filter(aluno__pk=request.session['user_id'], atividade__in=atividades)

        atividades_feitas = []
        for r in respostas:
            atividades_feitas.append(r.atividade.id)

        ofertas_id = []
        for o in ofertas:
            ofertas_id.append(o.id)
        ofertas_nao_matriculadas = Oferta.objects.exclude(pk__in=ofertas_id)
        atividades = Atividade.objects.exclude(Q(pk__in=atividades_feitas) | Q(oferta__in=ofertas_nao_matriculadas)).order_by('entrega_date')
    print(f'coordenacao/{home_name}.html')
    return render(request, f'coordenacao/{home_name}.html', {'ofertas' : ofertas,
                                                            'atividades' : atividades,
                                                            'cursos' : cursos})

def logout(request):
    '''
    Faz logout, limpa Session
    '''
    request.session.flush()
    return redirect(reverse('index'))