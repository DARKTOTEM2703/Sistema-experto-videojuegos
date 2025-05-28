import os
import json
from datetime import datetime

def guardar_feedback(respuestas, recomendacion, feedback):
    """Guarda el feedback del usuario para mejorar el sistema"""
    datos = {
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'preferencias': respuestas,
        'recomendacion': recomendacion,
        'feedback': feedback
    }
    
    # Crear directorio si no existe
    os.makedirs('feedback', exist_ok=True)
    
    # Nombre del archivo con timestamp
    filename = f"feedback/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Guardar datos
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    return True