from django.db import models
from apps.users.models import Delegacion

# Create your models here.
class Voting(models.Model):
    delegacion = models.ForeignKey(Delegacion, on_delete=models.PROTECT, null=True)
    tema = models.TextField(blank=False, null=False)
    pregunta = models.TextField(blank=False, null=False)
    fecha_de_inicio = models.DateTimeField(auto_now=False)
    fecha_de_cierre = models.DateTimeField(auto_now=False)

    def __str__(self):
        return '{}: {}'.format(self.tema, self.pregunta)

class Answer(models.Model):
    votacion = models.ForeignKey(Voting, on_delete=models.PROTECT)
    respuesta = models.TextField(blank=False, null=False)

    def __str__(self):
        return '{}: {}'.format(self.votacion, self.respuesta)
        