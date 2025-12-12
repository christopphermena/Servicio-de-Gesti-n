# main.py
"""
Punto de entrada principal del proyecto Kiosko Objeto Feliz.

Este archivo es el que se ejecuta para iniciar la aplicación.
Su función es:
- Cargar variables de entorno desde archivo .env
- Verificar conexión a Oracle XE antes de iniciar
- Iniciar la interfaz gráfica principal (Tkinter)
"""

import os
from dotenv import load_dotenv
from config.database import probar_conexion
from gui.main_window import MainWindow

def main():
    """
    Función principal que inicializa la aplicación.
    """
    # PASO 1: Cargar variables de entorno desde archivo .env
    # Estas variables contienen las credenciales de conexión a Oracle XE
    # (DB_USER, DB_PASSWORD, DB_DSN)
    load_dotenv()

    # Mensaje de bienvenida en consola
    print("===================================")
    print("  Kiosko Objeto Feliz - Iniciando ")
    print("===================================")

    # PASO 2: Verificar conexión a la base de datos Oracle XE
    # Si no hay conexión, la app funcionará en "modo memoria" (sin persistencia)
    print("Verificando conexión a la base de datos...")
    if probar_conexion():
        print("✔ Conexión exitosa a Oracle XE.")
    else:
        print("✖ No se pudo conectar a Oracle XE.")
        print("   → La aplicación continuará en 'Modo Memoria'.")
        print("   → Las operaciones CRUD NO se guardarán en la base de datos.")
        print("")

    # PASO 3: Crear e iniciar la ventana principal de la aplicación
    # MainWindow es la clase que contiene toda la interfaz gráfica
    print("Abriendo interfaz gráfica (Tkinter)...")
    app = MainWindow()  # Crea la ventana principal
    app.mainloop()  # Inicia el bucle de eventos de Tkinter (mantiene la ventana abierta)


# Punto de entrada: cuando ejecutas "python main.py", se ejecuta main()
if __name__ == "__main__":
    main()
