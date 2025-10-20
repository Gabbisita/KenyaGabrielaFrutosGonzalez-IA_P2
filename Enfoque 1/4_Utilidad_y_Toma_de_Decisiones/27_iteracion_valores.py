
def iteracion_de_valores(mdp, epsilon=0.001):
    """
    Algoritmo de Iteración de Valores para resolver un MDP.
    
    Args:
        mdp (dict): La definición del Proceso de Decisión de Markov.
        epsilon (float): El umbral para la convergencia.
    """
    # 1. Inicialización: Todas las utilidades a 0.
    utilidades = {s: 0 for s in mdp['estados']}
    gamma = mdp['gamma']
    
    while True:
        nuevas_utilidades = utilidades.copy()
        delta = 0
        
        # 2. Bucle de Iteración: para cada estado
        for estado in mdp['estados']:
            # Si es un estado terminal, su utilidad es su recompensa.
            if estado in mdp['terminales']:
                nuevas_utilidades[estado] = mdp['recompensas'].get(estado, 0)
                continue

            # Aplicar la Ecuación de Bellman 
            valores_acciones = []
            for accion in mdp['acciones']:
                valor_accion = 0
                # Calcular el valor esperado para una acción
                for (prob, estado_siguiente) in mdp['transiciones'](estado, accion):
                    recompensa = mdp['recompensas'].get(estado_siguiente, 0)
                    valor_accion += prob * (recompensa + gamma * utilidades[estado_siguiente])
                valores_acciones.append(valor_accion)
            
            # El nuevo valor del estado es el máximo de los valores de sus acciones
            nuevas_utilidades[estado] = max(valores_acciones)
            # --- Fin de la Ecuación de Bellman ---
            
            # Medir el cambio máximo en las utilidades
            delta = max(delta, abs(nuevas_utilidades[estado] - utilidades[estado]))
            
        utilidades = nuevas_utilidades
        
        # 3. Terminar: si los valores ya no cambian mucho, hemos convergido.
        if delta < epsilon * (1 - gamma) / gamma:
            return utilidades

def extraer_politica_optima(mdp, utilidades):
    """
    Una vez calculadas las utilidades, extrae la mejor acción para cada estado.
    """
    politica = {}
    for estado in mdp['estados']:
        if estado in mdp['terminales']:
            politica[estado] = None
            continue
            
        mejor_accion = None
        max_valor = -float('inf')
        for accion in mdp['acciones']:
            valor_accion = 0
            for (prob, estado_siguiente) in mdp['transiciones'](estado, accion):
                valor_accion += prob * utilidades[estado_siguiente]
            
            if valor_accion > max_valor:
                max_valor = valor_accion
                mejor_accion = accion
        politica[estado] = mejor_accion
    return politica


if __name__ == "__main__":
    
    # Definición de nuestro laberinto (Grid World)
    filas, cols = 3, 4
    estados = [(f, c) for f in range(filas) for c in range(cols)]
    recompensas = {(0, 3): 1, (1, 3): -1}
    terminales = [(0, 3), (1, 3)]
    paredes = [(1, 1)]
    acciones = ['arriba', 'abajo', 'izquierda', 'derecha']

    def transiciones(estado, accion):
        # Función que devuelve los posibles estados siguientes y sus probabilidades
        # En este mundo determinista, solo hay un resultado con probabilidad 1.0
        if estado in terminales:
            return [(1.0, estado)] # No hay movimiento desde un terminal
        
        f, c = estado
        f_nuevo, c_nuevo = f, c
        
        if accion == 'arriba': f_nuevo -= 1
        elif accion == 'abajo': f_nuevo += 1
        elif accion == 'izquierda': c_nuevo -= 1
        elif accion == 'derecha': c_nuevo += 1
            
        estado_siguiente = (f_nuevo, c_nuevo)
        
        # Si el movimiento es inválido (fuera del tablero o contra una pared), se queda en su lugar
        if not (0 <= f_nuevo < filas and 0 <= c_nuevo < cols and estado_siguiente not in paredes):
            estado_siguiente = estado
            
        return [(1.0, estado_siguiente)]

    mdp = {
        'estados': estados,
        'acciones': acciones,
        'transiciones': transiciones,
        'recompensas': recompensas,
        'terminales': terminales,
        'gamma': 0.9
    }
    
    # 1. Calcular las utilidades
    utilidades_optimas = iteracion_de_valores(mdp)
    
    print("Utilidades Óptimas (Valor de cada estado)")
    for f in range(filas):
        linea = " | ".join([f"{utilidades_optimas.get((f, c), 0):.2f}" for c in range(cols)])
        print(linea)

    # 2. Extraer la política
    politica_optima = extraer_politica_optima(mdp, utilidades_optimas)
    
    print("\nPolítica Óptima (Mejor acción en cada estado)")
    for f in range(filas):
        row = []
        for c in range(cols):
            accion = politica_optima.get((f, c))
            row.append(f"{accion if accion is not None else '---':^9}")
        linea = " | ".join(row)
        print(linea)