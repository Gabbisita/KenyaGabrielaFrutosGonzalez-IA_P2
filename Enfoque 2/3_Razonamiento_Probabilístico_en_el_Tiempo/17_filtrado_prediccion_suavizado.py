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

# Algoritmo Hacia Delante (Filtrado)
def normalizar(creencia):
    total = sum(creencia.values())
    if total == 0: return {s: 1.0/len(creencia) for s in creencia}
    return {s: p / total for s, p in creencia.items()}

def forward_update(creencia_anterior, observacion):
    """Realiza un paso de FILTRADO: Calcula P(X_t | e_{1:t})"""
    # Predicción (Time Update)
    creencia_predicha = {s_sig: 0.0 for s_sig in estados}
    for s_sig in estados:
        suma = 0
        for s_act in estados:
            suma += p_transicion[s_act][s_sig] * creencia_anterior[s_act]
        creencia_predicha[s_sig] = suma
        
    # Actualización (Measurement Update)
    creencia_actualizada = {s: 0.0 for s in estados}
    for s in estados:
        creencia_actualizada[s] = p_observacion[s][observacion] * creencia_predicha[s]
        
    return normalizar(creencia_actualizada)

# Función de Predicción
def predecir(creencia_actual, k_pasos):
    """Realiza PREDICCIÓN: Calcula P(X_{t+k} | e_{1:t})"""
    creencia_predicha = creencia_actual.copy()
    for _ in range(k_pasos):
        creencia_siguiente_paso = {s_sig: 0.0 for s_sig in estados}
        for s_sig in estados:
            suma = 0
            for s_act in estados:
                suma += p_transicion[s_act][s_sig] * creencia_predicha[s_act]
            creencia_siguiente_paso[s_sig] = suma
        # No se normaliza aquí usualmente, pero lo haremos para ver la distribución
        creencia_predicha = normalizar(creencia_siguiente_paso)
    return creencia_predicha

# Simulación
if __name__ == "__main__":
    
    observaciones_secuencia = ['Paraguas', 'Paraguas']
    
    creencia_actual = p_inicial
    print(f"Creencia Inicial (Día 0): P(Llueve)={creencia_actual['Llueve']:.2f}")
    
    # Filtrado día a día
    for i, obs in enumerate(observaciones_secuencia):
        print(f"\n Día {i+1}")
        print(f"Observación: {obs}")
        creencia_actual = forward_update(creencia_actual, obs)
        print("Resultado del FILTRADO:")
        print(f"  P(X_{i+1}='Llueve' | e_{1:{i+1}}) = {creencia_actual['Llueve']:.3f}")
        
    # Predicción después del último filtrado
    print("\nPredicción para el futuro (basado en Día 2)")
    k = 1 # Predecir 1 día adelante (Día 3)
    creencia_predicha_k1 = predecir(creencia_actual, k)
    print(f"Resultado de la PREDICCIÓN para Día {len(observaciones_secuencia) + k}:")
    print(f"  P(X_{len(observaciones_secuencia) + k}='Llueve' | e_{1:{len(observaciones_secuencia)}}) = {creencia_predicha_k1['Llueve']:.3f}")

    k = 2 # Predecir 2 días adelante (Día 4)
    creencia_predicha_k2 = predecir(creencia_actual, k)
    print(f"\nResultado de la PREDICCIÓN para Día {len(observaciones_secuencia) + k}:")
    print(f"  P(X_{len(observaciones_secuencia) + k}='Llueve' | e_{1:{len(observaciones_secuencia)}}) = {creencia_predicha_k2['Llueve']:.3f}")

    print("\n(Para Suavizado y Explicación Más Probable se necesitan otros algoritmos como Forward-Backward y Viterbi)")