from persistencia.conexion import abrir_conexion, obtener_motor, marcador_sql
from dominio.empleado import Empleado

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()
        sql = f"""
            INSERT INTO empleado (nombre, correo, telefono, fecha_inicio_contrato, salario)
            VALUES ({marcador}, {marcador}, {marcador}, {marcador}, {marcador})
        """
        print("----")
        cursor.execute(sql, (empleado.nombre, empleado.correo, empleado.telefono, empleado.fecha_inicio_contrato, empleado.salario))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()
        sql = f"""
                SELECT id, nombre, correo, telefono, fecha_inicio_contrato, salario
                FROM empleado WHERE id = {marca}
            """
        cursor.execute(sql, (id_empleado,))
        fila = cursor.fetchone()
        conexion.close()
        if fila is None:
            return None
        return Empleado(id=fila[0], nombre=fila[1], correo=fila[2], telefono=fila[3], fecha_inicio_contrato=fila[4], salario=fila[5])

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre, correo, telefono, fecha_inicio_contrato, salario FROM empleado"
        )
        filas = cursor.fetchall()
        conexion.close()
        empleados = []
        for fila in filas:
            empleados.append(
                Empleado(
                    id=fila[0], nombre=fila[1], correo=fila[2], 
                    telefono=fila[3], fecha_inicio_contrato=fila[4], salario=fila[5]
                )
            )
        return empleados

    @staticmethod
    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "UPDATE empleado "
                f"SET nombre = {marca}, correo = {marca}, telefono = {marca}, fecha_inicio_contrato = {marca}, salario = {marca} "
                f"WHERE id = {marca}"
            )
            cursor.execute(
                sql,
                (empleado.nombre, empleado.correo, empleado.telefono, empleado.fecha_inicio_contrato, empleado.salario, empleado.id)
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
    def eliminar(id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()
        sql = (
            "DELETE FROM empleado "
            f"WHERE id = {marca}"
        )
        cursor.execute(sql, (id_empleado,))
        conexion.commit()
        eliminado = cursor.rowcount > 0
        conexion.close()
        return eliminado