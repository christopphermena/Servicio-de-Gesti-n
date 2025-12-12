# models/producto.py
"""
Clase Producto que representa un producto del kiosko.
Maneja el cálculo del precio con IVA (19% en Chile).
"""

class Producto:
    """
    Clase que representa un producto disponible en el kiosko.
    """
    
    # Constante de clase: factor de IVA chileno (19%)
    # Se usa para calcular el precio con IVA
    IVA_FACTOR = 1.19

    def __init__(self, codigo: str, nombre: str, precio_neto: float, estado: str = "ACTIVO"):
        """
        Constructor del Producto.
        
        Args:
            codigo: Código único del producto (ej: "PROD001")
            nombre: Nombre descriptivo del producto
            precio_neto: Precio sin IVA (en pesos chilenos)
            estado: Estado del producto - "ACTIVO" o "INACTIVO"
        """
        self.codigo = codigo
        self.nombre = nombre
        self.precio_neto = float(precio_neto)  # Asegurar que sea número decimal
        self.estado = estado

    def precio_con_iva(self) -> float:
        """
        Calcula el precio del producto con IVA incluido.
        En Chile el IVA es 19%, por eso multiplicamos por 1.19.
        
        Returns:
            Precio con IVA redondeado a 2 decimales
        """
        return round(self.precio_neto * self.IVA_FACTOR, 2)
