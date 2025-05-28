import tkinter as tk
from tkinter import ttk
import threading
import time
import requests
import os
import io
from PIL import Image, ImageTk
import logging
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener token desde variables de entorno
HF_TOKEN = os.environ.get("HF_TOKEN")
USAR_API_REAL = True  # Activa la generación real con Hugging Face

# Verificar que el token exista
if not HF_TOKEN and USAR_API_REAL:
    logging.warning("No se encontró el token HF_TOKEN en las variables de entorno. La generación de imágenes podría fallar.")

# Obtener logger
logger = logging.getLogger("SistemaExperto")

def generar_imagen_ia(root, descripcion):
    """Genera una imagen basada en la descripción usando IA"""
    # Mostrar ventana de proceso
    ventana_proceso = tk.Toplevel(root)
    ventana_proceso.title("Generando imagen...")
    ventana_proceso.geometry("400x150")
    ventana_proceso.configure(bg="#2C3E50")
    
    # Mensaje de proceso
    proceso_lbl = tk.Label(ventana_proceso, 
                         text="Generando imagen a partir de la descripción...",
                         font=("Arial", 12), bg="#2C3E50", fg="white")
    proceso_lbl.pack(pady=20)
    
    # Barra de progreso
    progreso = ttk.Progressbar(ventana_proceso, mode='indeterminate')
    progreso.pack(fill="x", padx=30, pady=10)
    progreso.start()
    
    # Elegir entre generación real o simulada
    if USAR_API_REAL:
        threading.Thread(
            target=lambda: generar_con_huggingface(ventana_proceso, progreso, root, descripcion)
        ).start()
    else:
        threading.Thread(
            target=lambda: simular_generacion(ventana_proceso, progreso, root, descripcion)
        ).start()

def generar_con_huggingface(ventana_proceso, progreso, root, descripcion):
    """Genera imagen usando la API de Hugging Face correctamente"""
    try:
        # Configurar el prompt basado en la descripción
        prompt = f"Imagen digital de un {descripcion} Vista general, colores vibrantes, detallada, 4K"
        logger.info(f"Generando imagen con prompt: {prompt}")
        
        # Importar el cliente de Gradio
        from gradio_client import Client
        
        # Crear cliente con el espacio correcto
        client = Client("stabilityai/stable-diffusion")
        
        # Realizar la petición
        result = client.predict(
            prompt=prompt,
            negative="baja calidad, pixelado, borroso, texto, marca de agua",
            scale=7.5,
            api_name="/infer"  # Usar el endpoint correcto
        )
        
        # El resultado es una lista con diccionarios que contienen 'image' (ruta) y 'caption'
        if result and len(result) > 0:
            image_path = result[0]['image']
            
            # Copiar la imagen al directorio del proyecto
            import shutil
            import os
            from datetime import datetime
            
            # Crear directorio si no existe
            os.makedirs("images", exist_ok=True)
            
            # Generar nombre con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_path = f"images/juego_{timestamp}.png"
            
            # Copiar el archivo
            shutil.copy(image_path, new_path)
            
            # Mostrar la imagen
            ventana_proceso.destroy()
            mostrar_imagen_real(root, new_path, prompt)
        else:
            logger.error("No se recibió una imagen válida de la API")
            ventana_proceso.destroy()
            mostrar_error_generacion(root, "No se generó ninguna imagen")
            
    except Exception as e:
        logger.exception(f"Error en generación de imagen: {str(e)}")
        ventana_proceso.destroy()
        mostrar_error_generacion(root, str(e))

def mostrar_imagen_real(root, imagen_path, prompt):
    """Muestra la imagen real generada por IA"""
    try:
        # Crear ventana
        ventana_img = tk.Toplevel(root)
        ventana_img.title("Imagen generada con IA")
        ventana_img.geometry("600x650")
        ventana_img.configure(bg="#2C3E50")
        
        # Cargar y mostrar la imagen
        img = Image.open(imagen_path)
        img.thumbnail((500, 500))  # Redimensionar manteniendo proporción
        
        # Convertir a formato Tkinter
        tk_img = ImageTk.PhotoImage(img)
        
        # Frame para la imagen
        img_frame = tk.Frame(ventana_img, bg="#34495E", width=520, height=520)
        img_frame.pack(pady=15)
        img_frame.pack_propagate(False)
        
        # Mostrar imagen
        img_lbl = tk.Label(img_frame, image=tk_img, bg="#34495E")
        img_lbl.image = tk_img  # Mantener referencia
        img_lbl.pack(expand=True)
        
        # Mostrar prompt utilizado
        prompt_titulo = tk.Label(ventana_img, text="Prompt utilizado:", 
                             font=("Arial", 12, "bold"), bg="#2C3E50", fg="#F39C12")
        prompt_titulo.pack(anchor="w", padx=20, pady=(10, 5))
        
        prompt_lbl = tk.Label(ventana_img, text=prompt,
                          font=("Arial", 10), bg="#2C3E50", fg="white",
                          wraplength=550, justify="left")
        prompt_lbl.pack(fill="x", padx=20)
        
        # Mostrar ruta de la imagen
        path_titulo = tk.Label(ventana_img, text="Imagen guardada en:", 
                           font=("Arial", 12, "bold"), bg="#2C3E50", fg="#F39C12")
        path_titulo.pack(anchor="w", padx=20, pady=(10, 5))
        
        path_lbl = tk.Label(ventana_img, text=imagen_path,
                        font=("Arial", 10), bg="#2C3E50", fg="white")
        path_lbl.pack(fill="x", padx=20)
        
        # Botón para cerrar
        btn_cerrar = tk.Button(ventana_img, text="Cerrar", 
                           command=ventana_img.destroy,
                           bg="#E74C3C", fg="white", padx=10)
        btn_cerrar.pack(pady=10)
        
    except Exception as e:
        # Si hay error al mostrar la imagen
        mostrar_error_generacion(root, f"Error al mostrar la imagen: {str(e)}")

def mostrar_error_generacion(root, mensaje="Error desconocido"):
    """Muestra un mensaje de error y ofrece la opción de ver una simulación"""
    ventana_error = tk.Toplevel(root)
    ventana_error.title("Error en generación de imagen")
    ventana_error.geometry("400x250")
    ventana_error.configure(bg="#2C3E50")
    
    # Icono de error
    error_lbl = tk.Label(ventana_error, text="⚠️", 
                      font=("Arial", 24), bg="#2C3E50", fg="#E74C3C")
    error_lbl.pack(pady=(20, 5))
    
    # Mensaje
    msg_lbl = tk.Label(ventana_error, 
                    text="No se pudo generar la imagen con IA.",
                    font=("Arial", 12), bg="#2C3E50", fg="white")
    msg_lbl.pack(pady=5)
    
    # Detalles del error
    detalle_lbl = tk.Label(ventana_error, 
                        text=mensaje,
                        font=("Arial", 10), bg="#2C3E50", fg="#F39C12",
                        wraplength=350)
    detalle_lbl.pack(pady=10)
    
    # Mensaje de alternativa
    alt_lbl = tk.Label(ventana_error, 
                    text="¿Deseas usar el modo de simulación?",
                    font=("Arial", 11), bg="#2C3E50", fg="white")
    alt_lbl.pack(pady=5)
    
    # Botones
    botones_frame = tk.Frame(ventana_error, bg="#2C3E50")
    botones_frame.pack(pady=10)
    
    # Botón para mostrar simulación
    btn_simular = tk.Button(botones_frame, 
                         text="Usar simulación", 
                         command=lambda: [ventana_error.destroy(), 
                                        mostrar_imagen_simulada(root, mensaje)],
                         bg="#3498DB", fg="white")
    btn_simular.pack(side="left", padx=5)
    
    # Botón para cancelar
    btn_cancelar = tk.Button(botones_frame, 
                          text="Cancelar", 
                          command=ventana_error.destroy,
                          bg="#7F8C8D", fg="white")
    btn_cancelar.pack(side="left", padx=5)

# Mantener las funciones existentes de simulación
def simular_generacion(ventana_proceso, progreso, root, descripcion):
    """Simula el proceso de generación de una imagen"""
    # Simulación de tiempo de generación
    time.sleep(2)
    progreso.stop()
    ventana_proceso.destroy()
    
    # Mostrar la imagen generada
    mostrar_imagen_simulada(root, descripcion)

def mostrar_imagen_simulada(root, descripcion):
    """Muestra una imagen simulada generada por IA"""
    ventana_img = tk.Toplevel(root)
    ventana_img.title("Imagen generada con IA")
    ventana_img.geometry("600x550")
    ventana_img.configure(bg="#2C3E50")
    
    # Frame para la imagen simulada
    img_frame = tk.Frame(ventana_img, bg="#34495E", width=500, height=300)
    img_frame.pack(pady=20, padx=20)
    img_frame.pack_propagate(False)
    
    # Simulación de imagen con texto
    txt_imagen = f"IMAGEN GENERADA POR IA\n\nBasada en:\n{descripcion}"
    img_lbl = tk.Label(img_frame, text=txt_imagen, 
                     font=("Arial", 11), bg="#34495E", fg="white",
                     wraplength=450, justify="center")
    img_lbl.pack(expand=True)
    
    # Prompt utilizado
    prompt_titulo = tk.Label(ventana_img, text="Prompt utilizado:", 
                           font=("Arial", 12, "bold"), bg="#2C3E50", fg="#F39C12")
    prompt_titulo.pack(anchor="w", padx=20, pady=(10, 5))
    
    prompt_txt = f"Imagen digital de un {descripcion} Vista general, colores vibrantes, detallada, 4K"
    prompt_lbl = tk.Label(ventana_img, text=prompt_txt,
                        font=("Arial", 10), bg="#2C3E50", fg="white",
                        wraplength=550, justify="left")
    prompt_lbl.pack(fill="x", padx=20)
    
    # Botón para cerrar
    btn_cerrar = tk.Button(ventana_img, text="Cerrar", 
                         command=ventana_img.destroy,
                         bg="#E74C3C", fg="white", padx=10)
    btn_cerrar.pack(pady=20)