# src/dominio/empleado.py
from datetime import date

class Empleado:

    #def __init__(self, nombre: str, direccion: str, telefono: int, correo: str, fechainiciocontrato: date, salario: int, id=None):

    def __init__(self, nombre: str, correo: str, telefono: int, fecha_inicio_contrato: date, salario: int, id=None):

        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario
        self.id = id

    def mostrar_datos(self) -> str:
        #return f"{self.nombre} - {self.direccion} - {self.telefono} - {self.correo} - {self.fechainiciocontrato} - {self.salario} - {self.id}"
        
        return f"{self.nombre} - {self.correo} - {self.id}"

    def gestionar_informacion(self) -> bool:
        return True
    
    def actualizar_datos(self) -> bool:
        return self.gestionar_informacion()

    def cambiar_departamento(self, nuevo_departamento) -> bool:
        return True