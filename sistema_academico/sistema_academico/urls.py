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
        path('cadastrar/', include([
            path('', views.form_curso, name='form_curso'),
            path('success/', views.create_curso, name='create_curso')
            ])),
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
        ])),
        path('<int:id_param>/', include([
            path('', views.view_periodo, name='view_periodo'),
            path('<int:id_oferta>/', views.list_alunos_matriculados, name='view_oferta'),
            path('<int:id_oferta>/', include([
                path('editar/', views.edit_oferta, name='edit_oferta'),
                path('success/', views.edit_oferta_success, name='edit_oferta_success' )
            ])),
            path('cadastrar-oferta/', include([
                path('', views.form_oferta, name='form_oferta'),
                path('success', views.create_oferta, name='create_oferta'),
            ]))
        ]))
    ])),
    

    # Perfil
    path('perfil/',  include([
        path('', views.view_perfil, name='view_perfil'),
        path('editar/', include([
            path('', views.form_editar_perfil, name='form_perfil'),
            path('success', views.edit_user, name='edit_user'),
            path('change-password/', views.edit_password, name='edit_password')
            ]))
        ])),

    # Alunos - Matrícula
    path('ofertas/', include([
        path('', views.list_ofertas, name='ofertas'),
        path('cadastrar/', views.create_matricula, name='create_matricula'),
    ])),

    # Disciplinas/Ofertas
    path('disciplinas-matriculadas/', views.list_ofertas_matriculadas, name='disciplinas_matriculadas'),
    path('disciplinas-lecionadas/', views.list_ofertas_lecionadas, name='disciplinas_lecionadas'),

    path('disciplina/', include([
        path('<int:id_param>/', include([
            path('', views.view_oferta, name='view_oferta'),
            path('notas/', include([
                path('', views.view_oferta_notas, name='view_oferta_notas'),
                path('cadastrar/', views.create_oferta_nota, name='create_oferta_nota'),
            ])),
            path('cadastrar-atividade/', include([
                path('', views.form_atividade, name='form_atividade'),
                path('success', views.create_atividade, name='create_atividade')
                ])),
            path('atividades/', include([
                path('', views.list_atividades, name='list_atividades'),
                path('<int:id_atividade>/', include([
                    path('', views.view_atividade, name='view_atividade'),
                    path('enviar-resposta/', views.create_reposta, name='create_resposta'),
                    path('cadastrar-notas/', views.update_reposta_nota, name='update_reposta_nota'),
                    path('download-resposta/<int:pk>/', views.download_resposta, name='download_resposta'),
                    path('download-atividade/', views.download_atividade, name='download_atividade')
                ])),
            ])),
            path('frequencias/', include([
                path('', views.list_frequencias, name='list_frequencias'),
                path('<int:id_freq>/', views.edit_frequencia, name='edit_frequencia'),
                path('cadastrar/', include([
                    path('', views.form_frequencia, name='form_frequencia'),
                    path('success', views.create_frequencia, name='create_frequencia')
                ]))
            ]))
        ]))
    ])),

    path('boletim/', views.view_boletim, name='boletim')
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)