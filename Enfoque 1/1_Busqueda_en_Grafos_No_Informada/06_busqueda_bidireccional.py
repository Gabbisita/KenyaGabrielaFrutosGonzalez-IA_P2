from collections import deque

def reconstruir_camino(padres_adelante, padres_atras, punto_encuentro):
    camino = [punto_encuentro]
    
    # Reconstruir camino hacia el inicio (hacia adelante)
    nodo_actual = punto_encuentro
    while padres_adelante.get(nodo_actual) is not None:
        nodo_actual = padres_adelante[nodo_actual]
        camino.insert(0, nodo_actual) # Inserta al principio
        
    # Reconstruir camino desde el objetivo (hacia atrás)
    nodo_actual = punto_encuentro
    while padres_atras.get(nodo_actual) is not None:
        nodo_actual = padres_atras[nodo_actual]
        camino.append(nodo_actual) # Añade al final

    return camino

def busqueda_bidireccional(grafo, inicio, objetivo):
    if inicio == objetivo:
        return [inicio]

    # Colas para las búsquedas hacia adelante y hacia atrás
    cola_adelante = deque([inicio])
    cola_atras = deque([objetivo])
    
    # Diccionarios para guardar los 'padres' de cada nodo y reconstruir el camino
    padres_adelante = {inicio: None}
    padres_atras = {objetivo: None}
    
    # Bucle principal: continuar mientras ambas búsquedas tengan nodos por explorar
    while cola_adelante and cola_atras:
        
        # Paso de la búsqueda hacia adelante
        nodo_actual_adelante = cola_adelante.popleft()
        
        # Comprobamos si el nodo actual ya fue visitado por la búsqueda que va hacia atrás
        if nodo_actual_adelante in padres_atras:
            return reconstruir_camino(padres_adelante, padres_atras, nodo_actual_adelante)
            
        for vecino in grafo.get(nodo_actual_adelante, []):
            if vecino not in padres_adelante:
                padres_adelante[vecino] = nodo_actual_adelante
                cola_adelante.append(vecino)

        # Paso de la búsqueda hacia atrás
        nodo_actual_atras = cola_atras.popleft()
        
        # Comprobamos si el nodo actual ya fue visitado por la búsqueda que va hacia adelante
        if nodo_actual_atras in padres_adelante:
            return reconstruir_camino(padres_adelante, padres_atras, nodo_actual_atras)
            
        # Para ir "hacia atrás", necesitamos encontrar los predecesores.
        # En un grafo no dirigido (como el nuestro), los predecesores son los mismos que los sucesores.
        for predecesor in grafo.get(nodo_actual_atras, []):
            if predecesor not in padres_atras:
                padres_atras[predecesor] = nodo_actual_atras
                cola_atras.append(predecesor)
                
    # Si una de las colas se vacía, no hay conexión
    return None

# Ejemplo de uso
if __name__ == "__main__":
    
    # Usamos un grafo no dirigido donde si A->B, entonces B->A
    mapa_ciudades = {
        'Guadalajara': ['Tepic', 'CDMX', 'Morelia'],
        'Tepic': ['Guadalajara', 'Mazatlan'],
        'CDMX': ['Guadalajara', 'Puebla', 'Monterrey'],
        'Morelia': ['Guadalajara', 'Patzcuaro'],
        'Mazatlan': ['Tepic', 'Culiacan'],
        'Puebla': ['CDMX'],
        'Monterrey': ['CDMX', 'Chihuahua'],
        'Patzcuaro': ['Morelia'],
        'Culiacan': ['Mazatlan'],
        'Chihuahua': ['Monterrey']
    }
    
    ciudad_inicio = 'Guadalajara'
    ciudad_destino = 'Chihuahua'
    
    print(f"Buscando ruta de '{ciudad_inicio}' a '{ciudad_destino}' con Búsqueda Bidireccional")
    
    camino_encontrado = busqueda_bidireccional(mapa_ciudades, ciudad_inicio, ciudad_destino)
    
    if camino_encontrado:
        print("\n¡Ruta óptima encontrada!")
        print(f"  -> Recorrido: {' -> '.join(camino_encontrado)}")
        print(f"  -> Pasos: {len(camino_encontrado) - 1}")
    else:
        print("No se encontró una ruta.")