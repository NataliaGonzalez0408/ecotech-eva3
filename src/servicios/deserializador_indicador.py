# src/servicios/deserializador_indicador.py
from dominio.indicador import Indicador
from servicios.api_dolar import extraer_primero

class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        # Reutiliza la función que extrae y valida los datos.
        fecha, valor = extraer_primero(datos)
        # Construye y devuelve un objeto de nuestro proyecto.
        return Indicador(fecha=fecha, valor=valor)
