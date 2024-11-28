import io
import datetime
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from coordenacao.models import User, Coordenador, Professor, Aluno
from coordenacao.models import Curso, Disciplina, Periodo, Oferta
from coordenacao.models import Matricula, Atividade, Resposta
from coordenacao.models import Nota, Frequencia, AlunoFrequencia
from sistema_academico.coordenacao.views.utils import checkbox_week_days

def download_resposta(pk):
    # this url is for download
    try:
        obj = Resposta.objects.get(pk=pk)
    except Resposta.DoesNotExist:
        return JsonResponse({'status_message': 'No Resource Found'})
    get_binary = obj.arquivo
    if get_binary is None:
        return JsonResponse({'status_message': 'Resource does not contain file'})
    if isinstance(get_binary, memoryview):
        binary_io = io.BytesIO(get_binary.tobytes())
    else:
        binary_io = io.BytesIO(get_binary)
    response = FileResponse(binary_io)
    response['Content-Type'] = 'application/x-binary'
    response['Content-Disposition'] = f'attachment; filename="{obj.atividade} - {obj.aluno.pk}.pdf"'.format(pk)
    return response

def download_atividade(id_atividade):
    # this url is for download
    try:
        obj = Atividade.objects.get(pk=id_atividade)
    except Atividade.DoesNotExist:
        return JsonResponse({'status_message': 'No Resource Found'})
    get_binary = obj.arquivo
    if get_binary is None:
        return JsonResponse({'status_message': 'Resource does not contain file'})
    if isinstance(get_binary, memoryview):
        binary_io = io.BytesIO(get_binary.tobytes())
    else:
        binary_io = io.BytesIO(get_binary)
    response = FileResponse(binary_io)
    response['Content-Type'] = 'application/x-binary'
    response['Content-Disposition'] = f'attachment; filename="{obj}.pdf"'.format(id_atividade)
    return response

def create_matricula(request):
    if request.method == 'POST' and request.session['user_id']:
        aluno = get_object_or_404(Aluno, pk=request.session['user_id'])
        disciplinas = Disciplina.objects.filter(curso__pk=aluno.curso.id)
        ofertas = Oferta.objects.filter(disciplina__in=disciplinas, periodo__start_date__lte=datetime.date.today(), 
                                        periodo__end_date__gte=datetime.date.today())
        for oferta in ofertas:
            try:
                if request.POST[f'{oferta.id}_oferta'] == 'True':
                    new_matricula = Matricula(aluno=aluno, oferta=oferta)
                    new_matricula.save()
            except:
                pass
        return redirect(reverse('ofertas'))
    else:   
        return redirect(reverse('index'))

def list_alunos_matriculados(request, id_param, id_oferta):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_oferta)
        matriculas = Matricula.objects.filter(oferta=oferta)
        return render(request, 'coordenacao/coordenador/alunos-matriculados.html', {'matriculas' : matriculas,
                                                                                  'oferta' : oferta})
    else:   
        return redirect(reverse('index'))
            
def list_ofertas_matriculadas(request):
    if request.method == 'GET' and request.session['user_id']:
        user = get_object_or_404(User, pk=request.session['user_id'])
        matriculas = Matricula.objects.filter(aluno__pk=user.pk) 
        return render(request, 'coordenacao/aluno/lista-matriculas.html', {'matriculas' : matriculas})
    else:   
        return redirect(reverse('index'))

def list_ofertas_lecionadas(request):
    if request.method == 'GET' and request.session['user_id']:
        user = get_object_or_404(User, pk=request.session['user_id'])
        query = '''SELECT o.id, o.disciplina_id, d.nome, count(distinct m.id) as count_alunos, count(distinct a.id) as count_atividades FROM coordenacao_oferta o
                    LEFT JOIN coordenacao_disciplina d
                    ON o.disciplina_id = d.id
                    LEFT JOIN coordenacao_matricula m
                    ON o.id = m.oferta_id
                    LEFT JOIN coordenacao_atividade a
                    ON o.id = a.oferta_id
                    where o.professor_id=%s
                    group by o.id;
                '''
        ofertas = Oferta.objects.raw(query, [user.pk])
        # ofertas = Oferta.objects.filter(professor__pk=user.pk) 
        return render(request, f'coordenacao/professor/lista-de-disciplinas-professor.html', {'ofertas' : ofertas})
    else:   
        return redirect(reverse('index'))

def list_atividades(request, id_param):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        atividades = Atividade.objects.filter(oferta=oferta).order_by('-entrega_date') 
        return render(request, 'coordenacao/professor/lista-atividades.html', {'oferta' : oferta,
                                                                                'atividades' : atividades})
    return redirect(reverse('index'))

def form_atividade(request, id_param):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        return render(request, 'coordenacao/professor/criar-atividade-professor.html',
                      {'oferta' : oferta})
    return redirect(reverse('index'))
            
def create_atividade(request, id_param):
    if request.method == 'POST' and request.session['user_type'] == 2:
        oferta = get_object_or_404(Oferta, pk=id_param) 
        file = request.FILES['arquivo'].file.getvalue()
        new_atividade = Atividade(nome=request.POST['nome'], descricao=request.POST['descricao'],
                        arquivo=file, entrega_date=request.POST['entrega_date'], oferta=oferta)
        new_atividade.save()
        return redirect(new_atividade)
    else:
        return redirect(reverse('index'))

def view_atividade(request, id_param, id_atividade):
    # if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        atividade = get_object_or_404(Atividade, pk=id_atividade)
        aberta = (atividade.entrega_date >= datetime.date.today())
        if request.session['user_type'] == 2:
            html_name = 'professor/atividade-e-nota'
            respostas = Resposta.objects.filter(atividade=atividade)
        else:
            html_name = 'aluno/atividade-aluno'
            respostas = Resposta.objects.filter(atividade=atividade, aluno__pk=request.session['user_id'])
        return render(request, f'coordenacao/{html_name}.html', {'oferta' : oferta,
                                                                'atividade' : atividade,
                                                                'respostas' : respostas,
                                                                'aberta' : aberta})

def update_reposta_nota(request, id_param, id_atividade):
    if request.method == 'POST' and request.session['user_type'] == 2:
        oferta = get_object_or_404(Oferta, pk=id_param)
        atividade = get_object_or_404(Atividade, pk=id_atividade) 
        respostas = Resposta.objects.filter(atividade=atividade, nota=None)
        for resposta in respostas:
            try:
                resposta_update = Resposta.objects.filter(pk=resposta.id).update(
                        nota = request.POST[f'{resposta.id}_nota'])
            except:
                pass
        return redirect(atividade)
    else:
        return redirect(reverse('index')) 

def view_oferta_notas(request, id_param):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        notas = Nota.objects.filter(matricula__oferta=oferta)
        query = '''SELECT m.id as id, m.aluno_id as aluno_id, m.oferta_id as oferta_id, COALESCE(ROUND(sum(r.nota)/4, 2),0) as sum_nota FROM coordenacao_matricula m
                    LEFT JOIN coordenacao_resposta r
                    ON m.aluno_id = r.aluno_id
                    where m.oferta_id=%s
                    group by id;'''
        matriculas = Matricula.objects.raw(query, [oferta.id])
        return render(request, f'coordenacao/professor/nota-professor.html', {'oferta' : oferta,
                                                                              'matriculas' : matriculas,
                                                                              'notas' : notas,
                                                                              'notas_len' : len(notas)})
    else:   
        return redirect(reverse('index'))

def create_oferta_nota(request, id_param):
    if request.method == 'POST' and request.session['user_type'] == 2:
        oferta = get_object_or_404(Oferta, pk=id_param) 
        matriculas = Matricula.objects.filter(oferta=oferta)
        for matricula in matriculas:
                av1 = float(request.POST[f'{matricula.id}_av1_nota'])
                av2 = float(request.POST[f'{matricula.id}_av2_nota'])
                reav = float(request.POST[f'{matricula.id}_reav_nota'])
                final = (sum(sorted([av1, av2, reav])[-2:]))/2

                new_nota = Nota(matricula=matricula, av1_nota=av1,
                                av2_nota=av2, reav_nota=reav,
                                final_nota=final)
                new_nota.save()
        return redirect('view_oferta_notas', id_param=id_param)
    else:
        return redirect(reverse('index'))

def create_reposta(request, id_param, id_atividade):
    if request.method == 'POST' and request.session['user_type'] == 3:
        oferta = get_object_or_404(Oferta, pk=id_param)
        atividade = get_object_or_404(Atividade, pk=id_atividade) 
        file = request.FILES['arquivo'].file.getvalue()
        new_resposta = Resposta(atividade=atividade, aluno_id=request.session['user_id'], descricao='',
                        arquivo=file, nota=None)
        new_resposta.save()
        return redirect(atividade)
    else:
        return redirect(reverse('index'))          

def list_frequencias(request, id_param):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        frequencias = Frequencia.objects.filter(oferta=oferta)
        return render(request, f'coordenacao/professor/frequencia-lista.html', {'oferta' : oferta,
                                                                                'frequencias' : frequencias })
    else:
        return redirect(reverse('index'))

def form_frequencia(request, id_param):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        matriculas = Matricula.objects.filter(oferta=oferta)
        return render(request, f'coordenacao/professor/criar-frequencia.html', {'oferta' : oferta,
                                                                                'matriculas' : matriculas})
    else:   
        return redirect(reverse('index'))

def create_frequencia(request, id_param):
    if request.method == 'POST' and request.session['user_type'] == 2:
        oferta = get_object_or_404(Oferta, pk=id_param)
        matriculas = Matricula.objects.filter(oferta=oferta)
        # Create frequencia
        new_frequencia, created = Frequencia.objects.get_or_create(aula_date=request.POST['aula_date'], oferta=oferta)
        new_frequencia.save()

        # Delete alunos fre
        AlunoFrequencia.objects.filter(frequencia=new_frequencia).delete()

        # Save alunos in frequencia
        for matricula in matriculas:
            try:
                if request.POST[f'{matricula.aluno.pk}_presenca'] == 'True':
                    new_freq_aluno = AlunoFrequencia(frequencia=new_frequencia, aluno=matricula.aluno)
                    new_freq_aluno.save()
            except:
                pass

        return redirect('list_frequencias', id_param=id_param)
    else:
        return redirect(reverse('index'))   
    
def edit_frequencia(request, id_param, id_freq):
    if request.method == 'GET' and request.session['user_id']:
        oferta = get_object_or_404(Oferta, pk=id_param)
        frequencia = get_object_or_404(Frequencia, pk=id_freq)
        frequencias = AlunoFrequencia.objects.filter(frequencia_id=id_freq)
        
        alunos_presentes = []
        for f in frequencias:
            alunos_presentes.append(f.aluno.pk)

        matriculas = Matricula.objects.exclude(aluno_id__in=alunos_presentes)
        matriculas_id = []
        for m in matriculas:
            matriculas_id.append(m.pk)
        matriculas = Matricula.objects.filter(pk__in=matriculas_id, oferta=oferta)
        return render(request, 'coordenacao/professor/criar-frequencia.html', {'oferta' : oferta,
                                                                                'matriculas' : matriculas,
                                                                                'frequencias' : frequencias,
                                                                                'date_freq' : frequencia.aula_date})
    else:
        return redirect(reverse('index'))

def view_boletim(request):
    if request.method == 'GET' and request.session['user_type'] == 3:
        matriculas = Matricula.objects.filter(aluno__pk=request.session['user_id'])
        notas = Nota.objects.filter(matricula__in=matriculas)
        return render(request, 'coordenacao/aluno/boletim.html', {'notas' : notas})