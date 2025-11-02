import numpy as np

# Definición del HMM
p_inicial = {'Llueve': 0.5, 'No Llueve': 0.5}
p_transicion = {
    'Llueve':    {'Llueve': 0.7, 'No Llueve': 0.3},
    'No Llueve': {'Llueve': 0.3, 'No Llueve': 0.7}
}

p_observacion = {
    'Llueve':    {'Paraguas': 0.9, 'No Paraguas': 0.1},
    'No Llueve': {'Paraguas': 0.2, 'No Paraguas': 0.8}
}
estados = list(p_inicial.keys())

# Funciones Auxiliares
def normalizar(creencia):
    total = sum(creencia.values())
    if total == 0: return {s: 1.0/len(creencia) for s in creencia}
    return {s: p / total for s, p in creencia.items()}

def forward_pass(observaciones_secuencia):
    """Realiza el pase hacia adelante y guarda todos los mensajes alfa."""
    mensajes_alfa = []
    creencia_actual = p_inicial
    
    # Alfa para t=0 (estado inicial) - Necesitamos ajustar para la fórmula
    # Lo calcularemos a partir de t=1
    
    alfa_t = p_inicial # Usaremos esto como P(X_0)
    
    for i, obs in enumerate(observaciones_secuencia):
        # Predicción (Time Update)
        creencia_predicha = {s_sig: 0.0 for s_sig in estados}
        for s_sig in estados:
            suma = 0
            for s_act in estados:
                # Si i=0, usamos p_inicial como creencia_anterior
                creencia_anterior_estado = alfa_t[s_act]
                suma += p_transicion[s_act][s_sig] * creencia_anterior_estado
            creencia_predicha[s_sig] = suma
            
        # Actualización (Measurement Update)
        creencia_actualizada = {s: 0.0 for s in estados}
        for s in estados:
            creencia_actualizada[s] = p_observacion[s][obs] * creencia_predicha[s]
        
        # Guardar el mensaje alfa normalizado (para filtrado) o sin normalizar
        # Para Forward-Backward, a menudo se usa sin normalizar, pero normalizar
        # ayuda a evitar underflow numérico. Guardaremos normalizado aquí.
        alfa_t = normalizar(creencia_actualizada)
        mensajes_alfa.append(alfa_t)
        
    return mensajes_alfa

# Pase Hacia Atrás
def backward_pass(observaciones_secuencia):
    """Realiza el pase hacia atrás y guarda todos los mensajes beta."""
    T = len(observaciones_secuencia)
    # Inicializar beta_T a 1
    mensajes_beta = [{} for _ in range(T + 1)]
    mensajes_beta[T] = {s: 1.0 for s in estados} # Beta(T) = 1

    # Iterar hacia atrás desde T-1 hasta 0
    for k in range(T - 1, -1, -1):
        obs_siguiente = observaciones_secuencia[k] # Observación en t = k+1
        beta_k = {s_k: 0.0 for s_k in estados} # Beta(k)
        
        for s_k in estados: # Estado actual en k
            suma = 0
            for s_k_mas_1 in estados: # Posible estado siguiente en k+1
                prob_trans = p_transicion[s_k][s_k_mas_1]
                prob_obs = p_observacion[s_k_mas_1][obs_siguiente]
                beta_siguiente = mensajes_beta[k + 1][s_k_mas_1]
                suma += prob_trans * prob_obs * beta_siguiente
            beta_k[s_k] = suma
            
        # Opcional: normalizar beta para evitar underflow/overflow
        mensajes_beta[k] = normalizar(beta_k) # Normalizamos en cada paso
        
    return mensajes_beta[1:] # Devolvemos desde beta_1 hasta beta_T


# Función de Suavizado
def smoothing(mensajes_alfa, mensajes_beta):
    """Calcula las probabilidades suavizadas P(X_k | e_{1:T})"""
    T = len(mensajes_alfa)
    prob_suavizadas = []
    
    for k in range(T):
        alfa_k = mensajes_alfa[k]
        beta_k = mensajes_beta[k] # Beta_k representa P(e_{k+1:T} | X_k)
        
        # Producto punto a punto (sin normalizar aún)
        producto = {s: alfa_k[s] * beta_k[s] for s in estados}
        
        # Normalizar para obtener la distribución final
        prob_suavizadas.append(normalizar(producto))
        
    return prob_suavizadas

# Simulación
if __name__ == "__main__":
    
    observaciones_secuencia = ['Paraguas', 'Paraguas', 'No Paraguas']
    T = len(observaciones_secuencia)
    
    print(" Ejecutando Algoritmo Forward-Backward ")
    
    # 1. Calcular mensajes hacia adelante (Filtrado)
    mensajes_alfa = forward_pass(observaciones_secuencia)
    print("\nMensajes Alfa (Filtrado P(X_k | e_{1:k})):")
    for k, alfa in enumerate(mensajes_alfa):
        print(f"  Día {k+1}: P(Llueve) = {alfa['Llueve']:.3f}")

    # 2. Calcular mensajes hacia atrás
    mensajes_beta = backward_pass(observaciones_secuencia)
    # (Los mensajes beta no tienen una interpretación tan directa, son intermedios)

    # 3. Calcular probabilidades suavizadas
    prob_suavizadas = smoothing(mensajes_alfa, mensajes_beta)
    print("\nProbabilidades Suavizadas P(X_k | e_{1:T}):")
    for k, prob in enumerate(prob_suavizadas):
        print(f"  Día {k+1}: P(Llueve) = {prob['Llueve']:.3f}")

    print("\nObserva cómo las probabilidades suavizadas pueden diferir de las filtradas,")
    print("especialmente en los primeros días, al incorporar la evidencia futura.")