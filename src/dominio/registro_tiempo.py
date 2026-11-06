from datetime import date

class RegistroTiempo:
    def __init__(self, id, empleado_id, horas, fecha, descripcion=""):
        self.id = id
        self.empleado_id = empleado_id
        self.horas = horas
        self.fecha = fecha
        self.descripcion = descripcion

    def __str__(self) -> str:
        return f"ID: {self.id} | Horas: {self.horas} | Fecha: {self.fecha} | Descripción: {self.descripcion}"

    def __repr__(self) -> str:
        return self.__str__()