from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO

def menu_departamento():
    print("\n===== ECOTECH - DEPARTAMENTOS =====")
    print("1. Registrar departamento")
    print("2. Listar departamentos")
    print("3. Buscar departamento")
    print("4. Actualizar departamento")
    print("5. Eliminar departamento")
    print("0. Salir")

def ejecutar_menu():
    while True:
        menu_departamento()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_departamento()
        elif opcion == "2":
            listar_departamentos()
        elif opcion == "3":
            buscar_departamento()
        elif opcion == "4":
            actualizar_departamento()
        elif opcion == "5":
            eliminar_departamento()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, intenta nuevamente.")

def registrar_departamento():
    while True:
        nombre = input("Nombre del departamento: ").strip()
        if nombre.replace(" ", "").isalnum(): # Permite letras y números
            break
        print("Error: El nombre del departamento no puede estar vacío ni contener símbolos especiales.")

    while True:
        gerente = input("Nombre del gerente: ").strip()
        if gerente.replace(" ", "").isalpha():
            break
        print("Error: El nombre del gerente solo puede contener letras.")
    
    departamento = Departamento(idDepartamento=None, nombre=nombre, gerente=gerente)
    try:
        DepartamentoDAO.insertar(departamento)
        print("Departamento registrado correctamente.")
    except Exception as e:
        print(f"No fue posible registrar el departamento: {e}")

def listar_departamentos():
    departamentos = DepartamentoDAO.listar()
    if departamentos:
        print("\nLista de departamentos:")
        for dep in departamentos:
            print(f"ID: {dep.idDepartamento}, Nombre: {dep.nombre}, Gerente: {dep.gerente}")
    else:
        print("No hay departamentos registrados.")

def buscar_departamento():
    id_departamento = input("Ingrese el ID del departamento a buscar: ").strip()
    departamento = DepartamentoDAO.buscar_por_id(id_departamento)
    if departamento:
        print(f"ID: {departamento.idDepartamento}, Nombre: {departamento.nombre}, Gerente: {departamento.gerente}")
    else:
        print("Departamento no encontrado.")

def actualizar_departamento():
    id_departamento = input("Ingrese el ID del departamento a actualizar: ").strip()
    departamento = DepartamentoDAO.buscar_por_id(id_departamento)
    if not departamento:
        print("Departamento no encontrado.")
        return

    while True:
        nombre = input(f"Nuevo nombre (actual: {departamento.nombre}): ").strip()
        if not nombre:
            nombre = departamento.nombre
            break
        elif nombre.replace(" ", "").isalnum():
            break
        print("Error: El nombre no puede contener símbolos especiales.")

    while True:
        gerente = input(f"Nuevo gerente (actual: {departamento.gerente}): ").strip()
        if not gerente:
            gerente = departamento.gerente
            break
        elif gerente.replace(" ", "").isalpha():
            break
        print("Error: El nombre del gerente solo puede contener letras.")
        
    departamento.nombre = nombre
    departamento.gerente = gerente
    try:
        DepartamentoDAO.actualizar(departamento)
        print("Departamento actualizado correctamente.")
    except Exception as e:
        print(f"No fue posible actualizar el departamento: {e}")

def eliminar_departamento():
    id_departamento = input("Ingrese el ID del departamento a eliminar: ").strip()
    departamento = DepartamentoDAO.buscar_por_id(id_departamento)
    if departamento:
        confirmacion = input(f"¿Seguro que desea eliminar el departamento '{departamento.nombre}'? (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                DepartamentoDAO.eliminar(id_departamento)
                print("Departamento eliminado correctamente.")
            except Exception as e:
                print(f"No fue posible eliminar el departamento: {e}")
        else:
            print("Eliminación cancelada.")
    else:
        print("Departamento no encontrado.")