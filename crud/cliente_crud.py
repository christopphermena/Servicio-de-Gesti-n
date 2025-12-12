# crud/cliente_crud.py
"""
Módulo CRUD (Create, Read, Update, Delete) para la entidad Cliente.
Contiene todas las operaciones de base de datos relacionadas con clientes.
Ejemplo de DEPENDENCIA: este módulo depende de config.database para obtener conexiones.
"""
from config.database import obtener_conexion

def crear_cliente(rut, nombre, email, contrasena_hash, nivel="General"):
    """
    CREATE: Crea un nuevo cliente en la base de datos.
    
    Args:
        rut: RUT del cliente (clave única)
        nombre: Nombre completo
        email: Correo electrónico
        contrasena_hash: Contraseña hasheada con bcrypt (nunca texto plano)
        nivel: Nivel del cliente ("General" o "Estudiante")
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            # INSERT usando parámetros nombrados (:rut, :nombre, etc.) para evitar SQL injection
            cur.execute("""
                INSERT INTO CLIENTE (RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL)
                VALUES (:rut, :nombre, :email, :hash, :nivel)
            """, {"rut": rut, "nombre": nombre, "email": email, "hash": contrasena_hash, "nivel": nivel})
        conn.commit()  # Confirmar la transacción
    finally:
        conn.close()  # Cerrar conexión siempre

def obtener_cliente_por_rut(rut):
    """
    READ: Obtiene un cliente de la base de datos por su RUT.
    
    Args:
        rut: RUT del cliente a buscar
        
    Returns:
        Tupla con los datos del cliente: (ID_CLIENTE, RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL)
        None si no se encuentra
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ID_CLIENTE, RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL FROM CLIENTE WHERE RUT = :rut", {"rut": rut})
            row = cur.fetchone()  # Obtener una sola fila
            return row
    finally:
        conn.close()

def eliminar_cliente_por_rut(rut):
    """
    DELETE: Elimina un cliente de la base de datos por su RUT.
    
    Args:
        rut: RUT del cliente a eliminar
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM CLIENTE WHERE RUT = :rut", {"rut": rut})
        conn.commit()  # Confirmar la eliminación
    finally:
        conn.close()

def actualizar_cliente(rut, nombre=None, email=None, contrasena_hash=None, nivel=None):
    """
    UPDATE: Actualiza los datos de un cliente existente.
    Solo actualiza los campos que se proporcionen (no None).
    Permite actualizar campos individuales sin afectar los demás.
    
    Args:
        rut: RUT del cliente a actualizar (usado para identificar)
        nombre: Nuevo nombre (opcional)
        email: Nuevo email (opcional)
        contrasena_hash: Nueva contraseña hasheada (opcional)
        nivel: Nuevo nivel (opcional)
    """
    conn = obtener_conexion()
    try:
        # Construir dinámicamente la consulta UPDATE solo con los campos a actualizar
        sets = []  # Lista de campos a actualizar
        params = {"rut": rut}  # Parámetros de la consulta
        
        # Agregar solo los campos que no sean None
        if nombre is not None:
            sets.append("NOMBRE = :nombre")
            params["nombre"] = nombre
        if email is not None:
            sets.append("EMAIL = :email")
            params["email"] = email
        if contrasena_hash is not None:
            sets.append("CONTRASENA_HASH = :hash")
            params["hash"] = contrasena_hash
        if nivel is not None:
            sets.append("NIVEL = :nivel")
            params["nivel"] = nivel
        
        # Si no hay campos para actualizar, salir
        if not sets:
            return
        
        # Construir y ejecutar la consulta UPDATE dinámica
        sql = f"UPDATE CLIENTE SET {', '.join(sets)} WHERE RUT = :rut"
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()