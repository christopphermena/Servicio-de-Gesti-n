# models/cliente.py
from .persona import Persona

class Cliente(Persona):
    def __init__(self, id_cliente: int | None, nombre: str, email: str, rut: str, contrasena_hash: str, nivel: str = "General"):
        super().__init__(nombre=nombre, email=email, rut=rut)
        self.id_cliente = id_cliente
        self.contrasena_hash = contrasena_hash
        self.nivel = nivel  # 'General' o 'Estudiante'

    def aplicar_descuento(self, subtotal: float) -> float:
        if self.nivel == "Estudiante":
            return round(subtotal * 0.10, 2)
        return 0.0
