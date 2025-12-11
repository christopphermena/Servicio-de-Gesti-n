# crud/producto_crud.py
from config.database import obtener_conexion

def crear_producto(codigo, nombre, precio_neto, estado="ACTIVO"):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO PRODUCTO (CODIGO, NOMBRE, PRECIO_NETO, ESTADO)
                VALUES (:codigo, :nombre, :precio, :estado)
            """, {"codigo": codigo, "nombre": nombre, "precio": precio_neto, "estado": estado})
        conn.commit()
    finally:
        conn.close()

def obtener_producto(codigo):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT CODIGO, NOMBRE, PRECIO_NETO, ESTADO FROM PRODUCTO WHERE CODIGO = :codigo", {"codigo": codigo})
            return cur.fetchone()
    finally:
        conn.close()

def eliminar_producto(codigo):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM PRODUCTO WHERE CODIGO = :codigo", {"codigo": codigo})
        conn.commit()
    finally:
        conn.close()
