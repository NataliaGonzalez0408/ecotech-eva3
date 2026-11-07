# persistencia/proyecto_dao.py
from dominio.proyecto import Proyecto
from persistencia.conexion import abrir_conexion, marcador_sql


class ProyectoDAO:

    @staticmethod
    def crear_tabla():
        """Asegura la existencia de la tabla proyecto."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT
        );
        """
        cursor.execute(sql)
        conexion.commit()
        conexion.close()

    @staticmethod
    def _fila_a_proyecto(fila):
        """Helper interno para convertir tuplas SQL a instancias de Proyecto."""
        if fila is None:
            return None
        return Proyecto(
            id=fila[0],
            nombre=fila[1],
            descripcion=fila[2],
            fecha_inicio=fila[3],
        )

    @staticmethod
    def insertar(proyecto):
        ProyectoDAO.crear_tabla()
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
            VALUES ({marcador}, {marcador}, {marcador})
        """
        cursor.execute(
            sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio)
        )
        proyecto.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return proyecto

    @staticmethod
    def listar_proyectos():
        ProyectoDAO.crear_tabla()
        conn = abrir_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, descripcion, fecha_inicio FROM proyecto ORDER"
            " BY id ASC"
        )
        filas = cursor.fetchall()
        conn.close()

        return [ProyectoDAO._fila_a_proyecto(fila) for fila in filas]

    @staticmethod
    def buscar_por_id(id_proyecto):
        ProyectoDAO.crear_tabla()
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            "SELECT id, nombre, descripcion, fecha_inicio FROM proyecto WHERE"
            f" id = {marcador}",
            (id_proyecto,),
        )
        fila = cursor.fetchone()
        conn.close()
        return ProyectoDAO._fila_a_proyecto(fila)

    @staticmethod
    def actualizar_proyecto(id_proyecto, nombre, descripcion, fecha_inicio):
        ProyectoDAO.crear_tabla()
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"UPDATE proyecto SET nombre = {marcador}, descripcion ="
            f" {marcador}, fecha_inicio = {marcador} WHERE id = {marcador}",
            (nombre, descripcion, fecha_inicio, id_proyecto),
        )
        actualizado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return actualizado

    @staticmethod
    def eliminar_proyecto(id_proyecto):
        ProyectoDAO.crear_tabla()
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"DELETE FROM proyecto WHERE id = {marcador}", (id_proyecto,)
        )
        eliminado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return eliminado