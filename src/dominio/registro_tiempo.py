from datetime import date

class RegistroTiempo:
    def __init__(self, fecha: date, cantidad_horas: float, tareas_realizadas: str, descripcion: str, id=None):
        self.fecha = fecha
        self.cantidad_horas = cantidad_horas
        self.tareas_realizadas = tareas_realizadas
        self.descripcion = descripcion
        self.id = id

    def mostrar_informacion(self):
        print(f"Fecha: {self.fecha}")
        print(f"Cantidad de horas: {self.cantidad_horas}")
        print(f"Tareas realizadas: {self.tareas_realizadas}")
        print(f"Descripción: {self.descripcion}")

    def gestionar_informacion(self):
        return True

    def actualizar_informacion(self):
        return self.gestionar_informacion()