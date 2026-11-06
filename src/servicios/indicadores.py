import requests
from servicios.api_dolar import obtener_datos
from servicios.permisos import exigir_sesion
from servicios.deserializador_indicador import DeserializadorIndicador
from persistencia.indicador_dao import IndicadorDAO


def consultar_indicador(sesion):
    exigir_sesion(sesion)

    try:
        datos = obtener_datos()
        dato = DeserializadorIndicador.desde_api(datos)
        
        # Guardar en la BD al consultar (opcional si deseas poblar el historial automáticamente)
        try:
            IndicadorDAO.guardar_indicador(dato)
        except Exception as error_bd:
            print(f"Advertencia: No se pudo guardar en el historial: {error_bd}")

        return dato
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        print("No pudimos consultar el servicio. Reintente.")
        return None


def obtener_historial(sesion):
    exigir_sesion(sesion)

    # Retorna la lista de indicadores desde el DAO
    return IndicadorDAO.obtener_historial()