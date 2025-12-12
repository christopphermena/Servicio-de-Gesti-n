# gui/main_window.py
"""
Ventana principal de la aplicación.
Simula una página web con panel izquierdo (menú) y panel derecho (contenido).
Ejemplo de HERENCIA: MainWindow hereda de tk.Tk (ventana principal de Tkinter).
Ejemplo de COMPOSICIÓN: MainWindow contiene las vistas (las crea y destruye).
"""
import tkinter as tk
from tkinter import messagebox
from gui.cliente_view import ClienteView
from gui.producto_view import ProductoView
from gui.carrito_view import CarritoView
from gui.api_view import ApiView

class MainWindow(tk.Tk):
    """
    Clase principal de la ventana de la aplicación.
    HERENCIA: Hereda de tk.Tk (ventana raíz de Tkinter).
    """
    
    def __init__(self):
        """
        Constructor de la ventana principal.
        Inicializa la ventana y construye la interfaz.
        """
        super().__init__()  # Llamar al constructor de tk.Tk
        self.title("Kiosko - Objeto Feliz")
        self.geometry("700x300")  # Tamaño inicial de la ventana
        self._build_ui()  # Construir la interfaz

    def _build_ui(self):
        """
        Construye la interfaz gráfica principal.
        Crea el diseño de dos paneles: menú izquierdo y contenido derecho.
        """
        # PANEL IZQUIERDO: Menú de navegación
        # Simula el menú lateral de una página web
        menu_frame = tk.Frame(self, width=200, bg="#f0f0f0")
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)  # Lado izquierdo, altura completa

        # PANEL DERECHO: Área de contenido dinámico
        # Aquí se mostrarán las diferentes vistas (Clientes, Productos, etc.)
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  # Lado derecho, expandible

        # BOTONES DEL MENÚ: Cada botón cambia la vista en el panel derecho
        btn_cliente = tk.Button(menu_frame, text="Clientes", command=self.show_cliente)
        btn_producto = tk.Button(menu_frame, text="Productos", command=self.show_producto)
        btn_carrito = tk.Button(menu_frame, text="Carrito", command=self.show_carrito)
        btn_api = tk.Button(menu_frame, text="Clima (API)", command=self.show_api)

        # Colocar todos los botones en el menú
        for w in (btn_cliente, btn_producto, btn_carrito, btn_api):
            w.pack(fill=tk.X, pady=6, padx=8)  # Ancho completo, espaciado vertical y horizontal

        # Variable para guardar la vista actual (COMPOSICIÓN)
        # Las vistas se crean y destruyen dinámicamente
        self.current_view = None
        self.show_cliente()  # Mostrar vista de Clientes por defecto

    def _switch_view(self, view_class):
        """
        Cambia la vista mostrada en el panel derecho.
        COMPOSICIÓN: Destruye la vista actual y crea una nueva.
        
        Args:
            view_class: Clase de la vista a mostrar (ClienteView, ProductoView, etc.)
        """
        # Destruir vista actual si existe
        if self.current_view:
            self.current_view.destroy()  # Liberar recursos
            self.current_view = None
        
        # Crear nueva vista y mostrarla en el panel derecho
        self.current_view = view_class(self.content_frame)  # COMPOSICIÓN: crear vista
        self.current_view.pack(expand=True, fill=tk.BOTH)  # Expandir para llenar el espacio

    def show_cliente(self):
        """Muestra la vista de gestión de clientes."""
        self._switch_view(ClienteView)

    def show_producto(self):
        """Muestra la vista de gestión de productos."""
        self._switch_view(ProductoView)

    def show_carrito(self):
        """Muestra la vista de carrito de compras."""
        self._switch_view(CarritoView)

    def show_api(self):
        """Muestra la vista de APIs externas (clima y conversión de moneda)."""
        self._switch_view(ApiView)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()  # Iniciar bucle de eventos de Tkinter
