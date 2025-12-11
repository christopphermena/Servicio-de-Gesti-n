# gui/main_window.py
import tkinter as tk
from tkinter import messagebox
from gui.cliente_view import ClienteView
from gui.producto_view import ProductoView
from gui.carrito_view import CarritoView
from gui.api_view import ApiView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kiosko - Objeto Feliz")
        self.geometry("900x600")
        self._build_ui()

    def _build_ui(self):
        # marco izquierdo (menu)
        menu_frame = tk.Frame(self, width=200, bg="#f0f0f0")
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # marco derecho (contenido)
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # botones del menu
        btn_cliente = tk.Button(menu_frame, text="Clientes", command=self.show_cliente)
        btn_producto = tk.Button(menu_frame, text="Productos", command=self.show_producto)
        btn_carrito = tk.Button(menu_frame, text="Carrito", command=self.show_carrito)
        btn_api = tk.Button(menu_frame, text="Clima (API)", command=self.show_api)

        for w in (btn_cliente, btn_producto, btn_carrito, btn_api):
            w.pack(fill=tk.X, pady=6, padx=8)

        # instancia de vistas (se crearán cuando se necesiten)
        self.current_view = None
        self.show_cliente()

    def _switch_view(self, view_class):
        # destruir vista actual
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
        # crear nueva vista
        self.current_view = view_class(self.content_frame)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_cliente(self):
        self._switch_view(ClienteView)

    def show_producto(self):
        self._switch_view(ProductoView)

    def show_carrito(self):
        self._switch_view(CarritoView)

    def show_api(self):
        self._switch_view(ApiView)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
