# src/servicios/gestion_tiempo.py
from datetime import datetime
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion


def validar_fecha_pasada(fecha_str):
    fecha_limpia = str(fecha_str).strip() if fecha_str else ""
    try:
        fecha_dt = datetime.strptime(fecha_limpia, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            "La fecha debe cumplir el formato YYYY-MM-DD (ej: 2026-11-06)."
        )

    if fecha_dt > datetime.now().date():
        raise ValueError(
            f"La fecha del registro ({fecha_limpia}) no puede ser una fecha"
            " futura."
        )
    return fecha_limpia


def obtener_registros_tiempo(usuario_actual):
    exigir_sesion(usuario_actual)

    if isinstance(usuario_actual, dict):
        rol = usuario_actual.get("rol", "")
        empleado_id = usuario_actual.get("empleado_id") or usuario_actual.get(
            "id"
        )
    else:
        rol = getattr(usuario_actual, "rol", "")
        empleado_id = getattr(
            usuario_actual,
            "empleado_id",
            getattr(usuario_actual, "id", None),
        )

    if rol == "admin":
        return RegistroTiempoDAO.listar_todos()
    else:
        if not empleado_id:
            raise ValueError(
                "No se pudo identificar el ID del empleado anclado a esta sesión."
            )
        return RegistroTiempoDAO.listar_por_empleado(empleado_id)


def registrar_tiempo_servicio(
    usuario_actual, proyecto_id, horas, fecha, descripcion=""
):
    exigir_sesion(usuario_actual)

    if isinstance(usuario_actual, dict):
        empleado_id = usuario_actual.get("empleado_id") or usuario_actual.get(
            "id"
        )
    else:
        empleado_id = getattr(
            usuario_actual,
            "empleado_id",
            getattr(usuario_actual, "id", None),
        )

    if not empleado_id:
        raise ValueError("Sesión inválida: No se identificó un empleado anclado.")

    try:
        proy_id = int(proyecto_id)
    except (ValueError, TypeError):
        raise ValueError("El ID de proyecto debe ser un entero válido.")

    try:
        horas_val = float(horas)
        if horas_val <= 0 or horas_val > 24:
            raise ValueError("Las horas deben estar en el rango de 0.5 a 24.")
    except (ValueError, TypeError):
        raise ValueError("La cantidad de horas ingresada no es válida.")

    fecha_limpia = validar_fecha_pasada(fecha)
    descripcion_limpia = str(descripcion).strip() if descripcion else ""

    return RegistroTiempoDAO.insertar(
        empleado_id=empleado_id,
        proyecto_id=proy_id,
        fecha=fecha_limpia,
        horas=horas_val,
        descripcion=descripcion_limpia,
    )