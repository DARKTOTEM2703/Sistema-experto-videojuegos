import logging
import os
import datetime

def setup_logger():
    """Configura el sistema de logs para la aplicación"""
    # Crear directorio de logs si no existe
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar formato con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"app_log_{timestamp}.txt")
    
    # Configurar logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # También muestra en consola
        ]
    )
    
    logger = logging.getLogger("SistemaExperto")
    return logger