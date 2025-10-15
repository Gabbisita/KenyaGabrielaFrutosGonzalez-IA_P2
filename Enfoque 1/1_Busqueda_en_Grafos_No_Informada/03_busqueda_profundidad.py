# No necesitamos librerías especiales.

def busqueda_en_profundidad(grafo, inicio, objetivo):
    
    # Usamos una lista como si fuera una Pila (Stack). Empezamos con el nodo de inicio.
    pila = [[inicio]]
    
    # Conjunto para guardar los nodos que ya visitamos y evitar ciclos.
    visitados = {inicio}

    # Mientras la pila no esté vacía, significa que aún hay caminos por explorar.
    while pila:
        
        # Sacamos el último camino que añadimos a la pila (comportamiento LIFO).
        # ¡Esta es la única línea que cambia respecto a BFS!
        camino_actual = pila.pop()
        nodo_actual = camino_actual[-1]

        # Si el nodo actual es el que buscamos, devolvemos el camino.
        if nodo_actual == objetivo:
            return camino_actual
            
        # Revisamos todos los vecinos del nodo actual.
        for vecino in grafo.get(nodo_actual, []):
            
            # Si es un vecino que no hemos visitado antes...
            if vecino not in visitados:
                
                # Lo marcamos como visitado.
                visitados.add(vecino)
                
                # Creamos el nuevo camino que incluye al vecino.
                nuevo_camino = list(camino_actual)
                nuevo_camino.append(vecino)
                
                # Y lo añadimos a la pila.
                pila.append(nuevo_camino)

    # Si el bucle termina, no se encontró un camino.
    return None

# Ejemplo de uso
if __name__ == "__main__":
    
    # 1. Definimos el mismo grafo sin costos que usamos en el ejemplo de BFS.
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
    
    # 2. Establecemos nuestro punto de partida y destino.
    ciudad_inicio = 'Guadalajara'
    ciudad_destino = 'Chihuahua'

    print(f"Buscando una ruta de '{ciudad_inicio}' a '{ciudad_destino}' con Búsqueda en Profundidad (DFS)...")
    
    # 3. Llamamos a la función DFS.
    camino_encontrado_dfs = busqueda_en_profundidad(mapa_ciudades, ciudad_inicio, ciudad_destino)
    
    # 4. Imprimimos el resultado.
    if camino_encontrado_dfs:
        print("\n Ruta encontrada por DFS:")
        print(f"  -> Recorrido: {' -> '.join(camino_encontrado_dfs)}")
        print(f"  -> Pasos: {len(camino_encontrado_dfs) - 1}")
        print("\n NOTA: La Búsqueda en Profundidad no garantiza que esta sea la ruta más corta.")
    else:
        print("No se encontró una ruta.")