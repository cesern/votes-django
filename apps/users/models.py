from django.db import models

class Delegacion(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre)

class Padron(models.Model):
    numero_de_empleado = models.PositiveIntegerField(default=0)
    nombre_completo = models.CharField(max_length=255, blank=False, null=False)
    delegacion = models.ForeignKey(Delegacion, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.numero_de_empleado)
