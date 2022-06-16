# Generated by Django 3.2.13 on 2022-06-16 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('periodos', models.IntegerField()),
                ('ementa', models.BinaryField(blank=True, null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
            },
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('periodo', models.IntegerField()),
                ('ementa', models.BinaryField(null=True)),
                ('carga_horaria', models.IntegerField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.curso')),
            ],
            options={
                'verbose_name': 'disciplina',
                'verbose_name_plural': 'disciplinas',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'verbose_name': 'periodo',
                'verbose_name_plural': 'periodos',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('cpf', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='coordenacao.user')),
            ],
            options={
                'verbose_name': 'aluno',
                'verbose_name_plural': 'alunos',
            },
        ),
        migrations.CreateModel(
            name='Coordenador',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='coordenacao.user')),
            ],
            options={
                'verbose_name': 'coordenador',
                'verbose_name_plural': 'coordenadores',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='coordenacao.user')),
                ('lattes', models.CharField(max_length=50)),
                ('area_atuacao', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'professor',
                'verbose_name_plural': 'professores',
            },
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aula_dias', models.CharField(max_length=7)),
                ('aula_hora_inicio', models.TimeField()),
                ('aula_hora_fim', models.TimeField()),
                ('capacidade', models.IntegerField(default=1)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.disciplina')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.periodo')),
                ('professor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coordenacao.professor')),
            ],
            options={
                'verbose_name': 'oferta',
                'verbose_name_plural': 'ofertas',
            },
        ),
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aula_date', models.DateField()),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.oferta')),
            ],
            options={
                'verbose_name': 'frequencia',
                'verbose_name_plural': 'frequencias',
            },
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('arquivo', models.BinaryField(blank=True, null=True)),
                ('entrega_date', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.oferta')),
            ],
            options={
                'verbose_name': 'atividade',
                'verbose_name_plural': 'atividades',
            },
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True)),
                ('arquivo', models.BinaryField(blank=True, null=True)),
                ('nota', models.IntegerField(blank=True, default=0, null=True)),
                ('entrega_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('atividade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.atividade')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.aluno')),
            ],
            options={
                'verbose_name': 'resposta',
                'verbose_name_plural': 'respostas',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.oferta')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.aluno')),
            ],
            options={
                'verbose_name': 'matricula',
                'verbose_name_plural': 'matriculas',
            },
        ),
        migrations.AddField(
            model_name='curso',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.coordenador'),
        ),
        migrations.CreateModel(
            name='AlunoFrequencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.frequencia')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.aluno')),
            ],
            options={
                'verbose_name': 'AlunoFrequencia',
                'verbose_name_plural': 'AlunoFrequencias',
            },
        ),
        migrations.AddField(
            model_name='aluno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.curso'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='periodo_ingresso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordenacao.periodo'),
        ),
    ]
