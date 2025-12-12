# gui/cliente_view.py
"""
Vista para gestionar clientes (CRUD completo).
HERENCIA: Hereda de tk.Frame.
DEPENDENCIA: Depende de CRUD, validations y utils.
Implementa modo memoria si no hay conexión a BD.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from config.database import probar_conexion
from crud.cliente_crud import crear_cliente, obtener_cliente_por_rut, eliminar_cliente_por_rut, actualizar_cliente
from utils.bcrypt_helper import hash_password
from validations.email_validator import is_valid_email
from validations.rut_validator import is_valid_rut, format_rut

class ClienteView(tk.Frame):
    """
    Vista para gestionar clientes con operaciones CRUD completas.
    """
    
    def __init__(self, parent):
        """
        Constructor de la vista de clientes.
        
        Args:
            parent: Widget padre (content_frame de MainWindow)
        """
        super().__init__(parent)  # HERENCIA: llamar constructor de tk.Frame
        # Verificar si hay conexión a BD
        self.use_db = probar_conexion()
        # Lista temporal en memoria si no hay BD (modo memoria)
        self._mem = []
        self._build()  # Construir la interfaz

    def _build(self):
        """
        Construye la interfaz gráfica de la vista de clientes.
        Crea formulario con campos y botones CRUD.
        """
        # MARCO SUPERIOR: Formulario con campos de entrada
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        # CAMPO RUT: Identificador único del cliente
        tk.Label(top, text="RUT:").grid(row=0, column=0, sticky=tk.W)
        self.e_rut = tk.Entry(top, width=32)
        self.e_rut.grid(row=0, column=1, padx=6, pady=2, sticky=tk.W)

        # CAMPO NOMBRE: Nombre completo del cliente
        tk.Label(top, text="Nombre:").grid(row=1, column=0, sticky=tk.W)
        self.e_nombre = tk.Entry(top, width=32)
        self.e_nombre.grid(row=1, column=1, padx=6, pady=2, sticky=tk.W)

        # CAMPO EMAIL: Correo electrónico (se valida con regex)
        tk.Label(top, text="Email:").grid(row=2, column=0, sticky=tk.W)
        self.e_email = tk.Entry(top, width=32)
        self.e_email.grid(row=2, column=1, padx=6, pady=2, sticky=tk.W)

        # CAMPO CONTRASEÑA: Se oculta con asteriscos (show="*")
        tk.Label(top, text="Contraseña:").grid(row=3, column=0, sticky=tk.W)
        self.e_pass = tk.Entry(top, width=32, show="*")
        self.e_pass.grid(row=3, column=1, padx=6, pady=2, sticky=tk.W)

        # CAMPO NIVEL: Combobox con opciones General/Estudiante
        tk.Label(top, text="Nivel:").grid(row=4, column=0, sticky=tk.W)
        self.cb_nivel = ttk.Combobox(top, values=["General", "Estudiante"], state="readonly", width=29)
        self.cb_nivel.current(0)  # Seleccionar "General" por defecto
        self.cb_nivel.grid(row=4, column=1, padx=6, pady=4, sticky=tk.W)

        # BOTONES CRUD: Create, Read, Delete, Update
        btn_frame = tk.Frame(top)
        btn_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=8)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)
        btn_crear = tk.Button(btn_frame, text="Crear Cliente", command=self.crear)
        btn_crear.grid(row=0, column=0, padx=4, sticky="ew")
        btn_buscar = tk.Button(btn_frame, text="Buscar por RUT", command=self.buscar)
        btn_buscar.grid(row=0, column=1, padx=4, sticky="ew")
        btn_eliminar = tk.Button(btn_frame, text="Eliminar por RUT", command=self.eliminar)
        btn_eliminar.grid(row=0, column=2, padx=4, sticky="ew")
        btn_actualizar = tk.Button(btn_frame, text="Actualizar", command=self.actualizar)
        btn_actualizar.grid(row=0, column=3, padx=4, sticky="ew")

        # LISTA INFERIOR: Muestra resultados y mensajes
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Mensaje inicial si no hay BD
        if not self.use_db:
            self.listbox.insert(tk.END, "No hay conexión a BD: trabajando en modo memoria (temporal)")

    def crear(self):
        """
        CREATE: Crea un nuevo cliente.
        Valida RUT y email antes de guardar.
        Hashea la contraseña con bcrypt por seguridad.
        Funciona en modo BD o memoria según disponibilidad.
        """
        # Obtener valores de los campos del formulario
        rut = self.e_rut.get().strip()
        nombre = self.e_nombre.get().strip()
        email = self.e_email.get().strip()
        pwd = self.e_pass.get().strip()
        nivel = self.cb_nivel.get()

        # VALIDACIÓN 1: Verificar que todos los campos estén completos
        if not (rut and nombre and email and pwd):
            messagebox.showwarning("Validación", "Completa todos los campos")
            return
        
        # VALIDACIÓN 2: Validar formato y dígito verificador del RUT
        if not is_valid_rut(rut):
            messagebox.showwarning("Validación", "RUT inválido")
            return
        
        # VALIDACIÓN 3: Validar formato del email
        if not is_valid_email(email):
            messagebox.showwarning("Validación", "Email inválido")
            return

        # SEGURIDAD: Hashear contraseña con bcrypt (nunca guardar texto plano)
        hashed = hash_password(pwd)

        # Guardar cliente según modo (BD o memoria)
        if self.use_db:
            try:
                # CREATE en base de datos usando función CRUD
                crear_cliente(rut, nombre, email, hashed, nivel)
                self.listbox.insert(tk.END, f"Cliente creado en BD: {nombre} ({rut})")
            except Exception as e:
                # MANEJO DE EXCEPCIONES: Mostrar error si falla
                messagebox.showerror("Error DB", str(e))
        else:
            # Modo memoria: guardar en lista temporal
            self._mem.append({"rut": rut, "nombre": nombre, "email": email, "hash": hashed, "nivel": nivel})
            self.listbox.insert(tk.END, f"[MEM] Cliente creado: {nombre} ({rut})")

    def buscar(self):
        """
        READ: Busca un cliente por RUT.
        Muestra los datos del cliente encontrado en la lista.
        """
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT a buscar")
            return
        
        if self.use_db:
            try:
                # READ desde base de datos
                row = obtener_cliente_por_rut(rut)
                if not row:
                    messagebox.showinfo("Resultado", "Cliente no encontrado")
                else:
                    # row: (ID_CLIENTE, RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL)
                    # Mostrar datos en la lista (sin mostrar contraseña)
                    self.listbox.insert(tk.END, f"DB -> {row[2]} | {row[1]} | {row[3]} | {row[5]}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Buscar en memoria
            found = [c for c in self._mem if c["rut"] == rut]
            if not found:
                messagebox.showinfo("Resultado", "Cliente no encontrado (memoria)")
            else:
                c = found[0]
                self.listbox.insert(tk.END, f"MEM -> {c['nombre']} | {c['rut']} | {c['email']} | {c['nivel']}")

    def eliminar(self):
        """
        DELETE: Elimina un cliente por RUT.
        """
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT a eliminar")
            return
        
        if self.use_db:
            try:
                # DELETE en base de datos
                eliminar_cliente_por_rut(rut)
                self.listbox.insert(tk.END, f"Cliente eliminado en BD: {rut}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Eliminar de memoria: filtrar lista excluyendo el RUT
            before = len(self._mem)
            self._mem = [c for c in self._mem if c["rut"] != rut]
            after = len(self._mem)
            if before == after:
                self.listbox.insert(tk.END, f"No se encontró cliente en memoria: {rut}")
            else:
                self.listbox.insert(tk.END, f"Cliente eliminado en memoria: {rut}")

    def actualizar(self):
        """
        UPDATE: Actualiza los datos de un cliente existente.
        Solo actualiza los campos que se completen (los vacíos se ignoran).
        Valida email si se proporciona.
        Hashea contraseña solo si se proporciona una nueva.
        """
        rut = self.e_rut.get().strip()
        if not rut:
            messagebox.showwarning("Validación", "Ingrese RUT para actualizar")
            return
        
        # Obtener valores (None si están vacíos - no se actualizarán)
        nombre = self.e_nombre.get().strip() or None
        email = self.e_email.get().strip() or None
        pwd = self.e_pass.get().strip() or None
        nivel = self.cb_nivel.get() or None

        # Validar email solo si se proporciona uno nuevo
        if email and not is_valid_email(email):
            messagebox.showwarning("Validación", "Email inválido")
            return
        
        # Hashear contraseña solo si se proporciona una nueva
        if pwd:
            hashed = hash_password(pwd)
        else:
            hashed = None  # No actualizar contraseña

        if self.use_db:
            try:
                # UPDATE en base de datos (solo actualiza campos no None)
                actualizar_cliente(rut, nombre=nombre, email=email, contrasena_hash=hashed, nivel=nivel)
                self.listbox.insert(tk.END, f"Cliente actualizado en BD: {rut}")
            except Exception as e:
                messagebox.showerror("Error DB", str(e))
        else:
            # Actualizar en memoria
            found = False
            for c in self._mem:
                if c["rut"] == rut:
                    # Actualizar solo los campos proporcionados
                    if nombre:
                        c["nombre"] = nombre
                    if email:
                        c["email"] = email
                    if hashed:
                        c["hash"] = hashed
                    if nivel:
                        c["nivel"] = nivel
                    found = True
                    break
            if not found:
                self.listbox.insert(tk.END, f"No se encontró cliente en memoria: {rut}")
            else:
                self.listbox.insert(tk.END, f"Cliente actualizado en memoria: {rut}")
