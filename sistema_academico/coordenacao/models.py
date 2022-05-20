from django.db import models
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

class Aluno(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    class Meta:
        verbose_name = _("aluno")
        verbose_name_plural = _("alunos")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.nome}"

    def get_absolute_url(self):
        return reverse("aluno_detail", kwargs={"pk": self.pk})

