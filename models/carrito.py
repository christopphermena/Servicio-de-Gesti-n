# models/carrito.py
"""
Clase Carrito que representa un carrito de compras.
Ejemplos de relaciones POO:
- AGREGACIÓN: Carrito contiene lista de ItemCarrito
- ASOCIACIÓN: Carrito usa Cliente (por ID y como parámetro)
"""
from typing import List

class Carrito:
    """
    Clase que representa un carrito de compras de un cliente.
    Contiene una lista de ítems (productos con cantidad).
    """
    
    def __init__(self, id_carrito: int | None, cliente_id: int, items: List = None):
        """
        Constructor del Carrito.
        
        Args:
            id_carrito: ID único del carrito en la base de datos (None si no está guardado)
            cliente_id: ID del cliente dueño del carrito (ASOCIACIÓN por ID)
            items: Lista de ItemCarrito (AGREGACIÓN - lista vacía por defecto)
        """
        self.id_carrito = id_carrito
        self.cliente_id = cliente_id  # ASOCIACIÓN: referencia al cliente por ID
        # AGREGACIÓN: Carrito contiene una lista de ItemCarrito
        # Los items pueden existir independientemente del carrito
        self.items = items or []  # lista de ItemCarrito

    def agregar_item(self, item):
        """
        Agrega un ítem al carrito.
        Si el producto ya existe en el carrito, suma la cantidad en lugar de duplicar.
        
        Args:
            item: Instancia de ItemCarrito a agregar
        """
        # Si el mismo producto ya está en el carrito, sumar la cantidad
        for it in self.items:
            if it.producto.codigo == item.producto.codigo:
                it.cantidad += item.cantidad  # Sumar cantidad en lugar de duplicar
                return
        # Si no existe, agregarlo como nuevo ítem
        self.items.append(item)

    def calcular_subtotal(self) -> float:
        """
        Calcula el subtotal del carrito sumando todos los subtotales de los ítems.
        
        Returns:
            Subtotal total del carrito (suma de todos los ítems) redondeado a 2 decimales
        """
        # Suma los subtotales de todos los ítems usando comprensión de listas
        s = sum(item.subtotal() for item in self.items)
        return round(s, 2)

    def aplicar_descuento(self, cliente) -> float:
        """
        Calcula el descuento aplicable según el nivel del cliente.
        ASOCIACIÓN: recibe el cliente como parámetro y usa su método aplicar_descuento().
        
        Args:
            cliente: Instancia de Cliente (ASOCIACIÓN por parámetro)
            
        Returns:
            Monto del descuento calculado según el nivel del cliente
        """
        subtotal = self.calcular_subtotal()
        # ASOCIACIÓN: usa el método del cliente para calcular el descuento
        return cliente.aplicar_descuento(subtotal)

    def calcular_total(self, cliente) -> float:
        """
        Calcula el total final del carrito aplicando el descuento.
        Total = Subtotal - Descuento
        
        Args:
            cliente: Instancia de Cliente para calcular el descuento
            
        Returns:
            Total final a pagar (subtotal - descuento) redondeado a 2 decimales
        """
        subtotal = self.calcular_subtotal()
        descuento = self.aplicar_descuento(cliente)  # Usa el método aplicar_descuento()
        total = subtotal - descuento
        return round(total, 2)
