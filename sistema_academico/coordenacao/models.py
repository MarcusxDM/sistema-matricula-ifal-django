from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

class User(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=50)
    password = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=50)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.cpf} | {self.nome}"

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})
    
class Coordenador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    class Meta:
        verbose_name = _("coordenador")
        verbose_name_plural = _("coordenadores")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.nome}"

    def get_absolute_url(self):
        return reverse("coordenador_detail", kwargs={"pk": self.pk})


class Professor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    lattes = models.CharField(max_length=50)
    area_atuacao = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("professor")
        verbose_name_plural = _("professores")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.nome}"

    def get_absolute_url(self):
        return reverse("professor_detail", kwargs={"pk": self.pk})

class Curso(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    periodos = models.IntegerField(null=False, blank=False)
    ementa = models.BinaryField(null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(Coordenador, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")

    def __str__(self):
        return f"{self.id} | {self.nome}"

    def get_absolute_url(self):
        return reverse("curso_detail", kwargs={"pk": self.pk})

class Periodo(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    class Meta:
        verbose_name = _("periodo")
        verbose_name_plural = _("periodos")

    def __str__(self):
        return self.pk

    def get_absolute_url(self):
        return reverse("periodo_detail", kwargs={"pk": self.pk})

class Aluno(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=False, blank=False)
    periodo_ingresso = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=False, blank=False)
    class Meta:
        verbose_name = _("aluno")
        verbose_name_plural = _("alunos")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.nome}"

    def get_absolute_url(self):
        return reverse("aluno_detail", kwargs={"pk": self.pk})

class Disciplina(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50, null=False)
    descricao = models.TextField(null=True, blank=True)
    periodo = models.IntegerField(null=False, blank=False)
    ementa = models.BinaryField(null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("disciplina")
        verbose_name_plural = _("disciplinas")

    def __str__(self):
        return f"{self.id} | {self.nome}"

    def get_absolute_url(self):
        return reverse("disciplina_detail", kwargs={"pk": self.pk})

class Oferta(models.Model):
    id = models.IntegerField(primary_key=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=False, blank=False)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=False, blank=False)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    aula_dias = models.CharField(max_length=7, null=False, blank=False) # '{0-6}' cada numero representa um dia da semana
    aula_hora_inicio = models.TimeField(null=False, blank=False)
    aula_hora_fim = models.TimeField(null=False, blank=False)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _("oferta")
        verbose_name_plural = _("ofertas")

    def __str__(self):
        return f"{self.id} | {self.disciplina.nome} | {self.professor.nome}"

    def get_absolute_url(self):
        return reverse("oferta_detail", kwargs={"pk": self.pk})

class Matricula(models.Model):
    id = models.IntegerField(primary_key=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("matricula")
        verbose_name_plural = _("matriculas")

    def __str__(self):
        return f"{self.id} | {self.disciplina.nome} | {self.aluno.nome}"

    def get_absolute_url(self):
        return reverse("matricula_detail", kwargs={"pk": self.pk})





