from gui.app_gui import SistemaExpertoApp
from data.load_knowledge import cargar_base_conocimiento  # Asegúrate de tener este archivo

# Cargar conocimiento guardado al iniciar
cargar_base_conocimiento()

if __name__ == "__main__":
    app = SistemaExpertoApp()
    app.ejecutar()