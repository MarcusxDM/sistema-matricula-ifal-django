from datetime import date
from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.urls import reverse
import re
from coordenacao.models import Atividade, Disciplina, Oferta, Resposta, User, Professor, Aluno, Coordenador, Curso, Periodo
from coordenacao.views.oferta import create_oferta
from coordenacao.views.aluno import form_aluno

COORDENADOR_USER_TYPE = 1
PROFESSOR_USER_TYPE = 2
ALUNO_USER_TYPE = 3

class LoginViewTest(TestCase):
    
    def setUp(self):
        self.user_coordenador = User.objects.create(cpf='05970331457', nome='Coordenador', password='senha123')
        self.coordenador = Coordenador.objects.create(user=self.user_coordenador)
        self.curso = Curso.objects.create(nome='Curso 1', periodos=8, created_by=self.coordenador)
        self.periodo = Periodo.objects.create(id='202401', start_date=date(2024, 1, 1), end_date=date(2024, 6, 30))
    
        self.user_aluno = User.objects.create(cpf='05970631458', nome='Aluno', password='senha123')
        Aluno.objects.create(user=self.user_aluno, curso=self.curso, periodo_ingresso=self.periodo)

        self.user_professor = User.objects.create(cpf='02323223457', nome='Professor', password='senha123')
        Professor.objects.create(user=self.user_professor)

    def login_user(self, user_name):
        """Função auxiliar para logar um coordenador e configurar a sessão."""

        # pega o usuário Coordenador
        user = User.objects.get(nome=user_name)
        
        # Realiza o login
        login_url = reverse('login')
        login_data = {
            'cpf': user.cpf,
            'password': user.password, 
        }

        # Cria o client e faz a requisição de login
        response = self.client.post(login_url, data=login_data)
        return response
    
    def test_login_coordenador(self):
        """Validar login de Coordenador"""
        response = self.login_user(self.user_coordenador.nome)
        
        self.assertRedirects(response, reverse('home'))

        session = self.client.session
        self.assertEqual(session.get('user_type'), COORDENADOR_USER_TYPE)
        self.assertEqual(session.get('user_id'), self.user_coordenador.cpf) 
    
    def test_login_aluno(self):
        """Validar login de Aluno"""
        response = self.login_user(self.user_aluno.nome)
        
        self.assertRedirects(response, reverse('home'))

        session = self.client.session
        self.assertEqual(session.get('user_type'), ALUNO_USER_TYPE)
        self.assertEqual(session.get('user_id'), self.user_aluno.cpf)
    
    def test_login_professor(self):
        """Validar login de Professor"""
        response = self.login_user(self.user_professor.nome)
        
        self.assertRedirects(response, reverse('home'))

        session = self.client.session
        self.assertEqual(session.get('user_type'), PROFESSOR_USER_TYPE)
        self.assertEqual(session.get('user_id'), self.user_professor.cpf)

    

class FormAlunoViewTest(TestCase):

    def setUp(self):
        # Coordenador
        self.user_coordenador = User.objects.create(cpf='05970331457', nome='Coordenador', password='senha123')
        self.coordenador = Coordenador.objects.create(user=self.user_coordenador)
        self.curso = Curso.objects.create(nome='Curso 1', periodos=8, created_by=self.coordenador)
        self.periodo = Periodo.objects.create(id='202401', start_date=date(2024, 1, 1), end_date=date(2024, 6, 30))

        # Aluno
        self.user_aluno = User.objects.create(cpf='82318817007', nome='Aluno', password='senha123')
        self.aluno = Aluno.objects.create(user=self.user_aluno, curso=self.curso, periodo_ingresso=self.periodo)

        # Mock requests
        self.factory = RequestFactory()

    def test_form_aluno_get(self):
        """Verifica se formulario de Aluno é acessível pelo Coordenador"""

        # Loga como coordenador
        request = self.factory.get(reverse('form_aluno')) # mock request
        request.session = {'user_type': COORDENADOR_USER_TYPE, 'user_id': self.user_coordenador.cpf}

        # Chama a view
        response = form_aluno(request)

        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cadastrar Novo Aluno')

    def test_form_aluno_invalid_user_type(self):
        """Verifica se é possível acessar o formulário de criação de Aluno
          com um usuário de tipo inválido (aluno)"""
        
        # Simula um usuário com tipo inválido (Aluno)
        request = self.factory.get(reverse('form_aluno')) # mock request
        request.session = {'user_type': ALUNO_USER_TYPE, 'user_id': self.user_aluno.cpf}

        # Chama a view
        response = form_aluno(request)

        # Verifica o código de status e o redirecionamento
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('index'))

class OfertaViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_type = COORDENADOR_USER_TYPE # tipo de usuário "Coordenador"
        self.user_id = '05970331457' # qualquer cpf
        self.periodo_id = 202401
        self.oferta_id = 1
        self.user_professor = User.objects.create(cpf='05970331457', nome='Professor')
        self.professor = Professor(user=self.user_professor)

    @patch('coordenacao.views.professor.Professor.objects.get')
    @patch('coordenacao.views.oferta.get_object_or_404')
    @patch('coordenacao.views.oferta.Oferta.save')
    def test_create_oferta(self, mock_save, mock_get_object_or_404, mock_get_professor):
        """Testar a criacao de Oferta de uma disciplina"""
        
        # Mocks
        mock_periodo = Periodo(id=self.periodo_id)
        mock_disciplina = Disciplina(id=1, nome='Matemática')
        mock_get_object_or_404.side_effect = [mock_periodo, mock_disciplina]

        mock_professor = self.professor
        mock_get_professor.return_value = mock_professor

        # Simula a requisição POST
        request = self.factory.post(reverse('create_oferta', args=[self.periodo_id]), {
            'professor': '1',
            'disciplina': '1',
            'capacidade': '30',
            'hora_inicio': '08:00',
            'hora_fim': '10:00',
        })
        request.session = {'user_type': self.user_type, 'user_id': self.user_id}

        # Chama a view
        response = create_oferta(request, self.periodo_id)

        # Verifica se os métodos e redirecionamentos foram chamados
        self.assertEqual(response.status_code, 302)
        mock_get_object_or_404.assert_any_call(Periodo, pk=self.periodo_id)
        mock_get_object_or_404.assert_any_call(Disciplina, pk='1')
        mock_get_professor.assert_called_once_with(pk='1')
        mock_save.assert_called_once()

class FileDownloadTest(TestCase):
    def setUp(self):
        # Coordenador
        self.user_coordenador = User.objects.create(cpf='05970331457', nome='Coordenador', password='senha123')
        self.coordenador = Coordenador.objects.create(user=self.user_coordenador)
        self.curso = Curso.objects.create(nome='Curso 1', periodos=8, created_by=self.coordenador)
        self.periodo = Periodo.objects.create(id='202401', start_date=date(2024, 1, 1), end_date=date(2024, 6, 30))

        # Aluno
        self.user_aluno = User.objects.create(cpf="12345678900", password="senha123")
        self.aluno = Aluno.objects.create(user=self.user_aluno, curso=self.curso, periodo_ingresso=self.periodo)
        

        # Criação do mock para a instância de Oferta
        self.oferta = MagicMock(spec=Oferta)
        self.oferta.nome = "Oferta Teste"
        
        # Simulando a propriedade _state para o mock
        self.oferta._state = MagicMock()

        # Atividade
        # self.atividade = Atividade.objects.create(nome="Atividade Teste", descricao="Descrição da atividade")
        self.atividade = MagicMock(spec=Atividade)
        self.atividade.nome = "Atividade Teste"
        self.atividade.oferta = self.oferta  # Relacionando com a Oferta mockada
        self.atividade._state = MagicMock()  # Simulando o atributo _state

        self.resposta = Resposta.objects.create(atividade = self.atividade, 
                                                aluno = self.aluno,
                                                arquivo = b"test content")