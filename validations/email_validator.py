# validations/email_validator.py
"""
Módulo de validación de correos electrónicos.
Usa la librería validate_email_address para validar el formato de emails.
"""
from validate_email_address import validate_email

def is_valid_email(email: str) -> bool:
    """
    Valida el formato de un correo electrónico usando la librería validate_email_address.
    Esta función se usa antes de guardar clientes para asegurar que el email sea válido.
    
    Args:
        email: String con el correo a validar
        
    Returns:
        True si el correo es válido, False en caso contrario
    """
    # Validar que sea un string
    if not isinstance(email, str):
        return False
    
    # Eliminar espacios al inicio y final
    email = email.strip()
    
    # Validar que no esté vacío
    if not email:
        return False
    
    # Usar la librería para validar el formato del email
    try:
        return validate_email(email)
    except Exception:
        # Si hay error en la validación, retornar False
        return False



