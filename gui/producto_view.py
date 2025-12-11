# gui/producto_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from config.database import probar_conexion
from crud.producto_crud import crear_producto, obtener_producto, eliminar_producto
from models.producto import Producto

class ProductoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.use_db = probar_conexion()
        self._mem = {}
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="Código:").grid(row=0, column=0)
        self.e_codigo = tk.Entry(top, width=15)
        self.e_codigo.grid(row=0, column=1, padx=6)

        tk.Label(top, text="Nombre:").grid(row=1, column=0)
        self.e_nombre = tk.Entry(top, width=40)
        self.e_nombre.grid(row=1, column=1, padx=6, columnspan=2)

        tk.Label(top, text="Precio Neto:").grid(row=2, column=0)
        self.e_precio = tk.Entry(top, width=15)
        self.e_precio.grid(row=2, column=1, padx=6)

        btn_crear = tk.Button(top, text="Crear Producto", command=self.crear)
        btn_buscar = tk.Button(top, text="Buscar", command=self.buscar)
        btn_eliminar = tk.Button(top, text="Eliminar", command=self.eliminar)

        btn_crear.grid(row=3, column=0, pady=8)
        btn_buscar.grid(row=3, column=1, pady=8)
        btn_eliminar.grid(row=3, column=2, pady=8)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        if not self.use_db:
            self.listbox.insert(tk.END, "SIN BD: Modo memoria para productos")

    def crear(self):
        codigo = self.e_codigo.get().strip()
        nombre = self.e_nombre.get().strip()
        precio = self.e_precio.get().strip()
        if not (codigo and nombre and precio):
            messagebox.showwarning("Validación", "Completa todos los campos")
            return
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
            p = Producto(codigo, nombre, precio_f)
            self._mem[codigo] = p
            self.listbox.insert(tk.END, f"[MEM] Producto creado: {codigo} - {nombre}")

    def buscar(self):
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
            p = self._mem.get(codigo)
            if not p:
                messagebox.showinfo("Resultado", "Producto no encontrado (memoria)")
            else:
                self.listbox.insert(tk.END, f"MEM -> {p.codigo} | {p.nombre} | {p.precio_neto}")

    def eliminar(self):
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
            if codigo in self._mem:
                del self._mem[codigo]
                self.listbox.insert(tk.END, f"Producto eliminado en memoria: {codigo}")
            else:
                self.listbox.insert(tk.END, f"Producto no encontrado en memoria: {codigo}")
