import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Tarea


# ----------------------------------------------------------------------
# Estas dos funciones son la "API": no devuelven HTML, devuelven JSON.
# El frontend (script.js) les va a hacer fetch() para leer y modificar
# los datos guardados en PostgreSQL.
#
# @csrf_exempt: Django protege por defecto los formularios contra un
# ataque llamado CSRF. Como acá el frontend es un archivo aparte (no
# un template de Django), lo simplificamos para la demo desactivando
# esa protección SOLO en estos endpoints. En un proyecto real en
# producción esto se resuelve de otra forma (tokens, DRF, etc.).
# ----------------------------------------------------------------------


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lista_tareas(request):
    if request.method == "GET":
        # 1) Traer todas las tareas de la base de datos
        tareas = Tarea.objects.all()
        # 2) Convertir cada una a diccionario
        datos = [t.to_dict() for t in tareas]
        # 3) Devolverlas como JSON
        return JsonResponse(datos, safe=False)

    # request.method == "POST" -> crear una tarea nueva
    body = json.loads(request.body or "{}")
    titulo = (body.get("titulo") or "").strip()

    if not titulo:
        return JsonResponse({"error": "El título no puede estar vacío"}, status=400)

    tarea = Tarea.objects.create(titulo=titulo)
    return JsonResponse(tarea.to_dict(), status=201)


@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def detalle_tarea(request, tarea_id):
    try:
        tarea = Tarea.objects.get(id=tarea_id)
    except Tarea.DoesNotExist:
        return JsonResponse({"error": "Tarea no encontrada"}, status=404)

    if request.method == "PATCH":
        # Cambiar el estado hecha/no hecha
        tarea.hecha = not tarea.hecha
        tarea.save()
        return JsonResponse(tarea.to_dict())

    # request.method == "DELETE" -> borrar la tarea
    tarea.delete()
    return JsonResponse({"ok": True})
