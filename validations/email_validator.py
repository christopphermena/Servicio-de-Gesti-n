# validations/email_validator.py
import re

_EMAIL_RE = re.compile(
    r"^(?P<local>[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+)@(?P<domain>([A-Za-z0-9-]+\.)+[A-Za-z]{2,})$"
)

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    email = email.strip()
    if len(email) > 254 or len(email) < 3:
        return False
    return bool(_EMAIL_RE.match(email))

def normalize_email(email: str) -> str:
    if not isinstance(email, str):
        raise TypeError("email debe ser str")
    email = email.strip()
    parts = email.split("@")
    if len(parts) != 2:
        raise ValueError("email inválido")
    local, domain = parts
    return f"{local}@{domain.lower()}"
