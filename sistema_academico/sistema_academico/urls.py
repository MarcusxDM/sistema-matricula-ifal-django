from django.contrib import admin
from django.urls import path
import coordenacao.views as views 
import sistema_academico.settings as settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('', views.login_auth.index, name='index'),
    path('home/', views.login_auth.home, name='home'),
    path('login-success/', views.login_auth.login, name='login'),
    path('logout', views.login_auth.logout, name='logout'),

    
    # Coordenadores - Alunos
    path('alunos/', views.aluno.list_alunos, name='alunos'),
    path('cadastrar-aluno/', views.aluno.form_aluno, name='form_aluno'),
    path('cadastrar-aluno-success/', views.aluno.create_aluno, name='create_aluno'),

    # Coordenadores - Professores
    path('professores/', views.professor.list_professores, name='professores'),
    path('cadastrar-professor/', views.professor.form_professor, name='form_professor'),
    path('cadastrar-professor-success/', views.professor.create_professor, name='create_professor'),

    # Coordenadores - Cursos e Disciplinas
    path('cursos/', include([
        path('', views.curso.list_curso, name='cursos'),
        path('cadastrar/', include([
            path('', views.curso.form_curso, name='form_curso'),
            path('success/', views.curso.create_curso, name='create_curso')
            ])),
        path('<int:id_param>/', include([
            path('', views.curso.view_curso, name='view_curso'),
            path('cadastrar-disciplina/', include([
                path('', views.curso.form_disciplina, name='form_disciplina'),
                path('success/', views.curso.create_disciplina, name='create_disciplina')
            ]))
        ]))
    ])),

    # Periodo Letivo
    path('periodos/', include([
        path('', views.periodo.list_periodo, name='periodos'),
        path('cadastrar/', include([
                path('', views.periodo.form_periodo, name='form_periodo'),
                path('success/', views.periodo.create_periodo, name='create_periodo')
        ])),
        path('<int:id_param>/', include([
            path('', views.periodo.view_periodo, name='view_periodo'),
            path('<int:id_oferta>/', views.matricula.list_alunos_matriculados, name='view_oferta'),
            path('<int:id_oferta>/', include([
                path('editar/', views.oferta.edit_oferta, name='edit_oferta'),
                path('success/', views.oferta.edit_oferta_success, name='edit_oferta_success' )
            ])),
            path('cadastrar-oferta/', include([
                path('', views.oferta.form_oferta, name='form_oferta'),
                path('success', views.oferta.create_oferta, name='create_oferta'),
            ]))
        ]))
    ])),
    

    # Perfil
    path('perfil/',  include([
        path('', views.perfil.view_perfil, name='view_perfil'),
        path('editar/', include([
            path('', views.perfil.form_editar_perfil, name='form_perfil'),
            path('success', views.perfil.edit_user, name='edit_user'),
            path('change-password/', views.perfil.edit_password, name='edit_password')
            ]))
        ])),

    # Alunos - Matrícula
    path('ofertas/', include([
        path('', views.oferta.list_ofertas, name='ofertas'),
        path('cadastrar/', views.matricula.create_matricula, name='create_matricula'),
    ])),

    # Disciplinas/Ofertas
    path('disciplinas-matriculadas/', views.matricula.list_ofertas_matriculadas, name='disciplinas_matriculadas'),
    path('disciplinas-lecionadas/', views.matricula.list_ofertas_lecionadas, name='disciplinas_lecionadas'),

    path('disciplina/', include([
        path('<int:id_param>/', include([
            path('', views.oferta.view_oferta, name='view_oferta'),
            path('notas/', include([
                path('', views.matricula.view_oferta_notas, name='view_oferta_notas'),
                path('cadastrar/', views.matricula.create_oferta_nota, name='create_oferta_nota'),
            ])),
            path('cadastrar-atividade/', include([
                path('', views.matricula.form_atividade, name='form_atividade'),
                path('success', views.matricula.create_atividade, name='create_atividade')
                ])),
            path('atividades/', include([
                path('', views.matricula.list_atividades, name='list_atividades'),
                path('<int:id_atividade>/', include([
                    path('', views.matricula.view_atividade, name='view_atividade'),
                    path('enviar-resposta/', views.matricula.create_reposta, name='create_resposta'),
                    path('cadastrar-notas/', views.matricula.update_reposta_nota, name='update_reposta_nota'),
                    path('download-resposta/<int:pk>/', views.matricula.download_resposta, name='download_resposta'),
                    path('download-atividade/', views.matricula.download_atividade, name='download_atividade')
                ])),
            ])),
            path('frequencias/', include([
                path('', views.matricula.list_frequencias, name='list_frequencias'),
                path('<int:id_freq>/', views.matricula.edit_frequencia, name='edit_frequencia'),
                path('cadastrar/', include([
                    path('', views.matricula.form_frequencia, name='form_frequencia'),
                    path('success', views.matricula.create_frequencia, name='create_frequencia')
                ]))
            ]))
        ]))
    ])),

    path('boletim/', views.matricula.view_boletim, name='boletim')
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)