# gui/api_view.py
"""
Vista para mostrar información del clima y APIs externas
HERENCIA: Hereda de tk.Frame.
DEPENDENCIA: Usa funciones de las APIs weather y currency
"""
import tkinter as tk
from tkinter import messagebox
from api.weather_api import get_weather_data

class ApiView(tk.Frame):
    """
    Vista para mostrar información del clima y APIs externas
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(top, text="Ciudad:").grid(row=0, column=0, sticky=tk.W)
        self.e_city = tk.Entry(top, width=22)
        self.e_city.grid(row=0, column=1, padx=6)
        btn_weather = tk.Button(top, text="Consultar Clima", command=self.buscar_weather)
        btn_weather.grid(row=0, column=2, padx=6)

        self.result = tk.Label(self, text="", anchor="w", justify=tk.LEFT)
        self.result.pack(fill=tk.X, padx=12, pady=8)

    def buscar_weather(self):
        city = self.e_city.get().strip()
        if not city:
            messagebox.showwarning("Validación", "Debe ingresar una ciudad")
            return
        try:
            data = get_weather_data(city)
            txt = f"Temp: {data['temp']}°C | {data['desc']}\nCiudad: {city.title()}"
            self.result.config(text=txt)
        except Exception as e:
            self.result.config(text="No se pudo obtener el clima: " + str(e))
