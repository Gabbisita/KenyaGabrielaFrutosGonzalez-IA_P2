import numpy as np

# Definición del HMM
estados_ocultos = ['Llueve', 'No Llueve']
observaciones_posibles = ['Paraguas', 'No Paraguas']
prob_inicial = {'Llueve': 0.5, 'No Llueve': 0.5}
matriz_transicion = {
    'Llueve':    {'Llueve': 0.7, 'No Llueve': 0.3},
    'No Llueve': {'Llueve': 0.3, 'No Llueve': 0.7}
}
matriz_emision = {
    'Llueve':    {'Paraguas': 0.9, 'No Paraguas': 0.1},
    'No Llueve': {'Paraguas': 0.2, 'No Paraguas': 0.8}
}

# Algoritmo de Viterbi

def viterbi(observaciones_sec, estados, p_ini, p_trans, p_emis):
    """
    Encuentra la secuencia de estados ocultos más probable usando Viterbi.
    """
    # T: Longitud de la secuencia de observaciones
    T = len(observaciones_sec)
    # N: Número de estados ocultos
    N = len(estados)
    # Mapeo de estado a índice para facilitar el acceso a matrices
    estado_a_idx = {estado: i for i, estado in enumerate(estados)}
    idx_a_estado = {i: estado for i, estado in enumerate(estados)}

    # T1: Matriz Viterbi - guarda la probabilidad máxima del camino hasta t
    #     viterbi_mat[i, t] = max_{x_{1:t-1}} P(x_1..x_{t-1}, X_t=i, e_1..e_t)
    viterbi_mat = np.zeros((N, T))
    # T2: Matriz Backpointer - guarda el índice del estado anterior en el camino más probable
    backpointer = np.zeros((N, T), dtype=int)

    # Inicialización (t=0)
    obs_0 = observaciones_sec[0]
    for i, estado in enumerate(estados):
        viterbi_mat[i, 0] = p_ini[estado] * p_emis[estado][obs_0]
        backpointer[i, 0] = 0 # No hay estado anterior

    # Recursión (t=1 hasta T-1)
    for t in range(1, T):
        obs_t = observaciones_sec[t]
        for j, estado_j in enumerate(estados): # Estado actual j
            max_prob = -1.0
            mejor_prev_estado_idx = -1
            for i, estado_i in enumerate(estados): # Estado anterior i
                # Prob = Prob_del_camino_hasta_i * Prob_transicion(i->j)
                prob_camino = viterbi_mat[i, t-1] * p_trans[estado_i][estado_j]
                if prob_camino > max_prob:
                    max_prob = prob_camino
                    mejor_prev_estado_idx = i

            # Multiplicar por la probabilidad de emisión P(obs_t | estado_j)
            viterbi_mat[j, t] = max_prob * p_emis[estado_j][obs_t]
            backpointer[j, t] = mejor_prev_estado_idx

    # Terminación
    # Encontrar la probabilidad del mejor camino completo
    prob_mejor_camino = np.max(viterbi_mat[:, T-1])
    # Encontrar el índice del último estado en el mejor camino
    mejor_ultimo_estado_idx = np.argmax(viterbi_mat[:, T-1])

    #  Reconstrucción del Camino (Backtracking)
    mejor_camino = [idx_a_estado[mejor_ultimo_estado_idx]]
    idx_actual = mejor_ultimo_estado_idx
    for t in range(T-1, 0, -1):
        idx_previo = backpointer[idx_actual, t]
        mejor_camino.insert(0, idx_a_estado[idx_previo])
        idx_actual = idx_previo

    return mejor_camino, prob_mejor_camino

# Ejecución
if __name__ == "__main__":
    observaciones_secuencia = ['Paraguas', 'Paraguas', 'No Paraguas']
    T = len(observaciones_secuencia)

    print(f"Observaciones: {observaciones_secuencia}")
    print("\nCalculando la secuencia de clima más probable usando Viterbi...")

    secuencia_mas_probable, probabilidad = viterbi(
        observaciones_secuencia,
        estados_ocultos,
        prob_inicial,
        matriz_transicion,
        matriz_emision
    )


    print("\nResultados")
    print(f"La secuencia de estados ocultos (clima) más probable es:")
    print(f"  -> {' -> '.join(secuencia_mas_probable)}")
    # print(f"Con una probabilidad (aproximada, sin escalar) de: {probabilidad:.4e}") # La probabilidad absoluta puede ser muy pequeña