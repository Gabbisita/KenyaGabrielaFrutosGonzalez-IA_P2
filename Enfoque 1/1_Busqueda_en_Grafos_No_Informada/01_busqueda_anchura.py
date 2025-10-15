# Importamos 'deque' para usar una cola eficiente, que es fundamental para BFS
from collections import deque

def busqueda_en_anchura(grafo, inicio, objetivo):
    """
    Busca el camino más corto en un grafo desde un nodo de inicio a un objetivo
    usando el algoritmo de Búsqueda en Anchura (BFS).
    """
    
    # Cola que guarda los caminos que necesitamos explorar. Empezamos con el nodo de inicio.
    cola = deque([[inicio]])
    
    # Conjunto para guardar los nodos que ya visitamos y así evitar ciclos infinitos.
    visitados = {inicio}

    # Mientras la cola no esté vacía, significa que aún hay caminos por revisar.
    while cola:
        
        # Sacamos el primer camino de la cola para analizarlo.
        camino_actual = cola.popleft()
        nodo_actual = camino_actual[-1] # El último nodo de ese camino es nuestra posición actual.

        # Si el nodo actual es el que buscamos, devolvemos el camino encontrado.
        if nodo_actual == objetivo:
            return camino_actual
            
        # Revisamos todos los vecinos (nodos conectados) del nodo actual.
        for vecino in grafo.get(nodo_actual, []):
            
            # Si es un vecino que no hemos visitado antes...
            if vecino not in visitados:
                
                # Lo marcamos como visitado.
                visitados.add(vecino)
                
                # Creamos un nuevo camino que incluye al vecino.
                nuevo_camino = list(camino_actual)
                nuevo_camino.append(vecino)
                
                # Añadimos este nuevo camino a la cola para explorarlo después.
                cola.append(nuevo_camino)

    # Si el bucle termina y no encontramos el objetivo, no existe un camino.
    return None

#Ejemplo de aplicación
if __name__ == "__main__":
    
    # 1. Definimos el grafo que vamos a recorrer.
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

    print(f"Buscando ruta de '{ciudad_inicio}' a '{ciudad_destino}'...")
    
    # 3. Llamamos a la función con nuestros datos.
    camino_encontrado = busqueda_en_anchura(mapa_ciudades, ciudad_inicio, ciudad_destino)
    
    # 4. Imprimimos el resultado.
    if camino_encontrado:
        print("Ruta más corta encontrada:")
        print(" -> ".join(camino_encontrado))
    else:
        print("No se encontró una ruta.")