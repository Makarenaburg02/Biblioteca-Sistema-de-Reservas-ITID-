from django.db import models

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)

class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateTimeField()