# models/item_carrito.py
class ItemCarrito:
    def __init__(self, producto, cantidad: int):
        self.producto = producto  # instancia de Producto
        self.cantidad = int(cantidad)

    def subtotal(self) -> float:
        return round(self.producto.precio_con_iva() * self.cantidad, 2)
