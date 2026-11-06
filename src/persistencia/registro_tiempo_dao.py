from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.registro_tiempo import RegistroTiempo

class RegistroTiempoDAO:

    @staticmethod
    def insertar(registro_tiempo):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"""
            INSERT INTO registro_tiempo (empleado_id, cantidad_horas, fecha, descripcion) 
            VALUES ({marcador}, {marcador}, {marcador}, {marcador})
        """
        cursor.execute(
            sql, 
            (
                registro_tiempo.empleado_id, 
                registro_tiempo.cantidad_horas, 
                registro_tiempo.fecha, 
                registro_tiempo.descripcion
            )
        )
        registro_tiempo.id = cursor.lastrowid
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def listar_todos():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT id, empleado_id, cantidad_horas, fecha, descripcion
            FROM registro_tiempo
            ORDER BY fecha DESC
        """
        cursor.execute(sql)
        registros = []
        for row in cursor.fetchall():
            registros.append(
                RegistroTiempo(
                    id=row[0],
                    empleado_id=row[1],
                    cantidad_horas=row[2],
                    fecha=row[3],
                    descripcion=row[4]
                )
            )
        cursor.close()
        conexion.close()
        return registros

    @staticmethod
    def listar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"""
            SELECT id, empleado_id, cantidad_horas, fecha, descripcion
            FROM registro_tiempo
            WHERE empleado_id = {marcador}
            ORDER BY fecha DESC
        """
        cursor.execute(sql, (empleado_id,))
        registros = []
        for row in cursor.fetchall():
            registros.append(
                RegistroTiempo(
                    id=row[0],
                    empleado_id=row[1],
                    cantidad_horas=row[2],
                    fecha=row[3],
                    descripcion=row[4]
                )
            )
        cursor.close()
        conexion.close()
        return registros