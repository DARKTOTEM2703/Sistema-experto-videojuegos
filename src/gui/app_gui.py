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
                # Añadir opción para agregar conocimiento aunque haya alternativas parciales
                self._mostrar_opcion_agregar_conocimiento()
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
        
        # Botón para ver/ocultar la explicación
        self.explicacion_visible = False
        self.explicacion_frame = tk.Frame(self.resultado_frame, bg="#34495E")
        self.explicacion_frame.pack(fill="x", padx=20, pady=10)
        self.explicacion_frame.pack_forget()  # Ocultar inicialmente
        
        # Contenido de la explicación (inicialmente oculto)
        desc_title = tk.Label(
            self.explicacion_frame, 
            text="📝 EXPLICACIÓN:",
            font=("Arial", 12, "bold"), bg="#34495E", fg="#F39C12"
        )
        desc_title.pack(pady=5)
        
        desc_label = tk.Label(
            self.explicacion_frame, 
            text=descripcion,
            font=("Arial", 11), bg="#34495E", fg="white", 
            wraplength=500, justify="left"
        )
        desc_label.pack(pady=10)
        
        # Botón para mostrar/ocultar explicación
        btn_explicacion = tk.Button(
            self.resultado_frame,
            text="📝 Ver explicación",
            command=self._toggle_explicacion,
            bg="#9b59b6", fg="white", font=("Arial", 11)
        )
        btn_explicacion.pack(pady=5)
        
        # Mostrar criterios
        self._mostrar_criterios_seleccionados()

    def _toggle_explicacion(self):
        """Mostrar u ocultar la explicación"""
        if self.explicacion_visible:
            self.explicacion_frame.pack_forget()
            # Buscar y actualizar el botón con el texto correcto
            for widget in self.resultado_frame.winfo_children():
                if isinstance(widget, tk.Button) and "explicación" in widget["text"]:
                    widget.config(text="📝 Ver explicación")
                    break
        else:
            self.explicacion_frame.pack(fill="x", padx=20, pady=10)
            # Buscar y actualizar el botón con el texto correcto
            for widget in self.resultado_frame.winfo_children():
                if isinstance(widget, tk.Button) and "explicación" in widget["text"]:
                    widget.config(text="🔼 Ocultar explicación")
                    break
        
        self.explicacion_visible = not self.explicacion_visible
    
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
        
        # Crear un frame para la explicación (inicialmente oculto)
        exp_frame = tk.Frame(alt_frame, bg="#2C3E50")
        
        # Descripción
        alt_desc = tk.Label(
            exp_frame, 
            text=desc,
            font=("Arial", 10), bg="#2C3E50", fg="white", 
            wraplength=450, justify="left"
        )
        alt_desc.pack(pady=5)
        
        # Variable para controlar visibilidad
        visible = tk.BooleanVar(value=False)
        
        # Función para mostrar/ocultar explicación
        def toggle_exp():
            if visible.get():
                exp_frame.pack_forget()
                btn_exp.config(text="📝 Ver explicación")
                visible.set(False)
            else:
                exp_frame.pack(fill="x", pady=5)
                btn_exp.config(text="🔼 Ocultar explicación")
                visible.set(True)
        
        # Botón para mostrar/ocultar explicación
        btn_exp = tk.Button(
            alt_frame,
            text="📝 Ver explicación",
            command=toggle_exp,
            bg="#9b59b6", fg="white", font=("Arial", 9)
        )
        btn_exp.pack(anchor="w", pady=5)
    
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
        """Mostrar mensaje cuando no hay recomendaciones y permitir enseñar al sistema"""
        # Mensaje principal
        sin_rec = tk.Label(
            self.resultado_frame, 
            text="No encontré juegos que coincidan con estas preferencias.",
            font=("Arial", 12), bg="#34495E", fg="#E74C3C"
        )
        sin_rec.pack(pady=20)
        
        # Mostrar criterios seleccionados para que el usuario vea qué combinación no existe
        self._mostrar_criterios_seleccionados()
        
        # Mensaje invitando a enseñar al sistema
        aprender_msg = tk.Label(
            self.resultado_frame,
            text="¿Conoces algún juego que podría recomendarse con estas preferencias?\n¡Ayúdame a aprender!",
            font=("Arial", 12), bg="#34495E", fg="#F39C12",
            wraplength=500, justify="center"
        )
        aprender_msg.pack(pady=20)
        
        # Botón para enseñar al sistema
        btn_ensenar = tk.Button(
            self.resultado_frame,
            text="🧠 Enseñar al sistema",
            command=self._abrir_ventana_ensenar,
            bg="#2ECC71", fg="white", font=("Arial", 12),
            padx=10, pady=5
        )
        btn_ensenar.pack(pady=10)
    
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
    
    def _abrir_ventana_ensenar(self):
        """Abre una ventana para que el usuario enseñe al sistema un nuevo juego"""
        from tkinter import messagebox
        import json
        import os
        from datetime import datetime
        
        ventana_ensenar = tk.Toplevel(self.root)
        ventana_ensenar.title("Agregar Nuevo Juego")
        ventana_ensenar.geometry("600x450")
        ventana_ensenar.configure(bg="#2C3E50")
        
        # Título
        titulo = tk.Label(ventana_ensenar, text="Agregar nuevo juego a la base de conocimiento",
                    font=("Arial", 16, "bold"), bg="#2C3E50", fg="#ECF0F1")
        titulo.pack(pady=20)
        
        # Mostrar los parámetros seleccionados
        parametros_frame = tk.Frame(ventana_ensenar, bg="#34495E", padx=20, pady=10)
        parametros_frame.pack(fill="x", padx=20)
        
        # Título de parámetros
        param_titulo = tk.Label(parametros_frame, text="Parámetros seleccionados:",
                      font=("Arial", 12, "bold"), bg="#34495E", fg="#F39C12")
        param_titulo.pack(anchor="w", pady=(0, 10))
        
        # Obtener parámetros
        narrativa = self.respuestas['narrativa']
        estilo = self.respuestas['estilo']
        estetica = self.respuestas['estetica']
        dinamica = self.respuestas['dinamica']
        
        # Mostrar cada parámetro
        param_narrativa = tk.Label(parametros_frame, text=f"• Narrativa: {narrativa}",
                        font=("Arial", 10), bg="#34495E", fg="white")
        param_narrativa.pack(anchor="w", padx=10)
        
        param_estilo = tk.Label(parametros_frame, text=f"• Estilo de juego: {estilo}",
                      font=("Arial", 10), bg="#34495E", fg="white")
        param_estilo.pack(anchor="w", padx=10)
        
        param_estetica = tk.Label(parametros_frame, text=f"• Estética visual: {estetica}",
                        font=("Arial", 10), bg="#34495E", fg="white")
        param_estetica.pack(anchor="w", padx=10)
        
        param_dinamica = tk.Label(parametros_frame, text=f"• Dinámica: {dinamica}",
                        font=("Arial", 10), bg="#34495E", fg="white")
        param_dinamica.pack(anchor="w", padx=10)
        
        # Determinar nombre del juego automáticamente según los parámetros
        if narrativa == "Juego de Tronos":
            prefijo = "Tronos"
        elif narrativa == "Star Wars":
            prefijo = "Galaxia" 
        elif narrativa == "The Walking Dead":
            prefijo = "Cuarentena"
        elif narrativa == "Black Mirror":
            prefijo = "Realidad"
    
        if estilo == "Solo":
            sufijo = "Interior"
        elif estilo == "Con amigos":
            sufijo = "Conexión"
        elif estilo == "Competencia online":
            sufijo = "Batalla"
        elif estilo == "Explorar sin presión":
            sufijo = "Viaje"
    
        nombre_sugerido = f"{prefijo} {sufijo}"
        
        # Form para nombre y descripción
        form_frame = tk.Frame(ventana_ensenar, bg="#34495E", padx=20, pady=20)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nombre del juego (editable pero presugerido)
        nombre_frame = tk.Frame(form_frame, bg="#34495E")
        nombre_frame.pack(fill="x", pady=5)
        
        nombre_lbl = tk.Label(nombre_frame, text="Nombre del juego:",
                            font=("Arial", 11), bg="#34495E", fg="white")
        nombre_lbl.pack(side="left")
        
        nombre_var = tk.StringVar(value=nombre_sugerido)
        nombre_entry = tk.Entry(nombre_frame, textvariable=nombre_var, width=30, font=("Arial", 11))
        nombre_entry.pack(side="left", padx=10)
        
        # Campo para descripción
        desc_titulo = tk.Label(form_frame, text="Descripción del juego:",
                          font=("Arial", 12), bg="#34495E", fg="#F39C12")
        desc_titulo.pack(anchor="w", pady=(10, 5))
        
        desc_text = tk.Text(form_frame, height=6, width=50, font=("Arial", 10))
        desc_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para botones
        botones_frame = tk.Frame(ventana_ensenar, bg="#2C3E50", pady=10)
        botones_frame.pack(fill="x", side="bottom")
        
        # Función para guardar el nuevo juego
        def guardar_conocimiento():
            # Obtener nombre y descripción
            nombre_juego = nombre_var.get().strip()
            descripcion = desc_text.get("1.0", "end-1c").strip()
            
            if not nombre_juego or not descripcion:
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos")
                return
            
            # Importar el diccionario de juegos
            from data.juegos_dictionary import videojuegos
            
            # Crear clave y valor
            clave = (narrativa, estilo, estetica, dinamica)
            # Crear nombre de archivo único para la imagen futura
            nombre_archivo = f"{nombre_juego.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            valor = (nombre_juego, f"images/{nombre_archivo}.png", descripcion)
            
            # Guardar en el diccionario
            videojuegos[clave] = valor
            
            # Guardar en archivo JSON para persistencia
            self._guardar_base_conocimiento()
            
            # Cerrar ventana
            ventana_ensenar.destroy()
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Conocimiento adquirido", 
                              f"¡Gracias! He aprendido sobre el juego '{nombre_juego}'.\n"
                              "La próxima vez que selecciones estos parámetros, te recomendaré este juego.")
            
            # Actualizar la vista actual para mostrar el nuevo conocimiento
            self.generar_y_mostrar_resultados()
        
        # Botón de guardar
        btn_guardar = tk.Button(botones_frame, text="Guardar conocimiento",
                             command=guardar_conocimiento,
                             bg="#2ECC71", fg="white", font=("Arial", 11),
                             padx=10, pady=5)
        btn_guardar.pack(side="right", padx=20)
        
        # Botón cancelar
        btn_cancelar = tk.Button(botones_frame, text="Cancelar",
                           command=ventana_ensenar.destroy,
                           bg="#E74C3C", fg="white", font=("Arial", 11),
                           padx=10, pady=5)
        btn_cancelar.pack(side="left", padx=20)
    
    def _guardar_base_conocimiento(self):
        """Guardar la base de conocimiento en un archivo JSON para persistencia"""
        from data.juegos_dictionary import videojuegos
        import json
        import os
        
        # Convertir el diccionario a un formato serializable
        data = {}
        for clave, valor in videojuegos.items():
            # Convertir tupla a string para usar como clave en JSON
            str_clave = "||".join(clave)
            data[str_clave] = valor
        
        # Asegurar que el directorio data existe
        os.makedirs('data', exist_ok=True)
        
        # Guardar en archivo
        with open('data/base_conocimiento.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def _mostrar_opcion_agregar_conocimiento(self):
        """Muestra un separador y botón para agregar un juego para la combinación actual"""
        # Crear un separador visual
        separador = tk.Frame(self.resultado_frame, height=2, bg="#7f8c8d")
        separador.pack(fill="x", pady=15, padx=20)
        
        # Frame para la opción de agregar conocimiento
        agregar_frame = tk.Frame(self.resultado_frame, bg="#34495E", pady=15)
        agregar_frame.pack(fill="x", padx=20, pady=10)
        
        # Mensaje explicativo
        mensaje = tk.Label(
            agregar_frame,
            text="¿Conoces un juego que coincida exactamente con los criterios seleccionados?\n¡Ayúdame a aprender!",
            font=("Arial", 12), bg="#34495E", fg="#F39C12",
            wraplength=500, justify="center"
        )
        mensaje.pack(pady=10)
        
        # Botón para agregar conocimiento
        btn_agregar = tk.Button(
            agregar_frame,
            text="🧠 Agregar un juego para esta combinación exacta",
            command=self._abrir_ventana_ensenar,
            bg="#2ECC71", fg="white", font=("Arial", 11),
            padx=10, pady=5
        )
        btn_agregar.pack(pady=10)