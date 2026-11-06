import math
import requests

def obtener_datos():
    url = "https://cl.dolarapi.com/v1/cotizaciones/usd"
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Lanza un error si la respuesta no es 2xx
    return response.json()  # Devuelve el JSON como diccionario

def extraer_primero(datos, campo="venta"):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener el valor del campo pedido ("compra", "venta" o "ultimoCierre").
    valor = datos.get(campo)

    # Aceptar solo números finitos y mayores que cero.
    # (bool es subclase de int, por eso se compara el tipo exacto)
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError(f"Valor del campo '{campo}' inválido.")

    # Obtener la fecha de actualización.
    fecha = datos.get("fechaActualizacion")
    if not isinstance(fecha, str) or not fecha:
        raise ValueError("Fecha de actualización inválida.")

    # Devolver la fecha y el valor como una tupla.
    return fecha, valor




# try:
# # Consultar la API y obtener los datos.
#     datos = obtener_datos()
# # Extraer y validar la fecha y el valor del primer registro.
#     fecha, valor = extraer_primero(datos)
# # Mostrar el valor con dos decimales y su unidad.
#     print(f"Dólar observado: {valor:.2f} CLP por USD")
# # Mostrar la fecha a la que corresponde el dato.
#     print(f"Fecha del registro: {fecha}")


# except requests.exceptions.RequestException:
# # Controlar fallos de conexión, espera, HTTP o decodificación JSON.
#     print("No pudimos consultar el servicio. Reintente.")
# except (ValueError, KeyError, TypeError):
# # Controlar valores inválidos, claves ausentes o tipos incorrectos.
#     print("La respuesta no contiene un indicador válido.")

