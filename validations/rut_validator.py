# validations/rut_validator.py
"""
Módulo de validación y formato de RUT chileno.
Implementa el algoritmo de validación del dígito verificador del RUT.
"""
import re

# Expresión regular para validar formato de RUT: 12.345.678-9 o 12345678-9
_RUT_RE = re.compile(r"^(\d{1,2}\.?\d{3}\.?\d{3})-?([\dkK])$")

def clean_rut(rut: str) -> str:
    """
    Limpia un RUT eliminando puntos y guiones, dejando solo números y el dígito verificador.
    
    Args:
        rut: RUT a limpiar
        
    Returns:
        RUT sin puntos ni guiones (ej: "123456789")
    """
    if not isinstance(rut, str):
        raise TypeError("rut debe ser str")
    # Eliminar todo excepto números, 'k' y 'K'
    return re.sub(r"[^\dkK]", "", rut)

def calcular_dv(rut_numbers: str) -> str:
    """
    Calcula el dígito verificador de un RUT usando el algoritmo chileno.
    Algoritmo: multiplicar dígitos por factores 2,3,4,5,6,7 (cíclicamente),
    sumar resultados, calcular 11 - (suma % 11).
    
    Args:
        rut_numbers: Solo los números del RUT (sin dígito verificador)
        
    Returns:
        Dígito verificador calculado ("0"-"9" o "K")
    """
    # Revertir los dígitos y convertirlos a enteros
    reversed_digits = map(int, reversed(rut_numbers))
    factors = [2,3,4,5,6,7]  # Factores del algoritmo chileno
    total = 0
    factor_index = 0
    
    # Multiplicar cada dígito por su factor correspondiente
    for d in reversed_digits:
        total += d * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)  # Ciclar los factores
    
    # Calcular dígito verificador
    dv = 11 - (total % 11)
    
    # Casos especiales
    if dv == 11:
        return "0"
    if dv == 10:
        return "K"
    return str(dv)

def is_valid_rut(rut: str) -> bool:
    """
    Valida si un RUT es válido verificando su formato y dígito verificador.
    
    Args:
        rut: RUT a validar (ej: "12.345.678-9")
        
    Returns:
        True si el RUT es válido, False en caso contrario
    """
    if not isinstance(rut, str):
        return False
    
    # Verificar formato con expresión regular
    m = _RUT_RE.match(rut)
    if not m:
        return False
    
    # Extraer números y dígito verificador
    numbers, dv = m.group(1), m.group(2)
    
    # Limpiar puntos de los números
    numbers_clean = re.sub(r"\.", "", numbers)
    
    # Calcular dígito verificador esperado
    calc = calcular_dv(numbers_clean)
    
    # Comparar con el dígito verificador proporcionado
    return calc.upper() == dv.upper()

def format_rut(rut: str) -> str:
    """
    Formatea un RUT válido al formato estándar: 12.345.678-9
    
    Args:
        rut: RUT válido a formatear
        
    Returns:
        RUT formateado con puntos y guión
        
    Raises:
        ValueError: Si el RUT no es válido
    """
    if not is_valid_rut(rut):
        raise ValueError("RUT inválido")
    
    # Extraer solo números
    numbers = re.sub(r"[^\d]", "", rut)
    # Extraer dígito verificador
    dv = rut[-1].upper()
    
    # Formatear con puntos cada 3 dígitos desde la derecha
    # formato: 12.345.678-9
    parts = []
    while numbers:
        parts.insert(0, numbers[-3:])  # Tomar últimos 3 dígitos
        numbers = numbers[:-3]  # Eliminar últimos 3 dígitos
    
    return ".".join(parts) + "-" + dv
