from django.db import models


class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def to_dict(self):
        return {
            "id": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email,
            "creado": self.creado.isoformat(),
        }

    class Profesionales(models.Model):
        id_profesional = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        telefono = models.CharField(max_length=20)
        especialidad = models.CharField(max_length=100)
        creada = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ["apellido", "nombre"]

        def __str__(self):
            return f"{self.nombre} {self.apellido}"

        def to_dict(self):
            return {
                "id": self.id_profesional,
                "nombre": self.nombre,
                "apellido": self.apellido,
                "telefono": self.telefono,
                "especialidad": self.especialidad,
                "creado": self.creado.isoformat(),
            }
    class Servicios(models.Model):
        id_servicio = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=100)
        descripcion = models.TextField()
        precio = models.DecimalField(max_digits=10, decimal_places=2)
        creada = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ["nombre"]

        def __str__(self):
            return self.nombre

        def to_dict(self):
            return {
                "id": self.id_servicio,
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "precio": str(self.precio),
                "creado": self.creado.isoformat(),
            }
    class Turnos(models.Model):
        id_turno = models.AutoField(primary_key=True)
        id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
        id_profesional = models.ForeignKey(Profesionales, on_delete=models.CASCADE)
        servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)
        fecha_hora = models.DateTimeField()
        estado = models.CharField(max_length=20, choices=[("pendiente", "Pendiente"), ("confirmado", "Confirmado"), ("cancelado", "Cancelado")], default="pendiente")
        creada = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ["fecha_hora"]

        def __str__(self):
            return f"Turno: {self.cliente} - {self.profesional} - {self.servicio} - {self.fecha_hora}"

        def to_dict(self):
            return {
                "id": self.id_turno,
                "cliente": self.cliente.to_dict(),
                "profesional": self.profesional.to_dict(),
                "servicio": self.servicio.to_dict(),
                "fecha_hora": self.fecha_hora.isoformat(),
                "creado": self.creado.isoformat(),
            }
     class historial_turnos(models.Model):
        id_historial = models.AutoField(primary_key=True)
        id_turno = models.ForeignKey(Turnos, on_delete=models.CASCADE)
        fecha_hora = models.DateTimeField(auto_now_add=True)
        estado = models.CharField(max_length=20, choices=[("pendiente", "Pendiente"), ("confirmado", "Confirmado"), ("cancelado", "Cancelado")])
        cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
        profesional = models.ForeignKey(Profesionales, on_delete=models.CASCADE)

        class Meta:
            ordering = ["fecha_hora"]

        def __str__(self):
            return f"Historial Turno: {self.turno} - {self.estado_anterior} -> {self.estado_nuevo} - {self.fecha_hora}"

        def to_dict(self):
            return {
                "id": self.id_historial,
                "turno": self.turno.to_dict(),
                "estado_anterior": self.estado_anterior,
                "estado_nuevo": self.estado_nuevo,
                "fecha_hora": self.fecha_hora.isoformat(),
            }
