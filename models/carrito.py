# models/carrito.py
from typing import List

class Carrito:
    def __init__(self, id_carrito: int | None, cliente_id: int, items: List = None):
        self.id_carrito = id_carrito
        self.cliente_id = cliente_id
        self.items = items or []  # lista de ItemCarrito

    def agregar_item(self, item):
        # si mismo producto, sumar cantidad
        for it in self.items:
            if it.producto.codigo == item.producto.codigo:
                it.cantidad += item.cantidad
                return
        self.items.append(item)

    def calcular_subtotal(self) -> float:
        s = sum(item.subtotal() for item in self.items)
        return round(s, 2)

    def aplicar_descuento(self, cliente) -> float:
        subtotal = self.calcular_subtotal()
        return cliente.aplicar_descuento(subtotal)

    def calcular_total(self, cliente) -> float:
        subtotal = self.calcular_subtotal()
        descuento = self.aplicar_descuento(cliente)
        total = subtotal - descuento
        return round(total, 2)
