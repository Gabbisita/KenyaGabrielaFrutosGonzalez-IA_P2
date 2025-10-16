
def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    pila = [[inicio]]
    # Para IDDFS, es crucial no usar un 'visitados' global entre llamadas con
    # diferentes límites, pero sí para evitar ciclos en un mismo camino.
    while pila:
        camino_actual = pila.pop()
        nodo_actual = camino_actual[-1]

        if nodo_actual == objetivo:
            return camino_actual
            
        if len(camino_actual) - 1 < limite:
            for vecino in grafo.get(nodo_actual, []):
                if vecino not in camino_actual:
                    nuevo_camino = list(camino_actual)
                    nuevo_camino.append(vecino)
                    pila.append(nuevo_camino)
    return None


def busqueda_profundidad_iterativa(grafo, inicio, objetivo):
    # Empezamos con un límite de profundidad de 0 y lo incrementamos.
    limite = 0
    while True:
        print(f"Intentando con límite de profundidad: {limite}...")
        
        # Llamamos a DLS con el límite actual.
        resultado = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite)
        
        # Si DLS encontró un resultado, esa es nuestra solución óptima.
        if resultado is not None:
            return resultado
        
        # Si no, incrementamos el límite y volvemos a intentarlo.
        limite += 1
        
        # Opcional: poner un límite máximo para evitar bucles infinitos en grafos
        # muy grandes o sin solución. len(grafo) es un límite razonable.
        if limite > len(grafo):
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
    
    print(f"Buscando ruta de '{ciudad_inicio}' a '{ciudad_destino}' con Búsqueda en Profundidad Iterativa (IDDFS)")
    
    camino_encontrado = busqueda_profundidad_iterativa(mapa_ciudades, ciudad_inicio, ciudad_destino)
    
    if camino_encontrado:
        print("\n¡Ruta óptima encontrada!")
        print(f"  -> Recorrido: {' -> '.join(camino_encontrado)}")
        print(f"  -> Pasos: {len(camino_encontrado) - 1}")
    else:
        print("No se encontró una ruta.")