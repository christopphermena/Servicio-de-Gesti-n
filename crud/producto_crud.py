# crud/producto_crud.py
"""
Módulo CRUD para la entidad Producto.
Operaciones de base de datos para gestionar productos del kiosko.
"""
from config.database import obtener_conexion

def crear_producto(codigo, nombre, precio_neto, estado="ACTIVO"):
    """
    CREATE: Crea un nuevo producto en la base de datos.
    
    Args:
        codigo: Código único del producto (clave primaria)
        nombre: Nombre del producto
        precio_neto: Precio sin IVA
        estado: Estado del producto ("ACTIVO" o "INACTIVO")
    """
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
    """
    READ: Obtiene un producto de la base de datos por su código.
    
    Args:
        codigo: Código del producto a buscar
        
    Returns:
        Tupla con los datos: (CODIGO, NOMBRE, PRECIO_NETO, ESTADO)
        None si no se encuentra
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT CODIGO, NOMBRE, PRECIO_NETO, ESTADO FROM PRODUCTO WHERE CODIGO = :codigo", {"codigo": codigo})
            return cur.fetchone()
    finally:
        conn.close()

def eliminar_producto(codigo):
    """
    DELETE: Elimina un producto de la base de datos por su código.
    
    Args:
        codigo: Código del producto a eliminar
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM PRODUCTO WHERE CODIGO = :codigo", {"codigo": codigo})
        conn.commit()
    finally:
        conn.close()

def actualizar_producto(codigo, nombre=None, precio_neto=None, estado=None):
    """
    UPDATE: Actualiza los datos de un producto existente.
    Solo actualiza los campos proporcionados (no None).
    
    Args:
        codigo: Código del producto a actualizar
        nombre: Nuevo nombre (opcional)
        precio_neto: Nuevo precio neto (opcional)
        estado: Nuevo estado (opcional)
    """
    conn = obtener_conexion()
    try:
        sets = []
        params = {"codigo": codigo}
        if nombre is not None:
            sets.append("NOMBRE = :nombre")
            params["nombre"] = nombre
        if precio_neto is not None:
            sets.append("PRECIO_NETO = :precio")
            params["precio"] = precio_neto
        if estado is not None:
            sets.append("ESTADO = :estado")
            params["estado"] = estado
        if not sets:
            return
        sql = f"UPDATE PRODUCTO SET {', '.join(sets)} WHERE CODIGO = :codigo"
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()