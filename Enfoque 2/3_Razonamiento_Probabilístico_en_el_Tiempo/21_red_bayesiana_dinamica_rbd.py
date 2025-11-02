import numpy as np

# Definición de la DBN

# Variables por time slice: X_t (Oculta: Clima), E_t (Observación: Paraguas)
estados_ocultos = ['Llueve', 'No Llueve']
observaciones_posibles = ['Paraguas', 'No Paraguas']

# Red Intra-Slice (en t=0): Define P(X_0)
# (No hay conexiones intra-slice en este HMM simple más allá de X_0)
p_inicial = {'Llueve': 0.5, 'No Llueve': 0.5}

# Red de Transición (de t-1 a t): Define P(X_t | X_{t-1}) y P(E_t | X_t)
# P(X_t | X_{t-1}) - Modelo de Transición
p_transicion = {
    'Llueve':    {'Llueve': 0.7, 'No Llueve': 0.3},
    'No Llueve': {'Llueve': 0.3, 'No Llueve': 0.7}
}
# P(E_t | X_t) - Modelo de Observación/Sensor
p_observacion = {
    'Llueve':    {'Paraguas': 0.9, 'No Paraguas': 0.1},
    'No Llueve': {'Paraguas': 0.2, 'No Paraguas': 0.8}
}

# Inferencia: Algoritmo Hacia Delante (Filtrado)
#    (Calcula P(X_t | e_{1:t}))

def normalizar(creencia):
    total = sum(creencia.values())
    if total == 0: return {s: 1.0/len(creencia) for s in creencia}
    return {s: p / total for s, p in creencia.items()}

def forward_update(creencia_anterior, observacion):
    """Realiza un paso de FILTRADO en la DBN (HMM)."""
    estados = list(creencia_anterior.keys())
    # Predicción (Time Update): P(X_t | e_{1:t-1})
    creencia_predicha = {s_sig: 0.0 for s_sig in estados}
    for s_sig in estados:
        suma = 0
        for s_act in estados:
            suma += p_transicion[s_act][s_sig] * creencia_anterior[s_act]
        creencia_predicha[s_sig] = suma

    # Actualización (Measurement Update): P(X_t | e_{1:t})
    creencia_actualizada = {s: 0.0 for s in estados}
    for s in estados:
        creencia_actualizada[s] = p_observacion[s][observacion] * creencia_predicha[s]

    return normalizar(creencia_actualizada)

def imprimir_creencia(creencia, dia):
    print(f"--- Creencia del Día {dia} (Filtrado DBN) ---")
    lluvia = creencia.get('Llueve', 0) * 100
    print(f"  P(Clima=Llueve) = {lluvia:.1f}%")

# Simulación
if __name__ == "__main__":
    observaciones_secuencia = ['Paraguas', 'Paraguas', 'No Paraguas']
    creencia_actual = p_inicial
    print("Creencia Inicial (Día 0): P(Llueve)=50.0%")

    for i, obs in enumerate(observaciones_secuencia):
        print(f"\n[Observación Día {i+1}: {obs}]")
        creencia_actual = forward_update(creencia_actual, obs)
        imprimir_creencia(creencia_actual, i+1)
        