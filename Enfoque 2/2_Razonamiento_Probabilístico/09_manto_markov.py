# Reutilizamos la definición de la estructura
estructura_bn = {
    'Nublado': [],
    'Aspersor': ['Nublado'],
    'Lluvia': ['Nublado'],
    'Pasto Mojado': ['Lluvia', 'Aspersor']
}

# Función para encontrar el Manto de Markov

def encontrar_manto_markov(nodo_objetivo, estructura):
    """
    Identifica el conjunto de nodos que forman el Manto de Markov
    para un nodo_objetivo dado.
    """
    manto = set()

    # 1. Añadir Padres
    padres = estructura.get(nodo_objetivo, [])
    manto.update(padres)

    # 2. Encontrar Hijos y sus Otros Padres
    hijos = []
    for nodo, lista_padres in estructura.items():
        if nodo_objetivo in lista_padres:
            hijos.append(nodo)
            manto.add(nodo) # Añadir Hijos
            # 3. Añadir Otros Padres de los Hijos
            otros_padres = [p for p in lista_padres if p != nodo_objetivo]
            manto.update(otros_padres)

    # Asegurarse de no incluir el nodo objetivo en su propio manto
    manto.discard(nodo_objetivo)

    return manto

if __name__ == "__main__":

    nodo = 'Lluvia'
    manto_lluvia = encontrar_manto_markov(nodo, estructura_bn)
    print(f"El Manto de Markov para el nodo '{nodo}' es: {manto_lluvia}")
    # Resultado esperado: {'Nublado', 'Pasto Mojado', 'Aspersor'}
    #   - Padres: 'Nublado'
    #   - Hijos: 'Pasto Mojado'
    #   - Otros Padres del Hijo ('Pasto Mojado'): 'Aspersor'

    nodo = 'Nublado'
    manto_nublado = encontrar_manto_markov(nodo, estructura_bn)
    print(f"El Manto de Markov para el nodo '{nodo}' es: {manto_nublado}")
    # Resultado esperado: {'Aspersor', 'Lluvia'}
    #   - Padres: {}
    #   - Hijos: 'Aspersor', 'Lluvia'
    #   - Otros Padres de los Hijos: {}