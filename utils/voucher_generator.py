# utils/voucher_generator.py
from datetime import datetime

def generar_voucher_texto(cliente_nombre: str, carrito_id: int, items: list, total: float) -> str:
    """
    items: lista de dicts -> [{"codigo":..., "nombre":..., "cantidad":..., "subtotal":...}, ...]
    Retorna el contenido del voucher como string.
    """
    lines = []
    lines.append("KIOSKO - VOUCHER")
    lines.append(f"Cliente: {cliente_nombre}")
    lines.append(f"Carrito ID: {carrito_id}")
    lines.append(f"Fecha: {datetime.now().isoformat(sep=' ', timespec='seconds')}")
    lines.append("-" * 40)
    for it in items:
        lines.append(f"{it['cantidad']} x {it['nombre']} ({it['codigo']}) -> {it['subtotal']:.2f}")
    lines.append("-" * 40)
    lines.append(f"TOTAL: {total:.2f}")
    return "\n".join(lines)
