# models/persona.py
"""
Clase base Persona que representa los datos comunes de una persona.
Esta clase será heredada por Cliente (relación de HERENCIA en POO).
"""

class Persona:
    """
    Clase base que representa una persona genérica.
    Contiene los atributos comunes: nombre, email y RUT.
    """
    
    def __init__(self, nombre: str, email: str, rut: str):
        """
        Constructor que inicializa los atributos básicos de una persona.
        
        Args:
            nombre: Nombre completo de la persona
            email: Correo electrónico
            rut: RUT chileno (formato: 12.345.678-9)
        """
        self.nombre = nombre
        self.email = email
        self.rut = rut

    def mostrar_resumen(self) -> str:
        """
        Retorna un resumen formateado de la persona.
        Útil para mostrar información en la interfaz.
        
        Returns:
            String con formato: "Nombre <email> - RUT"
        """
        return f"{self.nombre} <{self.email}> - {self.rut}"
