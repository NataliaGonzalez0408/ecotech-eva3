# src/persistencia/registro_tiempo_dao.py

from persistencia.conexion import abrir_conexion, marcador_sql


class RegistroTiempoDAO:

    @staticmethod
    def listar_todos():
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        sql = """
            SELECT 
                rt.id,
                rt.fecha,
                rt.cantidad_horas,
                rt.tareas_realizadas,
                rt.empleado_id,
                e.nombre AS nombre_empleado,
                rt.proyecto_id
            FROM registro_tiempo rt
            INNER JOIN empleado e ON rt.empleado_id = e.id
            ORDER BY rt.fecha DESC
        """
        cursor.execute(sql)
        filas = cursor.fetchall()

        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def listar_por_empleado(empleado_id):
        """Obtiene los registros de un empleado específico anclado a su ID."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()

        sql = f"""
            SELECT 
                rt.id,
                rt.empleado_id,
                e.nombre AS nombre_empleado,
                rt.proyecto_id,
                rt.fecha,
                rt.cantidad_horas,
                rt.tareas_realizadas
            FROM registro_tiempo rt
            INNER JOIN empleado e ON rt.empleado_id = e.id
            WHERE rt.empleado_id = {m}
            ORDER BY rt.fecha DESC
        """
        cursor.execute(sql, (empleado_id,))
        filas = cursor.fetchall()

        cursor.close()
        conexion.close()
        return filas

    @staticmethod
    def insertar(empleado_id, proyecto_id, fecha, horas, descripcion):
        """Inserta un nuevo registro de tiempo anclado al empleado."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()

        sql = f"""
            INSERT INTO registro_tiempo (empleado_id, proyecto_id, fecha, horas_trabajadas, actividad)
            VALUES ({m}, {m}, {m}, {m}, {m})
        """
        cursor.execute(
            sql, (empleado_id, proyecto_id, fecha, horas, descripcion)
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid

        cursor.close()
        conexion.close()
        return nuevo_id