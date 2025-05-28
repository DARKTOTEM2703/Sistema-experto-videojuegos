# Sistema Experto para Recomendación de Videojuegos

## 📋 Descripción

Sistema experto basado en reglas que analiza las preferencias del usuario para recomendar videojuegos personalizados. Utilizando técnicas de inteligencia artificial, este proyecto evalúa múltiples factores como género, plataforma, complejidad y estilo visual para ofrecer recomendaciones precisas y generar visualizaciones conceptuales de los juegos recomendados.

## ✨ Características principales

- Motor de inferencia basado en reglas para recomendación personalizada
- Interfaz gráfica intuitiva para la interacción con el usuario
- Generación de imágenes conceptuales de los videojuegos recomendados
- Base de conocimiento extensa con información categorizada de videojuegos
- Explicación del razonamiento detrás de cada recomendación

## 🔧 Tecnologías utilizadas

- Python 3.8+
- PyQt5/Tkinter para la interfaz gráfica
- Sistema de reglas personalizado
- Algoritmos de procesamiento de imágenes
- Bibliotecas de machine learning para mejora de recomendaciones

## 📁 Estructura del proyecto

```
└───src
    ├───__pycache__
    ├───gui                    # Interfaz gráfica de usuario
    │   └───__pycache__
    ├───expert_system          # Motor de inferencia y sistema de reglas
    │   └───__pycache__
    ├───image_generation       # Generación de imágenes conceptuales
    │   └───__pycache__
    ├───utils                  # Funciones de utilidad y herramientas
    └───data                   # Base de conocimiento y recursos
        └───__pycache__
```

## 📋 Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Dependencias adicionales listadas en `requirements.txt`

## 🚀 Instalación

1. Clonar el repositorio:

```
git clone https://github.com/usuario/sistema-experto-videojuegos.git
cd sistema-experto-videojuegos
```

2. Crear y activar un entorno virtual (opcional pero recomendado):

```
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias:

```
# Procesamiento de imágenes
pip install Pillow

# Para realizar peticiones HTTP
pip install requests

# Para integración con la API de generación de imágenes
pip install gradio-client

# Para manejo de archivos de configuración
pip install python-dotenv
```

## 💻 Uso

1. Ejecutar la aplicación:

```
python src/main.py
```

2. Interactuar con la interfaz para:
   - Especificar preferencias de videojuegos
   - Recibir recomendaciones personalizadas
   - Visualizar imágenes conceptuales
   - Explorar la explicación de las recomendaciones

## 🧪 Pruebas

Para ejecutar las pruebas automatizadas:

```
python -m unittest discover tests
```

## 📚 Documentación

La documentación detallada está disponible en la [Wiki](https://github.com/usuario/sistema-experto-videojuegos/wiki) del proyecto.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, siga estos pasos:

1. Fork el repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/amazing-feature`)
3. Realice sus cambios y haga commit (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abra un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autor

- Jafeth Gamboa Baas - Estudiante de Ingeniería en Sistemas

## 📧 Contacto

Para preguntas o colaboraciones, por favor contactar a: [jafethgamboa@gmail.com](mailto:jafethgamboa@gmail.com)
