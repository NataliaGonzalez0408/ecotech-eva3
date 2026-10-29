# main.py
from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from servicios.autenticacion import registrar_usuario
from menus.menu_usuario import solicitar_login, menu_privado

crear_tablas()



# emp=Empleado(nombre="admin", correo="admin@admin.com", telefono="" , fecha_inicio_contrato="" , salario="" )
# EmpleadoDAO.insertar(emp)

# user=registrar_usuario(emp.id, "admin","admin12332")

# print(emp.mostrar_datos())
# print(user)


def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")


if __name__ == "__main__":
    main()