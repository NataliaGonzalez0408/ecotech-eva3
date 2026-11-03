import requests
from servicios.indicadores import obtener_datos, DeserializadorIndicador, buscar_respaldo, exigir_sesion
from persistencia.indicador_dao import IndicadorDAO

def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        datos = obtener_datos()
        dato = DeserializadorIndicador.desde_api(datos)
    except (requests.exceptions.RequestException,
ValueError, KeyError, TypeError):
        return buscar_respaldo()

    def obtener_historial(sesion):
        exigir_sesion(sesion)
    return IndicadorDAO.listar()