
heuristica = {'A': 1, 'B': 6, 'C': 8, 'D': 2, 'E': 4, 'F': 0, 'G': 0}

# Grafo Y/O (AND-OR)
# Estructura: 'Nodo': [[Lista de hijos], [Lista de hijos], ...]
# Cada lista interna es una alternativa (OR). Si una lista tiene múltiples nodos,
# es un conector AND.
grafo = {
    'A': [['B'], ['C']],
    'B': [['F']],
    'C': [['D', 'E']], # Para resolver C, DEBES resolver D y E (conector AND)
    'D': [['G']],
    'E': [['G']]
}

# Costos de las aristas (el costo de realizar una acción)
costos = {
    'A': {'B': 1, 'C': 1},
    'C': {'D': 1, 'E': 1},
    'B': {'F': 5},
    'D': {'G': 1},
    'E': {'G': 3}
}

# ALGORITMO AO*

def busqueda_ao_estrella(nodo_inicio, solucion):
    """
    Función principal que inicia la búsqueda del plan de menor costo.
    """
    global grafo, heuristica, costos
    print("ESTADO ACTUAL DEL GRAFO DE SOLUCIÓN:", solucion)
    print("==========================================================")
    
    if nodo_inicio in solucion:
        return # Si el nodo ya tiene una solución marcada, no hacemos nada.
        
    if not grafo.get(nodo_inicio): # Si es un nodo terminal (sin hijos)
        return

    # 1. Calcular el costo de cada alternativa (OR)
    costos_alternativas = {}
    for alternativa in grafo[nodo_inicio]:
        costo = 0
        camino = []
        # 2. Si es una alternativa con subtareas (AND), sumar sus costos
        for nodo_hijo in alternativa:
            costo += costos[nodo_inicio].get(nodo_hijo, 0) # Costo de la arista
            costo += heuristica[nodo_hijo] # Costo estimado del hijo
            camino.append(nodo_hijo)
        costos_alternativas[tuple(camino)] = costo

    # 3. Encontrar la alternativa de menor costo
    min_costo = min(costos_alternativas.values())
    mejor_alternativa = list(min(costos_alternativas, key=costos_alternativas.get))
    
    # 4. Actualizar la heurística del nodo actual y marcar el mejor camino
    heuristica[nodo_inicio] = min_costo
    solucion[nodo_inicio] = mejor_alternativa
    
    print("PROCESANDO NODO:", nodo_inicio, "| MEJOR ALTERNATIVA:", mejor_alternativa, "| COSTO ESTIMADO:", min_costo)

    # 5. Llamada recursiva: seguir explorando el plan que ahora parece ser el mejor
    for nodo_hijo in mejor_alternativa:
        busqueda_ao_estrella(nodo_hijo, solucion)


# Ejemplo de uso
if __name__ == "__main__":
    solucion_encontrada = {} # Diccionario para guardar el plan de solución
    nodo_inicial = 'A'
    
    print("Iniciando Búsqueda AO* para el problema:", nodo_inicial)
    print("----------------------------------------------------------")
    
    busqueda_ao_estrella(nodo_inicial, solucion_encontrada)
    
    print("\n\nBÚSQUEDA FINALIZADA")
    print("El plan de solución de menor costo encontrado es:")
    for nodo, plan in solucion_encontrada.items():
        print(f"  Para resolver '{nodo}', el mejor plan es ir a: {plan}")
        
    print(f"\nEl costo mínimo calculado para resolver '{nodo_inicial}' es: {heuristica[nodo_inicial]}")