"""
1. Búsqueda en Anchura (BFS): Para grafos no ponderados.
2. Búsqueda A* (A-Star): Para grafos ponderados con heurística.
"""

from collections import deque
import heapq
import math

# 1: BÚSQUEDA EN ANCHURA (BFS)

def busqueda_en_anchura(grafo, inicio, objetivo):
    # Cola para guardar los caminos a explorar
    cola = deque([[inicio]])
    # Conjunto de nodos visitados para evitar ciclos
    visitados = {inicio}

    while cola:
        # Tomar el primer camino de la cola
        camino_actual = cola.popleft()
        nodo_actual = camino_actual[-1]

        # Si es el objetivo, hemos terminado
        if nodo_actual == objetivo:
            return camino_actual
            
        # Revisar todos los vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                nuevo_camino = list(camino_actual)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)

    return None # No se encontró camino

# 2: BÚSQUEDA A* (A-STAR)
def heuristica(nodo, objetivo, coordenadas):
    """Calcula la distancia en línea recta (nuestra estimación h(n))."""
    x1, y1 = coordenadas[nodo]
    x2, y2 = coordenadas[objetivo]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def busqueda_a_estrella(grafo, inicio, objetivo, coordenadas):
    """Encuentra el camino de menor costo en un grafo ponderado."""
    # g(n): costo real desde el inicio
    costo_g = {inicio: 0}
    # f(n) = g(n) + h(n): costo total estimado
    costo_f = {inicio: heuristica(inicio, objetivo, coordenadas)}
    
    # Cola de prioridad que ordena por el costo_f
    cola_prioridad = [(costo_f[inicio], inicio)]
    padres = {inicio: None}

    while cola_prioridad:
        _, nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.insert(0, nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino, costo_g[objetivo]

        for vecino, costo_tramo in grafo.get(nodo_actual, {}).items():
            nuevo_costo_g = costo_g[nodo_actual] + costo_tramo
            
            if vecino not in costo_g or nuevo_costo_g < costo_g[vecino]:
                padres[vecino] = nodo_actual
                costo_g[vecino] = nuevo_costo_g
                costo_f[vecino] = nuevo_costo_g + heuristica(vecino, objetivo, coordenadas)
                heapq.heappush(cola_prioridad, (costo_f[vecino], vecino))

    return None, float('inf')


# Ejemplo de uso
if __name__ == "__main__":
    
    # Ejemplo 1: Grafo No Ponderado (usando BFS)
    print("1: BÚSQUEDA EN ANCHURA (BFS)")
    mapa_ciudades = {
        'Guadalajara': ['Tepic', 'CDMX'], 'Tepic': ['Mazatlan'],
        'CDMX': ['Monterrey'], 'Mazatlan': [], 'Monterrey': ['Chihuahua'], 'Chihuahua': []
    }
    
    print("Objetivo: Encontrar la ruta con menos escalas de Guadalajara a Chihuahua.")
    camino_bfs = busqueda_en_anchura(mapa_ciudades, 'Guadalajara', 'Chihuahua')
    
    if camino_bfs:
        print("Ruta más corta (en pasos):", " -> ".join(camino_bfs))
        print(f"Número de pasos: {len(camino_bfs) - 1}\n")
    else:
        print("No se encontró ruta.\n")

    print("\n" + "="*50 + "\n")

    # Ejemplo 2: Grafo Ponderado (usando A*)
    print("### EJEMPLO 2: BÚSQUEDA A* (A-STAR) ###")
    mapa_carreteras = {
        'Guadalajara': {'Tepic': 216, 'CDMX': 540},
        'Tepic': {'Mazatlan': 260},
        'CDMX': {'Monterrey': 900},
        'Mazatlan': {},
        'Monterrey': {'Chihuahua': 760},
        'Chihuahua': {}
    }
    coordenadas_ciudades = {
        'Guadalajara': (20, 103), 'Tepic': (21, 104), 'CDMX': (19, 99),
        'Mazatlan': (23, 106), 'Monterrey': (25, 100), 'Chihuahua': (28, 106)
    }

    print("Objetivo: Encontrar la ruta más barata (en km) de Guadalajara a Chihuahua.")
    camino_a_star, costo = busqueda_a_estrella(mapa_carreteras, 'Guadalajara', 'Chihuahua', coordenadas_ciudades)

    if camino_a_star:
        print("Ruta más barata (en costo):", " -> ".join(camino_a_star))
        print(f"Costo total: {round(costo, 2)} km")
    else:
        print("No se encontró ruta.")