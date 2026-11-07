# src/servicios/gestion_empleados.py

from datetime import datetime
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin, exigir_sesion


def validar_fecha_pasada(fecha_str):
    """
    Sanitiza y valida que la fecha sea YYYY-MM-DD, de calendario real 
    y no futura respecto al día de hoy.
    """
    if not fecha_str:
        raise ValueError("La fecha no puede estar vacía.")

    fecha_limpia = str(fecha_str).strip().replace("\r", "").replace("\n", "")

    try:
        fecha_dt = datetime.strptime(fecha_limpia, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("La fecha debe tener un formato de calendario válido 'YYYY-MM-DD' (ej: 2026-05-20).")

    if fecha_dt > datetime.now().date():
        raise ValueError(f"La fecha ingresada ({fecha_limpia}) no puede ser posterior a la fecha actual.")

    return fecha_limpia


def listar_todos(sesion_actual):
    """Obtiene la lista de todos los empleados (Requiere rol Administrador)."""
    exigir_admin(sesion_actual)
    if hasattr(EmpleadoDAO, "listar"):
        return EmpleadoDAO.listar()
    return EmpleadoDAO.obtener_todos()


def obtener_empleado_por_id(sesion_actual, empleado_id):
    """Busca un empleado específico por su ID."""
    exigir_sesion(sesion_actual)

    try:
        emp_id = int(empleado_id)
    except (ValueError, TypeError):
        raise ValueError("El ID del empleado debe ser un número entero.")

    empleado = EmpleadoDAO.buscar_por_id(emp_id)
    if not empleado:
        raise ValueError(f"No se encontró ningún empleado con el ID {emp_id}.")

    return empleado


def crear_empleado_servicio(
    sesion_actual,
    nombre,
    correo,
    telefono,
    fecha_contratacion,
    salario,
    departamento_id,
):
    """Crea un nuevo empleado en la base de datos (Requiere rol Administrador)."""
    exigir_admin(sesion_actual)

    # 1. Sanitización de texto y correo
    nombre_limpio = nombre.strip().replace("\r", "").replace("\n", "") if nombre else ""
    correo_limpio = (
        correo.strip().lower().replace("\r", "").replace("\n", "").replace(" ", "")
        if correo else ""
    )
    telefono_limpio = telefono.strip().replace("\r", "").replace("\n", "") if telefono else ""

    if not nombre_limpio:
        raise ValueError("El nombre del empleado no puede estar vacío.")

    if "@" not in correo_limpio or not correo_limpio.endswith("@ecotech.com"):
        raise ValueError("El correo electrónico debe pertenecer al dominio corporativo (@ecotech.com).")

    # 2. Validación de fecha
    fecha_limpia = validar_fecha_pasada(fecha_contratacion)

    # 3. Conversión numérica
    try:
        salario_val = float(salario)
        if salario_val < 0:
            raise ValueError("El salario no puede ser un valor negativo.")
        elif salario_val > 1000000:
            raise ValueError("El salario no debe sobrepasar los 1.000.000.")
    except (ValueError, TypeError) as e:
        if "salario" in str(e).lower():
            raise e
        raise ValueError("El salario debe ser un número válido.")

    try:
        dept_id = int(departamento_id)
        if dept_id <= 0:
            raise ValueError("El ID de departamento debe ser mayor a 0.")
    except (ValueError, TypeError):
        raise ValueError("El ID de departamento debe ser un entero válido.")

    nuevo_empleado = None
    try:
        nuevo_empleado = Empleado(
            None,
            nombre_limpio,
            correo_limpio,
            telefono_limpio,
            fecha_limpia,
            salario_val,
            dept_id,
        )
    except TypeError:
        try:
            nuevo_empleado = Empleado(
                nombre_limpio,
                correo_limpio,
                telefono_limpio,
                fecha_limpia,
                salario_val,
                dept_id,
            )
        except TypeError:
            nuevo_empleado = Empleado(
                nombre=nombre_limpio,
                correo=correo_limpio,
                telefono=telefono_limpio,
                fecha_contratacion=fecha_limpia,
                salario=salario_val,
                departamento_id=dept_id,
            )

    return EmpleadoDAO.insertar(nuevo_empleado)


def actualizar_empleado_servicio(
    sesion_actual, empleado_id, nombre, correo, telefono, salario
):
    exigir_admin(sesion_actual)

    try:
        emp_id = int(empleado_id)
    except (ValueError, TypeError):
        raise ValueError("El ID del empleado debe ser un número entero.")

    empleado_existente = EmpleadoDAO.buscar_por_id(emp_id)
    if not empleado_existente:
        raise ValueError(f"No existe ningún empleado con el ID {emp_id}.")

    nombre_limpio = nombre.strip().replace("\r", "").replace("\n", "") if nombre else ""
    correo_limpio = correo.strip().lower().replace("\r", "").replace("\n", "") if correo else ""
    telefono_limpio = telefono.strip().replace("\r", "").replace("\n", "") if telefono else ""

    if not nombre_limpio:
        raise ValueError("El nombre del empleado no puede estar vacío.")

    if "@" not in correo_limpio or "." not in correo_limpio:
        raise ValueError("El correo electrónico ingresado no es válido.")

    if not correo_limpio.endswith("@ecotech.com"):
        raise ValueError("El correo electrónico debe pertenecer al dominio corporativo (@ecotech.com).")

    try:
        salario_val = float(salario)
        if salario_val < 0:
            raise ValueError("El salario no puede ser un valor negativo.")
    except (ValueError, TypeError):
        raise ValueError("El salario debe ser un número válido.")

    try:
        return EmpleadoDAO.actualizar(
            emp_id,
            nombre_limpio,
            correo_limpio,
            telefono_limpio,
            salario_val,
        )
    except Exception:
        return EmpleadoDAO.actualizar(
            empleado_id=emp_id,
            nombre=nombre_limpio,
            correo=correo_limpio,
            telefono=telefono_limpio,
            salario=salario_val,
        )


def eliminar_empleado_servicio(sesion_actual, empleado_id):
    exigir_admin(sesion_actual)

    try:
        emp_id = int(empleado_id)
    except (ValueError, TypeError):
        raise ValueError("El ID del empleado debe ser un número entero.")

    empleado_existente = EmpleadoDAO.buscar_por_id(emp_id)
    if not empleado_existente:
        raise ValueError(f"No existe ningún empleado con el ID {emp_id}.")

    return EmpleadoDAO.eliminar(emp_id)