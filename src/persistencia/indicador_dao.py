# persistencia/indicador_dao.py
import sqlite3
from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion, marcador_sql


class IndicadorDAO:

    @staticmethod
    def crear_tabla():
        """Crea la tabla indicador_api si aún no existe."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS indicador_api (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL,
            codigo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL,
            unidad TEXT NOT NULL,
            verificado_en TEXT,
            UNIQUE (fuente, codigo, fecha)
        );
        """
        cursor.execute(sql)
        conexion.commit()
        conexion.close()

    @staticmethod
    def guardar_indicador(indicador: Indicador):
        # Garantiza que la tabla exista antes de insertar
        IndicadorDAO.crear_tabla()

        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql_guardar = f"""
        INSERT INTO indicador_api
        (fuente, codigo, fecha, valor, unidad, verificado_en)
        VALUES ({marcador}, {marcador}, {marcador}, {marcador}, {marcador}, {marcador})
        ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
        valor = excluded.valor,
        unidad = excluded.unidad,
        verificado_en = excluded.verificado_en
        """

        cursor.execute(
            sql_guardar,
            (
                indicador.fuente,
                indicador.codigo,
                indicador.fecha,
                indicador.valor,
                indicador.unidad,
                indicador.verificado_en,
            ),
        )

        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_historial(limite=10):
        # Garantiza que la tabla exista antes de consultar
        IndicadorDAO.crear_tabla()

        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = marcador_sql()

        sql = f"""
        SELECT fecha, valor, verificado_en, fuente
        FROM indicador_api
        ORDER BY id DESC
        LIMIT {marcador}
        """

        cursor.execute(sql, (limite,))
        filas = cursor.fetchall()
        conexion.close()

        historial = []
        for fila in filas:
            ind = Indicador(
                fecha=fila[0],
                valor=fila[1],
                verificado_en=fila[2],
                fuente=fila[3],
            )
            historial.append(ind)

        return historial
    
    @staticmethod
    def guardar_consulta(fecha_indicador, valor, verificado_en, fuente):
        """Guarda una consulta de indicador económico en el historial de la BD."""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        m = marcador_sql()

        sql = f"""
            INSERT INTO historial_indicador (fecha, valor, verificado_en, fuente)
            VALUES ({m}, {m}, {m}, {m})
        """
        cursor.execute(sql, (fecha_indicador, valor, verificado_en, fuente))
        conexion.commit()

        cursor.close()
        conexion.close()