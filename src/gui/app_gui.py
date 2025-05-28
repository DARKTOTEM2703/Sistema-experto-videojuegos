import tkinter as tk
from tkinter import ttk, messagebox

from gui.frames import (
    crear_frame_bienvenida,
    crear_frame_narrativa,
    crear_frame_estilo,
    crear_frame_estetica,
    crear_frame_dinamica,
    crear_frame_resultados
)
from expert_system.inference_engine import buscar_recomendacion, buscar_alternativas
from image_generation.image_generator import generar_imagen_ia

class SistemaExpertoApp:
    def __init__(self):
        # Configuración principal de la ventana
        self.root = tk.Tk()
        self.root.title("Sistema Experto - Recomendación de Videojuegos")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")
        
        # Variables para almacenar respuestas
        self.respuestas = {}
        self.frame_actual = 0
        self.frames = []
        
        # Variables para opciones seleccionadas
        self.var_narrativa = tk.StringVar()
        self.var_estilo = tk.StringVar()
        self.var_estetica = tk.StringVar()
        self.var_dinamica = tk.StringVar()
        
        # Frame para resultados (se inicializa en crear_frame_resultados)
        self.resultado_frame = None
        
        # Crear y configurar todos los frames
        self.crear_frames()
        self.mostrar_frame(0)
    
    def crear_frames(self):
        """Crear todos los frames del sistema"""
        self.frames = [
            crear_frame_bienvenida(self),
            crear_frame_narrativa(self),
            crear_frame_estilo(self),
            crear_frame_estetica(self),
            crear_frame_dinamica(self),
            crear_frame_resultados(self)
        ]
    
    def mostrar_frame(self, indice):
        """Mostrar un frame específico"""
        # Ocultar todos los frames
        for frame in self.frames:
            frame.pack_forget()
        
        # Mostrar el frame actual
        if 0 <= indice < len(self.frames):
            self.frame_actual = indice
            self.frames[indice].pack(fill="both", expand=True, padx=20, pady=20)
            
            # Si es el frame de resultados, generar las recomendaciones
            if indice == 5:
                self.generar_y_mostrar_resultados()
    
    def siguiente_frame(self):
        """Ir al siguiente frame"""
        # Validar respuestas antes de avanzar
        if self.frame_actual == 1 and not self.var_narrativa.get():
            messagebox.showwarning("Atención", "Por favor selecciona un tipo de narrativa")
            return
        elif self.frame_actual == 2 and not self.var_estilo.get():
            messagebox.showwarning("Atención", "Por favor selecciona un estilo de juego")
            return
        elif self.frame_actual == 3 and not self.var_estetica.get():
            messagebox.showwarning("Atención", "Por favor selecciona una estética visual")
            return
        elif self.frame_actual == 4 and not self.var_dinamica.get():
            messagebox.showwarning("Atención", "Por favor selecciona una dinámica de juego")
            return
        
        # Guardar respuestas
        if self.frame_actual == 1:
            self.respuestas['narrativa'] = self.var_narrativa.get()
        elif self.frame_actual == 2:
            self.respuestas['estilo'] = self.var_estilo.get()
        elif self.frame_actual == 3:
            self.respuestas['estetica'] = self.var_estetica.get()
        elif self.frame_actual == 4:
            self.respuestas['dinamica'] = self.var_dinamica.get()
        
        if self.frame_actual < len(self.frames) - 1:
            self.mostrar_frame(self.frame_actual + 1)
    
    def anterior_frame(self):
        """Ir al frame anterior"""
        if self.frame_actual > 0:
            self.mostrar_frame(self.frame_actual - 1)
    
    def generar_y_mostrar_resultados(self):
        """Mostrar resultados basados en las selecciones del usuario"""
        # Limpiar frame de resultados
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()
        
        # Construir clave para buscar
        clave = (
            self.respuestas['narrativa'],
            self.respuestas['estilo'], 
            self.respuestas['estetica'], 
            self.respuestas['dinamica']
        )
        
        # Buscar recomendación exacta
        recomendacion = buscar_recomendacion(clave)
        
        if recomendacion:
            self._mostrar_recomendacion_principal(recomendacion)
        else:
            # Buscar alternativas
            alternativas = buscar_alternativas(clave)
            
            if alternativas:
                self._mostrar_alternativas(alternativas)
            else:
                self._mostrar_sin_recomendaciones()
    
    def _mostrar_recomendacion_principal(self, recomendacion):
        """Mostrar la recomendación principal"""
        nombre_juego, url_imagen, descripcion = recomendacion
        
        # Título
        titulo_principal = tk.Label(self.resultado_frame, text="🎯 RECOMENDACIÓN PRINCIPAL:",
                                  font=("Arial", 14, "bold"), bg="#34495E", fg="#F39C12")
        titulo_principal.pack(pady=10)
        
        # Nombre juego
        nombre_label = tk.Label(self.resultado_frame, text=nombre_juego,
                              font=("Arial", 13, "bold"), bg="#34495E", fg="#2ECC71")
        nombre_label.pack(pady=5)
        
        # Frame para imagen
        img_frame = tk.Frame(self.resultado_frame, bg="#2C3E50", width=300, height=200)
        img_frame.pack(pady=15)
        img_frame.pack_propagate(False)
        
        img_placeholder = tk.Label(img_frame, text="🎮\n[Imagen del juego]", 
                                 font=("Arial", 14), bg="#2C3E50", fg="white")
        img_placeholder.pack(expand=True)
        
        # Botón para generar imagen
        btn_generar_img = tk.Button(
            self.resultado_frame, 
            text="🖼️ Generar imagen con IA", 
            command=lambda desc=descripcion: generar_imagen_ia(self.root, desc),
            bg="#3498DB", fg="white", font=("Arial", 11), padx=10
        )
        btn_generar_img.pack(pady=10)
        
        # Descripción
        self._mostrar_descripcion(descripcion)
        
        # Mostrar criterios
        self._mostrar_criterios_seleccionados()
    
    def _mostrar_alternativas(self, alternativas):
        """Mostrar recomendaciones alternativas"""
        # Mensaje sin coincidencia exacta
        no_exacto = tk.Label(
            self.resultado_frame, 
            text="No se encontró una coincidencia exacta con tus preferencias.",
            font=("Arial", 12), bg="#34495E", fg="#E74C3C"
        )
        no_exacto.pack(pady=10)
        
        # Título alternativas
        alt_titulo = tk.Label(
            self.resultado_frame, 
            text="🎮 RECOMENDACIONES SUGERIDAS:",
            font=("Arial", 14, "bold"), bg="#34495E", fg="#F39C12"
        )
        alt_titulo.pack(pady=10)
        
        # Mostrar cada alternativa
        for i, (nombre, imagen, desc, coincidencias) in enumerate(alternativas[:3]):
            self._mostrar_alternativa_individual(i, nombre, imagen, desc, coincidencias)
    
    def _mostrar_alternativa_individual(self, indice, nombre, imagen, desc, coincidencias):
        """Mostrar una alternativa individual"""
        # Frame para la alternativa
        alt_frame = tk.Frame(self.resultado_frame, bg="#2C3E50", padx=15, pady=10)
        alt_frame.pack(fill="x", pady=10, padx=20)
        
        # Nombre
        alt_nombre = tk.Label(
            alt_frame, 
            text=f"{indice+1}. {nombre}",
            font=("Arial", 12, "bold"), bg="#2C3E50", fg="#F39C12"
        )
        alt_nombre.pack(anchor="w")
        
        # Descripción
        alt_desc = tk.Label(
            alt_frame, 
            text=desc,
            font=("Arial", 10), bg="#2C3E50", fg="white", 
            wraplength=450, justify="left"
        )
        alt_desc.pack(anchor="w", pady=5)
        
        # Coincidencias
        alt_coinc = tk.Label(
            alt_frame, 
            text=f"Coincidencias: {coincidencias}/4 criterios",
            font=("Arial", 9), bg="#2C3E50", fg="#2ECC71"
        )
        alt_coinc.pack(anchor="w")
        
        # Botón para generar imagen
        btn_img = tk.Button(
            alt_frame, 
            text="🖼️ Generar imagen", 
            command=lambda d=desc: generar_imagen_ia(self.root, d),
            bg="#3498DB", fg="white", font=("Arial", 9)
        )
        btn_img.pack(anchor="e", pady=5)
    
    def _mostrar_descripcion(self, descripcion):
        """Mostrar la descripción del juego"""
        desc_title = tk.Label(
            self.resultado_frame, 
            text="📝 DESCRIPCIÓN:",
            font=("Arial", 12, "bold"), bg="#34495E", fg="#F39C12"
        )
        desc_title.pack(pady=5)
        
        desc_label = tk.Label(
            self.resultado_frame, 
            text=descripcion,
            font=("Arial", 11), bg="#34495E", fg="white", 
            wraplength=500, justify="left"
        )
        desc_label.pack(pady=10, padx=20)
    
    def _mostrar_criterios_seleccionados(self):
        """Mostrar los criterios seleccionados por el usuario"""
        criterios_titulo = tk.Label(
            self.resultado_frame, 
            text="🔍 CRITERIOS SELECCIONADOS:",
            font=("Arial", 12, "bold"), bg="#34495E", fg="#F39C12"
        )
        criterios_titulo.pack(pady=(20, 5))
        
        criterios = [
            f"🎭 Narrativa: {self.respuestas['narrativa']}",
            f"👥 Estilo de juego: {self.respuestas['estilo']}",
            f"🎨 Estética visual: {self.respuestas['estetica']}",
            f"⚡ Dinámica: {self.respuestas['dinamica']}"
        ]
        
        for criterio in criterios:
            crit_label = tk.Label(
                self.resultado_frame, 
                text=criterio,
                font=("Arial", 11), bg="#34495E", fg="white"
            )
            crit_label.pack(pady=2, padx=20, anchor="w")
    
    def _mostrar_sin_recomendaciones(self):
        """Mostrar mensaje cuando no hay recomendaciones"""
        sin_rec = tk.Label(
            self.resultado_frame, 
            text="Lo siento, no se encontraron juegos que coincidan con tus preferencias.",
            font=("Arial", 12), bg="#34495E", fg="#E74C3C"
        )
        sin_rec.pack(pady=20)
    
    def reiniciar_sistema(self):
        """Reiniciar el sistema para una nueva consulta"""
        self.respuestas = {}
        self.var_narrativa.set("")
        self.var_estilo.set("")
        self.var_estetica.set("")
        self.var_dinamica.set("")
        self.mostrar_frame(0)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()