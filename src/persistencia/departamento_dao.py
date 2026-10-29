from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.departamento import Departamento

class DepartamentoDAO:
    @staticmethod
    def insertar(departamento: Departamento):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"INSERT INTO departamento (nombre, gerente) VALUES ({marcador}, {marcador})",
            (departamento.nombre, departamento.gerente)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def listar():
        conn = abrir_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, gerente FROM departamento")
        rows = cursor.fetchall()
        conn.close()
        return [Departamento(idDepartamento=row[0], nombre=row[1], gerente=row[2]) for row in rows]

    @staticmethod
    def buscar_por_id(id_departamento):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"SELECT id, nombre, gerente FROM departamento WHERE id = {marcador}",
            (id_departamento,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return Departamento(idDepartamento=row[0], nombre=row[1], gerente=row[2])
        return None

    @staticmethod
    def actualizar(departamento: Departamento):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(
            f"UPDATE departamento SET nombre = {marcador}, gerente = {marcador} WHERE id = {marcador}",
            (departamento.nombre, departamento.gerente, departamento.idDepartamento)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id_departamento):
        conn = abrir_conexion()
        cursor = conn.cursor()
        marcador = marcador_sql()
        cursor.execute(f"DELETE FROM departamento WHERE id = {marcador}", (id_departamento,))
        conn.commit()
        conn.close()