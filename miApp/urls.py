from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sala/<int:sala_id>/', views.detalle_sala, name="detalle_sala"),
]