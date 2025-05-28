import json
import os
from data.juegos_dictionary import videojuegos

def cargar_base_conocimiento():
    """Carga el conocimiento guardado en JSON (si existe)"""
    try:
        if os.path.exists('data/base_conocimiento.json'):
            with open('data/base_conocimiento.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Convertir las claves de string a tuplas
                for str_clave, valor in data.items():
                    # Separar la cadena en componentes
                    componentes = str_clave.split("||")
                    if len(componentes) == 4:  # Asegurar que la clave tiene el formato correcto
                        clave = tuple(componentes)
                        videojuegos[clave] = valor
            
            return True
    except Exception as e:
        print(f"Error al cargar conocimiento desde JSON: {e}")
    
    return False