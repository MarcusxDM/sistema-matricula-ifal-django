from django.contrib import admin
from coordenacao.models import User, Coordenador, Professor, Aluno, Curso, Periodo, Matricula, Oferta, Disciplina, Atividade

admin.site.register(User)
admin.site.register(Coordenador)
admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Curso)
admin.site.register(Periodo)
admin.site.register(Disciplina)
admin.site.register(Matricula)
admin.site.register(Oferta)
admin.site.register(Atividade)