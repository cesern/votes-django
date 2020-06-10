from django.db import models
from apps.management.models import Voting, Answer
from django.contrib.auth.models import User
# Create your models here.
class Vote(models.Model):
    votacion = models.ForeignKey(Voting, on_delete=models.PROTECT)
    respuesta = models.ForeignKey(Answer, on_delete=models.PROTECT)
    
    def __str__(self):
        return '{}'.format(self.respuesta)

class IVoted(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    votacion = models.ForeignKey(Voting, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}: {}'.format(self.votacion, self.usuario, self.fecha)