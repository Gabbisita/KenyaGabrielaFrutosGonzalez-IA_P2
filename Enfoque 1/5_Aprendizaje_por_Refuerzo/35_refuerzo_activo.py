import random

# 1. Definición del Entorno
FILAS, COLS = 3, 4
ESTADOS = [(f, c) for f in range(FILAS) for c in range(COLS)]
TERMINALES = [(0, 3), (1, 3)]
PAREDES = [(1, 1)]
RECOMPENSAS = {(0, 3): 1, (1, 3): -1}
ACCIONES = ['arriba', 'abajo', 'izquierda', 'derecha']

def obtener_transicion_estocastica(estado, accion):
    """
    Simula el mundo aleatorio. El agente intenta 'accion', 
    pero puede resbalar (80% éxito, 10% izq, 10% der).
    """
    if estado in TERMINALES:
        return estado, 0 # Se queda en el terminal, sin recompensa
    
    # Acciones ortogonales (resbalones)
    acciones_laterales = {
        'arriba': ['izquierda', 'derecha'], 'abajo': ['izquierda', 'derecha'],
        'izquierda': ['arriba', 'abajo'], 'derecha': ['arriba', 'abajo']
    }
    
    num_aleatorio = random.random()
    if num_aleatorio < 0.8: 
        accion_final = accion
    elif num_aleatorio < 0.9: 
        accion_final = acciones_laterales[accion][0]
    else: 
        accion_final = acciones_laterales[accion][1]
    
    # Calcula el estado siguiente basado en la acción final
    f, c = estado
    if accion_final == 'arriba': f -= 1
    elif accion_final == 'abajo': f += 1
    elif accion_final == 'izquierda': c -= 1
    elif accion_final == 'derecha': c += 1
    
    estado_siguiente = (f, c)
    
    # Si choca o es inválido, se queda en su lugar
    if not (0 <= f < FILAS and 0 <= c < COLS and estado_siguiente not in PAREDES):
        estado_siguiente = estado
        
    recompensa = RECOMPENSAS.get(estado_siguiente, 0)
    return estado_siguiente, recompensa

# 2. Algoritmo Q-Learning

def q_learning(num_episodios, alpha, gamma, epsilon):
    """
    Aprende la política óptima Q(s, a) usando Q-Learning.
    """
    # Inicializa la tabla Q con ceros
    Q_tabla = {}
    for estado in ESTADOS:
        Q_tabla[estado] = {}
        for accion in ACCIONES:
            Q_tabla[estado][accion] = 0.0

    estados_inicio_validos = [s for s in ESTADOS if s not in TERMINALES and s not in PAREDES]

    for _ in range(num_episodios):
        estado_actual = random.choice(estados_inicio_validos)

        while estado_actual not in TERMINALES:
            
            # Lógica Epsilon-Greedy para elegir una acción
            if random.random() < epsilon:
                # Exploración
                accion = random.choice(ACCIONES)
            else:
                # Explotación
                accion = max(Q_tabla[estado_actual], key=Q_tabla[estado_actual].get)
            # Fin

            # Simular el movimiento
            estado_siguiente, recompensa = obtener_transicion_estocastica(estado_actual, accion)

            # Actualización Q-Learning
            viejo_q = Q_tabla[estado_actual][accion]
            
            # Obtener el valor de la mejor acción posible desde el *siguiente* estado
            max_q_siguiente = 0.0
            if estado_siguiente not in TERMINALES:
                max_q_siguiente = max(Q_tabla[estado_siguiente].values())
            
            # Calcular la nueva estimación (TD Target)
            nueva_estimacion = recompensa + gamma * max_q_siguiente
            
            # Actualizar el Q-valor
            Q_tabla[estado_actual][accion] = viejo_q + alpha * (nueva_estimacion - viejo_q)
            
            estado_actual = estado_siguiente
            
    return Q_tabla

def extraer_politica_de_Q(Q_tabla):
    """Extrae la política óptima a partir de la Q-tabla aprendida."""
    politica = {}
    for estado in ESTADOS:
        if estado in TERMINALES or estado in PAREDES:
            politica[estado] = '---'
            continue
        # La mejor política es simplemente tomar la acción con el Q-valor más alto
        politica[estado] = max(Q_tabla[estado], key=Q_tabla[estado].get)
    return politica

if __name__ == "__main__":
    
    # Parámetros
    ALPHA = 0.1       # Tasa de aprendizaje
    GAMMA = 0.9       # Factor de descuento
    EPSILON = 0.1     # 10% de probabilidad de explorar
    NUM_EPISODIOS = 50000 # Necesita muchas simulaciones para converger
    
    
    Q_tabla_aprendida = q_learning(NUM_EPISODIOS, ALPHA, GAMMA, EPSILON)
    
    politica_optima = extraer_politica_de_Q(Q_tabla_aprendida)

    print("\nPolítica Óptima Aprendida por Q-Learning")
    for f in range(FILAS):
        linea = " | ".join([f"{politica_optima.get((f, c), '---'):^9}" for c in range(COLS)])
        print(linea)