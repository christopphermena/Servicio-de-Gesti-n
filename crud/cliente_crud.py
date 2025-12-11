# crud/cliente_crud.py
from config.database import obtener_conexion

def crear_cliente(rut, nombre, email, contrasena_hash, nivel="General"):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO CLIENTE (RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL)
                VALUES (:rut, :nombre, :email, :hash, :nivel)
            """, {"rut": rut, "nombre": nombre, "email": email, "hash": contrasena_hash, "nivel": nivel})
        conn.commit()
    finally:
        conn.close()

def obtener_cliente_por_rut(rut):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ID_CLIENTE, RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL FROM CLIENTE WHERE RUT = :rut", {"rut": rut})
            row = cur.fetchone()
            return row
    finally:
        conn.close()

def eliminar_cliente_por_rut(rut):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM CLIENTE WHERE RUT = :rut", {"rut": rut})
        conn.commit()
    finally:
        conn.close()
