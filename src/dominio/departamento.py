from dominio.empleado import Empleado

class Departamento:
    def __init__(self, idDepartamento: int , nombre: str , gerente: str):
        self.idDepartamento = idDepartamento
        self.nombre = nombre
        self.gerente = gerente
        self._empleados: list[Empleado] = []

    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def eliminar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:
            self._empleados.remove(empleado)
            return True
        return False

    def asignar_gerente(self, gerente: str) -> None:
        self.gerente = gerente

    def mostrar_datos(self) -> str:
        return f"ID: {self.idDepartamento}, Nombre: {self.nombre}, Gerente: {self.gerente}, Empleados: {[empleado.mostrar_datos() for empleado in self._empleados]}"

    def validar_departamento(self) -> bool:
        return True