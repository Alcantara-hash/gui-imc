import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import sys
import csv

# Obtener la ruta del archivo ejecutable o del script
def resource_path(relative_path):
    """Obtiene la ruta absoluta, considerando el empaquetado con PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Aplicacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Aplicación de IMC")
        self.x = 900
        self.y = 550
        self.ventana.geometry(f"{self.x}x{self.y}")

        icono = PhotoImage(file= resource_path('img/imc-1.png'))
        self.ventana.iconphoto(True, icono)

        # Colores verdosos intensos
        self.color_verde_fondo = "#288316"
        self.color_verde_texto = "white"

        # Bloquear redimensionamiento de la ventana
        self.ventana.resizable(False, False)

        # Crear frame principal
        self.frame_principal = tk.Frame(self.ventana)
        self.frame_principal.pack(fill="both", expand=True)

        # Mostrar la pantalla de bienvenida
        self.mostrar_bienvenida()

    def mostrar_bienvenida(self):
        # Limpiar el frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Cargar imagen de fondo
        imagen_fondo_path = resource_path("img/background.jpeg")
        imagen_fondo = Image.open(imagen_fondo_path)
        imagen_fondo = imagen_fondo.resize((self.x, self.y))
        imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

        # Mostrar imagen de fondo
        label_fondo = tk.Label(self.frame_principal, image=imagen_fondo)
        label_fondo.image = imagen_fondo  # Guardar referencia para evitar que se recoja basura
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.lower()

        # Resto de contenido
        label_bienvenida = tk.Label(self.frame_principal, text="¡Bienvenido a nuestra aplicación!", font=("Arial", 16), bg=self.color_verde_fondo, fg=self.color_verde_texto)
        label_bienvenida.pack(pady=20)

        button_abrir_calculadora = tk.Button(self.frame_principal, text="Abrir Calculadora de IMC", command=self.mostrar_calculadora_imc, font=("Arial", 12), bg=self.color_verde_fondo, fg=self.color_verde_texto, cursor="hand2")
        button_abrir_calculadora.pack(pady=10)

    def mostrar_calculadora_imc(self):
        # Limpiar el frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Colores verdosos intensos para la calculadora
        color_verde_fondo = "#288316"
        color_verde_texto = "black"

        # Cargar imagen de fondo
        imagen_fondo_path = resource_path("img/banner.png")
        imagen_fondo = Image.open(imagen_fondo_path)
        imagen_fondo = imagen_fondo.resize((self.x, self.y))
        imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

        # Mostrar imagen de fondo
        label_fondo = tk.Label(self.frame_principal, image=imagen_fondo)
        label_fondo.image = imagen_fondo  # Guardar referencia para evitar que se recoja basura
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.lower()

        label_bienvenida = tk.Label(self.frame_principal, text="Bienvenido a la Calculadora de IMC", font=("Arial", 16), fg=color_verde_texto)
        label_bienvenida.pack(pady=20)

        label_nombre = tk.Label(self.frame_principal, text="Nombre:", font=("Arial", 12), fg=color_verde_texto)
        label_nombre.pack(pady=5)
        self.entry_nombre = tk.Entry(self.frame_principal, font=("Arial", 12))
        self.entry_nombre.pack()

        label_apellido = tk.Label(self.frame_principal, text="Apellido:", font=("Arial", 12), fg=color_verde_texto)
        label_apellido.pack(pady=5)
        self.entry_apellido = tk.Entry(self.frame_principal, font=("Arial", 12))
        self.entry_apellido.pack()

        label_edad = tk.Label(self.frame_principal, text="Edad:", font=("Arial", 12), fg=color_verde_texto)
        label_edad.pack(pady=5)
        self.entry_edad = tk.Entry(self.frame_principal, font=("Arial", 12))
        self.entry_edad.pack()

        label_peso = tk.Label(self.frame_principal, text="Peso (kg):", font=("Arial", 12), fg=color_verde_texto)
        label_peso.pack(pady=5)
        self.entry_peso = tk.Entry(self.frame_principal, font=("Arial", 12))
        self.entry_peso.pack()

        label_altura = tk.Label(self.frame_principal, text="Altura (m):", font=("Arial", 12), fg=color_verde_texto)
        label_altura.pack(pady=5)
        self.entry_altura = tk.Entry(self.frame_principal, font=("Arial", 12))
        self.entry_altura.pack()

        # Botón Calcular IMC con imagen
        image_calcular_path = resource_path("img/imc.png")
        image_calcular = tk.PhotoImage(file=image_calcular_path)
        image_calcular = image_calcular.subsample(12, 12)

        button_calcular = tk.Button(self.frame_principal, text="Calcular IMC", command=self.calcular_imc, font=("Arial", 12), bg=color_verde_fondo, fg=color_verde_texto, cursor="hand2", image=image_calcular)
        button_calcular.image = image_calcular
        button_calcular.pack(pady=10)

        self.label_resultado = tk.Label(self.frame_principal, text="", font=("Arial", 12), fg=color_verde_texto)
        self.label_resultado.pack(pady=20)

        # Botón para ver el archivo CSV
        button_ver_csv = tk.Button(self.frame_principal, text="Ver archivo CSV", command=self.ver_archivo_csv, font=("Arial", 12), bg=color_verde_fondo, fg=color_verde_texto, cursor="hand2")
        button_ver_csv.pack(pady=10)

    def calcular_imc(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        edad_str = self.entry_edad.get()
        peso_str = self.entry_peso.get()
        altura_str = self.entry_altura.get()

        try:
            edad = int(edad_str)
            peso = float(peso_str)
            altura = float(altura_str)
        except ValueError:
            self.label_resultado.config(text="Error: Ingresa valores válidos para nombre, apellido, edad, peso y altura.", fg="red")
            return

        if peso <= 0 or altura <= 0 or edad <= 0:
            self.label_resultado.config(text="Error: Peso, altura y edad deben ser mayores que cero.", fg="red")
        else:
            imc = peso / (altura ** 2)
            self.label_resultado.config(text=f"Tu IMC es: {imc:.2f}", fg="blue")
            self.guardar_datos_csv(nombre, apellido, edad, peso, altura, imc)

    def guardar_datos_csv(self, nombre, apellido, edad, peso, altura, imc):
        with open('resultados_imc.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nombre, apellido, edad, peso, altura, imc])

    def ver_archivo_csv(self):
        try:
            os.startfile('resultados_imc.csv')
        except Exception as e:
            self.label_resultado.config(text=f"Error al abrir el archivo CSV: {str(e)}", fg="red")

if __name__ == "__main__":
    app = Aplicacion()
    app.ventana.mainloop()
