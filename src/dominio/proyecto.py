from datetime import date


class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: date, id=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.id = id

    def __str__(self):
        return f"[{self.id}] {self.nombre} (inicio: {self.fecha_inicio}) - {self.descripcion}"

    def __repr__(self):
        return self.__str__()

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Fecha de inicio: {self.fecha_inicio}")

    def gestionar_informacion(self):
        return True

    def actualizar_informacion(self):
        return self.gestionar_informacion()

    def actualizar_datos(self):
        return self.gestionar_informacion()

    def cambiar_estado(self, nuevo_estado):
        return True