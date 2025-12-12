# utils/bcrypt_helper.py
"""
Módulo de utilidades para hash de contraseñas usando bcrypt.
NUNCA se guardan contraseñas en texto plano por seguridad.
bcrypt es un algoritmo de hash seguro y ampliamente usado.
"""
import bcrypt

def hash_password(plain: str) -> str:
    """
    Genera un hash seguro de una contraseña usando bcrypt.
    Esta función se usa al crear o actualizar clientes.
    IMPORTANTE: Nunca guardar contraseñas en texto plano.
    
    Args:
        plain: Contraseña en texto plano
        
    Returns:
        Contraseña hasheada (string que se guarda en la base de datos)
        
    Raises:
        TypeError: Si plain no es un string
    """
    if not isinstance(plain, str):
        raise TypeError("password debe ser str")
    
    # Generar salt aleatorio y crear hash
    # El salt asegura que el mismo password tenga diferentes hashes
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def check_password(plain: str, hashed: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash.
    Útil para autenticación de usuarios (aunque no se usa en este proyecto).
    
    Args:
        plain: Contraseña en texto plano a verificar
        hashed: Hash almacenado en la base de datos
        
    Returns:
        True si la contraseña coincide, False en caso contrario
    """
    if not (isinstance(plain, str) and isinstance(hashed, str)):
        return False
    
    # bcrypt.checkpw compara el password con el hash de forma segura
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
