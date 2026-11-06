# servicios/gestion_tiempo.py
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion

def obtener_registros_tiempo(usuario_actual):
    exigir_sesion(usuario_actual)

    # Extraer campos de manera segura tanto para dict como para object
    if isinstance(usuario_actual, dict):
        rol = usuario_actual.get("rol", "")
        empleado_id = usuario_actual.get("empleado_id") or usuario_actual.get("id")
    else:
        rol = getattr(usuario_actual, "rol", "")
        empleado_id = getattr(usuario_actual, "empleado_id", getattr(usuario_actual, "id", None))

    if rol == "admin":
        return RegistroTiempoDAO.listar_todos()
    else:
        return RegistroTiempoDAO.listar_por_empleado(empleado_id)