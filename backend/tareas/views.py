oads(request.body or "{}")
        cliente.nombre = body.get("nombre", cliente.nombre)
        cliente.apellido = body.get("apellido", cliente.apellido)
        cliente.telefono = body.get("telefono", cliente.telefono)
        cliente.email = body.get("email", cliente.email)
        cliente.save()
        return JsonResponse(cliente.to_dict())

    cliente.delete()
    return JsonResponse({"mensaje": "Cliente eliminado"}, status=204)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lista_profesionales(request):
    if request.method == "GET":
        profesionales = Profesional.objects.all()
        return JsonResponse([p.to_dict() for p in profesionales], safe=False)

    body = json.loads(request.body or "{}")
    nombre = (body.get("nombre") or "").strip()
    apellido = (body.get("apellido") or "").strip()

    if not nombre or not apellido:
        return JsonResponse({"error": "Nombre y apellido son obligatorios"}, status=400)

    profesional = Profesional.objects.create(
        nombre=nombre,
        apellido=apellido,
        telefono=body.get("telefono", ""),
        especialidad=body.get("especialidad", ""),
    )
    return JsonResponse(profesional.to_dict(), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def detalle_profesional(request, profesional_id):
    try:
        profesional = Profesional.objects.get(id_profesional=profesional_id)
    except Profesional.DoesNotExist:
        return JsonResponse({"error": "Profesional no encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(profesional.to_dict())

    if request.method == "PUT":
        body = json.loads(request.body or "{}")
        profesional.nombre = body.get("nombre", profesional.nombre)
        profesional.apellido = body.get("apellido", profesional.apellido)
        profesional.telefono = body.get("telefono", profesional.telefono)
        profesional.especialidad = body.get("especialidad", profesional.especialidad)
        profesional.save()
        return JsonResponse(profesional.to_dict())

    profesional.delete()
    return JsonResponse({"mensaje": "Profesional eliminado"}, status=204)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lista_servicios(request):
    if request.method == "GET":
        servicios = Servicio.objects.all()
        return JsonResponse([s.to_dict() for s in servicios], safe=False)

    body = json.loads(request.body or "{}")
    nombre = (body.get("nombre") or "").strip()
    precio = body.get("precio")

    if not nombre or not precio:
        return JsonResponse({"error": "Nombre y precio son obligatorios"}, status=400)

    servicio = Servicio.objects.create(
        nombre=nombre,
        descripcion=body.get("descripcion", ""),
        precio=precio,
    )
    return JsonResponse(servicio.to_dict(), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def detalle_servicio(request, servicio_id):
    try:
        servicio = Servicio.objects.get(id_servicio=servicio_id)
    except Servicio.DoesNotExist:
        return JsonResponse({"error": "Servicio no encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(servicio.to_dict())

    if request.method == "PUT":
        body = json.loads(request.body or "{}")
        servicio.nombre = body.get("nombre", servicio.nombre)
        servicio.descripcion = body.get("descripcion", servicio.descripcion)
        servicio.precio = body.get("precio", servicio.precio)
        servicio.save()
        return JsonResponse(servicio.to_dict())

    servicio.delete()
    return JsonResponse({"mensaje": "Servicio eliminado"}, status=204)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lista_turnos(request):
    if request.method == "GET":
        turnos = Turno.objects.all()
        return JsonResponse([t.to_dict() for t in turnos], safe=False)

    body = json.loads(request.body or "{}")
    cliente_id = body.get("cliente_id")
    profesional_id = body.get("profesional_id")
    servicio_id = body.get("servicio_id")
    fecha_hora = body.get("fecha_hora")

    if not cliente_id or not profesional_id or not servicio_id or not fecha_hora:
        return JsonResponse({"error": "Faltan datos obligatorios"}, status=400)

    try:
        cliente = Cliente.objects.get(id_cliente=cliente_id)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

    try:
        profesional = Profesional.objects.get(id_profesional=profesional_id)
    except Profesional.DoesNotExist:
        return JsonResponse({"error": "Profesional no encontrado"}, status=404)

    try:
        servicio = Servicio.objects.get(id_servicio=servicio_id)
    except Servicio.DoesNotExist:
        return JsonResponse({"error": "Servicio no encontrado"}, status=404)

    turno = Turno.objects.create(
        cliente=cliente,
        profesional=profesional,
        servicio=servicio,
        fecha_hora=fecha_hora,
    )
    return JsonResponse(turno.to_dict(), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def detalle_turno(request, turno_id):
    try:
        turno = Turno.objects.get(id_turno=turno_id)
    except Turno.DoesNotExist:
        return JsonResponse({"error": "Turno no encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(turno.to_dict())

    if request.method == "PUT":
        body = json.loads(request.body or "{}")
        nuevo_estado = body.get("estado")

        if nuevo_estado and nuevo_estado != turno.estado:
            HistorialTurno.objects.create(
                turno=turno,
                estado_anterior=turno.estado,
                estado_nuevo=nuevo_estado,
            )
            turno.estado = nuevo_estado

        if "fecha_hora" in body:
            turno.fecha_hora = body["fecha_hora"]

        turno.save()
        return JsonResponse(turno.to_dict())

    turno.delete()
    return JsonResponse({"mensaje": "Turno eliminado"}, status=204)


@require_http_methods(["GET"])
def historial_de_turno(request, turno_id):
    try:
        turno = Turno.objects.get(id_turno=turno_id)
    except Turno.DoesNotExist:
        return JsonResponse({"error": "Turno no encontrado"}, status=404)

    historial = turno.historial.all()
    return JsonResponse([h.to_dict() for h in historial], safe=False)
    return JsonResponse({"ok": True})
