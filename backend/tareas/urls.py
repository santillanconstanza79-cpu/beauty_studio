from django.urls import path
from . import views

urlpatterns = [
    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("clientes/<int:cliente_id>/", views.detalle_cliente, name="detalle_cliente"),

    path("profesionales/", views.lista_profesionales, name="lista_profesionales"),
    path("profesionales/<int:profesional_id>/", views.detalle_profesional, name="detalle_profesional"),

    path("servicios/", views.lista_servicios, name="lista_servicios"),
    path("servicios/<int:servicio_id>/", views.detalle_servicio, name="detalle_servicio"),

    path("turnos/", views.lista_turnos, name="lista_turnos"),
    path("turnos/<int:turno_id>/", views.detalle_turno, name="detalle_turno"),
    path("turnos/<int:turno_id>/historial/", views.historial_de_turno, name="historial_de_turno"),
]
