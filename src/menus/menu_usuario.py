import math
from datetime import datetime
from getpass import getpass
from entradas import pedir_dato
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.autenticacion import registrar_usuario, autenticar
from servicios.indicadores import consultar_indicador, obtener_historial
from servicios.gestion_empleados import listar_todos, crear_empleado_servicio, actualizar_empleado_servicio,eliminar_empleado_servicio
from servicios.gestion_tiempo import obtener_registros_tiempo
from servicios.gestion_proyectos import listar_proyectos_servicio, crear_proyecto_servicio, actualizar_proyecto_servicio, eliminar_proyecto_servicio,asignar_empleado_a_proyecto_servicio,desvincular_empleado_de_proyecto_servicio,ver_equipo_proyecto_servicio,ver_proyectos_empleado_servicio

def solicitar_registro(usuario_actual):
    try:
        print("\n--- Registro de Usuario Enlazado a Empleado ---")
        empleado_id = pedir_dato("ID del empleado a vincular: ", int)

        empleado = EmpleadoDAO.buscar_por_id(empleado_id)
        if not empleado:
            print(f"\nError: El empleado con ID {empleado_id} no existe.")
            return None

        nombre_emp = empleado.nombre if hasattr(empleado, "nombre") else empleado[1]
        print(f"Enlazando usuario al empleado: {nombre_emp} (ID: {empleado_id})")

        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)

        if clave != getpass("Repita la contraseña: "):
            print("\nLas contraseñas no coinciden. Operación cancelada.")
            return None

        print("\nSeleccione el rol del usuario a registrar:")
        print("1.- Administrador")
        print("2.- Empleado (Por defecto)")

        rol_opcion = input("Opción: ").strip()
        if rol_opcion == "1":
            rol = "admin"
        elif rol_opcion == "2":
            rol = "empleado"
        else:
            print("Opción no válida.")
            return None

        usuario_id = registrar_usuario(usuario_actual, empleado_id, nombre, clave, rol)
        print(f"\nCuenta creada exitosamente con ID {usuario_id} enlazada a '{nombre_emp}'.")
        return usuario_id
    except (TypeError, ValueError) as error:
        print("\nHubo un error al registrar el usuario:", error)
        return None
    except PermissionError as error:
        print(f"\nError de permisos: {error}")
        return None

def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None

    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario

def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return

    nombre = usuario_actual.get("nombre_usuario") or usuario_actual.get("nombre", "N/A")
    emp_id = usuario_actual.get("empleado_id") or usuario_actual.get("id", "N/A")
    rol = str(usuario_actual.get("rol", "No asignado")).upper()

    print("\n========================================")
    print("         PERFIL DE USUARIO              ")
    print("========================================")
    print(f"  Usuario     : {nombre}")
    print(f"  Empleado ID : {emp_id}")
    print(f"  Rol / Acceso: {rol}")
    print("========================================\n")


def menu_indicador(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return

    ejecutando = True
    while ejecutando:
        print("\n----------- Menú de Indicadores -----------")
        print("1.- Mostrar indicador actual")
        print("2.- Historial de indicadores")
        print("0.- Volver al menú principal")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            ejecutando = False
        elif opcion == "1":
            datos = consultar_indicador(usuario_actual)
            if datos:
                print(f"Indicador actual: {datos}")
            else:
                print("No se pudo obtener el indicador.")
        elif opcion == "2":
            try:
                historial = obtener_historial(usuario_actual)
                if historial:
                    print("\n--- Historial de Indicadores ---")
                    for ind in historial:
                        print(ind)
                else:
                    print("No hay historial disponible.")
            except Exception as error:
                print(f"Error al obtener el historial: {error}")
        else:
            print("Opción no válida.")


def menu_registros_tiempo(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return

    ejecutando = True
    while ejecutando:
        print("\n----------- Gestión de Registro de Tiempo -----------")
        print("1.- Consultar registros de tiempo")
        print("0.- Volver")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            ejecutando = False
        elif opcion == "1":
            try:
                registros = obtener_registros_tiempo(usuario_actual)
                if not registros:
                    print("\nNo hay registros de tiempo disponibles.")
                else:
                    rol = usuario_actual.get("rol", "") if isinstance(usuario_actual, dict) else getattr(usuario_actual, "rol", "")
                    tipo_vista = "Administrador - Todos los empleados" if rol == "admin" else "Mis Registros"
                    
                    print(f"\n--- Registros de Tiempo ({tipo_vista}) ---")
                    for reg in registros:
                        # reg = (id, empleado_id, nombre_empleado, fecha, horas, descripcion)
                        print(f"ID Reg: {reg[0]} | Emp ID: {reg[1]} | Empleado: {reg[2]} | Fecha: {reg[3]} | Horas: {reg[4]} hrs | Desc: {reg[5]}")
            except Exception as err:
                print(f"\nError: {err}")
        else:
            print("Opción no válida.")

def menu_proyectos_admin(usuario_actual):
    ejecutando = True
    while ejecutando:
        print("\n----------- Gestión de Proyectos -----------")
        print("1.- Consultar todos los proyectos ")
        print("2.- Crear nuevo proyecto ")
        print("3.- Modificar proyecto existente")
        print("4.- Eliminar proyecto ")
        print("5.- Asignar empleado a proyecto")
        print("6.- Desvincular empleado de proyecto")
        print("7.- Ver equipo de un proyecto")
        print("0.- Volver al menú principal")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            ejecutando = False
        elif opcion == "1":
            try:
                proyectos = listar_proyectos_servicio(usuario_actual)
                if not proyectos:
                    print("\nNo hay proyectos disponibles.")
                else:
                    print("\n--- Lista General de Proyectos ---")
                    for proy in proyectos:
                        print(proy)
            except Exception as err:
                print(f"\nError al listar proyectos: {err}")

        elif opcion == "2":
            try:
                nombre = input("Nombre del proyecto: ").strip()
                descripcion = input("Descripción: ").strip()
                fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
                proy = crear_proyecto_servicio(usuario_actual, nombre, descripcion, fecha_inicio)
                print(f"\n¡Proyecto creado exitosamente con ID {proy.id}!")
            except Exception as err:
                print(f"\nError al crear proyecto: {err}")

        elif opcion == "3":
            try:
                proy_id = input("ID del proyecto a modificar: ").strip()
                nombre = input("Nuevo nombre: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                fecha_inicio = input("Nueva fecha (YYYY-MM-DD): ").strip()

                if actualizar_proyecto_servicio(usuario_actual, proy_id, nombre, descripcion, fecha_inicio):
                    print("\n¡Proyecto actualizado exitosamente!")
            except Exception as err:
                print(f"\nError al actualizar proyecto: {err}")

        elif opcion == "4":
            try:
                proy_id = input("ID del proyecto a eliminar: ").strip()
                confirm = input(f"¿Confirma eliminar el proyecto ID {proy_id}? (s/n): ").strip().lower()

                if confirm == "s":
                    if eliminar_proyecto_servicio(usuario_actual, proy_id):
                        print("\n¡Proyecto eliminado correctamente!")
                    else:
                        print("\nNo se pudo eliminar el proyecto.")
                else:
                    print("\nOperación cancelada.")
            except Exception as err:
                print(f"\nError al eliminar proyecto: {err}")

        elif opcion == "5":
            try:
                empleado_id = pedir_dato("ID del empleado: ", int)
                proyecto_id = pedir_dato("ID del proyecto: ", int)
                rol_proyecto = input("Rol en el proyecto (ej: Desarrollador, QA): ").strip()

                if asignar_empleado_a_proyecto_servicio(usuario_actual, empleado_id, proyecto_id, rol_proyecto):
                    print("\n¡Empleado asignado al proyecto exitosamente!")
            except Exception as err:
                print(f"\nError al asignar empleado: {err}")

        elif opcion == "6":
            try:
                empleado_id = pedir_dato("ID del empleado a desvincular: ", int)
                proyecto_id = pedir_dato("ID del proyecto: ", int)

                if desvincular_empleado_de_proyecto_servicio(usuario_actual, empleado_id, proyecto_id):
                    print("\n¡Empleado desvinculado del proyecto!")
                else:
                    print("\nNo se encontró una asignación activa entre el empleado y ese proyecto.")
            except Exception as err:
                print(f"\nError al desvincular empleado: {err}")

        elif opcion == "7":
            try:
                proy_id = pedir_dato("ID del proyecto a consultar: ", int)
                equipo = ver_equipo_proyecto_servicio(usuario_actual, proy_id)
                if not equipo:
                    print("\nNo hay equipo asignado o el ID no existe.")
                else:
                    print(f"\n--- Equipo del Proyecto (ID: {proy_id}) ---")
                    for e in equipo:
                        print(f"ID Empleado: {e[0]} | Nombre: {e[1]} | Rol: {e[3]}")
            except Exception as err:
                print(f"\nError al consultar equipo: {err}")
        else:
            print("Opción no válida.")


def menu_proyectos_empleado(usuario_actual):
    emp_id = usuario_actual.get("empleado_id") if isinstance(usuario_actual, dict) else getattr(usuario_actual, "empleado_id", None)
    ejecutando = True

    while ejecutando:
        print("\n----------- Consulta de Proyectos -----------")
        print("1.- Ver mis proyectos asignados")
        print("2.- Consultar lista general de proyectos")
        print("3.- Ver equipo de un proyecto")
        print("0.- Volver al menú principal")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            ejecutando = False
        elif opcion == "1":
            try:
                proyectos = ver_proyectos_empleado_servicio(usuario_actual, emp_id)
                if not proyectos:
                    print("\nNo tienes proyectos asignados actualmente.")
                else:
                    print("\n--- Tus Proyectos Asignados ---")
                    for p in proyectos:
                        print(f"ID: {p[0]} | Proyecto: {p[1]} | Rol: {p[4]} | Asignado el: {p[5]}")
            except Exception as err:
                print(f"\nError al consultar tus proyectos: {err}")

        elif opcion == "2":
            try:
                proyectos = listar_proyectos_servicio(usuario_actual)
                if not proyectos:
                    print("\nNo hay proyectos disponibles.")
                else:
                    print("\n--- Lista General de Proyectos ---")
                    for proy in proyectos:
                        print(proy)
            except Exception as err:
                print(f"\nError al listar proyectos: {err}")

        elif opcion == "3":
            try:
                proy_id = pedir_dato("ID del proyecto a consultar: ", int)
                equipo = ver_equipo_proyecto_servicio(usuario_actual, proy_id)
                if not equipo:
                    print("\nNo hay equipo asignado o el ID no existe.")
                else:
                    print(f"\n--- Equipo del Proyecto (ID: {proy_id}) ---")
                    for e in equipo:
                        print(f"ID Empleado: {e[0]} | Nombre: {e[1]} | Rol: {e[3]}")
            except Exception as err:
                print(f"\nError al consultar equipo: {err}")
        else:
            print("Opción no válida.")

def menu_privado_admin(usuario_actual):
    """Menú Principal del Administrador con CRUD de Empleados y Proyectos."""
    ejecutando = True
    while ejecutando:
        print("\n==================================================")
        print("      MENÚ PRINCIPAL DE ADMINISTRADOR     ")
        print("==================================================")
        print("1.- Mostrar perfil")
        print("2.- Consultar empleados")
        print("3.- Crear nuevo empleado")
        print("4.- Modificar empleado existente")
        print("5.- Eliminar empleado")
        print("6.- Registrar usuario enlazado a empleado")
        print("7.- Mostrar indicadores económicos")
        print("8.- Gestión de registro de tiempo")
        print("9.- Gestión de proyectos")
        print("99.- Cerrar sesión")
        print("0.- Salir del sistema")

        opcion = input("Opción: ").strip()

        if opcion in ("0", "99"):
            return "9" if opcion == "99" else "0"

        elif opcion == "1":
            mostrar_perfil(usuario_actual)

        # --- READ (Empleados) ---
        elif opcion == "2":
            try:
                empleados = listar_todos(usuario_actual)
                print("\n--- Lista General de Empleados ---")
                for emp in empleados:
                    print(emp)
            except Exception as error:
                print(f"\nError al listar empleados: {error}")

        # --- CREATE (Empleado) ---
        elif opcion == "3":
            print("\n--- Crear Nuevo Empleado (Ingrese '0' en cualquier momento para cancelar) ---")
            cancelado = False   

            nombre = ""
            campo_valido = False
            cancelado = False
            while not campo_valido and not cancelado:
                nombre = input("Nombre completo: ").strip()
                if nombre == "0":
                    cancelado = True
                elif nombre:
                    campo_valido = True
                else:
                    print("El nombre no puede estar vacío, vuelva a intentarlo.")

                if cancelado:
                    print("Creación de empleado cancelada.")
                    continue

                correo = ""
                campo_valido = False
                cancelado = False
                while not campo_valido and not cancelado:
                    correo = input("Correo electrónico: ").strip()
                    if correo == "0":
                        print("Operación cancelada.")
                        cancelado = True
                    elif "@" in correo and correo.endswith("ecotech.com"):
                        campo_valido = True
                    else:
                        print("Debe ingresar un correo válido. (Ej: usuario@ecotech.com)")
                if cancelado:
                    print("Creación de empleado cancelada.")
                    continue

                telefono = ""
                campo_valido = False
                cancelado = False
                while not campo_valido and not cancelado:
                    telefono = input("Teléfono: ").strip()
                    if telefono == "0":
                        print("Operación cancelada.")
                        cancelado = True
                    elif telefono:
                        campo_valido = True
                    else:
                        print("El teléfono no puede estar vacío, vuelva a intentarlo.")
                if cancelado:
                    print("Creación de empleado cancelada.")
                    continue

            fecha_inicio = ""
            campo_valido = False
            while not campo_valido and not cancelado:
                entrada_raw = input(
                    "Fecha contrato (YYYY-MM-DD): "
                )  # ej: 2026-05-22
                fecha_inicio = (
                    entrada_raw.strip().replace("\r", "").replace("\n", "")
                )

                if fecha_inicio == "0":
                    cancelado = True
                else:
                    fecha_dt = None
                    try:
                        fecha_dt = datetime.strptime(
                            fecha_inicio, "%Y-%m-%d"
                        ).date()
                    except ValueError:
                        print(
                            " Error: La fecha debe ser un calendario real en"
                            " formato YYYY-MM-DD (ej: 2023-12-05)."
                        )

                    if fecha_dt is not None:
                        if fecha_dt > datetime.now().date():
                            print(
                                f" Error: La fecha ({fecha_inicio}) es posterior a la fecha actual y no se permite ingresar fechas futuras."
                            )
                        else:
                            campo_valido = True

            salario = ""
            campo_valido = False
            while not campo_valido and not cancelado:
                entrada_raw = input("Salario base: ")
                salario_str = (
                    entrada_raw.strip().replace("\r", "").replace("\n", "")
                )

                if salario_str == "0":
                    cancelado = True
                else:
                    try:
                        salario_val = float(salario_str)
                        if salario_val < 0:
                            print(" Error: El salario no puede ser negativo.")
                        elif salario_val > 1000000:
                            print(
                                " Error: El salario no debe sobrepasar los 1.000.000."
                            )
                        else:
                            salario = salario_str
                            campo_valido = True
                    except ValueError:
                        print(
                            " Error: Debe ingresar un valor numérico válido para el salario."
                        )

            if cancelado:
                print("Operación cancelada.")
                continue

            dept_id = 0
            campo_valido = False
            while not campo_valido and not cancelado:
                dept_str = input("ID Departamento: ").strip()
                if dept_str == "0":
                    cancelado = True
                else:
                    try:
                        dept_id = int(dept_str)
                        if dept_id > 0:
                            campo_valido = True
                        else:
                            print(" Error: El ID de departamento debe ser mayor a 0. Intente nuevamente.")
                    except ValueError:
                        print(" Error: El ID de departamento debe ser un número entero válido.")

            if cancelado:
                print("Operación cancelada.")
                continue

            try:
                emp = crear_empleado_servicio(
                    usuario_actual, nombre, correo, telefono, fecha_inicio, salario, dept_id
                )
                print(f"\n¡Empleado creado exitosamente con ID {emp.id}!")
            except Exception as err:
                print(f"\nError al guardar empleado: {err}")

        # --- UPDATE (Empleado) ---
        elif opcion == "4":
            try:
                emp_id = int(input("ID del empleado a modificar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                correo = input("Nuevo correo: ").strip()
                telefono = input("Nuevo teléfono: ").strip()
                salario = float(input("Nuevo salario: ").strip())

                if actualizar_empleado_servicio(
                    usuario_actual, emp_id, nombre, correo, telefono, salario
                ):
                    print("\n¡Empleado actualizado correctamente!")
            except Exception as err:
                print(f"\nError al actualizar empleado: {err}")

        # --- DELETE (Empleado) ---
        elif opcion == "5":
            try:
                emp_id = int(input("ID del empleado a eliminar: ").strip())
                confirm = input(f"¿Confirma eliminar al empleado ID {emp_id}? (s/n): ").strip().lower()

                if confirm == "s":
                    if eliminar_empleado_servicio(usuario_actual, emp_id):
                        print("\n¡Empleado eliminado exitosamente!")
                    else:
                        print("\nNo se pudo eliminar el empleado.")
                else:
                    print("\nOperación cancelada.")
            except Exception as err:
                print(f"\nError al eliminar empleado: {err}")

        elif opcion == "6":
            solicitar_registro(usuario_actual)

        elif opcion == "7":
            menu_indicador(usuario_actual)

        elif opcion == "8":
            menu_registros_tiempo(usuario_actual)

        elif opcion == "9":
            menu_proyectos_admin(usuario_actual)

        else:
            print("Opción no válida.")


def menu_privado_empleado(usuario_actual):
    """Menú Principal del Empleado (Sin opciones CRUD ni de administración)."""
    ejecutando = True
    while ejecutando:
        print("\n=========================================")
        print("        MENÚ PRINCIPAL     ")
        print("=========================================")
        print("1.- Mostrar perfil")
        print("2.- Mostrar indicadores económicos")
        print("3.- Consultar mi registro de tiempo")
        print("4.- Consultar proyectos")
        print("9.- Cerrar sesión")
        print("0.- Salir del sistema")

        opcion = input("Opción: ").strip()

        if opcion in ("0", "9"):
            return opcion
        elif opcion == "1":
            mostrar_perfil(usuario_actual)
        elif opcion == "2":
            menu_indicador(usuario_actual)
        elif opcion == "3":
            menu_registros_tiempo(usuario_actual)
        elif opcion == "4":
            menu_proyectos_empleado(usuario_actual)
        else:
            print("Opción no válida.")


def menu_privado(usuario_actual):
    """Enrutador de sesión por rol."""
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"

    rol_sesion = (
        usuario_actual.get("rol")
        if isinstance(usuario_actual, dict)
        else getattr(usuario_actual, "rol", "")
    )

    if rol_sesion == "admin":
        return menu_privado_admin(usuario_actual)
    else:
        return menu_privado_empleado(usuario_actual)