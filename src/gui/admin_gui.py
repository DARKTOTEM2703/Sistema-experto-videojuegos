import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from data.juegos_dictionary import videojuegos

class InterfazExperto:
    def __init__(self, root=None):
        # Si no se proporciona una ventana, crear una nueva
        self.es_ventana_independiente = root is None
        if self.es_ventana_independiente:
            self.root = tk.Tk()
            self.root.title("Modo Experto - Administración de Conocimiento")
            self.root.geometry("900x600")
            self.root.configure(bg="#2C3E50")
        else:
            self.root = tk.Toplevel(root)
            self.root.title("Modo Experto - Administración de Conocimiento")
            self.root.geometry("900x600")
            self.root.configure(bg="#2C3E50")
        
        # Título principal
        titulo = tk.Label(self.root, text="Administración de Base de Conocimiento", 
                         font=("Arial", 16, "bold"), bg="#2C3E50", fg="#ECF0F1")
        titulo.pack(pady=20)
        
        # Frame principal con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Pestaña: Añadir nuevo conocimiento
        self.tab_add = tk.Frame(self.notebook, bg="#34495E")
        self.notebook.add(self.tab_add, text="Añadir Conocimiento")
        
        # Pestaña: Ver/Editar conocimiento existente
        self.tab_view = tk.Frame(self.notebook, bg="#34495E")
        self.notebook.add(self.tab_view, text="Ver/Editar Conocimiento")
        
        # Pestaña: Estadísticas
        self.tab_stats = tk.Frame(self.notebook, bg="#34495E")
        self.notebook.add(self.tab_stats, text="Estadísticas")
        
        # Configurar las pestañas
        self._configurar_tab_add()
        self._configurar_tab_view()
        self._configurar_tab_stats()
        
    def _configurar_tab_add(self):
        """Configurar la pestaña de añadir nuevo conocimiento"""
        # Frame para el formulario
        form_frame = tk.Frame(self.tab_add, bg="#34495E", pady=20)
        form_frame.pack(fill="both", expand=True, padx=20)
        
        # Variables para almacenar valores
        self.var_narrativa = tk.StringVar()
        self.var_estilo = tk.StringVar()
        self.var_estetica = tk.StringVar()
        self.var_dinamica = tk.StringVar()
        self.var_nombre = tk.StringVar()
        
        # Opciones disponibles
        opciones_narrativa = ["Juego de Tronos", "Star Wars", "The Walking Dead", "Black Mirror"]
        opciones_estilo = ["Solo", "Con amigos", "Competencia online", "Explorar sin presión"]
        opciones_estetica = ["Animación", "Realismo", "Mezcla estilizada", "Arte abstracto"]
        opciones_dinamica = ["Toma de decisiones", "Supervivencia", "Misterio/Investigación", "Aventura/Descubrimiento"]
        
        # Crear campos del formulario
        campos = [
            {"label": "Narrativa:", "var": self.var_narrativa, "options": opciones_narrativa},
            {"label": "Estilo de Juego:", "var": self.var_estilo, "options": opciones_estilo},
            {"label": "Estética Visual:", "var": self.var_estetica, "options": opciones_estetica},
            {"label": "Dinámica:", "var": self.var_dinamica, "options": opciones_dinamica},
        ]
        
        # Crear los dropdown para cada campo
        for i, campo in enumerate(campos):
            # Label
            lbl = tk.Label(form_frame, text=campo["label"], 
                         font=("Arial", 12), bg="#34495E", fg="white")
            lbl.grid(row=i, column=0, sticky="w", padx=10, pady=10)
            
            # Dropdown
            dropdown = ttk.Combobox(form_frame, textvariable=campo["var"], 
                                   values=campo["options"],
                                   width=30, font=("Arial", 11))
            dropdown.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            
        # Nombre del juego
        lbl_nombre = tk.Label(form_frame, text="Nombre del Juego:", 
                            font=("Arial", 12), bg="#34495E", fg="white")
        lbl_nombre.grid(row=len(campos), column=0, sticky="w", padx=10, pady=10)
        
        entry_nombre = tk.Entry(form_frame, textvariable=self.var_nombre, 
                              width=32, font=("Arial", 11))
        entry_nombre.grid(row=len(campos), column=1, sticky="w", padx=10, pady=10)
        
        # Descripción del juego
        lbl_desc = tk.Label(form_frame, text="Descripción:", 
                          font=("Arial", 12), bg="#34495E", fg="white")
        lbl_desc.grid(row=len(campos)+1, column=0, sticky="nw", padx=10, pady=10)
        
        self.txt_descripcion = tk.Text(form_frame, height=5, width=40, 
                                     font=("Arial", 11))
        self.txt_descripcion.grid(row=len(campos)+1, column=1, sticky="w", 
                                padx=10, pady=10)
        
        # Botones
        btn_frame = tk.Frame(form_frame, bg="#34495E")
        btn_frame.grid(row=len(campos)+2, column=0, columnspan=2, pady=20)
        
        btn_guardar = tk.Button(btn_frame, text="Guardar Conocimiento", 
                              command=self._guardar_conocimiento,
                              bg="#2ECC71", fg="white", font=("Arial", 12),
                              padx=10, pady=5)
        btn_guardar.pack(side="left", padx=10)
        
        btn_limpiar = tk.Button(btn_frame, text="Limpiar Formulario", 
                              command=self._limpiar_formulario,
                              bg="#E74C3C", fg="white", font=("Arial", 12),
                              padx=10, pady=5)
        btn_limpiar.pack(side="left", padx=10)
    
    def _configurar_tab_view(self):
        """Configurar la pestaña de ver/editar conocimiento existente"""
        # Frame para la búsqueda
        search_frame = tk.Frame(self.tab_view, bg="#34495E", pady=10)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        lbl_search = tk.Label(search_frame, text="Buscar:", 
                            font=("Arial", 12), bg="#34495E", fg="white")
        lbl_search.pack(side="left", padx=5)
        
        self.var_search = tk.StringVar()
        entry_search = tk.Entry(search_frame, textvariable=self.var_search, 
                              width=40, font=("Arial", 11))
        entry_search.pack(side="left", padx=5)
        
        btn_search = tk.Button(search_frame, text="Buscar", 
                             command=self._buscar_conocimiento,
                             bg="#3498DB", fg="white", font=("Arial", 11))
        btn_search.pack(side="left", padx=5)
        
        # Frame para la lista de conocimientos
        list_frame = tk.Frame(self.tab_view, bg="#34495E")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tabla de conocimientos
        columns = ("Narrativa", "Estilo", "Estética", "Dinámica", "Juego")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Colocar elementos
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para botones de acción
        actions_frame = tk.Frame(self.tab_view, bg="#34495E", pady=10)
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        btn_edit = tk.Button(actions_frame, text="Editar Seleccionado", 
                           command=self._editar_conocimiento,
                           bg="#F39C12", fg="white", font=("Arial", 11),
                           padx=10, pady=5)
        btn_edit.pack(side="left", padx=10)
        
        btn_delete = tk.Button(actions_frame, text="Eliminar Seleccionado", 
                             command=self._eliminar_conocimiento,
                             bg="#E74C3C", fg="white", font=("Arial", 11),
                             padx=10, pady=5)
        btn_delete.pack(side="left", padx=10)
        
        # Cargar datos iniciales
        self._cargar_conocimientos()
    
    def _configurar_tab_stats(self):
        """Configurar la pestaña de estadísticas"""
        stats_frame = tk.Frame(self.tab_stats, bg="#34495E", pady=20)
        stats_frame.pack(fill="both", expand=True, padx=20)
        
        # Título
        title = tk.Label(stats_frame, text="Estadísticas de la Base de Conocimiento", 
                        font=("Arial", 14, "bold"), bg="#34495E", fg="#ECF0F1")
        title.pack(pady=10)
        
        # Frame para las estadísticas
        info_frame = tk.Frame(stats_frame, bg="#2C3E50", padx=20, pady=20)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Calcular estadísticas
        total = len(videojuegos)
        por_narrativa = self._contar_por_categoria(0)
        por_estilo = self._contar_por_categoria(1)
        por_estetica = self._contar_por_categoria(2)
        por_dinamica = self._contar_por_categoria(3)
        
        # Mostrar estadísticas
        stats = [
            f"Total de reglas: {total}",
            f"\nReglas por narrativa:",
            *[f"  • {k}: {v}" for k, v in por_narrativa.items()],
            f"\nReglas por estilo de juego:",
            *[f"  • {k}: {v}" for k, v in por_estilo.items()],
            f"\nReglas por estética:",
            *[f"  • {k}: {v}" for k, v in por_estetica.items()],
            f"\nReglas por dinámica:",
            *[f"  • {k}: {v}" for k, v in por_dinamica.items()],
        ]
        
        stats_text = "\n".join(stats)
        
        # Mostrar en un widget de texto
        txt_stats = tk.Text(info_frame, height=20, width=50, 
                          font=("Arial", 12), bg="#2C3E50", fg="white",
                          wrap="word")
        txt_stats.insert("1.0", stats_text)
        txt_stats.config(state="disabled")  # Solo lectura
        txt_stats.pack(fill="both", expand=True)
    
    def _contar_por_categoria(self, indice):
        """Contar reglas por categoría según el índice (0=narrativa, 1=estilo, etc.)"""
        contador = {}
        for clave in videojuegos.keys():
            categoria = clave[indice]
            contador[categoria] = contador.get(categoria, 0) + 1
        return contador
    
    def _guardar_conocimiento(self):
        """Guardar nuevo conocimiento en la base de conocimiento"""
        # Validar campos obligatorios
        narrativa = self.var_narrativa.get()
        estilo = self.var_estilo.get()
        estetica = self.var_estetica.get()
        dinamica = self.var_dinamica.get()
        nombre = self.var_nombre.get()
        descripcion = self.txt_descripcion.get("1.0", "end-1c")
        
        if not all([narrativa, estilo, estetica, dinamica, nombre, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Crear la clave y el valor
        clave = (narrativa, estilo, estetica, dinamica)
        url_imagen = f"https://example.com/images/{nombre.lower().replace(' ', '_')}.jpg"
        valor = (nombre, url_imagen, descripcion)
        
        # Verificar si ya existe
        if clave in videojuegos:
            respuesta = messagebox.askyesno("Confirmación", 
                                         "Esta combinación ya existe. ¿Deseas sobrescribirla?")
            if not respuesta:
                return
        
        # Guardar en la base de conocimiento
        videojuegos[clave] = valor
        
        # También guardar en un archivo JSON de respaldo
        self._guardar_en_json()
        
        messagebox.showinfo("Éxito", "Conocimiento guardado exitosamente")
        self._limpiar_formulario()
        
        # Actualizar la vista de conocimientos
        if self.notebook.index("current") != 0:  # Si no estamos en la pestaña añadir
            self._cargar_conocimientos()
    
    def _limpiar_formulario(self):
        """Limpiar los campos del formulario"""
        self.var_narrativa.set("")
        self.var_estilo.set("")
        self.var_estetica.set("")
        self.var_dinamica.set("")
        self.var_nombre.set("")
        self.txt_descripcion.delete("1.0", "end")
    
    def _cargar_conocimientos(self):
        """Cargar todos los conocimientos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar datos
        for clave, valor in videojuegos.items():
            narrativa, estilo, estetica, dinamica = clave
            nombre, _, _ = valor
            self.tree.insert("", "end", values=(narrativa, estilo, estetica, dinamica, nombre))
    
    def _buscar_conocimiento(self):
        """Buscar conocimiento según el texto ingresado"""
        busqueda = self.var_search.get().lower()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtrar y mostrar resultados
        for clave, valor in videojuegos.items():
            narrativa, estilo, estetica, dinamica = clave
            nombre, _, descripcion = valor
            
            # Buscar en todos los campos
            if (busqueda in narrativa.lower() or busqueda in estilo.lower() or
                busqueda in estetica.lower() or busqueda in dinamica.lower() or
                busqueda in nombre.lower() or busqueda in descripcion.lower()):
                self.tree.insert("", "end", values=(narrativa, estilo, estetica, dinamica, nombre))
    
    def _editar_conocimiento(self):
        """Editar el conocimiento seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Información", "Por favor selecciona un conocimiento para editar")
            return
        
        # Obtener datos del ítem seleccionado
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Crear ventana de edición
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Conocimiento")
        edit_window.geometry("700x500")
        edit_window.configure(bg="#2C3E50")
        
        # Variables para los campos
        var_narrativa = tk.StringVar(value=values[0])
        var_estilo = tk.StringVar(value=values[1])
        var_estetica = tk.StringVar(value=values[2])
        var_dinamica = tk.StringVar(value=values[3])
        var_nombre = tk.StringVar(value=values[4])
        
        # Obtener la descripción completa
        clave_original = (values[0], values[1], values[2], values[3])
        _, _, descripcion = videojuegos.get(clave_original, ("", "", ""))
        
        # Crear formulario
        form_frame = tk.Frame(edit_window, bg="#34495E", pady=20)
        form_frame.pack(fill="both", expand=True, padx=20)
        
        # Opciones disponibles
        opciones_narrativa = ["Juego de Tronos", "Star Wars", "The Walking Dead", "Black Mirror"]
        opciones_estilo = ["Solo", "Con amigos", "Competencia online", "Explorar sin presión"]
        opciones_estetica = ["Animación", "Realismo", "Mezcla estilizada", "Arte abstracto"]
        opciones_dinamica = ["Toma de decisiones", "Supervivencia", "Misterio/Investigación", "Aventura/Descubrimiento"]
        
        # Crear campos
        campos = [
            {"label": "Narrativa:", "var": var_narrativa, "options": opciones_narrativa},
            {"label": "Estilo de Juego:", "var": var_estilo, "options": opciones_estilo},
            {"label": "Estética Visual:", "var": var_estetica, "options": opciones_estetica},
            {"label": "Dinámica:", "var": var_dinamica, "options": opciones_dinamica},
        ]
        
        for i, campo in enumerate(campos):
            lbl = tk.Label(form_frame, text=campo["label"], 
                         font=("Arial", 12), bg="#34495E", fg="white")
            lbl.grid(row=i, column=0, sticky="w", padx=10, pady=10)
            
            dropdown = ttk.Combobox(form_frame, textvariable=campo["var"], 
                                   values=campo["options"],
                                   width=30, font=("Arial", 11))
            dropdown.grid(row=i, column=1, sticky="w", padx=10, pady=10)
        
        # Nombre
        lbl_nombre = tk.Label(form_frame, text="Nombre del Juego:", 
                            font=("Arial", 12), bg="#34495E", fg="white")
        lbl_nombre.grid(row=len(campos), column=0, sticky="w", padx=10, pady=10)
        
        entry_nombre = tk.Entry(form_frame, textvariable=var_nombre, 
                              width=32, font=("Arial", 11))
        entry_nombre.grid(row=len(campos), column=1, sticky="w", padx=10, pady=10)
        
        # Descripción
        lbl_desc = tk.Label(form_frame, text="Descripción:", 
                          font=("Arial", 12), bg="#34495E", fg="white")
        lbl_desc.grid(row=len(campos)+1, column=0, sticky="nw", padx=10, pady=10)
        
        txt_descripcion = tk.Text(form_frame, height=5, width=40, 
                                font=("Arial", 11))
        txt_descripcion.grid(row=len(campos)+1, column=1, sticky="w", 
                           padx=10, pady=10)
        txt_descripcion.insert("1.0", descripcion)
        
        # Botones
        btn_frame = tk.Frame(form_frame, bg="#34495E")
        btn_frame.grid(row=len(campos)+2, column=0, columnspan=2, pady=20)
        
        # Función para guardar cambios
        def guardar_cambios():
            # Obtener valores actualizados
            nueva_narrativa = var_narrativa.get()
            nuevo_estilo = var_estilo.get()
            nueva_estetica = var_estetica.get()
            nueva_dinamica = var_dinamica.get()
            nuevo_nombre = var_nombre.get()
            nueva_descripcion = txt_descripcion.get("1.0", "end-1c")
            
            if not all([nueva_narrativa, nuevo_estilo, nueva_estetica, nueva_dinamica, nuevo_nombre, nueva_descripcion]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Nueva clave y valor
            nueva_clave = (nueva_narrativa, nuevo_estilo, nueva_estetica, nueva_dinamica)
            url_imagen = f"https://example.com/images/{nuevo_nombre.lower().replace(' ', '_')}.jpg"
            nuevo_valor = (nuevo_nombre, url_imagen, nueva_descripcion)
            
            # Eliminar la antigua entrada si cambió la clave
            if clave_original != nueva_clave and clave_original in videojuegos:
                del videojuegos[clave_original]
            
            # Guardar la nueva entrada
            videojuegos[nueva_clave] = nuevo_valor
            
            # Guardar en JSON
            self._guardar_en_json()
            
            # Cerrar ventana
            edit_window.destroy()
            
            # Actualizar tabla
            self._cargar_conocimientos()
            messagebox.showinfo("Éxito", "Conocimiento actualizado exitosamente")
        
        # Botón guardar
        btn_guardar = tk.Button(btn_frame, text="Guardar Cambios", 
                              command=guardar_cambios,
                              bg="#2ECC71", fg="white", font=("Arial", 12),
                              padx=10, pady=5)
        btn_guardar.pack(side="left", padx=10)
        
        # Botón cancelar
        btn_cancelar = tk.Button(btn_frame, text="Cancelar", 
                               command=edit_window.destroy,
                               bg="#E74C3C", fg="white", font=("Arial", 12),
                               padx=10, pady=5)
        btn_cancelar.pack(side="left", padx=10)
    
    def _eliminar_conocimiento(self):
        """Eliminar el conocimiento seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Información", "Por favor selecciona un conocimiento para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar eliminación", 
                                      "¿Estás seguro de que deseas eliminar este conocimiento?")
        if not respuesta:
            return
        
        # Obtener datos del ítem seleccionado
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Construir la clave
        clave = (values[0], values[1], values[2], values[3])
        
        # Eliminar de la base de conocimiento
        if clave in videojuegos:
            del videojuegos[clave]
            
            # Guardar en JSON
            self._guardar_en_json()
            
            # Actualizar tabla
            self._cargar_conocimientos()
            messagebox.showinfo("Éxito", "Conocimiento eliminado exitosamente")
        else:
            messagebox.showerror("Error", "No se encontró el conocimiento en la base de datos")
    
    def _guardar_en_json(self):
        """Guardar la base de conocimiento en un archivo JSON"""
        # Convertir el diccionario a un formato serializable
        data = {}
        for clave, valor in videojuegos.items():
            # Convertir tupla a string para usar como clave en JSON
            str_clave = "||".join(clave)
            data[str_clave] = valor
        
        # Guardar en archivo
        os.makedirs('data', exist_ok=True)
        with open('data/base_conocimiento.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        if self.es_ventana_independiente:
            self.root.mainloop()