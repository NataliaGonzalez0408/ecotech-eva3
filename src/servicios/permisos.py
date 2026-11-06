# servicios/permisos.py
def exigir_sesion(sesion):
    if not isinstance(sesion, dict):
        raise PermissionError("Inicie sesión.")
    if sesion.get("rol") not in ("admin", "empleado"):
        raise PermissionError("Acceso no permitido.")
    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("Sesión inválida.")


def exigir_admin(sesion):
    exigir_sesion(sesion)
    if sesion["rol"] != "admin":
        raise PermissionError("Acción solo para administrador.")

def obtener_campo(datos, campo, valor_defecto=None):
    if datos is None:
        return valor_defecto
    if isinstance(datos, dict):
        return datos.get(campo, valor_defecto)
    return getattr(datos, campo, valor_defecto)