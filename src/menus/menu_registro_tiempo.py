from datetime import datetime
from dominio.registro_tiempo import RegistroTiempo
from persistencia.registro_tiempo_dao import RegistroTiempoDAO

def menu_registro_tiempo():
    print("\n===== ECOTECH - REGISTROS DE TIEMPO =====")
    print("1. Registrar registro de tiempo")
    print("2. Listar registros de tiempo")
    print("3. Buscar registro de tiempo")
    print("4. Actualizar registro de tiempo")
    print("5. Eliminar registro de tiempo")
    print("0. Salir")

def ejecutar_menu():
    while True:
        menu_registro_tiempo()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_registro_tiempo()
        elif opcion == "2":
            listar_registros_tiempo()
        elif opcion == "3":
            buscar_registro_tiempo()
        elif opcion == "4":
            actualizar_registro_tiempo()
        elif opcion == "5":
            eliminar_registro_tiempo()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, intenta nuevamente.")

def registrar_registro_tiempo():
    while True:
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")

    while True:
        try:
            cantidad_horas = float(input("Cantidad de horas: ").strip())
            if cantidad_horas > 0:
                break
            print("Error: La cantidad de horas debe ser mayor a 0.")
        except ValueError:
            print("Error: La cantidad de horas debe ser numérica.")

    while True:
        tareas_realizadas = input("Tareas realizadas: ").strip()
        if tareas_realizadas:
            break
        print("Error: El campo de tareas no puede estar vacío.")

    while True:
        descripcion = input("Descripción: ").strip()
        if descripcion:
            break
        print("Error: La descripción no puede estar vacía.")
    
    registro_tiempo = RegistroTiempo(fecha=fecha, cantidad_horas=cantidad_horas, tareas_realizadas=tareas_realizadas, descripcion=descripcion)
    try:
        RegistroTiempoDAO.insertar(registro_tiempo)
        print("Registro de tiempo guardado correctamente.")
    except Exception as e:
        print(f"No fue posible registrar el tiempo: {e}")

def listar_registros_tiempo():
    try:
        registros = RegistroTiempoDAO.listar()
        if registros:
            print("\nLista de registros de tiempo:")
            for reg in registros:
                print(f"ID: {reg.id}, Fecha: {reg.fecha}, Horas: {reg.cantidad_horas}, Tareas: {reg.tareas_realizadas}")
        else:
            print("No hay registros de tiempo registrados.")
    except Exception as e:
        print(f"Error al listar los registros: {e}")

def buscar_registro_tiempo():
    id_registro = input("Ingrese el ID del registro a buscar: ").strip()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
        if registro:
            print(f"ID: {registro.id}, Fecha: {registro.fecha}, Horas: {registro.cantidad_horas}, Tareas: {registro.tareas_realizadas}, Descripción: {registro.descripcion}")
        else:
            print("Registro de tiempo no encontrado.")
    except Exception as e:
        print(f"Error al buscar el registro: {e}")

def actualizar_registro_tiempo():
    id_registro = input("Ingrese el ID del registro a actualizar: ").strip()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
        if not registro:
            print("Registro de tiempo no encontrado.")
            return

        while True:
            nueva_fecha = input(f"Fecha ({registro.fecha}): ").strip()
            if not nueva_fecha:
                nueva_fecha = registro.fecha
                break
            try:
                datetime.strptime(nueva_fecha, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
            
        while True:
            nuevas_horas = input(f"Horas ({registro.cantidad_horas}): ").strip()
            if not nuevas_horas:
                nueva_cantidad_horas = registro.cantidad_horas
                break
            try:
                nueva_cantidad_horas = float(nuevas_horas)
                if nueva_cantidad_horas > 0:
                    break
                print("Error: Las horas deben ser mayor a 0.")
            except ValueError:
                print("Error: Las horas deben ser numéricas.")
                
        nuevas_tareas = input(f"Tareas ({registro.tareas_realizadas}): ").strip() or registro.tareas_realizadas
        nueva_descripcion = input(f"Descripción ({registro.descripcion}): ").strip() or registro.descripcion
        
        registro.fecha = nueva_fecha
        registro.cantidad_horas = nueva_cantidad_horas
        registro.tareas_realizadas = nuevas_tareas
        registro.descripcion = nueva_descripcion
        
        RegistroTiempoDAO.actualizar(registro)
        print("Registro actualizado correctamente.")
    except Exception as e:
        print(f"No fue posible actualizar el registro: {e}")

def eliminar_registro_tiempo():
    id_registro = input("Ingrese el ID del registro a eliminar: ").strip()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
        if registro:
            confirmacion = input(f"¿Seguro que desea eliminar el registro de la fecha {registro.fecha}? (s/n): ").strip().lower()
            if confirmacion == 's':
                RegistroTiempoDAO.eliminar(id_registro)
                print("Registro eliminado correctamente.")
            else:
                print("Eliminación cancelada.")
        else:
            print("Registro de tiempo no encontrado.")
    except Exception as e:
        print(f"No fue posible eliminar el registro: {e}")