from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from coordenacao.models import Curso, Disciplina, Oferta, Periodo

def list_periodo(request):
    '''
    Retorna html com lista de cursos
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        periodos = Periodo.objects.all()
        return render(request,
                      'coordenacao/coordenador/periodos-cadastrados-coordenador.html',
                    {'periodos':periodos})
    return redirect(reverse('index'))

def form_periodo(request):
    '''
    Retorna html com formulário de criação de periodo
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, 'coordenacao/coordenador/cadastrar-periodo.html')
    return redirect(reverse('index'))

def create_periodo(request):
    if request.method == 'POST' and request.session['user_type'] == 1:
        try:
            Periodo.objects.get(pk=request.POST['ano']+request.POST['semestre'])
            request.session['periodo_create_error'] = True
            return redirect(reverse('form_periodo'))
        except:
            new_periodo = Periodo(id=request.POST['ano']+request.POST['semestre'],
                                  start_date=request.POST['data_inicio'],
                                  end_date=request.POST['data_fim'])
            new_periodo.save()
            return redirect(reverse('periodos')) #get com id como param
    return redirect(reverse('index'))

def view_periodo(request, id_param):
    '''
    Retorna html com lista de ofertas do periodo
    OBS.: apenas ofertas com disciplinas pertencentes aos cursos criados pelo coordenador
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        periodo = get_object_or_404(Periodo, pk=id_param)
        cursos = Curso.objects.filter(created_by__pk=request.session['user_id'])
        disciplinas = Disciplina.objects.filter(curso__in=cursos)
        ofertas = Oferta.objects.filter(disciplina__in=disciplinas, periodo=periodo)
        return render(request, 'coordenacao/coordenador/visualizar-periodo.html',
                      {'ofertas':ofertas,
                       'periodo':periodo})
    return redirect(reverse('index'))