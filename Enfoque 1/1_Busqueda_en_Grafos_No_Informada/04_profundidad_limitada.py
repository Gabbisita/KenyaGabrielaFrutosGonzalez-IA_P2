def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    # La pila guarda los caminos a explorar.
    pila = [[inicio]]
    
    # El conjunto de visitados es importante, pero en DLS a veces se maneja de forma
    # más compleja para permitir encontrar rutas alternativas dentro del límite.
    # Para este ejemplo, lo mantendremos simple para evitar ciclos obvios.
    visitados = {inicio}

    while pila:
        camino_actual = pila.pop()
        nodo_actual = camino_actual[-1]

        if nodo_actual == objetivo:
            return camino_actual
            
        # Solo exploramos los vecinos si el camino actual no ha alcanzado el límite.
        # La profundidad es el número de pasos, es decir, len(camino) - 1.
        if len(camino_actual) - 1 < limite:
            for vecino in grafo.get(nodo_actual, []):
                
                # Para DLS, es importante poder revisitar nodos por caminos diferentes
                # siempre que no creemos un ciclo en el camino actual.
                if vecino not in camino_actual: # Evita ciclos simples (A->B->A)
                    
                    nuevo_camino = list(camino_actual)
                    nuevo_camino.append(vecino)
                    pila.append(nuevo_camino)

    # Si la pila se vacía, no se encontró un camino dentro del límite.
    return None

# Ejemplo de uso 
if __name__ == "__main__":
    
    mapa_ciudades = {
        'Guadalajara': ['Tepic', 'CDMX', 'Morelia'],
        'Tepic': ['Guadalajara', 'Mazatlan'],
        'CDMX': ['Guadalajara', 'Puebla', 'Monterrey'],
        'Morelia': ['Guadalajara'],
        'Mazatlan': ['Tepic'],
        'Puebla': ['CDMX'],
        'Monterrey': ['CDMX', 'Chihuahua'],
        'Chihuahua': ['Monterrey']
    }
    
    ciudad_inicio = 'Guadalajara'
    ciudad_destino = 'Chihuahua'
    
    print(f"Buscando ruta de '{ciudad_inicio}' a '{ciudad_destino}' con Búsqueda en Profundidad Limitada (DLS)")

    # CASO 1: Límite insuficiente
    limite_insuficiente = 2
    print(f"\n Probando con un límite de profundidad de {limite_insuficiente} ")
    
    # La ruta más corta es GDL -> CDMX -> Monterrey -> Chihuahua (3 pasos)
    # Por lo tanto, con un límite de 2, NO debería encontrarla.
    camino_caso1 = busqueda_profundidad_limitada(mapa_ciudades, ciudad_inicio, ciudad_destino, limite_insuficiente)
    
    if camino_caso1:
        print("Ruta encontrada:")
        print(" -> ".join(camino_caso1))
    else:
        print(f"No se encontró una ruta. El límite de {limite_insuficiente} pasos es demasiado bajo.")

    # CASO 2: Límite suficiente
    limite_suficiente = 3
    print(f"\n Probando con un límite de profundidad de {limite_suficiente} ")

    # Con un límite de 3, ahora sí debería poder encontrar la solución.
    camino_caso2 = busqueda_profundidad_limitada(mapa_ciudades, ciudad_inicio, ciudad_destino, limite_suficiente)

    if camino_caso2:
        print("Ruta encontrada:")
        print(" -> ".join(camino_caso2))
    else:
        print("No se encontró una ruta (esto no debería pasar con este límite).")