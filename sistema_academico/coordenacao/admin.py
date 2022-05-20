from django.contrib import admin
from coordenacao.models import User, Coordenador, Professor, Aluno

admin.site.register(User)
admin.site.register(Coordenador)
admin.site.register(Professor)
admin.site.register(Aluno)