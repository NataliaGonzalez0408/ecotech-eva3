from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.registro_tiempo import RegistroTiempo

class RegistroTiempoDAO:
    @staticmethod
    def insertar(registro_tiempo):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"INSERT INTO registro_tiempo (fecha, cantidad_horas, tareas_realizadas, descripcion) VALUES ({marcador}, {marcador}, {marcador}, {marcador})"
        cursor.execute(sql, (registro_tiempo.fecha, registro_tiempo.cantidad_horas, registro_tiempo.tareas_realizadas, registro_tiempo.descripcion))
        registro_tiempo.id = cursor.lastrowid
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = "SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion FROM registro_tiempo"
        cursor.execute(sql)
        registros = []
        for row in cursor.fetchall():
            registros.append(RegistroTiempo(id=row[0], fecha=row[1], cantidad_horas=row[2], tareas_realizadas=row[3], descripcion=row[4]))
        cursor.close()
        conexion.close()
        return registros

    @staticmethod
    def buscar_por_id(id_registro):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion FROM registro_tiempo WHERE id = {marcador}"
        cursor.execute(sql, (id_registro,))
        row = cursor.fetchone()
        cursor.close()
        conexion.close()
        if row:
            return RegistroTiempo(id=row[0], fecha=row[1], cantidad_horas=row[2], tareas_realizadas=row[3], descripcion=row[4])
        return None

    @staticmethod
    def actualizar(registro_tiempo):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"UPDATE registro_tiempo SET fecha = {marcador}, cantidad_horas = {marcador}a, tareas_realizadas = {marcador}, descripcion = {marcador} WHERE id = {marcador}"
        cursor.execute(sql, (registro_tiempo.fecha, registro_tiempo.cantidad_horas, registro_tiempo.tareas_realizadas, registro_tiempo.descripcion, registro_tiempo.id))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id_registro):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"DELETE FROM registro_tiempo WHERE id = {marcador}"
        cursor.execute(sql, (id_registro,))
        conexion.commit()
        cursor.close()
        conexion.close()