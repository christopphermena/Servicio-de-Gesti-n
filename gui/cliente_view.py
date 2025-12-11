# gui/cliente_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from config.database import probar_conexion
from crud.cliente_crud import crear_cliente, obtener_cliente_por_rut, eliminar_cliente_por_rut
from utils.bcrypt_helper import hash_password
from validations.email_validator import is_valid_email
from validations.rut_validator import is_valid_rut, format_rut

class ClienteView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.use_db = probar_conexion()
        self._mem = []  # lista de clientes locales si no hay BD
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="RUT:").grid(row=0, column=0, sticky=tk.W)
        self.e_rut = tk.Entry(top, width=20)
        self.e_rut.grid(row=0, column=1, padx=6)

        tk.Label(top, text="Nombre:").grid(row=1, column=0, sticky=tk.W)
        self.e_nombre = tk.Entry(top, width=40)
        self.e_nombre.grid(row=1, column=1, columnspan=2, padx=6, pady=4, sticky=tk.W)

        tk.Label(top, text="Email:").grid(row=2, column=0, sticky=tk.W)
        self.e_email = tk.Entry(top, width=40)
        self.e_email.grid(row=2, column=1, columnspan=2, padx=6, pady=4, sticky=tk.W)

        tk.Label(top, text="Contraseña:").grid(row=3, column=0, sticky=tk.W)
        self.e_pass = tk.Entry(top, width=20, show="*")
        self.e_pass.grid(row=3, column=1, padx=6)

        tk.Label(top, text="Nivel:").grid(row=4, column=0, sticky=tk.W)
        self.cb_nivel = ttk.Combobox(top, values=["General", "Estudiante"], state="readonly")
        self.cb_nivel.current(0)
        self.cb_nivel.grid(row=4, column=1, padx=6, pady=4, sticky=tk.W)

        btn_crear = tk.Button(top, text="Crear Cliente", command=self.crear)
        btn_crear.grid(row=5, column=0, pady=8)

        btn_buscar = tk.Button(top, text="Buscar por RUT", command=self.buscar)
        btn_buscar.grid(row=5, column=1, pady=8)

        btn_eliminar = tk.Button(top, text="Eliminar por RUT", command=self.eliminar)
        btn_eliminar.grid(row=5, column=2, pady=8)

        # lista inferior
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # mensaje inicial
        if not self.use_db:
            self.listbox.insert(tk.END, "No hay conexión a BD: trabajando en modo memoria (temporal)")

    def crear(self):
        rut = self.e_rut.get().strip()
        nombre = self.e_nombre.get().strip()
        email = self.e_email.get().strip()
        pwd = self.e_pass.get().strip()
        nivel = self.cb_nivel.get()

        if not (rut and nombre and email and pwd):
            messagebox.showwarning("Validación", "Completa todos los campos")
            return
        if not is_valid_rut(rut):
            messagebox.showwarning("Validación", "RUT inválido")
            return
        if not is_valid_email(email):
            messagebox.showwarning("Validación", "Email inválido")
            return

        hashed = hash_password(pwd)

        if self.use_db:
            try:
                crear_cliente(rut, nombre, email, hashed, nivel)
                self.listbox.insert(tk.END, f"Cliente creado en BD: {nombre} ({rut})")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            self._mem.append({"rut": rut, "nombre": nombre, "email": email, "hash": hashed, "nivel": nivel})
            self.listbox.insert(tk.END, f"[MEM] Cliente creado: {nombre} ({rut})")

    def buscar(self):
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT a buscar")
            return
        if self.use_db:
            try:
                row = obtener_cliente_por_rut(rut)
                if not row:
                    messagebox.showinfo("Resultado", "Cliente no encontrado")
                else:
                    # row: (ID_CLIENTE, RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL)
                    self.listbox.insert(tk.END, f"DB -> {row[2]} | {row[1]} | {row[3]} | {row[5]}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            found = [c for c in self._mem if c["rut"] == rut]
            if not found:
                messagebox.showinfo("Resultado", "Cliente no encontrado (memoria)")
            else:
                c = found[0]
                self.listbox.insert(tk.END, f"MEM -> {c['nombre']} | {c['rut']} | {c['email']} | {c['nivel']}")

    def eliminar(self):
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT a eliminar")
            return
        if self.use_db:
            try:
                eliminar_cliente_por_rut(rut)
                self.listbox.insert(tk.END, f"Cliente eliminado en BD: {rut}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            before = len(self._mem)
            self._mem = [c for c in self._mem if c["rut"] != rut]
            after = len(self._mem)
            if before == after:
                self.listbox.insert(tk.END, f"No se encontró cliente en memoria: {rut}")
            else:
                self.listbox.insert(tk.END, f"Cliente eliminado en memoria: {rut}")
