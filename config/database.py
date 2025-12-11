# config/database.py
import os
from dotenv import load_dotenv
import oracledb

load_dotenv()

def obtener_conexion():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    if not (user and password and dsn):
        raise RuntimeError("Faltan variables de entorno DB_USER/DB_PASSWORD/DB_DSN")

    # Ajusta parámetros si necesitas wallet/puerto
    conexion = oracledb.connect(user=user, password=password, dsn=dsn)
    return conexion

def probar_conexion() -> bool:
    try:
        conn = obtener_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM dual")
                r = cur.fetchone()
                return bool(r and r[0] == 1)
        finally:
            conn.close()
    except Exception:
        return False
