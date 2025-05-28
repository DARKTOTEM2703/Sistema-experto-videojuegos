from gui.app_gui import SistemaExpertoApp
import data.load_knowledge  # Importar módulo que carga la base de conocimiento

# Cargar el conocimiento antes de iniciar la app
data.load_knowledge.cargar_base_conocimiento()

if __name__ == "__main__":
    app = SistemaExpertoApp()
    app.ejecutar()