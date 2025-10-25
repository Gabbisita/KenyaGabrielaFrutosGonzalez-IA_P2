import numpy as np

# Definición de la Red Bayesiana Dinámica (HMM)

# P(X_0) - Probabilidad Inicial
p_inicial = {'Llueve': 0.5, 'No Llueve': 0.5}

# P(X_t | X_{t-1}) - Modelo de Transición (Cómo cambia el clima)
p_transicion = {
    'Llueve':    {'Llueve': 0.7, 'No Llueve': 0.3}, # Si hoy llueve, 70% prob. de que mañana también
    'No Llueve': {'Llueve': 0.3, 'No Llueve': 0.7}  # Si hoy no llueve, 70% prob. de que mañana tampoco
}
p_transicion = {
    'Llueve':    {'Llueve': 0.7, 'No Llueve': 0.3}, # Si hoy llueve, 70% prob. de que mañana también
    'No Llueve': {'Llueve': 0.3, 'No Llueve': 0.7}  # Si hoy no llueve, 70% prob. de que mañana tampoco
}

# P(E_t | X_t) - Modelo de Observación (Sensor)
p_observacion = {
    'Llueve':    {'Paraguas': 0.9, 'No Paraguas': 0.1}, # Si llueve, 90% prob. de que traiga paraguas
    'No Llueve': {'Paraguas': 0.2, 'No Paraguas': 0.8}  # Si no llueve, 20% prob. de que lo traiga "por si acaso"
}

# Algoritmo de Filtrado (Hacia Delante)

def normalizar(creencia):
    """Asegura que las probabilidades sumen 1.0"""
    total = sum(creencia.values())
    if total == 0:
        return creencia
    for estado in creencia:
        creencia[estado] /= total
    return creencia

def forward_update(creencia_anterior, observacion):
    """
    Realiza un paso de filtrado (Predicción + Actualización).
    Calcula P(X_t | e_1, ..., e_t)
    """
    estados = creencia_anterior.keys()
    creencia_predicha = {s: 0.0 for s in estados}
    
    # Paso de predicción
    # P(X_t | e_1, ..., e_{t-1}) = Σ P(X_t | x_{t-1}) * P(x_{t-1} | e_1, ..., e_{t-1})
    for estado_siguiente in estados:
        suma = 0
        for estado_actual in estados:
            prob_trans = p_transicion[estado_actual][estado_siguiente]
            prob_anterior = creencia_anterior[estado_actual]
            suma += prob_trans * prob_anterior
        creencia_predicha[estado_siguiente] = suma
        
    # Paso de actualización
    # P(X_t | e_1, ..., e_t) ∝ P(e_t | X_t) * P(X_t | e_1, ..., e_{t-1})
    creencia_actualizada = {s: 0.0 for s in estados}
    for estado in estados:
        prob_obs = p_observacion[estado][observacion]
        creencia_actualizada[estado] = prob_obs * creencia_predicha[estado]
        
    # Normalización
    return normalizar(creencia_actualizada)

def imprimir_creencia(creencia, dia):
    print(f"Creencia del Día {dia}")
    lluvia = creencia.get('Llueve', 0) * 100
    print(f"  P(Llueve)    = {lluvia:.1f}%")
    print(f"  P(No Llueve) = {(100 - lluvia):.1f}%")

# Simulación a lo largo del tiempo
if __name__ == "__main__":
    
    # Secuencia de observaciones (lo que vemos cada día)
    observaciones_secuencia = ['Paraguas', 'Paraguas', 'No Paraguas', 'No Paraguas']
    
    # Creencia inicial (Día 0)
    creencia_actual = p_inicial
    print("Creencia Inicial (Día 0): 50.0% de que llueve.")
    
    # Simulación
    for i, obs in enumerate(observaciones_secuencia):
        print(f"\n[Observación Día {i+1}: {obs}]")
        creencia_actual = forward_update(creencia_actual, obs)
        imprimir_creencia(creencia_actual, i+1)