import heapq
import math

def heuristica(nodo, objetivo, coordenadas):
    """
    Calcula la distancia en línea recta (Euclidiana) entre dos nodos.
    Esta es nuestra 'h(n)', la estimación del costo restante.
    """
    x1, y1 = coordenadas[nodo]
    x2, y2 = coordenadas[objetivo]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def busqueda_voraz(grafo, inicio, objetivo, coordenadas):
    """
    Busca un camino usando la Búsqueda Voraz.
    Solo se guía por la heurística h(n).
    """
    # La cola de prioridad guardará tuplas de (valor_heuristico, nodo).
    cola_prioridad = [(heuristica(inicio, objetivo, coordenadas), inicio)]
    
    # Usamos un diccionario para reconstruir el camino al final.
    padres = {inicio: None}
    # Un conjunto para no visitar el mismo nodo dos veces y evitar ciclos.
    visitados = {inicio}

    while cola_prioridad:
        # Sacamos el nodo que PARECE estar más cerca del objetivo.
        _, nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == objetivo:
            # Reconstruir y devolver el camino.
            camino = []
            while nodo_actual is not None:
                camino.insert(0, nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino

        for vecino in grafo.get(nodo_actual, {}):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = nodo_actual
                # La prioridad es solo el valor de la heurística del vecino.
                prioridad = heuristica(vecino, objetivo, coordenadas)
                heapq.heappush(cola_prioridad, (prioridad, vecino))

    return None # No se encontró ruta

# Ejemplo de uso
if __name__ == "__main__":
    
    # 1. Creamos un mapa con una "trampa" para la búsqueda voraz.
    # La ruta por Zacatecas parece más directa (heurística baja), pero es más larga.
    mapa_con_trampa = {
        'Guadalajara': {'Tepic': 216, 'Zacatecas': 310},
        'Tepic': {'Mazatlan': 260},
        'Zacatecas': {'Chihuahua': 900}, # Ruta "directa" pero muy costosa
        'Mazatlan': {'Culiacan': 220},
        'Culiacan': {'Chihuahua': 550}, # Ruta más larga pero más barata en total
        'Chihuahua': {}
    }

    # 2. Coordenadas para la heurística. Zacatecas está en línea recta hacia Chihuahua.
    coordenadas = {
        'Guadalajara': (20, 103), 'Tepic': (21, 104), 'Zacatecas': (22, 102),
        'Mazatlan': (23, 106), 'Culiacan': (24, 107), 'Chihuahua': (28, 106)
    }
    
    ciudad_inicio = 'Guadalajara'
    ciudad_destino = 'Chihuahua'
    
    print(f"Buscando ruta de '{ciudad_inicio}' a '{ciudad_destino}'...")

    # Ejecutamos
    print("\nRESULTADO CON BÚSQUEDA VORAZ")
    camino_voraz = busqueda_voraz(mapa_con_trampa, ciudad_inicio, ciudad_destino, coordenadas)
    
    if camino_voraz:
        # Calculamos el costo real del camino que encontró
        costo_real = 0
        for i in range(len(camino_voraz) - 1):
            costo_real += mapa_con_trampa[camino_voraz[i]][camino_voraz[i+1]]
            
        print("Ruta encontrada:", " -> ".join(camino_voraz))
        print(f"Costo real de esta ruta: {costo_real} km")
        print("El algoritmo fue 'engañado' por la heurística y tomó la ruta que parecía más directa.")
    else:
        print("No se encontró una ruta.")