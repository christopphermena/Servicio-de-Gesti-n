# models/item_carrito.py
"""
Clase ItemCarrito que representa un producto dentro del carrito.
Ejemplo de COMPOSICIÓN en POO: ItemCarrito contiene un Producto.
"""

class ItemCarrito:
    """
    Clase que representa un ítem (producto con cantidad) en el carrito de compras.
    Relación de COMPOSICIÓN: ItemCarrito contiene un Producto como parte esencial.
    """
    
    def __init__(self, producto, cantidad: int):
        """
        Constructor del ItemCarrito.
        
        Args:
            producto: Instancia de la clase Producto (COMPOSICIÓN)
            cantidad: Cantidad de unidades de este producto en el carrito
        """
        # COMPOSICIÓN: ItemCarrito contiene un Producto
        # El producto es parte esencial del item
        self.producto = producto  # instancia de Producto
        self.cantidad = int(cantidad)  # Asegurar que sea número entero

    def subtotal(self) -> float:
        """
        Calcula el subtotal de este ítem.
        Multiplica el precio con IVA del producto por la cantidad.
        
        Returns:
            Subtotal del ítem (precio con IVA × cantidad) redondeado a 2 decimales
        """
        # Usa el método precio_con_iva() del producto y lo multiplica por la cantidad
        return round(self.producto.precio_con_iva() * self.cantidad, 2)
