from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, marcador_sql

class UsuarioDAO:

    @staticmethod
    def insertar(usuario):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = f"""
            INSERT INTO usuario
            (nombre_usuario, contrasena,empleado_id)
            VALUES ({marca}, {marca}, {marca})
        """

        cursor.execute(
            sql,
            (
                usuario.nombre_usuario,
                usuario.contrasena,
                usuario.empleado_id
            )
        )

        usuario.id = cursor.lastrowid
        conexion.commit()
        conexion.close()

        return usuario

    @staticmethod
    def fila_a_usuario(fila):
        if fila is None:
            return None

        return Usuario(
            id=fila[0],
            nombre_usuario=fila[1],
            contrasena=fila[2],
            empleado_id=fila[3]
        )

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = f"""
            SELECT id, nombre_usuario, contrasena, rol, empleado_id
            FROM usuario
            WHERE id = {marca}
        """

        cursor.execute(sql, (id_usuario,))
        fila = cursor.fetchone()

        conexion.close()

        return UsuarioDAO.fila_a_usuario(fila)

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = f"""
            SELECT id, nombre_usuario, contrasena, empleado_id
            FROM usuario
            WHERE nombre_usuario = {marca}
        """

        cursor.execute(sql, (nombre_usuario,))
        fila = cursor.fetchone()

        conexion.close()

        return UsuarioDAO.fila_a_usuario(fila)

    @staticmethod
    def listar(filtrar_por_empleado_id=None):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        if filtrar_por_empleado_id is None:
            sql = """
                SELECT id, nombre_usuario, contrasena,  empleado_id
                FROM usuario
            """
            cursor.execute(sql)
        else:
            sql = f"""
                SELECT id, nombre_usuario, contrasena, empleado_id
                FROM usuario
                WHERE empleado_id = {marca}
            """
            cursor.execute(sql, (filtrar_por_empleado_id,))

        filas = cursor.fetchall()
        conexion.close()

        usuarios = []

        for fila in filas:
            usuarios.append(
                UsuarioDAO.fila_a_usuario(fila)
            )

        return usuarios

    @staticmethod
    def actualizar(usuario):
        conexion = None

        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()

            sql = (
                "UPDATE usuario "
                f"SET nombre_usuario = {marca}, "
                f"contrasena = {marca}, "
                f"empleado_id = {marca} "
                f"WHERE id = {marca}"
            )

            cursor.execute(
                sql,
                (
                    usuario.nombre_usuario,
                    usuario.contrasena,
                    usuario.empleado_id,
                    usuario.id
                )
            )

            conexion.commit()

            return cursor.rowcount > 0

        except Exception:
            if conexion:
                conexion.rollback()
            raise

        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_usuario):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()

        sql = (
            "DELETE FROM usuario "
            f"WHERE id = {marca}"
        )

        cursor.execute(sql, (id_usuario,))

        conexion.commit()

        eliminado = cursor.rowcount > 0

        conexion.close()

        return eliminado