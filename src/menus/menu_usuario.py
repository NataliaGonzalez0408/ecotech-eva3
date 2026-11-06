import math
from getpass import getpass
from entradas import pedir_dato
from dominio.usuario import Usuario
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.autenticacion import registrar_usuario, autenticar
from servicios.indicadores import consultar_indicador, obtener_historial
from servicios.gestion_empleados import listar_todos
from servicios.gestion_tiempo import obtener_registros_tiempo


def solicitar_registro():
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None

        print("Seleccione el rol del usuario a registrar:")
        print("1.- Administrador")
        print("2.- Empleado (Por defecto)")

        rol_opcion = input("Opción: ").strip()
        if rol_opcion == "1":
            rol = "admin"
        elif rol_opcion == "2":
            rol = "empleado"  # Alineado a los roles estándar
        else:
            print("Opción no válida.")
            return None

        usuario_id = registrar_usuario(empleado_id, nombre, clave, rol)
    except (TypeError, ValueError) as error:
        print("Hubo un error al registrar el usuario:", error)
        return None

    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id

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
    rol = usuario_actual.get("rol", "No asignado")

    print(f"Usuario: {nombre}")
    print(f"Empleado ID: {emp_id}")
    print(f"Rol: {rol}")

def menu_indicador(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"

    while True:
        print("\n----------- Menú de Indicadores -----------")
        print("1.- Mostrar indicador, 2.- Historial de Indicadores, 0.- Volver al menú principal")

        opcion = input("Opción: ").strip()

        if opcion in ("0", "9"):
            return opcion
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

    while True:
        print("\n----------- Gestión de Registro de Tiempo -----------")
        print("1.- Consultar registros de tiempo")
        print("0.- Volver")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            try:
                # Llama a la función del módulo servicios/gestion_tiempo.py
                registros = obtener_registros_tiempo(usuario_actual)

                if not registros:
                    print("\nNo hay registros de tiempo.")
                else:
                    rol = usuario_actual.get("rol", "") if isinstance(usuario_actual, dict) else getattr(usuario_actual, "rol", "")
                    tipo_vista = "Administrador" if rol == "admin" else "Empleado"
                    print(f"\n--- Registros de Tiempo ({tipo_vista}) ---")
                    for reg in registros:
                        print(reg)
            except Exception as err:
                print(f"\nError: {err}")
        else:
            print("Opción no válida.")

def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"

    rol = usuario_actual.get("rol") if isinstance(usuario_actual, dict) else getattr(usuario_actual, "rol", "")

    while True:
        print("\n----------- Menú de Opciones -----------")
        print("1.- Mostrar perfil, 2.- Mostrar indicador, 3.- Consultar registros de tiempo")

        if rol == "admin":
            print("4.- Registrar empleados, 5.- Listar empleados")

        print("9.- Cerrar sesión, 0.- Salir")

        opcion = input("Opción: ").strip()

        if opcion in ("0", "9"):
            return opcion
        elif opcion == "1":
            mostrar_perfil(usuario_actual)
        elif opcion == "2":
            menu_indicador(usuario_actual)
        elif opcion == "3":
            menu_registros_tiempo(usuario_actual)
        elif opcion == "4" and rol == "admin":
            print("Función de registro de empleados en construcción.")
        elif opcion == "5" and rol == "admin":
            try:
                empleados = listar_todos(usuario_actual)
                for empleado in empleados:
                    print(empleado)
            except PermissionError as error:
                print(error)
        else:
            print("Opción no válida o no autorizada.")