import json
import os

def cargar_base_conocimiento():
    """Carga la base de conocimiento desde el archivo JSON"""
    try:
        if os.path.exists('data/base_conocimiento.json'):
            from data.juegos_dictionary import videojuegos
            
            with open('data/base_conocimiento.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convertir las claves de string a tupla
            for str_clave, valor in data.items():
                # Separar la cadena usando el separador ||
                componentes = str_clave.split("||")
                if len(componentes) == 4:  # Verificar que sea una clave válida
                    videojuegos[tuple(componentes)] = valor
            
            print(f"Base de conocimiento cargada: {len(data)} entradas")
            return True
    except Exception as e:
        print(f"Error al cargar la base de conocimiento: {e}")
    
    return False