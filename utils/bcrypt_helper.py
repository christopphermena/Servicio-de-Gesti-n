# utils/bcrypt_helper.py
import bcrypt

def hash_password(plain: str) -> str:
    if not isinstance(plain, str):
        raise TypeError("password debe ser str")
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def check_password(plain: str, hashed: str) -> bool:
    if not (isinstance(plain, str) and isinstance(hashed, str)):
        return False
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
