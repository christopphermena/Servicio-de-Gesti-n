# crud/carrito_crud.py
from config.database import obtener_conexion

def crear_carrito(id_cliente):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO CARRITO (ID_CLIENTE) VALUES (:id_cliente) RETURNING ID_CARRITO INTO :out_id", {"id_cliente": id_cliente, "out_id": cur.var(int)})
            # NOTE: some oracledb versions require different fetching of returning values; simple approach: inserir y luego consultar
            conn.commit()
            # recuperar último carrito creado para el cliente
            cur.execute("SELECT ID_CARRITO FROM CARRITO WHERE ID_CLIENTE = :id ORDER BY FECHA_CREACION DESC FETCH FIRST 1 ROWS ONLY", {"id": id_cliente})
            row = cur.fetchone()
            return row[0] if row else None
    finally:
        conn.close()

def agregar_item_carrito(id_carrito, codigo_producto, cantidad, subtotal_item):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ITEM_CARRITO (ID_CARRITO, CODIGO_PRODUCTO, CANTIDAD, SUBTOTAL_ITEM)
                VALUES (:id_carrito, :codigo, :cantidad, :subtotal)
            """, {"id_carrito": id_carrito, "codigo": codigo_producto, "cantidad": cantidad, "subtotal": subtotal_item})
        conn.commit()
    finally:
        conn.close()
