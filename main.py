# main.py
"""
Punto de entrada principal del proyecto Kiosko Objeto Feliz.

- Carga variables de entorno
- Verifica conexión a Oracle XE
- Inicia la GUI principal (Tkinter)
"""

import os
from dotenv import load_dotenv
from config.database import probar_conexion
from gui.main_window import MainWindow

def main():
    # Cargar variables de entorno
    load_dotenv()

    print("===================================")
    print("  Kiosko Objeto Feliz - Iniciando ")
    print("===================================")

    # Verificar BD antes de lanzar GUI
    print("Verificando conexión a la base de datos...")
    if probar_conexion():
        print("✔ Conexión exitosa a Oracle XE.")
    else:
        print("✖ No se pudo conectar a Oracle XE.")
        print("   → La aplicación continuará en 'Modo Memoria'.")
        print("   → Las operaciones CRUD NO se guardarán en la base de datos.")
        print("")

    # Lanzar GUI
    print("Abriendo interfaz gráfica (Tkinter)...")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
