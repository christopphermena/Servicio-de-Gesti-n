# gui/api_view.py
import tkinter as tk
from tkinter import messagebox
from api.weather_api import get_weather_by_city

class ApiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="Ciudad:").grid(row=0, column=0)
        self.e_ciudad = tk.Entry(top, width=20)
        self.e_ciudad.grid(row=0, column=1, padx=6)

        btn_get = tk.Button(top, text="Obtener Clima", command=self.obtener_clima)
        btn_get.grid(row=0, column=2, padx=6)

        self.txt = tk.Text(self, height=10)
        self.txt.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

    def obtener_clima(self):
        ciudad = self.e_ciudad.get().strip()
        if not ciudad:
            messagebox.showwarning("Validación", "Ingrese ciudad")
            return
        data = get_weather_by_city(ciudad)
        self.txt.delete("1.0", tk.END)
        lines = [
            f"Ciudad: {data.get('city')}",
            f"Temperatura: {data.get('temp')}",
            f"Descripción: {data.get('description')}",
            f"Humedad: {data.get('humidity')}",
        ]
        self.txt.insert(tk.END, "\n".join(lines))
