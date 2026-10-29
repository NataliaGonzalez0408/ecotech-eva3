# En un archivo Python de prueba:
import requests
import math

def obtener_datos():
    respuesta = requests.get(
        "https://mindicador.cl/api/dolar",
        timeout=(3, 5),
    )
    respuesta.raise_for_status()
    return respuesta.json()

def extraer_primero(datos):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener la lista de registros del indicador.
    serie = datos.get("serie")

    # Comprobar que sea una lista y contenga registros.
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles.")

    # seleccionar el primer registro y obtener su valor.
    registro = serie[0]
    valor = registro["valor"]

    # Aceptar solo números finitos y mayores que cero.
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del indicador inválido.")

    # Devolver la fecha y el valor como una tupla.
    return registro["fecha"], valor

try:
    # Consultar la API y obtener los datos.
    datos = obtener_datos()

    # Extraer y validar la fecha y el valor del primer registro.
    fecha, valor = extraer_primero(datos)

    # Mostrar el valor con dos decimales y su unidad.
    print(f"Dólar observado: {valor:.2f} CLP por USD")

    # Mostrar la fecha a la que corresponde el dato.
    print(f"Fecha del registro: {fecha}")

except requests.exceptions.RequestException:
    # Controlar fallos de conexión, espera, HTTP o decodificación JSON.
    print("No pudimos consultar el servicio. Reintente.")

except (ValueError, KeyError, TypeError):
    # Controlar valores inválidos, claves ausentes o tipos incorrectos.
    print("La respuesta no contiene un indicador válido.")
