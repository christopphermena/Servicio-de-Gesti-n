# gui/carrito_view.py
import tkinter as tk
from tkinter import messagebox
from config.database import probar_conexion
from models.producto import Producto
from models.item_carrito import ItemCarrito
from models.carrito import Carrito
from crud.carrito_crud import crear_carrito, agregar_item_carrito
from crud.producto_crud import obtener_producto
from utils.voucher_generator import generar_voucher_texto
from crud.cliente_crud import obtener_cliente_por_rut

class CarritoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.use_db = probar_conexion()
        self._mem_products = {}
        self._mem_clientes = {}
        self.carrito = None
        self.client_id = None
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="RUT Cliente:").grid(row=0, column=0)
        self.e_rut = tk.Entry(top, width=20)
        self.e_rut.grid(row=0, column=1, padx=6)

        btn_crear_carrito = tk.Button(top, text="Crear Carrito para RUT", command=self.crear_carrito)
        btn_crear_carrito.grid(row=0, column=2, padx=6)

        # producto
        tk.Label(top, text="Código Producto:").grid(row=1, column=0)
        self.e_codigo = tk.Entry(top, width=15)
        self.e_codigo.grid(row=1, column=1, padx=6)

        tk.Label(top, text="Cantidad:").grid(row=1, column=2)
        self.e_cantidad = tk.Entry(top, width=6)
        self.e_cantidad.grid(row=1, column=3, padx=6)

        btn_agregar = tk.Button(top, text="Agregar Item", command=self.agregar_item)
        btn_agregar.grid(row=1, column=4, padx=6)

        btn_voucher = tk.Button(top, text="Generar Voucher (archivo .txt)", command=self.generar_voucher)
        btn_voucher.grid(row=2, column=0, columnspan=2, pady=8)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        if not self.use_db:
            self.listbox.insert(tk.END, "SIN BD: modo memoria para carrito/products")

    def crear_carrito(self):
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT")
            return

        # Si BD: obtener cliente id
        if self.use_db:
            row = obtener_cliente_por_rut(rut)
            if not row:
                messagebox.showwarning("Cliente", "Cliente no encontrado en BD. Crea el cliente primero.")
                return
            id_cliente = row[0]
            try:
                cid = crear_carrito(id_cliente)
                self.carrito = Carrito(cid, id_cliente, [])
                self.client_id = id_cliente
                self.listbox.insert(tk.END, f"Carrito creado ID={cid} para cliente {rut}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # modo memoria simple: carrito id incremental
            self.client_id = rut
            self.carrito = Carrito(id_carrito=1, cliente_id=rut, items=[])
            self.listbox.insert(tk.END, f"[MEM] Carrito creado para {rut}")

    def _get_producto(self, codigo):
        if self.use_db:
            row = obtener_producto(codigo)
            if not row:
                return None
            # row: (CODIGO, NOMBRE, PRECIO_NETO, ESTADO)
            return Producto(row[0], row[1], float(row[2]), row[3])
        else:
            return self._mem_products.get(codigo)

    def agregar_item(self):
        if not self.carrito:
            messagebox.showwarning("Carrito", "Crea un carrito primero")
            return
        codigo = self.e_codigo.get().strip()
        cantidad = self.e_cantidad.get().strip()
        if not (codigo and cantidad):
            messagebox.showwarning("Validación", "Completa código y cantidad")
            return
        try:
            cantidad_i = int(cantidad)
            if cantidad_i <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Validación", "Cantidad inválida")
            return

        producto = self._get_producto(codigo)
        if not producto:
            # en modo memoria, crear producto temporal si no existe
            if not self.use_db:
                # pedir nombre y precio default
                nombre = codigo
                precio = 100.0
                producto = Producto(codigo, nombre, precio)
                self._mem_products[codigo] = producto
                self.listbox.insert(tk.END, f"[MEM] Producto temporal creado: {codigo}")
            else:
                messagebox.showwarning("Producto", "Producto no encontrado en BD")
                return

        item = ItemCarrito(producto, cantidad_i)
        self.carrito.agregar_item(item)
        self.listbox.insert(tk.END, f"Item agregado: {cantidad_i} x {producto.nombre} -> {item.subtotal():.2f}")

        # persistir item si BD
        if self.use_db:
            try:
                agregar_item_carrito(self.carrito.id_carrito, producto.codigo, cantidad_i, item.subtotal())
            except Exception as e:
                messagebox.showerror("Error DB", f"No se pudo agregar item en BD: {e}")

    def generar_voucher(self):
        if not self.carrito:
            messagebox.showwarning("Carrito", "Crea un carrito primero")
            return
        # obtener info cliente sencilla
        cliente_nombre = str(self.client_id)
        if self.use_db and isinstance(self.client_id, int):
            # intentar obtener nombre de cliente
            try:
                # suponemos que existe función en crud
                # reusar obtener_cliente_por_rut no sirve porque tenemos id; hacemos consulta simple
                from config.database import obtener_conexion
                conn = obtener_conexion()
                with conn.cursor() as cur:
                    cur.execute("SELECT NOMBRE FROM CLIENTE WHERE ID_CLIENTE = :id", {"id": self.client_id})
                    row = cur.fetchone()
                    if row:
                        cliente_nombre = row[0]
                conn.close()
            except Exception:
                pass

        items_for_voucher = []
        for it in self.carrito.items:
            items_for_voucher.append({
                "codigo": it.producto.codigo,
                "nombre": it.producto.nombre,
                "cantidad": it.cantidad,
                "subtotal": it.subtotal()
            })
        total = self.carrito.calcular_subtotal()
        txt = generar_voucher_texto(cliente_nombre, self.carrito.id_carrito or 0, items_for_voucher, total)
        # guardar archivo
        filename = f"voucher_carrito_{self.carrito.id_carrito or 'mem'}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(txt)
        messagebox.showinfo("Voucher", f"Voucher generado: {filename}")
        self.listbox.insert(tk.END, f"Voucher generado: {filename}")
