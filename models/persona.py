# models/persona.py
class Persona:
    def __init__(self, nombre: str, email: str, rut: str):
        self.nombre = nombre
        self.email = email
        self.rut = rut

    def mostrar_resumen(self) -> str:
        return f"{self.nombre} <{self.email}> - {self.rut}"
