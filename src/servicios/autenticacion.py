import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin

MAX_BYTES_BCRYPT = 72

def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")

    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")

def registrar_usuario(empleado_id, nombre, clave, rol):
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")

    hash_guardado = crear_hash(clave)

    usuario = Usuario(
        id=None,
        nombre_usuario=nombre,
        contrasena=hash_guardado,
        empleado_id=empleado_id,
        rol=rol,
    )

    usuario_guardado = UsuarioDAO.insertar(usuario)
    return usuario_guardado.id


def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)

    if cuenta is None:
        print(f"No se encontró la cuenta para el usuario: {nombre}")
        return None

    if not bcrypt.checkpw(datos, cuenta.contrasena.encode("utf-8")):
        return None

    return {
        "id": cuenta.id,
        "empleado_id": cuenta.empleado_id,
        "nombre_usuario": cuenta.nombre_usuario,
        "rol": cuenta.rol,
    }

# servicios/autenticacion.py


def registrar_usuario(sesion_actual, empleado_id, nombre_usuario, clave, rol="empleado"):
    # 1. Verificar permisos de administrador
    exigir_admin(sesion_actual)

    # 2. Validar que el empleado exista en la base de datos
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    if not empleado:
        raise ValueError(f"No existe ningún empleado registrado con el ID {empleado_id}.")

    # 3. Validar que el empleado no tenga ya una cuenta de usuario
    if UsuarioDAO.buscar_por_empleado_id(empleado_id):
        raise ValueError(f"El empleado (ID {empleado_id}) ya posee una cuenta de usuario asignada.")

    # 4. Sanitizar entradas
    nombre_limpio = nombre_usuario.strip()
    if not nombre_limpio:
        raise ValueError("El nombre de usuario no puede estar vacío.")

    # 5. Generar hash de contraseña y registrar
    pass_hash = crear_hash(clave)
    return UsuarioDAO.insertar(empleado_id, nombre_limpio, pass_hash, rol)