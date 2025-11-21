from django.shortcuts import render, redirect
from .models import Sala, Reserva
from django.utils import timezone
from datetime import timedelta

def home(request):

# Actualizar estado de las salas automáticamente.

    actualizar_estado_salas()
    
    salas = Sala.objects.all()
    
    if request.method == "POST":

# Obtención de datos del formulario :D

        rut_usuario = request.POST.get('rut_u')
        sala_id = request.POST.get('sala_id')
        
# Crear objeto Reserva
        sala = Sala.objects.get(id=sala_id)
        nueva_reserva = Reserva(
            rut=rut_usuario,
            sala=sala,
            fecha_inicio=timezone.now(),
            fecha_termino=timezone.now() + timedelta(hours=2)
        )
        nueva_reserva.save()
        
# Muestra que la sala no esta disponible..

        sala.disponible = False
        sala.save()
        
        return redirect('home')
    
    contexto = {
        'salas': salas
    }
    return render(request, "main.html", contexto)

def detalle_sala(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    
# Buscar reserva activa para la sala.

    ahora = timezone.now()
    reserva_activa = Reserva.objects.filter(
        sala=sala, 
        fecha_termino__gt=ahora
    ).first()
    
    contexto = {
        'sala': sala,
        'reserva_activa': reserva_activa
    }
    return render(request, "detalle_sala.html", contexto)

def actualizar_estado_salas():

# Para cada sala, verifica si hay reservas activas y actualiza su disponibilidad.

    ahora = timezone.now()
    salas = Sala.objects.all()
    
    for sala in salas:

# Muestra reservas que aún no han terminado.

        reserva_activa = Reserva.objects.filter(
            sala=sala,
            fecha_termino__gt=ahora
        ).exists()
        
        # Actualizar disponibilidad
        if reserva_activa:
            sala.disponible = False
        else:
            sala.disponible = True
        sala.save()