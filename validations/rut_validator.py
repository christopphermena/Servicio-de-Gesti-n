# validations/rut_validator.py
import re

_RUT_RE = re.compile(r"^(\d{1,2}\.?\d{3}\.?\d{3})-?([\dkK])$")

def clean_rut(rut: str) -> str:
    if not isinstance(rut, str):
        raise TypeError("rut debe ser str")
    return re.sub(r"[^\dkK]", "", rut)

def calcular_dv(rut_numbers: str) -> str:
    reversed_digits = map(int, reversed(rut_numbers))
    factors = [2,3,4,5,6,7]
    total = 0
    factor_index = 0
    for d in reversed_digits:
        total += d * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)
    dv = 11 - (total % 11)
    if dv == 11:
        return "0"
    if dv == 10:
        return "K"
    return str(dv)

def is_valid_rut(rut: str) -> bool:
    if not isinstance(rut, str):
        return False
    m = _RUT_RE.match(rut)
    if not m:
        return False
    numbers, dv = m.group(1), m.group(2)
    numbers_clean = re.sub(r"\.", "", numbers)
    calc = calcular_dv(numbers_clean)
    return calc.upper() == dv.upper()

def format_rut(rut: str) -> str:
    if not is_valid_rut(rut):
        raise ValueError("RUT inválido")
    numbers = re.sub(r"[^\d]", "", rut)
    dv = rut[-1].upper()
    # formato: 12.345.678-9
    parts = []
    while numbers:
        parts.insert(0, numbers[-3:])
        numbers = numbers[:-3]
    return ".".join(parts) + "-" + dv
