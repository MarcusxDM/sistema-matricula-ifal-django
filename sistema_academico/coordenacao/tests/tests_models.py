from datetime import date
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.urls import reverse
import re
from coordenacao.models import Disciplina, Oferta, User, Professor, Aluno, Coordenador, Curso, Periodo
from coordenacao.views import create_oferta, edit_oferta, form_aluno

COORDENADOR_USER_TYPE = 1
PROFESSOR_USER_TYPE = 2
ALUNO_USER_TYPE = 3

class UserTestCase(TestCase):
    def validar_cpf(self, cpf):
        # Remover caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)

        # Verificar se tem 11 dígitos e não é uma sequência repetida (ex.: 111.111.111-11)
        if not cpf or len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Validar os dois dígitos verificadores
        for i in range(9, 11):
            soma = sum(int(cpf[j]) * (i + 1 - j) for j in range(i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if digito != int(cpf[i]):
                return False
        return True
    
    def setUp(self):
        User.objects.create(cpf="05970331457", nome="Marcus", password="senha123")
        

    def test_user_create(self):
        """Criação de Usuário"""
        User.objects.create(cpf = '82318817006',
                            nome = 'User',
                            password = 'senha123')
        user = User.objects.get(cpf='82318817006')
        self.assertEqual(user.nome, 'User')
    
    def test_user_create_without_password(self):
        """Garantir que criar usuário sem senha levanta exceçao"""
        with self.assertRaises(ValidationError):
            user = User(cpf='82318817007', nome='User')
            user.full_clean()
            user.save()
    
    def test_cpf_invalido(self):
        """Verificar se podem ser criados usuarios com CPF invalido"""
        with self.assertRaises(ValidationError):
            user = User.objects.create(cpf="12345678", nome="CPFnaovalido", password="senha123")
            cpf = user.cpf
            self.assertTrue(self.validar_cpf(cpf))
    
    def test_user_create_cpf_duplicate(self):
        """Garantir que criar usuário com CPF duplicado levanta exceçao"""
        User.objects.create(cpf='82318817007', nome='User 1', password="senha123")
        with self.assertRaises(IntegrityError):
            User.objects.create(cpf='82318817007', nome='User2')
        
class CoordenadorTestCase(TestCase):

    def setUp(self):
        User.objects.create(cpf="05970331457", nome="User", password="senha123")
    
    def test_create_coordenador(self):
        """Criacao de Coordenador com User"""
        user = User.objects.get(nome="User")
        coordenador = Coordenador.objects.create(user=user)

        self.assertEquals(coordenador.user.cpf, user.cpf)
    
    def test_create_coordenador_without_user(self):
        """Nao eh possível criar um Coordenador sem um User"""
        
        with self.assertRaises(IntegrityError):
            Coordenador.objects.create()