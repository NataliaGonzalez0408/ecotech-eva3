# servicios/gestion_proyectos.py
from datetime import datetime
import re
from dominio.proyecto import Proyecto
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.empleado_proyecto_dao import EmpleadoProyectoDAO
from persistencia.proyecto_dao import ProyectoDAO
from servicios.permisos import exigir_admin, exigir_sesion, obtener_campo


def validar_fecha_pasada(fecha_str):
    """Sanitiza y valida que la fecha sea YYYY-MM-DD, de calendario real y no futura."""
    fecha_limpia = str(fecha_str).strip() if fecha_str else ""

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_limpia):
        raise ValueError("La fecha debe cumplir el formato YYYY-MM-DD (ej: 2026-11-06).")

    try:
        fecha_dt = datetime.strptime(fecha_limpia, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("La fecha ingresada no corresponde a un día válido del calendario.")

    if fecha_dt > datetime.now().date():
        raise ValueError(f"La fecha ingresada ({fecha_limpia}) no puede ser una fecha futura.")

    return fecha_limpia


def listar_proyectos_servicio(sesion):
    exigir_sesion(sesion)
    return ProyectoDAO.listar_proyectos()


def crear_proyecto_servicio(sesion, nombre, descripcion, fecha_inicio):
    exigir_admin(sesion)

    # 1. Sanitización de texto
    nombre_limpio = nombre.strip() if nombre else ""
    descripcion_limpia = descripcion.strip() if descripcion else ""

    # 2. Validación de Nombre
    if not nombre_limpio:
        raise ValueError("El nombre del proyecto es obligatorio.")
    if len(nombre_limpio) < 3 or len(nombre_limpio) > 100:
        raise ValueError("El nombre del proyecto debe contener entre 3 y 100 caracteres.")

    # 3. Validación de Descripción
    if len(descripcion_limpia) > 255:
        raise ValueError("La descripción no puede superar los 255 caracteres.")

    # 4 y 5. Sanitización y validación estricta de fecha (pasada o presente)
    fecha_limpia = validar_fecha_pasada(fecha_inicio)

    nuevo_proyecto = Proyecto(
        id=None,
        nombre=nombre_limpio,
        descripcion=descripcion_limpia,
        fecha_inicio=fecha_limpia,
    )

    try:
        return ProyectoDAO.insertar(nuevo_proyecto)
    except Exception:
        return ProyectoDAO.insertar(nombre_limpio, descripcion_limpia, fecha_limpia)


def actualizar_proyecto_servicio(sesion_actual, proyecto_id, nombre, descripcion, fecha_inicio):
    exigir_admin(sesion_actual)

    try:
        proy_id = int(proyecto_id)
    except (ValueError, TypeError):
        raise ValueError("El ID del proyecto debe ser un número entero.")

    # Validar existencia previa del proyecto
    proyecto_existente = ProyectoDAO.buscar_por_id(proy_id)
    if not proyecto_existente:
        raise ValueError(f"No existe ningún proyecto con el ID {proy_id}.")

    nombre_limpio = nombre.strip() if nombre else ""
    descripcion_limpia = descripcion.strip() if descripcion else ""

    if not nombre_limpio:
        raise ValueError("El nombre del proyecto no puede estar vacío.")
    if len(nombre_limpio) < 3 or len(nombre_limpio) > 100:
        raise ValueError("El nombre del proyecto debe contener entre 3 y 100 caracteres.")

    if len(descripcion_limpia) > 255:
        raise ValueError("La descripción no puede superar los 255 caracteres.")

    # Validar formato y restricciones de fecha
    fecha_limpia = validar_fecha_pasada(fecha_inicio)

    # Llamada robusta según firma del DAO (objeto vs posicional)
    try:
        proyecto_actualizado = Proyecto(
            id=proy_id,
            nombre=nombre_limpio,
            descripcion=descripcion_limpia,
            fecha_inicio=fecha_limpia,
        )
        return ProyectoDAO.actualizar(proyecto_actualizado)
    except Exception:
        try:
            return ProyectoDAO.actualizar(proy_id, nombre_limpio, descripcion_limpia, fecha_limpia)
        except Exception:
            return ProyectoDAO.actualizar(
                proyecto_id=proy_id,
                nombre=nombre_limpio,
                descripcion=descripcion_limpia,
                fecha_inicio=fecha_limpia,
            )


def eliminar_proyecto_servicio(sesion, id_proyecto):
    exigir_admin(sesion)
    try:
        id_proyecto = int(id_proyecto)
    except (ValueError, TypeError):
        raise ValueError("El ID del proyecto debe ser un número entero.")

    if not ProyectoDAO.buscar_por_id(id_proyecto):
        raise ValueError(f"El proyecto con ID {id_proyecto} no existe.")

    if hasattr(ProyectoDAO, "eliminar_proyecto"):
        return ProyectoDAO.eliminar_proyecto(id_proyecto)
    return ProyectoDAO.eliminar(id_proyecto)


def asignar_empleado_a_proyecto_servicio(sesion, empleado_id, proyecto_id, rol_en_proyecto):
    """Permite a un admin vincular un empleado existente a un proyecto existente."""
    exigir_admin(sesion)

    try:
        empleado_id = int(empleado_id)
        proyecto_id = int(proyecto_id)
    except (ValueError, TypeError):
        raise ValueError("Los IDs de empleado y proyecto deben ser números enteros válidos.")

    if not EmpleadoDAO.buscar_por_id(empleado_id):
        raise ValueError(f"El empleado con ID {empleado_id} no existe en el sistema.")

    if not ProyectoDAO.buscar_por_id(proyecto_id):
        raise ValueError(f"El proyecto con ID {proyecto_id} no existe en el sistema.")

    rol_limpio = rol_en_proyecto.strip() if rol_en_proyecto else ""
    if not rol_limpio:
        raise ValueError("El rol en el proyecto es obligatorio y no puede estar vacío.")

    if len(rol_limpio) < 2 or len(rol_limpio) > 50:
        raise ValueError("El rol en el proyecto debe tener entre 2 y 50 caracteres.")

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-_]+$", rol_limpio):
        raise ValueError(
            "El rol contiene caracteres no válidos. Use solo letras, números y espacios."
        )

    exito = EmpleadoProyectoDAO.asignar_empleado_a_proyecto(empleado_id, proyecto_id, rol_limpio)
    if not exito:
        raise ValueError(
            f"El empleado (ID {empleado_id}) ya está asignado al proyecto (ID {proyecto_id})."
        )
    return True


def desvincular_empleado_de_proyecto_servicio(sesion, empleado_id, proyecto_id):
    """Permite a un admin desvincular un empleado de un proyecto."""
    exigir_admin(sesion)
    try:
        empleado_id = int(empleado_id)
        proyecto_id = int(proyecto_id)
    except (ValueError, TypeError):
        raise ValueError("Los IDs deben ser números enteros válidos.")

    if not EmpleadoDAO.buscar_por_id(empleado_id):
        raise ValueError(f"El empleado con ID {empleado_id} no existe.")

    if not ProyectoDAO.buscar_por_id(proyecto_id):
        raise ValueError(f"El proyecto con ID {proyecto_id} no existe.")

    return EmpleadoProyectoDAO.desvincular_empleado_de_proyecto(empleado_id, proyecto_id)


def ver_equipo_proyecto_servicio(sesion, proyecto_id):
    """Permite ver qué empleados participan en un proyecto específico."""
    exigir_sesion(sesion)
    try:
        proyecto_id = int(proyecto_id)
    except (ValueError, TypeError):
        raise ValueError("El ID del proyecto debe ser un entero.")

    if not ProyectoDAO.buscar_por_id(proyecto_id):
        raise ValueError(f"El proyecto con ID {proyecto_id} no existe.")

    return EmpleadoProyectoDAO.obtener_empleados_de_proyecto(proyecto_id)


def ver_proyectos_empleado_servicio(sesion, empleado_id):
    """Permite ver a qué proyectos está asignado un empleado específico."""
    exigir_sesion(sesion)
    try:
        empleado_id = int(empleado_id)
    except (ValueError, TypeError):
        raise ValueError("El ID del empleado debe ser un entero.")

    if not EmpleadoDAO.buscar_por_id(empleado_id):
        raise ValueError(f"El empleado con ID {empleado_id} no existe.")

    return EmpleadoProyectoDAO.obtener_proyectos_de_empleado(empleado_id)