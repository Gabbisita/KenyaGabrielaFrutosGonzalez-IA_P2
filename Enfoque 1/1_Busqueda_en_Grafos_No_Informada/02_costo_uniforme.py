# heapq es la librería de Python para implementar colas de prioridad.
import heapq

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    
    # La cola de prioridad guardará tuplas de (costo_acumulado, camino).
    # Empezamos con un costo de 0 para el camino que solo contiene el nodo de inicio.
    cola_prioridad = [(0, [inicio])]
    
    # Usamos un diccionario para llevar el registro del costo mínimo encontrado 
    # para llegar a cada nodo. Así evitamos explorar caminos más caros.
    costos = {inicio: 0}

    # Mientras la cola no esté vacía, significa que aún hay caminos por explorar.
    while cola_prioridad:
        
        # Sacamos el camino con el menor costo actual de la cola de prioridad.
        costo_actual, camino_actual = heapq.heappop(cola_prioridad)
        nodo_actual = camino_actual[-1]

        # Si ya hemos encontrado un camino más barato para llegar a este nodo, ignoramos este.
        if costo_actual > costos[nodo_actual]:
            continue

        # Si el nodo actual es el que buscamos, devolvemos el camino y su costo.
        if nodo_actual == objetivo:
            return camino_actual, costo_actual
            
        # Revisamos todos los vecinos y el costo para llegar a ellos.
        # grafo.get(nodo_actual, {}).items() nos da cada vecino y el costo de ese tramo.
        for vecino, costo_tramo in grafo.get(nodo_actual, {}).items():
            
            nuevo_costo = costo_actual + costo_tramo

            # Si no habíamos visitado al vecino o encontramos una ruta más barata para llegar a él...
            if vecino not in costos or nuevo_costo < costos[vecino]:
                
                # ...actualizamos su costo mínimo.
                costos[vecino] = nuevo_costo
                
                # Creamos el nuevo camino.
                nuevo_camino = list(camino_actual)
                nuevo_camino.append(vecino)
                
                # Y lo añadimos a la cola de prioridad.
                heapq.heappush(cola_prioridad, (nuevo_costo, nuevo_camino))

    # Si el bucle termina y no encontramos el objetivo, no existe un camino.
    return None, float('inf')

# Ejemplo de uso
if __name__ == "__main__":
    
    # 1. Definimos el grafo con los costos (distancias en km) de cada tramo.
    #    La estructura es: 'Ciudad': {'Vecino1': costo1, 'Vecino2': costo2, ...}
    mapa_carreteras = {
        'Guadalajara': {'Tepic': 216, 'CDMX': 540, 'Morelia': 295},
        'Tepic': {'Guadalajara': 216, 'Mazatlan': 260},
        'CDMX': {'Guadalajara': 540, 'Puebla': 130, 'Monterrey': 900},
        'Morelia': {'Guadalajara': 295, 'Patzcuaro': 58},
        'Mazatlan': {'Tepic': 260, 'Culiacan': 220},
        'Puebla': {'CDMX': 130},
        'Monterrey': {'CDMX': 900, 'Chihuahua': 760},
        'Patzcuaro': {'Morelia': 58},
        'Culiacan': {'Mazatlan': 220},
        'Chihuahua': {'Monterrey': 760}
    }
    
    # 2. Establecemos nuestro punto de partida y destino.
    ciudad_inicio = 'Guadalajara'
    ciudad_destino = 'Chihuahua'

    print(f"Buscando la ruta más corta (en km) de '{ciudad_inicio}' a '{ciudad_destino}'...")
    
    # 3. Llamamos a la función.
    camino_encontrado, costo_total = busqueda_costo_uniforme(mapa_carreteras, ciudad_inicio, ciudad_destino)
    
    # 4. Imprimimos el resultado.
    if camino_encontrado:
        print("\nRuta de menor costo encontrada:")
        print(f"  -> Recorrido: {' -> '.join(camino_encontrado)}")
        print(f"  -> Costo total: {costo_total} km")
    else:
        print("No se encontró una ruta.")