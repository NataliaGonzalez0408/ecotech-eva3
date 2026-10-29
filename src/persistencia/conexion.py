import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()

def abrir_conexion():
    motor = obtener_motor()

    if motor == "sqlite":
        return sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))

    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            )
    raise ValueError(f"Motor no soportado: {motor}")

def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"


conexion = None
try:
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    # ejecutar operación

    conexion.commit()

except Exception:
    if conexion:
        conexion.rollback()
    raise

finally:
    if conexion:
        conexion.close()