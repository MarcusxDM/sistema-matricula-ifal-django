from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from coordenacao.models import User, Coordenador, Professor, Aluno, Curso, Disciplina
from django.core.mail import send_mail
import secrets
import string

def generate_password(): 
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))

def send_email_new_user(email_destinatario, password, user_nome):
    send_mail('SIACA - Sua conta foi criada!', 
    
    f'Olá {user_nome}!\nSua conta do Sistema Acadêmico foi criada, utilize seu CPF e a senha: {password} para fazer login.', 
    
    'mvgp1@aluno.ifal.edu.br',
    [email_destinatario], fail_silently=False)
def index(request):
    '''
    Página de index
    '''
    request.session.flush()
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
    else:
        return redirect(reverse('index'))

def home(request):
    '''
    Página Home
    '''
    try:
        user_name = User.objects.get(cpf=request.session['user_id']).nome
        request.session['user_name'] = user_name
        if request.session['user_type'] == 1:
            home_name = 'coordenador/home-coordenador'
        elif request.session['user_type'] == 2:
            home_name = 'professor/home-professor'
        else:
            home_name = 'aluno/home-aluno'
        print(f'coordenacao/{home_name}.html')
        return render(request, f'coordenacao/{home_name}.html')
    except:
        return redirect(reverse('index'))

def logout(request):
    '''
    Faz logout, limpa Session
    '''
    request.session.flush()
    return redirect(reverse('index'))

# Aluno
def list_alunos(request):
    '''
    Retorna html com lista de Alunos Cadastrados
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        alunos = Aluno.objects.all()
        return render(request, f'coordenacao/coordenador/coordenador-aba-aluno.html', {'alunos':alunos})
    else:
        return redirect(reverse('index'))

def form_aluno(request):
    '''
    Retorna html com formulário de criação de aluno
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, f'coordenacao/coordenador/create-aluno.html')
    else:
        return redirect(reverse('index'))

def create_aluno(request):
    '''
    Retorna html com formulário de criação de aluno
    '''
    if request.method == 'POST' and request.session['user_type'] == 1:
        try:
            # Gera Senha
            passwrd = generate_password()
            # Cria Usuário
            new_user = User(cpf=request.POST['cpf'], email=request.POST['email'], password=passwrd, nome=request.POST['nome'], telefone=request.POST['telefone'],
                            endereco=request.POST['endereco'], bairro=request.POST['bairro'], cidade=request.POST['cidade'], estado=request.POST['estado'])
            new_user.save()

            # Envia email com senha gerada
            send_email_new_user(request.POST['email'], passwrd, request.POST['nome'])
            # Cria Aluno com novo Usuário
            new_aluno = Aluno(user=new_user)
            new_aluno.save()
            return redirect(reverse('alunos'))
        except:
            render(request, f'coordenacao/coordenador/create-aluno.html')
    else:
        return redirect(reverse('index'))

# Professor
def list_professores(request):
    '''
    Retorna html com lista de Professores Cadastrados
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        professores = Professor.objects.all()
        return render(request, f'coordenacao/coordenador/coordenador-aba-professores.html', {'professores':professores})
    else:
        return redirect(reverse('index'))

def form_professor(request):
    '''
    Retorna html com formulário de criação de professores
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, f'coordenacao/coordenador/create-professor.html')
    else:
        return redirect(reverse('index'))

def create_professor(request):
    '''
    Retorna html com formulário de criação de professores
    '''
    if request.method == 'POST' and request.session['user_type'] == 1:
        try:
            # Gera Senha
            passwrd = generate_password()
            # Cria Usuário
            new_user = User(cpf=request.POST['cpf'], email=request.POST['email'], password=passwrd, nome=request.POST['nome'], telefone=request.POST['telefone'],
                            endereco=request.POST['endereco'], bairro=request.POST['bairro'], cidade=request.POST['cidade'], estado=request.POST['estado'])
            new_user.save()

            # Envia email com senha gerada
            send_email_new_user(request.POST['email'], passwrd, request.POST['nome'])
            
            # Cria Aluno com novo Usuário
            new_professor = Professor(user=new_user, lattes=request.POST['lattes'], area_atuacao=request.POST['atuacao'])
            new_professor.save()
            return redirect(reverse('professores'))
        except:
            render(request, f'coordenacao/coordenador/create-professor.html')
    else:
        return redirect(reverse('index'))

def list_curso(request):
    '''
    Retorna html com lista de cursos criados pelo usuário coordenador em sessão
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        cursos = Curso.objects.filter(created_by=Coordenador.objects.get(user_id=request.session['user_id']))
        render(request, f'coordenacao/coordenador/list-cursos.html', {'cursos':cursos})
    else:
        return redirect(reverse('index'))

def form_curso(request):
    '''
    Retorna html com formulário de criação de curso
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, f'coordenacao/coordenador/create-curso.html')
    else:
        return redirect(reverse('index'))

def create_curso(request):
    if request.method == 'POST' and request.session['user_type'] == 1:
        # try:
        new_curso = Curso(nome=request.POST['nome'], descricao=request.POST['descricao'],
                        periodos=request.POST['periodos'], ementa=request.POST['ementa'], 
                        created_by=Coordenador.objects.get(pk=request.session['user_id']))
        new_curso.save()
        return redirect(reverse('cursos'))
        # except:
    else:
        return redirect(reverse('index'))

def view_curso(request, id_param):
    '''
    Retorna html com lista de disciplinas do curso
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        # try:
        curso = get_object_or_404(Curso, pk=id_param)
        disciplinas = Disciplina.objects.filter(curso=curso)
        render(request, f'coordenacao/coordenador/list-disciplinas.html', {'disciplinas':disciplinas})
        # except:
        #     pass
    else:
        return redirect(reverse('index'))

def list_disciplina(request):
    '''
    Retorna html com lista de disciplinas de um curso
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        disciplinas = Disciplina.objects.filter(curso=Curso.objects.get(pk=request.GET['curso_id']))
        render(request, f'coordenacao/coordenador/list-disciplinas.html', {'disciplinas':disciplinas})
    else:
        return redirect(reverse('index'))

def form_disciplina(request):
    '''
    Retorna html com formulário de criação de disciplina
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, f'coordenacao/coordenador/create-disciplina.html')
    else:
        return redirect(reverse('index'))

def create_disciplina(request, curso_id):
    if request.method == 'POST' and request.session['user_type'] == 1:
        # try:
        curso = get_object_or_404(Curso, pk=curso_id)
        new_disciplina = Disciplina(nome=request.POST['nome'], descricao=request.POST['descricao'],
                        periodo=request.POST['periodo'], ementa=request.POST['ementa'], 
                        curso=curso)
        new_disciplina.save()
        # except:
    else:
        return redirect(reverse('index'))


            
