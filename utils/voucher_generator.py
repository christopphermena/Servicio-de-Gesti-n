# utils/voucher_generator.py
"""
Módulo para generar vouchers de compra en formato texto.
Genera un archivo .txt con los detalles de la compra.
"""
from datetime import datetime

def generar_voucher_texto(
    cliente_nombre: str,
    carrito_id: int,
    items: list,
    subtotal: float,
    descuento: float,
    total: float,
) -> str:
    """
    Genera el contenido del voucher como texto formateado.
    El voucher incluye:
    - Datos del cliente
    - Lista de productos con cantidad y subtotales
    - Subtotal general
    - Descuento aplicado
    - Total final
    
    Args:
        cliente_nombre: Nombre del cliente
        carrito_id: ID del carrito
        items: Lista de diccionarios con datos de cada ítem
               Formato: [{"codigo": "...", "nombre": "...", "cantidad": ..., "subtotal": ...}, ...]
        subtotal: Subtotal general (suma de todos los ítems)
        descuento: Descuento aplicado (ej: 10% para estudiantes)
        total: Total final a pagar (subtotal - descuento)
        
    Returns:
        String con el contenido completo del voucher formateado
    """
    lines = []
    
    # Encabezado del voucher
    lines.append("KIOSKO - VOUCHER")
    lines.append(f"Cliente: {cliente_nombre}")
    lines.append(f"Carrito ID: {carrito_id}")
    lines.append(f"Fecha: {datetime.now().isoformat(sep=' ', timespec='seconds')}")
    lines.append("-" * 40)
    
    # Lista de productos comprados
    for it in items:
        # Formato: "2 x Producto (COD001) -> 2380.00"
        lines.append(f"{it['cantidad']} x {it['nombre']} ({it['codigo']}) -> {it['subtotal']:.2f}")
    
    # Resumen de totales
    lines.append("-" * 40)
    lines.append(f"Subtotal: {subtotal:.2f}")  # Suma de todos los ítems
    lines.append(f"Descuento: {descuento:.2f}")  # Descuento aplicado (si hay)
    lines.append(f"TOTAL: {total:.2f}")  # Total final a pagar
    
    # Unir todas las líneas con saltos de línea
    return "\n".join(lines)
