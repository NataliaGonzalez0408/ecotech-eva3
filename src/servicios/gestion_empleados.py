# servicios/gestion_empleados.py
from servicios.permisos import exigir_admin
from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado

def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()
    