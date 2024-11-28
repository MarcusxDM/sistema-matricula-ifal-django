from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from coordenacao.models import Coordenador, Curso, Disciplina 

def form_curso(request):
    '''
    Retorna html com formulário de criação de curso
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, 'coordenacao/coordenador/cadastrar-novo-curso-coordenador.html')
    return redirect(reverse('index'))

def create_curso(request):
    if request.method == 'POST' and request.session['user_type'] == 1:
        file = request.FILES['ementa'].file.getvalue()
        new_curso = Curso(nome=request.POST['nome'],
                          descricao=request.POST['descricao'],
                          periodos=request.POST['periodos'], ementa=file,
                          created_by=Coordenador.objects.get(pk=request.session['user_id']))
        new_curso.save()
        return redirect(reverse('cursos'))
    return redirect(reverse('index'))

def view_curso(request, id_param):
    '''
    Retorna html com lista de disciplinas do curso
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        curso = get_object_or_404(Curso, pk=id_param)
        disciplinas = Disciplina.objects.filter(curso=curso)
        return render(request, 
                      'coordenacao/coordenador/disciplinas-vigentes-coordenador.html', 
                      {'disciplinas' : disciplinas, 'curso' : curso})
    return redirect(reverse('index'))

def form_disciplina(request, id_param):
    '''
    Retorna html com formulário de criação de disciplina
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, 'coordenacao/coordenador/cadastrar-nova-disciplina-coordenador.html', 
                      {'id_param':id_param})
    return redirect(reverse('index'))

def create_disciplina(request, id_param):
    if request.method == 'POST' and request.session['user_type'] == 1:
        curso = get_object_or_404(Curso, pk=id_param) 
        file = request.FILES['ementa'].file.getvalue()
        new_disciplina = Disciplina(nome=request.POST['nome'], 
                                    descricao=request.POST['descricao'], 
                                    carga_horaria=request.POST['carga_horaria'],
                                    periodo=request.POST['periodo'],
                                    ementa=file,
                                    curso=curso)
        new_disciplina.save()
        return redirect(curso)
    return redirect(reverse('index'))

def list_curso(request):
    '''
    Retorna html com lista de cursos criados pelo usuário coordenador em sessão
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        cursos = Curso.objects.filter(
            created_by=Coordenador.objects.get(
                user_id=request.session['user_id']))
        return render(request, 'coordenacao/coordenador/curso-vigentes-coordenador.html',
                      {'cursos':cursos})
    return redirect(reverse('index'))