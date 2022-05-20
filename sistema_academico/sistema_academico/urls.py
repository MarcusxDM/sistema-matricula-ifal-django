from django.contrib import admin
from django.urls import path
from coordenacao import views
import sistema_academico.settings as settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login-success/', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # Alunos
    path('alunos/', views.list_alunos, name='alunos'),
    path('cadastrar-aluno/', views.form_aluno, name='form_aluno'),
    path('cadastrar-aluno-success/', views.create_aluno, name='create_aluno'),

    # Professores
    path('professores/', views.list_professores, name='professores'),
    path('cadastrar-professor/', views.form_professor, name='form_professor'),
    path('cadastrar-professor-success/', views.create_professor, name='create_professor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)