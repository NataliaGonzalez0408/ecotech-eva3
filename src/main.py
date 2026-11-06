import sys
from persistencia.crear_bd import crear_tablas
from persistencia.semilla_bd import sembrar_datos
from menus.menu_usuario import solicitar_login, menu_privado

def inicializar_aplicacion():
    try:
        crear_tablas()
        sembrar_datos()
    except Exception as e:
        print(f"Error al inicializar la aplicación: {e}")
        sys.exit(1)

def main():
    inicializar_aplicacion()
    print("Bienvenido a la aplicación de gestión de empleados, querido usuario.")

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
        print("Sesión cerrada. Por favor, inicie sesión nuevamente.")

if __name__ == "__main__":
    main()