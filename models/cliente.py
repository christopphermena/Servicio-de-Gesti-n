# models/cliente.py
"""
Clase Cliente que hereda de Persona.
Ejemplo de HERENCIA en POO: Cliente ES-UN Persona con atributos adicionales.
"""
from .persona import Persona

class Cliente(Persona):
    """
    Clase que representa un cliente del kiosko.
    Hereda de Persona (HERENCIA) y agrega atributos específicos de cliente.
    """
    
    def __init__(self, id_cliente: int | None, nombre: str, email: str, rut: str, contrasena_hash: str, nivel: str = "General"):
        """
        Constructor del Cliente.
        
        Args:
            id_cliente: ID único en la base de datos (None si no está guardado)
            nombre: Nombre del cliente (heredado de Persona)
            email: Email del cliente (heredado de Persona)
            rut: RUT del cliente (heredado de Persona)
            contrasena_hash: Contraseña hasheada con bcrypt (nunca se guarda en texto plano)
            nivel: Nivel del cliente - "General" o "Estudiante" (los estudiantes tienen 10% descuento)
        """
        # Llamar al constructor de la clase padre (Persona)
        # Esto es HERENCIA: reutilizamos el código de Persona
        super().__init__(nombre=nombre, email=email, rut=rut)
        
        # Atributos específicos del Cliente (no están en Persona)
        self.id_cliente = id_cliente
        self.contrasena_hash = contrasena_hash  # Contraseña hasheada (seguridad)
        self.nivel = nivel  # 'General' o 'Estudiante'

    def aplicar_descuento(self, subtotal: float) -> float:
        """
        Calcula el descuento aplicable según el nivel del cliente.
        Los estudiantes tienen 10% de descuento, los generales no tienen descuento.
        
        Args:
            subtotal: Monto antes del descuento
            
        Returns:
            Monto del descuento (0.0 para General, 10% para Estudiante)
        """
        if self.nivel == "Estudiante":
            return round(subtotal * 0.10, 2)  # 10% de descuento
        return 0.0  # Sin descuento para clientes generales
