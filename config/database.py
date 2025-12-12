# config/database.py
"""
Módulo de configuración de base de datos.
Maneja la conexión a Oracle XE usando variables de entorno desde archivo .env.
Ejemplo de DEPENDENCIA: los módulos CRUD dependen de este módulo.
"""
import os
from dotenv import load_dotenv
import oracledb

# Cargar variables de entorno al importar el módulo
load_dotenv()

def obtener_conexion():
    """
    Obtiene una conexión a la base de datos Oracle XE.
    Lee las credenciales desde variables de entorno (.env):
    - DB_USER: Usuario de Oracle
    - DB_PASSWORD: Contraseña
    - DB_DSN: Data Source Name (ej: "localhost/XEPDB1")
    
    Returns:
        Objeto de conexión a Oracle XE
        
    Raises:
        RuntimeError: Si faltan variables de entorno
    """
    # Leer credenciales desde variables de entorno (archivo .env)
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    # Validar que todas las variables estén definidas
    if not (user and password and dsn):
        raise RuntimeError("Faltan variables de entorno DB_USER/DB_PASSWORD/DB_DSN")

    # Crear conexión a Oracle XE usando la librería oracledb
    conexion = oracledb.connect(user=user, password=password, dsn=dsn)
    return conexion

def probar_conexion() -> bool:
    """
    Prueba si es posible conectarse a la base de datos Oracle XE.
    Ejecuta una consulta simple (SELECT 1 FROM dual) para verificar la conexión.
    
    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    try:
        conn = obtener_conexion()
        try:
            # Ejecutar consulta simple para verificar que la conexión funciona
            # "dual" es una tabla especial de Oracle que siempre existe
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM dual")
                r = cur.fetchone()
                # Si obtuvimos resultado, la conexión funciona
                return bool(r and r[0] == 1)
        finally:
            conn.close()  # Cerrar conexión siempre, incluso si hay error
    except Exception:
        # Si hay cualquier error, retornar False (sin conexión)
        return False
