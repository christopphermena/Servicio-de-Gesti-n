# crud/carrito_crud.py
"""
Módulo CRUD para la entidad Carrito.
Operaciones de base de datos para gestionar carritos de compra e ítems.
"""
from config.database import obtener_conexion

def crear_carrito(id_cliente):
    """
    CREATE: Crea un nuevo carrito de compras para un cliente.
    
    Args:
        id_cliente: ID del cliente dueño del carrito
        
    Returns:
        ID del carrito creado, o None si hay error
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            # Insertar el carrito en la base de datos
            cur.execute("INSERT INTO CARRITO (ID_CLIENTE) VALUES (:id_cliente) RETURNING ID_CARRITO INTO :out_id", {"id_cliente": id_cliente, "out_id": cur.var(int)})
            # Nota: algunas versiones de oracledb requieren diferentes formas de obtener el ID
            # Usamos el enfoque simple: insertar y luego consultar
            conn.commit()
            
            # Recuperar el ID del último carrito creado para este cliente
            # Ordenamos por fecha de creación descendente y tomamos el primero
            cur.execute("SELECT ID_CARRITO FROM CARRITO WHERE ID_CLIENTE = :id ORDER BY FECHA_CREACION DESC FETCH FIRST 1 ROWS ONLY", {"id": id_cliente})
            row = cur.fetchone()
            return row[0] if row else None
    finally:
        conn.close()

def agregar_item_carrito(id_carrito, codigo_producto, cantidad, subtotal_item):
    """
    CREATE: Agrega un ítem (producto con cantidad) a un carrito existente.
    
    Args:
        id_carrito: ID del carrito al que se agrega el ítem
        codigo_producto: Código del producto a agregar
        cantidad: Cantidad de unidades
        subtotal_item: Subtotal del ítem (precio con IVA × cantidad)
    """
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
