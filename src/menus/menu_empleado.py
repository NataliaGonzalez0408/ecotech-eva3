import re
from datetime import datetime
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

def menu_empleado():
    print("\n===== ECOTECH - EMPLEADOS =====")
    print("1. Registrar empleado")
    print("2. Listar empleados")
    print("3. Buscar empleado")
    print("4. Actualizar empleado")
    print("5. Eliminar empleado")
    print("0. Salir")

def ejecutar_menu():
    while True:
        menu_empleado()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            listar_empleados()
        elif opcion == "3":
            buscar_empleado()
        elif opcion == "4":
            actualizar_empleado()
        elif opcion == "5":
            eliminar_empleado()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, intenta nuevamente.")

def registrar_empleado():
    while True:
        nombre = input("Nombre: ").strip()
        if nombre.replace(" ", "").isalpha() and len(nombre) >= 2 and len(nombre) <= 100:
            break
        print("Error: El nombre no puede contener menos de 2 caracteres y no más de 100 caracteres.")

    while True:
        correo = input("Correo: ").strip()
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo) and len(correo) <= 50 and correo.endswith("@ecotech.com"):
            break
        print("Error: Formato inválido. Ejemplo: usuario@ecotech.com")

    while True:
        telefono = input("Teléfono: ").strip()
        if telefono.isdigit() and len(telefono) == 10:
            break
        print("Error: El teléfono debe contener solo 10 números.")

    while True:
        fecha_inicio_contrato = input("Fecha de inicio de contrato (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha_inicio_contrato, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")

    while True:
        try:
            salario = float(input("Salario: ").strip())
            if salario > 150000 and salario <= 1000000:
                break
            print("Error: El salario debe ser mayor a 150000 y no mas de 1000000.")
        except ValueError:
            print("Error: El salario debe ser numérico.")

    empleado = Empleado(nombre=nombre, correo=correo, telefono=telefono, fecha_inicio_contrato=fecha_inicio_contrato, salario=salario)
    try:
        EmpleadoDAO.insertar(empleado)
        print("Empleado registrado correctamente.")
    except Exception as e:
        print(f"No fue posible registrar el empleado: {e}")

def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if empleados:
        print("\nLista de empleados:")
        for emp in empleados:
            print(f"ID: {emp.id}, Nombre: {emp.nombre}, Correo: {emp.correo}, Teléfono: {emp.telefono}, Salario: {emp.salario}")
    else:
        print("No hay empleados registrados.")

def buscar_empleado():
    id_empleado = input("Ingrese el ID del empleado a buscar: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado:
        print(f"ID: {empleado.id}, Nombre: {empleado.nombre}, Correo: {empleado.correo}, Teléfono: {empleado.telefono}, Salario: {empleado.salario}")
    else:
        print("Empleado no encontrado.")

def actualizar_empleado():
    id_empleado = input("Ingrese el ID del empleado a actualizar: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if not empleado:
        print("Empleado no encontrado.")
        return

    while True:
        nombre = input(f"Nombre ({empleado.nombre}): ").strip()
        if not nombre:
            nombre = empleado.nombre
            break
        elif nombre.replace(" ", "").isalpha():
            break
        print("Error: El nombre solo puede contener letras.")

    while True:
        correo = input(f"Correo ({empleado.correo}): ").strip()
        if not correo:
            correo = empleado.correo
            break
        elif re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
            break
        print("Error: Formato inválido. Ejemplo: usuario@correo.com")

    while True:
        telefono = input(f"Teléfono ({empleado.telefono}): ").strip()
        if not telefono:
            telefono = empleado.telefono
            break
        elif telefono.isdigit() and len(telefono) == 8:
            break
        print("Error: El teléfono debe contener solo 8 números.")

    while True:
        fecha = input(f"Fecha Contrato ({empleado.fecha_inicio_contrato}): ").strip()
        if not fecha:
            fecha = empleado.fecha_inicio_contrato
            break
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")

    while True:
        salario_str = input(f"Salario ({empleado.salario}): ").strip()
        if not salario_str:
            salario = empleado.salario
            break
        try:
            salario = float(salario_str)
            if salario > 0:
                break
            print("Error: El salario debe ser mayor a 0.")
        except ValueError:
            print("Error: El salario debe ser numérico.")

    empleado.nombre = nombre
    empleado.correo = correo
    empleado.telefono = telefono
    empleado.fecha_inicio_contrato = fecha
    empleado.salario = salario
    
    try:
        EmpleadoDAO.actualizar(empleado)
        print("Empleado actualizado correctamente.")
    except Exception as e:
        print(f"No fue posible actualizar el empleado: {e}")

def eliminar_empleado():
    id_empleado = input("Ingrese el ID del empleado a eliminar: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado:
        confirmacion = input(f"¿Seguro que desea eliminar al empleado {empleado.nombre}? (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                EmpleadoDAO.eliminar(id_empleado)
                print("Empleado eliminado correctamente.")
            except Exception as e:
                print(f"No fue posible eliminar el empleado: {e}")
        else:
            print("Eliminación cancelada.")
    else:
        print("Empleado no encontrado.")

def cambiar_departamento_empleado():
    id_empleado = input("Ingrese el ID del empleado: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado:
        nuevo_departamento = input("Ingrese el nuevo departamento: ").strip()
        if empleado.cambiar_departamento(nuevo_departamento):
            print(f"Empleado {empleado.nombre} ha sido cambiado al departamento {nuevo_departamento}.")
        else:
            print("No fue posible cambiar el departamento del empleado.")
    else:
        print("Empleado no encontrado.")