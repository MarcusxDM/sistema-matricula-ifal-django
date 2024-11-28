import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from coordenacao.models import Atividade, Curso, Disciplina, Matricula
from coordenacao.models import Oferta, Periodo, Professor, User
from sistema_academico.coordenacao.views.utils import checkbox_week_days

def form_oferta(request, id_param):
    '''
    Retorna html com lista de ofertas do periodo
    OBS.: apenas ofertas com disciplinas pertencentes aos cursos criados pelo coordenador
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        periodo = get_object_or_404(Periodo, pk=id_param)
        cursos = Curso.objects.filter(created_by__pk=request.session['user_id'])
        disciplinas = Disciplina.objects.filter(curso__in=cursos)
        professores = Professor.objects.all()
        return render(request, 'coordenacao/coordenador/cadastrar-oferta.html',
                      {'professores': professores, 
                       'disciplinas': disciplinas,
                       'periodo': periodo})
    return redirect(reverse('index'))

def create_oferta(request, id_param):
    if request.method == 'POST' and request.session['user_type'] == 1:
        if request.POST['professor'] == "None":
            professor = None
        else:
            professor = Professor.objects.get(pk=request.POST['professor'])
            
        aula_dias = checkbox_week_days(request)
        periodo = get_object_or_404(Periodo, pk=id_param)
        disciplina = get_object_or_404(Disciplina, pk=request.POST['disciplina'])
        new_oferta = Oferta(periodo=periodo,
                            disciplina=disciplina, 
                            professor=professor,
                            capacidade=request.POST['capacidade'],
                            aula_dias=aula_dias, 
                            aula_hora_inicio=request.POST['hora_inicio'],
                            aula_hora_fim=request.POST['hora_fim'])
        new_oferta.save()
        return redirect(periodo)
    return redirect(reverse('index'))

def edit_oferta(request, id_param, id_oferta):
    periodo = get_object_or_404(Periodo, pk=id_param)
    oferta = get_object_or_404(Oferta, pk=id_oferta)
    cursos = Curso.objects.filter(created_by__pk=request.session['user_id'])
    disciplinas = Disciplina.objects.filter(curso__in=cursos)
    professores = Professor.objects.all()
    return render(request, f'coordenacao/coordenador/edit-oferta.html',
                  {'professores': professores,
                   'disciplinas': disciplinas,
                   'periodo': periodo,
                   'oferta' : oferta})

def edit_oferta_success(request, id_param, id_oferta):
    if request.method == 'POST' and request.session['user_type'] == 1:
        if request.POST['professor'] == "None":
            professor = None
        else:
            professor = Professor.objects.get(pk=request.POST['professor'])
        aula_dias = checkbox_week_days(request)
        periodo = get_object_or_404(Periodo, pk=id_param)
        disciplina = get_object_or_404(Disciplina, pk=request.POST['disciplina'])
        Oferta.objects.filter(pk=id_oferta).update(
                        periodo=periodo,
                        disciplina=disciplina, 
                        professor=professor,
                        capacidade=request.POST['capacidade'],
                        aula_dias=aula_dias, 
                        aula_hora_inicio=request.POST['hora_inicio'],
                        aula_hora_fim=request.POST['hora_fim'])
        return redirect(periodo)
    return redirect(reverse('index'))

def view_oferta_matriculados(request, id_param):
    if request.method == 'GET' and request.session['user_type'] == 1:
        matriculas = Matricula.objects.filter(oferta__pk=id_param)
        return render(request,
                      'coordenacao/coordenador/oferta-matriculas.html',
                      {'matriculas': matriculas})
    return redirect(reverse('index'))

def list_ofertas(request):
    if request.method == 'GET' and request.session['user_id']:
        user = User.objects.get(cpf=request.session['user_id'])
        matriculas = Matricula.objects.filter(aluno__pk=request.session['user_id'],
                                            oferta__periodo__start_date__lte=datetime.date.today(), 
                                            oferta__periodo__end_date__gte=datetime.date.today())
        if len(matriculas)>0:
            return render(request, 'coordenacao/aluno/matricula-realizada.html', {'matriculas' : matriculas})
        else:
            # form matricula
            disciplinas = Disciplina.objects.filter(curso__pk=user.aluno.curso.id)
            ofertas = Oferta.objects.filter(disciplina__in=disciplinas,
                                            periodo__start_date__lte=datetime.date.today(), 
                                            periodo__end_date__gte=datetime.date.today())
        return render(request, 'coordenacao/aluno/new-matricula.html', {'ofertas' : ofertas})
    return redirect(reverse('index'))

def view_oferta(request, id_param):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        atividades = Atividade.objects.filter(oferta=oferta).order_by('-entrega_date') 
        return render(request, 'coordenacao/professor/menu-de-disciplinas-professor.html', 
                      {'oferta' : oferta,
                       'atividades' : atividades,
                       'count_atividades' : len(atividades)})
    return redirect(reverse('index'))