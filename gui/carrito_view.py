# gui/carrito_view.py
"""
Vista para gestionar carritos de compra.
HERENCIA: Hereda de tk.Frame.
ASOCIACIÓN: Usa clases Producto, ItemCarrito, Carrito.
COMPOSICIÓN: Contiene un Carrito (self.carrito).
Implementa creación de carrito, agregar ítems y generar voucher.
"""
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
    """
    Vista para gestionar carritos de compra.
    Permite crear carrito, agregar productos y generar voucher.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.use_db = probar_conexion()
        self._mem_products = {}  # Productos en memoria si no hay BD
        self._mem_clientes = {}  # Clientes en memoria si no hay BD
        self.carrito = None  # COMPOSICIÓN: Carrito actual de la vista
        self.client_id = None  # ID del cliente dueño del carrito
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="RUT Cliente:").grid(row=0, column=0, sticky=tk.W)
        self.e_rut = tk.Entry(top, width=32)
        self.e_rut.grid(row=0, column=1, padx=6, pady=2, sticky=tk.W)
        btn_crear_carrito = tk.Button(top, text="Crear Carrito para RUT", command=self.crear_carrito)
        btn_crear_carrito.grid(row=0, column=2, padx=6, pady=2, sticky=tk.W)

        tk.Label(top, text="Código Producto:").grid(row=1, column=0, sticky=tk.W)
        self.e_codigo = tk.Entry(top, width=32)
        self.e_codigo.grid(row=1, column=1, padx=6, pady=2, sticky=tk.W)
        tk.Label(top, text="Cantidad:").grid(row=2, column=0, sticky=tk.W)
        self.e_cantidad = tk.Entry(top, width=32)
        self.e_cantidad.grid(row=2, column=1, padx=6, pady=2, sticky=tk.W)

        btn_frame = tk.Frame(top)
        btn_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=8)
        btn_frame.columnconfigure((0, 1), weight=1)
        btn_agregar = tk.Button(btn_frame, text="Agregar Item", command=self.agregar_item)
        btn_agregar.grid(row=0, column=0, padx=4, sticky="ew")
        btn_voucher = tk.Button(btn_frame, text="Generar Voucher (archivo .txt)", command=self.generar_voucher)
        btn_voucher.grid(row=0, column=1, padx=4, sticky="ew")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        if not self.use_db:
            self.listbox.insert(tk.END, "SIN BD: modo memoria para carrito/products")

    def crear_carrito(self):
        """
        CREATE: Crea un nuevo carrito para un cliente.
        Verifica que el cliente exista antes de crear el carrito.
        Usa prefijo "objeto" en la instanciación.
        """
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT")
            return

        if self.use_db:
            # Verificar que el cliente exista en BD
            row = obtener_cliente_por_rut(rut)
            if not row:
                messagebox.showwarning("Cliente", "Cliente no encontrado en BD. Crea el cliente primero.")
                return
            id_cliente = row[0]  # ID del cliente en BD
            try:
                # Crear carrito en BD y obtener su ID
                cid = crear_carrito(id_cliente)
                # PREFIJO "objeto": Instanciar Carrito con prefijo
                objeto_carrito = Carrito(cid, id_cliente, [])
                self.carrito = objeto_carrito  # COMPOSICIÓN: guardar carrito en la vista
                self.client_id = id_cliente
                self.listbox.insert(tk.END, f"Carrito creado ID={cid} para cliente {rut}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Modo memoria: usar RUT como identificador
            self.client_id = rut
            objeto_carrito = Carrito(id_carrito=1, cliente_id=rut, items=[])
            self.carrito = objeto_carrito
            self.listbox.insert(tk.END, f"[MEM] Carrito creado para {rut}")

    def _get_producto(self, codigo):
        """
        Método helper para obtener un producto por código.
        Retorna instancia de Producto desde BD o memoria.
        Usa prefijo "objeto" en la instanciación.
        
        Args:
            codigo: Código del producto a buscar
            
        Returns:
            Instancia de Producto o None si no se encuentra
        """
        if self.use_db:
            # Obtener desde BD y crear objeto Producto
            row = obtener_producto(codigo)
            if not row:
                return None
            # row: (CODIGO, NOMBRE, PRECIO_NETO, ESTADO)
            # PREFIJO "objeto": Instanciar con prefijo
            objeto_producto = Producto(row[0], row[1], float(row[2]), row[3])
            return objeto_producto
        else:
            # Obtener desde memoria (diccionario)
            return self._mem_products.get(codigo)

    def agregar_item(self):
        """
        Agrega un producto al carrito actual.
        Valida cantidad y verifica que el producto exista.
        Usa prefijo "objeto" en instanciaciones.
        """
        if not self.carrito:
            messagebox.showwarning("Carrito", "Crea un carrito primero")
            return
        
        codigo = self.e_codigo.get().strip()
        cantidad = self.e_cantidad.get().strip()
        if not (codigo and cantidad):
            messagebox.showwarning("Validación", "Completa código y cantidad")
            return
        
        # Validar que cantidad sea un número entero positivo
        try:
            cantidad_i = int(cantidad)
            if cantidad_i <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Validación", "Cantidad inválida")
            return

        # Obtener producto (de BD o memoria)
        producto = self._get_producto(codigo)
        if not producto:
            # En modo memoria, crear producto temporal si no existe
            if not self.use_db:
                nombre = codigo
                precio = 100.0
                objeto_producto = Producto(codigo, nombre, precio)
                producto = objeto_producto
                self._mem_products[codigo] = objeto_producto
                self.listbox.insert(tk.END, f"[MEM] Producto temporal creado: {codigo}")
            else:
                messagebox.showwarning("Producto", "Producto no encontrado en BD")
                return

        # PREFIJO "objeto": Crear ItemCarrito con prefijo
        objeto_item = ItemCarrito(producto, cantidad_i)
        # AGREGACIÓN: Agregar item al carrito (el carrito contiene items)
        self.carrito.agregar_item(objeto_item)
        self.listbox.insert(tk.END, f"Item agregado: {cantidad_i} x {producto.nombre} -> {objeto_item.subtotal():.2f}")

        # Persistir item en BD si hay conexión
        if self.use_db:
            try:
                agregar_item_carrito(self.carrito.id_carrito, producto.codigo, cantidad_i, objeto_item.subtotal())
            except Exception as e:
                messagebox.showerror("Error DB", f"No se pudo agregar item en BD: {e}")

    def generar_voucher(self):
        """
        Genera un archivo .txt con el voucher de compra.
        El voucher incluye:
        - Datos del cliente
        - Lista de productos con cantidad y subtotales
        - Subtotal general
        - Descuento aplicado (10% para estudiantes)
        - Total final
        """
        if not self.carrito:
            messagebox.showwarning("Carrito", "Crea un carrito primero")
            return
        
        # Obtener información del cliente para el voucher
        cliente_nombre = str(self.client_id)
        nivel_cliente = "General"
        if self.use_db and isinstance(self.client_id, int):
            # Obtener nombre y nivel del cliente desde BD
            try:
                from config.database import obtener_conexion
                conn = obtener_conexion()
                with conn.cursor() as cur:
                    cur.execute("SELECT NOMBRE, NIVEL FROM CLIENTE WHERE ID_CLIENTE = :id", {"id": self.client_id})
                    row = cur.fetchone()
                    if row:
                        cliente_nombre = row[0]
                        nivel_cliente = row[1] or "General"
                conn.close()
            except Exception:
                pass

        # Preparar lista de ítems para el voucher
        items_for_voucher = []
        for it in self.carrito.items:
            items_for_voucher.append({
                "codigo": it.producto.codigo,
                "nombre": it.producto.nombre,
                "cantidad": it.cantidad,
                "subtotal": it.subtotal(),  # Subtotal del ítem (precio con IVA × cantidad)
            })

        # Calcular totales del carrito
        subtotal = self.carrito.calcular_subtotal()  # Suma de todos los ítems
        descuento = 0.0
        if nivel_cliente == "Estudiante":
            descuento = round(subtotal * 0.10, 2)  # 10% de descuento para estudiantes
        total = round(subtotal - descuento, 2)  # Total final

        # Generar texto del voucher usando la función utilitaria
        txt = generar_voucher_texto(
            cliente_nombre, self.carrito.id_carrito or 0, items_for_voucher, subtotal, descuento, total
        )
        
        # Guardar voucher en archivo .txt
        filename = f"voucher_carrito_{self.carrito.id_carrito or 'mem'}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(txt)
        messagebox.showinfo("Voucher", f"Voucher generado: {filename}")
        self.listbox.insert(tk.END, f"Voucher generado: {filename}")
