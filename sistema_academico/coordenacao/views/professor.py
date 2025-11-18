from django.shortcuts import render, redirect
from django.urls import reverse
from coordenacao.models import User, Professor
from coordenacao.views.utils import send_email_new_user, generate_password

# Professor
def list_professores(request):
    '''
    Retorna html com lista de Professores Cadastrados
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        request.session['professor_create_error'] = False
        professores = Professor.objects.all()
        return render(request,
                      'coordenacao/coordenador/coordenador-aba-professores.html',
                      {'professores':professores})
    return redirect(reverse('index'))

def form_professor(request):
    '''
    Retorna html com formulário de criação de professores
    '''
    if request.method == 'GET' and request.session['user_type'] == 1:
        return render(request, 'coordenacao/coordenador/create-professor.html')
    return redirect(reverse('index'))

def create_professor(request):
    '''
    Retorna html com formulário de criação de professores
    '''
    if request.method == 'POST' and request.session['user_type'] == 1:
        try:
            User.objects.get(cpf=request.POST['cpf'])
            request.session['professor_create_error'] = True
            return redirect(reverse('form_professor'))
        except:
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
    return redirect(reverse('index'))
