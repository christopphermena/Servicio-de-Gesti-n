# models/producto.py
class Producto:
    IVA_FACTOR = 1.19

    def __init__(self, codigo: str, nombre: str, precio_neto: float, estado: str = "ACTIVO"):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_neto = float(precio_neto)
        self.estado = estado

    def precio_con_iva(self) -> float:
        return round(self.precio_neto * self.IVA_FACTOR, 2)
