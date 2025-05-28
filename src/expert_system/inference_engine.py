from data.juegos_dictionary import videojuegos

def buscar_recomendacion(clave):
    """Busca una recomendación exacta en el diccionario de juegos"""
    if clave in videojuegos:
        return videojuegos[clave]
    return None

def buscar_alternativas(clave_original):
    """Encuentra juegos similares cuando no hay coincidencia exacta"""
    narrativa, estilo, estetica, dinamica = clave_original
    alternativas = []
    
    for k, datos_juego in videojuegos.items():
        coincidencias = 0
        # Verificar cada criterio
        if k[0] == narrativa: coincidencias += 1
        if k[1] == estilo: coincidencias += 1
        if k[2] == estetica: coincidencias += 1
        if k[3] == dinamica: coincidencias += 1
        
        # Si coincide en al menos 2 criterios, es una alternativa válida
        if coincidencias >= 2:
            nombre, url, descripcion = datos_juego
            alternativas.append((nombre, url, descripcion, coincidencias))
    
    # Ordenar por número de coincidencias (de mayor a menor)
    return sorted(alternativas, key=lambda x: x[3], reverse=True)

def obtener_opciones_disponibles(categoria_idx):
    """Devuelve todas las opciones disponibles para una categoría específica
    0: narrativa, 1: estilo, 2: estetica, 3: dinamica"""
    return sorted(set(clave[categoria_idx] for clave in videojuegos.keys()))