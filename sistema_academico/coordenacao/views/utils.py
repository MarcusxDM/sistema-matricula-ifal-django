from django.core.mail import send_mail
import secrets
import string

def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))

def checkbox_week_days(request):
    result = ''
    try:
        result = result+request.POST['segunda']
    except:
        pass
    try:
        result = result+request.POST['terca']
    except:
        pass
    try:
        result = result+request.POST['quarta']
    except:
        pass
    try:
        result = result+request.POST['quinta']
    except:
        pass
    try:
        result = result+request.POST['sexta']
    except:
        pass
    try:
        result = result+request.POST['sabado']
    except:
        pass
    try:
        result = result+request.POST['domingo']
    except:
        pass
    return result

def send_email_new_user(email_destinatario, password, user_nome):
    send_mail('SIACA - Sua conta foi criada!', 
              f'Olá {user_nome}!\nSua conta do Sistema Acadêmico foi criada, utilize seu CPF e a senha: {password} para fazer login.', 
            'mvgp1@aluno.ifal.edu.br',
    [email_destinatario], fail_silently=False)