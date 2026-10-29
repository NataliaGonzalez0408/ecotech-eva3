from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.proyecto import Proyecto

class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"""
            INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
            VALUES ({marcador}, {marcador}, {marcador})
        """
        cursor.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
        proyecto.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return proyecto

    @staticmethod
    def listar_proyectos():
        conn = abrir_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyecto")
        proyectos = cursor.fetchall()
        conn.close()
        return proyectos

    @staticmethod
    def buscar_por_id(id_proyecto):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"SELECT id, nombre, descripcion, fecha_inicio FROM proyecto WHERE id = {marcador}",
            (id_proyecto,)
        )
        proyecto = cursor.fetchone()
        conn.close()
        return proyecto

    @staticmethod
    def actualizar_proyecto(id_proyecto, nombre, descripcion, fecha_inicio):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"UPDATE proyecto SET nombre = {marcador}, descripcion = {marcador}, fecha_inicio = {marcador} WHERE id = {marcador}",
            (nombre, descripcion, fecha_inicio, id_proyecto)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar_proyecto(id_proyecto):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(f"DELETE FROM proyecto WHERE id = {marcador}", (id_proyecto,))
        conn.commit()
        conn.close()