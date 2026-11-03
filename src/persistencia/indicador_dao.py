from persistencia.conexion import abrir_conexion, marcador_sql
import sqlite3
from dominio.indicador import Indicador

class IndicadorDAO:
    def __init__(self):
        pass

    def mostrar_indicador(self):
        conexion = sqlite3.connect("indicadores.db")
        cursor = conexion.cursor()
        marcador = marcador_sql()
        SQL_GUARDAR = f"""
        INSERT INTO indicador_api
        (fuente, codigo, fecha, valor, unidad, verificado_en)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
        valor = excluded.valor,
        unidad = excluded.unidad,
        verificado_en = excluded.verificado_en
        """
        print("----")
        cursor.execute(SQL_GUARDAR, (Indicador.fuente, Indicador.codigo, Indicador.fecha, Indicador.valor, Indicador.unidad, Indicador.verificado_en))
        conexion.commit()