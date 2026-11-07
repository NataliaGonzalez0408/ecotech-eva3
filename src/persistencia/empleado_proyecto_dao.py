# persistencia/empleado_proyecto_dao.py
from persistencia.conexion import abrir_conexion, marcador_sql

class EmpleadoProyectoDAO:

    @staticmethod
    def asignar_empleado_a_proyecto(
        empleado_id, proyecto_id, rol_en_proyecto=""
    ):
        """Asigna un empleado a un proyecto especifico."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            INSERT INTO empleado_proyecto (empleado_id, proyecto_id, rol_en_proyecto)
            VALUES ({marcador}, {marcador}, {marcador})
        """
        try:
            cursor.execute(sql, (empleado_id, proyecto_id, rol_en_proyecto))
            conexion.commit()
            exito = True
        except Exception:
            exito = False
        finally:
            cursor.close()
            conexion.close()
        return exito

    @staticmethod
    def desvincular_empleado_de_proyecto(empleado_id, proyecto_id):
        """Elimina la relacion entre un empleado y un proyecto."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            DELETE FROM empleado_proyecto 
            WHERE empleado_id = {marcador} AND proyecto_id = {marcador}
        """
        cursor.execute(sql, (empleado_id, proyecto_id))
        eliminado = cursor.rowcount > 0
        conexion.commit()
        cursor.close()
        conexion.close()
        return eliminado

    @staticmethod
    def obtener_proyectos_de_empleado(empleado_id):
        """Obtiene la lista de proyectos asignados a un empleado."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            SELECT p.id, p.nombre, p.descripcion, p.fecha_inicio, ep.rol_en_proyecto, ep.fecha_asignacion
            FROM proyecto p
            INNER JOIN empleado_proyecto ep ON p.id = ep.proyecto_id
            WHERE ep.empleado_id = {marcador}
            ORDER BY p.id ASC
        """
        cursor.execute(sql, (empleado_id,))
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def obtener_empleados_de_proyecto(proyecto_id):
        """Obtiene la lista de empleados asignados a un proyecto especifico."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
            SELECT e.id, e.nombre, e.correo, ep.rol_en_proyecto, ep.fecha_asignacion
            FROM empleado e
            INNER JOIN empleado_proyecto ep ON e.id = ep.empleado_id
            WHERE ep.proyecto_id = {marcador}
            ORDER BY e.id ASC
        """
        cursor.execute(sql, (proyecto_id,))
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas