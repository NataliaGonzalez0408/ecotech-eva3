from datetime import datetime
from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO

def menu_proyecto():
    print("\n===== ECOTECH - PROYECTOS =====")
    print("1. Registrar proyecto")
    print("2. Listar proyectos")
    print("3. Buscar proyecto")
    print("4. Actualizar proyecto")
    print("5. Eliminar proyecto")
    print("0. Salir")

def ejecutar_menu():
    while True:
        menu_proyecto()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_proyecto()
        elif opcion == "2":
            listar_proyectos()
        elif opcion == "3":
            buscar_proyecto()
        elif opcion == "4":
            actualizar_proyecto()
        elif opcion == "5":
            eliminar_proyecto()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, intenta nuevamente.")

def registrar_proyecto():
    while True:
        nombre_proyecto = input("Nombre del proyecto: ").strip()
        if nombre_proyecto:
            break
        print("Error: El nombre del proyecto no puede estar vacío.")

    while True:
        descripcion = input("Descripción del proyecto: ").strip()
        if descripcion:
            break
        print("Error: La descripción no puede estar vacía.")

    while True:
        fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
    
    proyecto = Proyecto(nombre=nombre_proyecto, descripcion=descripcion, fecha_inicio=fecha_inicio)
    try:
        ProyectoDAO.insertar(proyecto)
        print("Proyecto registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar el proyecto: {e}")

def listar_proyectos():
    try:
        proyectos = ProyectoDAO.listar_proyectos()
        if proyectos:
            print("\nLista de proyectos:")
            for proyecto in proyectos:
                print(f"ID: {proyecto[0]}, Nombre: {proyecto[1]}, Descripción: {proyecto[2]}, Fecha: {proyecto[3]}")
        else:
            print("No hay proyectos registrados.")
    except Exception as e:
        print(f"Error al listar proyectos: {e}")

def buscar_proyecto():
    id_proyecto = input("Ingrese el ID del proyecto a buscar: ").strip()
    try:
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if proyecto:
            print(f"ID: {proyecto[0]}, Nombre: {proyecto[1]}, Descripción: {proyecto[2]}, Fecha: {proyecto[3]}")
        else:
            print("Proyecto no encontrado.")
    except Exception as e:
        print(f"Error al buscar el proyecto: {e}")

def actualizar_proyecto():
    id_proyecto = input("Ingrese el ID del proyecto a actualizar: ").strip()
    try:
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if not proyecto:
            print("Proyecto no encontrado.")
            return

        print(f"Datos actuales -> ID: {proyecto[0]}, Nombre: {proyecto[1]}, Descripción: {proyecto[2]}, Fecha: {proyecto[3]}")
        
        nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ").strip() or proyecto[1]
        descripcion = input("Nueva descripción (dejar en blanco para no cambiar): ").strip() or proyecto[2]
        
        while True:
            fecha_inicio = input("Nueva fecha (YYYY-MM-DD) (dejar en blanco para no cambiar): ").strip()
            if not fecha_inicio:
                fecha_inicio = proyecto[3]
                break
            try:
                datetime.strptime(fecha_inicio, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
        
        ProyectoDAO.actualizar_proyecto(id_proyecto, nombre, descripcion, fecha_inicio)
        print("Proyecto actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar el proyecto: {e}")

def eliminar_proyecto():
    id_proyecto = input("Ingrese el ID del proyecto a eliminar: ").strip()
    try:
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if proyecto:
            confirmacion = input(f"¿Seguro que desea eliminar el proyecto '{proyecto[1]}'? (s/n): ").strip().lower()
            if confirmacion == 's':
                ProyectoDAO.eliminar_proyecto(id_proyecto)
                print("Proyecto eliminado correctamente.")
            else:
                print("Eliminación cancelada.")
        else:
            print("Proyecto no encontrado.")
    except Exception as e:
        print(f"Error al eliminar el proyecto: {e}")