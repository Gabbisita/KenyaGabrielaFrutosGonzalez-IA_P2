def busqueda_online_dfs(mapa, inicio, objetivo):
    """
    Simula un agente de búsqueda online que explora un entorno desconocido.
    
    Returns:
        list: El camino total recorrido por el agente, incluyendo la exploración y el backtracking.
    """
    posicion_actual = inicio
    camino_recorrido = [inicio] # Guarda cada paso que da el agente
    historial_camino = [inicio] # Se usa como pila para el backtracking
    visitados = {inicio}
    
    print(f"Agente empieza en '{inicio}' sin conocer el mapa.")

    while posicion_actual != objetivo:
        # 1. El agente "mira a su alrededor" (esto es lo único que conoce)
        vecinos = mapa.get(posicion_actual, [])
        
        vecino_no_visitado = None
        # 2. Busca una nueva ruta para explorar
        for vecino in vecinos:
            if vecino not in visitados:
                vecino_no_visitado = vecino
                break
        
        # 3. Decide a dónde moverse
        if vecino_no_visitado is not None:
            # Encontró un nuevo lugar: avanza
            visitados.add(vecino_no_visitado)
            posicion_actual = vecino_no_visitado
            historial_camino.append(posicion_actual)
            camino_recorrido.append(posicion_actual)
            print(f"  -> Explora hacia '{posicion_actual}'...")
        else:
            # Callejón sin salida: todos los vecinos ya fueron visitados
            print(f"  -> Callejón sin salida en '{posicion_actual}'. Retrocediendo...")
            # Elimina el último elemento para retroceder
            historial_camino.pop()
            if not historial_camino:
                return None # No puede retroceder más, no hay solución
            
            # Se mueve a la posición anterior en su historial
            posicion_actual = historial_camino[-1]
            camino_recorrido.append(posicion_actual)
            print(f"  -> Vuelve a '{posicion_actual}'...")

    return camino_recorrido
if __name__ == "__main__":
    
    mapa_laberinto = {
        'A': ['C', 'B'], # ¡Este es el único cambio!
        'B': ['A', 'D'],
        'C': ['A', 'F'],
        'D': ['B', 'E'],
        'E': ['D', 'G'],
        'F': ['C'],
        'G': ['E']
    }
    
    ciudad_inicio = 'A'
    ciudad_objetivo = 'G'

    print("Iniciando simulación de Búsqueda Online (forzando backtracking)...")
    
    ruta_total = busqueda_online_dfs(mapa_laberinto, ciudad_inicio, ciudad_objetivo)
    
    print("\n" + "-"*40)
    if ruta_total:
        print("¡Objetivo encontrado!")
        print(f"El camino final de la solución es: A -> B -> D -> E -> G")
        print(f"\nEl recorrido TOTAL que el agente tuvo que hacer para descubrirlo fue:")
        print(" -> ".join(ruta_total))
    else:
        print("No se encontró una ruta al objetivo.")