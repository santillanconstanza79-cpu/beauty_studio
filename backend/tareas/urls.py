from django.urls import path

from . import views

urlpatterns = [
    path("tareas/", views.lista_tareas, name="lista_tareas"),
    path("tareas/<int:tarea_id>/", views.detalle_tarea, name="detalle_tarea"),
]
