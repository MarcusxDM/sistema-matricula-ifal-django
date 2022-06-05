from django.contrib import admin
from django.urls import path
from coordenacao import views
import sistema_academico.settings as settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login-success/', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    
    # Coordenadores - Alunos
    path('alunos/', views.list_alunos, name='alunos'),
    path('cadastrar-aluno/', views.form_aluno, name='form_aluno'),
    path('cadastrar-aluno-success/', views.create_aluno, name='create_aluno'),

    # Coordenadores - Professores
    path('professores/', views.list_professores, name='professores'),
    path('cadastrar-professor/', views.form_professor, name='form_professor'),
    path('cadastrar-professor-success/', views.create_professor, name='create_professor'),

    # Coordenadores - Cursos e Disciplinas
    path('cursos/', include([
        path('', views.list_curso, name='cursos'),
        path('cadastrar/', views.form_curso, name='form_curso'),
        path('<int:id_param>/', include([
            path('', views.view_curso, name='view_curso'),
            path('cadastrar-disciplina/', include([
                path('', views.form_disciplina, name='form_disciplina'),
                path('success/', views.create_disciplina, name='create_disciplina')
            ]))
        ]))
    ])),

    # Periodo Letivo
    path('periodos/', include([
        path('', views.list_periodo, name='periodos'),
        path('cadastrar/', include([
                path('', views.form_periodo, name='form_periodo'),
                path('success/', views.create_periodo, name='create_periodo')
        ]))
    ]))



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)