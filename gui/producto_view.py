# gui/producto_view.py
"""
Vista para gestionar productos (CRUD completo).
HERENCIA: Hereda de tk.Frame.
ASOCIACIÓN: Usa la clase Producto del modelo.
DEPENDENCIA: Depende de CRUD y models.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from config.database import probar_conexion
from crud.producto_crud import crear_producto, obtener_producto, eliminar_producto, actualizar_producto
from models.producto import Producto

class ProductoView(tk.Frame):
    """
    Vista para gestionar productos con operaciones CRUD completas.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.use_db = probar_conexion()
        self._mem = {}  # Diccionario en memoria si no hay BD (clave: código)
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="Código:").grid(row=0, column=0, sticky=tk.W)
        self.e_codigo = tk.Entry(top, width=32)
        self.e_codigo.grid(row=0, column=1, padx=6, pady=2, sticky=tk.W)

        tk.Label(top, text="Nombre:").grid(row=1, column=0, sticky=tk.W)
        self.e_nombre = tk.Entry(top, width=32)
        self.e_nombre.grid(row=1, column=1, padx=6, pady=2, sticky=tk.W)

        tk.Label(top, text="Precio Neto:").grid(row=2, column=0, sticky=tk.W)
        self.e_precio = tk.Entry(top, width=32)
        self.e_precio.grid(row=2, column=1, padx=6, pady=2, sticky=tk.W)

        btn_frame = tk.Frame(top)
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=8)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)
        btn_crear = tk.Button(btn_frame, text="Crear Producto", command=self.crear)
        btn_crear.grid(row=0, column=0, padx=4, sticky="ew")
        btn_buscar = tk.Button(btn_frame, text="Buscar", command=self.buscar)
        btn_buscar.grid(row=0, column=1, padx=4, sticky="ew")
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=2, padx=4, sticky="ew")
        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.actualizar)
        btn_actualizar.grid(row=0, column=3, padx=4, sticky="ew")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        if not self.use_db:
            self.listbox.insert(tk.END, "SIN BD: Modo memoria para productos")

    def crear(self):
        """
        CREATE: Crea un nuevo producto.
        Valida que el precio sea un número válido.
        Usa prefijo "objeto" en la instanciación según requerimiento.
        """
        codigo = self.e_codigo.get().strip()
        nombre = self.e_nombre.get().strip()
        precio = self.e_precio.get().strip()
        
        # Validar campos completos
        if not (codigo and nombre and precio):
            messagebox.showwarning("Validación", "Completa todos los campos")
            return
        
        # Validar que precio sea un número válido
        try:
            precio_f = float(precio)
        except ValueError:
            messagebox.showwarning("Validación", "Precio no válido")
            return

        if self.use_db:
            try:
                crear_producto(codigo, nombre, precio_f)
                self.listbox.insert(tk.END, f"Producto creado en BD: {codigo} - {nombre}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # PREFIJO "objeto": Instanciar con prefijo según requerimiento
            objeto_producto = Producto(codigo, nombre, precio_f)
            self._mem[codigo] = objeto_producto
            self.listbox.insert(tk.END, f"[MEM] Producto creado: {codigo} - {nombre}")

    def buscar(self):
        """
        READ: Busca un producto por código.
        Muestra los datos del producto encontrado.
        """
        codigo = self.e_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Validación", "Ingrese código")
            return
        
        if self.use_db:
            try:
                row = obtener_producto(codigo)
                if not row:
                    messagebox.showinfo("Resultado", "Producto no encontrado")
                else:
                    # row: (CODIGO, NOMBRE, PRECIO_NETO, ESTADO)
                    self.listbox.insert(tk.END, f"DB -> {row[0]} | {row[1]} | {row[2]} | {row[3]}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Buscar en memoria usando diccionario
            p = self._mem.get(codigo)
            if not p:
                messagebox.showinfo("Resultado", "Producto no encontrado (memoria)")
            else:
                self.listbox.insert(tk.END, f"MEM -> {p.codigo} | {p.nombre} | {p.precio_neto}")

    def eliminar(self):
        """
        DELETE: Elimina un producto por código.
        """
        codigo = self.e_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Validación", "Ingrese código")
            return
        
        if self.use_db:
            try:
                eliminar_producto(codigo)
                self.listbox.insert(tk.END, f"Producto eliminado en BD: {codigo}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Eliminar de memoria usando del en diccionario
            if codigo in self._mem:
                del self._mem[codigo]
                self.listbox.insert(tk.END, f"Producto eliminado en memoria: {codigo}")
            else:
                self.listbox.insert(tk.END, f"Producto no encontrado en memoria: {codigo}")

    def actualizar(self):
        """
        UPDATE: Actualiza los datos de un producto existente.
        Solo actualiza los campos proporcionados (los vacíos se ignoran).
        Valida que el precio sea un número válido si se proporciona.
        """
        codigo = self.e_codigo.get().strip()
        nombre = self.e_nombre.get().strip() or None
        precio = self.e_precio.get().strip() or None
        
        if not codigo:
            messagebox.showwarning("Validación", "Ingrese código")
            return
        
        # Validar precio solo si se proporciona
        precio_f = None
        if precio:
            try:
                precio_f = float(precio)
            except ValueError:
                messagebox.showwarning("Validación", "Precio no válido")
                return

        if self.use_db:
            try:
                # UPDATE en BD (solo actualiza campos no None)
                actualizar_producto(codigo, nombre=nombre, precio_neto=precio_f)
                self.listbox.insert(tk.END, f"Producto actualizado en BD: {codigo}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Actualizar en memoria
            p = self._mem.get(codigo)
            if not p:
                self.listbox.insert(tk.END, f"Producto no encontrado en memoria: {codigo}")
            else:
                # Actualizar solo los campos proporcionados
                if nombre:
                    p.nombre = nombre
                if precio_f is not None:
                    p.precio_neto = precio_f
                self.listbox.insert(tk.END, f"Producto actualizado en memoria: {codigo}")
