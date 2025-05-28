import tkinter as tk
from tkinter import ttk

def crear_frame_base(app, titulo, numero_frame):
    """Crea un frame base con el estilo común"""
    frame = tk.Frame(app.root, bg="#34495E", relief="raised", bd=2)
    
    # Título del frame
    titulo_label = tk.Label(frame, text=f"Frame {numero_frame}", 
                          font=("Arial", 10), bg="#34495E", fg="white")
    titulo_label.pack(pady=5)
    
    # Título principal
    main_title = tk.Label(frame, text=titulo, 
                        font=("Arial", 16, "bold"), bg="#34495E", fg="white")
    main_title.pack(pady=10)
    
    return frame

def crear_frame_bienvenida(app):
    """Frame 1: Pantalla de bienvenida"""
    frame = crear_frame_base(app, "Bienvenido al Sistema Experto de Recomendación de Videojuegos", 1)
    
    # Imagen/icono del personaje (simulado con texto)
    char_frame = tk.Frame(frame, bg="#D4A574", width=200, height=150)
    char_frame.pack(pady=20)
    char_frame.pack_propagate(False)
    
    char_label = tk.Label(char_frame, text="🎮\n¡Hola!\nSoy tu asistente\nde videojuegos", 
                        font=("Arial", 12), bg="#D4A574", justify="center")
    char_label.pack(expand=True)
    
    # Pregunta principal
    pregunta = tk.Label(frame, text="¿Te gustaría que te recomiende\nel videojuego perfecto para ti?", 
                      font=("Arial", 14), bg="#34495E", fg="white", justify="center")
    pregunta.pack(pady=20)
    
    # Botones de navegación
    nav_frame = tk.Frame(frame, bg="#34495E")
    nav_frame.pack(side="bottom", pady=20)
    
    btn_siguiente = tk.Button(nav_frame, text="▶", font=("Arial", 12), 
                            command=lambda: app.siguiente_frame())
    btn_siguiente.pack(side="right", padx=10)
    
    # Agregar botón Modo Experto en la esquina superior derecha
    btn_experto = tk.Button(
        frame, 
        text="👨‍🔬 Modo Experto", 
        command=lambda: abrir_modo_experto(app),
        bg="#9b59b6", fg="white", font=("Arial", 10)
    )
    btn_experto.place(relx=0.95, rely=0.05, anchor="ne")
    
    return frame

def abrir_modo_experto(app):
    """Abre el modo experto para gestionar la base de conocimiento"""
    # Crear ventana para modo experto
    ventana_experto = tk.Toplevel(app.root)
    ventana_experto.title("Modo Experto - Gestión de Base de Conocimiento")
    ventana_experto.geometry("900x600")
    ventana_experto.configure(bg="#2C3E50")
    
    # Crear interfaz de administración
    admin_frame = tk.Frame(ventana_experto, bg="#34495E", padx=20, pady=20)
    admin_frame.pack(fill="both", expand=True)
    
    # Título
    titulo = tk.Label(admin_frame, text="Administración de Base de Conocimiento", 
                   font=("Arial", 16, "bold"), bg="#34495E", fg="#ECF0F1")
    titulo.pack(pady=20)
    
    # Crear notebook (pestañas)
    notebook = ttk.Notebook(admin_frame)
    notebook.pack(fill="both", expand=True)
    
    # Pestaña 1: Agregar conocimiento
    tab_agregar = tk.Frame(notebook, bg="#2C3E50")
    notebook.add(tab_agregar, text="Agregar Conocimiento")
    
    # Campos para agregar nuevo conocimiento
    crear_formulario_agregar(tab_agregar, app)
    
    # Pestaña 2: Ver/Editar conocimiento
    tab_editar = tk.Frame(notebook, bg="#2C3E50")
    notebook.add(tab_editar, text="Ver/Editar Conocimiento")
    
    # Tabla para ver y editar conocimiento existente
    crear_tabla_conocimiento(tab_editar, app)

def crear_frame_narrativa(app):
    """Frame 2: Pregunta sobre narrativa"""
    frame = crear_frame_base(app, "¿Qué tipo de historia te atrae más?", 2)
    
    # Personaje
    char_frame = tk.Frame(frame, bg="#D4A574", width=150, height=100)
    char_frame.pack(pady=10)
    char_frame.pack_propagate(False)
    
    char_label = tk.Label(char_frame, text="🎭", font=("Arial", 30), bg="#D4A574")
    char_label.pack(expand=True)
    
    # Opciones
    opciones_narrativa = [
        ("🏰 Juego de Tronos", "Juego de Tronos"),
        ("🚀 Star Wars", "Star Wars"), 
        ("🧟 The Walking Dead", "The Walking Dead"),
        ("🤖 Black Mirror", "Black Mirror")
    ]
    
    for texto, valor in opciones_narrativa:
        rb = tk.Radiobutton(frame, text=texto, variable=app.var_narrativa, value=valor,
                          font=("Arial", 12), bg="#34495E", fg="white", 
                          selectcolor="#2C3E50", activebackground="#34495E")
        rb.pack(pady=5)
    
    # Botones de navegación
    nav_frame = tk.Frame(frame, bg="#34495E")
    nav_frame.pack(side="bottom", pady=20)
    
    btn_anterior = tk.Button(nav_frame, text="◀", font=("Arial", 12),
                           command=lambda: app.anterior_frame())
    btn_anterior.pack(side="left", padx=10)
    
    btn_siguiente = tk.Button(nav_frame, text="▶", font=("Arial", 12),
                            command=lambda: app.siguiente_frame())
    btn_siguiente.pack(side="right", padx=10)
    
    return frame

def crear_frame_estilo(app):
    """Frame 3: Pregunta sobre estilo de juego"""
    frame = crear_frame_base(app, "¿Cómo prefieres jugar?", 3)
    
    # Personaje
    char_frame = tk.Frame(frame, bg="#D4A574", width=150, height=100)
    char_frame.pack(pady=10)
    char_frame.pack_propagate(False)
    
    char_label = tk.Label(char_frame, text="👥", font=("Arial", 30), bg="#D4A574")
    char_label.pack(expand=True)
    
    # Opciones
    opciones_estilo = [
        ("🎯 Solo", "Solo"),
        ("👫 Con amigos", "Con amigos"),
        ("⚔️ Competencia online", "Competencia online"),
        ("🌍 Explorar sin presión", "Explorar sin presión")
    ]
    
    for texto, valor in opciones_estilo:
        rb = tk.Radiobutton(frame, text=texto, variable=app.var_estilo, value=valor,
                          font=("Arial", 12), bg="#34495E", fg="white",
                          selectcolor="#2C3E50", activebackground="#34495E")
        rb.pack(pady=5)
    
    # Botones de navegación
    nav_frame = tk.Frame(frame, bg="#34495E")
    nav_frame.pack(side="bottom", pady=20)
    
    btn_anterior = tk.Button(nav_frame, text="◀", font=("Arial", 12),
                           command=lambda: app.anterior_frame())
    btn_anterior.pack(side="left", padx=10)
    
    btn_siguiente = tk.Button(nav_frame, text="▶", font=("Arial", 12),
                            command=lambda: app.siguiente_frame())
    btn_siguiente.pack(side="right", padx=10)
    
    return frame

def crear_frame_estetica(app):
    """Frame 4: Pregunta sobre estética visual"""
    frame = crear_frame_base(app, "¿Qué estilo visual prefieres?", 4)
    
    # Personaje
    char_frame = tk.Frame(frame, bg="#D4A574", width=150, height=100)
    char_frame.pack(pady=10)
    char_frame.pack_propagate(False)
    
    char_label = tk.Label(char_frame, text="🎨", font=("Arial", 30), bg="#D4A574")
    char_label.pack(expand=True)
    
    # Opciones
    opciones_estetica = [
        ("🎭 Animación", "Animación"),
        ("📷 Realismo", "Realismo"),
        ("🎪 Mezcla estilizada", "Mezcla estilizada"),
        ("🌀 Arte abstracto", "Arte abstracto")
    ]
    
    for texto, valor in opciones_estetica:
        rb = tk.Radiobutton(frame, text=texto, variable=app.var_estetica, value=valor,
                          font=("Arial", 12), bg="#34495E", fg="white",
                          selectcolor="#2C3E50", activebackground="#34495E")
        rb.pack(pady=5)
    
    # Botones de navegación
    nav_frame = tk.Frame(frame, bg="#34495E")
    nav_frame.pack(side="bottom", pady=20)
    
    btn_anterior = tk.Button(nav_frame, text="◀", font=("Arial", 12),
                           command=lambda: app.anterior_frame())
    btn_anterior.pack(side="left", padx=10)
    
    btn_siguiente = tk.Button(nav_frame, text="▶", font=("Arial", 12),
                            command=lambda: app.siguiente_frame())
    btn_siguiente.pack(side="right", padx=10)
    
    return frame

def crear_frame_dinamica(app):
    """Frame 5: Pregunta sobre dinámica de juego"""
    frame = crear_frame_base(app, "¿Qué experiencia de juego buscas?", 5)
    
    # Personaje
    char_frame = tk.Frame(frame, bg="#D4A574", width=150, height=100)
    char_frame.pack(pady=10)
    char_frame.pack_propagate(False)
    
    char_label = tk.Label(char_frame, text="⚡", font=("Arial", 30), bg="#D4A574")
    char_label.pack(expand=True)
    
    # Opciones
    opciones_dinamica = [
        ("🤔 Toma de decisiones", "Toma de decisiones"),
        ("🏕️ Supervivencia", "Supervivencia"),
        ("🔍 Misterio/Investigación", "Misterio/Investigación"),
        ("🗺️ Aventura/Descubrimiento", "Aventura/Descubrimiento")
    ]
    
    for texto, valor in opciones_dinamica:
        rb = tk.Radiobutton(frame, text=texto, variable=app.var_dinamica, value=valor,
                          font=("Arial", 12), bg="#34495E", fg="white",
                          selectcolor="#2C3E50", activebackground="#34495E")
        rb.pack(pady=5)
    
    # Botones de navegación
    nav_frame = tk.Frame(frame, bg="#34495E")
    nav_frame.pack(side="bottom", pady=20)
    
    btn_anterior = tk.Button(nav_frame, text="◀", font=("Arial", 12),
                           command=lambda: app.anterior_frame())
    btn_anterior.pack(side="left", padx=10)
    
    btn_siguiente = tk.Button(nav_frame, text="▶", font=("Arial", 12),
                            command=lambda: app.siguiente_frame())
    btn_siguiente.pack(side="right", padx=10)
    
    return frame

def crear_frame_resultados(app):
    """Frame 6: Mostrar resultados"""
    frame = crear_frame_base(app, "🏆 Tu Recomendación Personalizada", 6)
    
    # Área de resultados con scroll
    canvas = tk.Canvas(frame, bg="#34495E", height=350)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#34495E")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Contenido de resultados (se llenará dinámicamente)
    app.resultado_frame = scrollable_frame
    
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar.pack(side="right", fill="y")
    
    # Botones de navegación
    nav_frame = tk.Frame(frame, bg="#34495E")
    nav_frame.pack(side="bottom", pady=20)
    
    btn_anterior = tk.Button(nav_frame, text="◀", font=("Arial", 12),
                           command=lambda: app.anterior_frame())
    btn_anterior.pack(side="left", padx=10)
    
    btn_reiniciar = tk.Button(nav_frame, text="🔄 Nueva Consulta", font=("Arial", 12),
                            command=lambda: app.reiniciar_sistema())
    btn_reiniciar.pack(side="right", padx=10)
    
    return frame