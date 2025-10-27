# Definición de un Modelo Oculto de Markov (HMM)

# 1. Conjunto de Estados Ocultos
estados_ocultos = ['Llueve', 'No Llueve']

# 2. Conjunto de Observaciones Posibles
observaciones_posibles = ['Paraguas', 'No Paraguas']

# 3. Probabilidades Iniciales (Pi) - P(X_0)
#    Asumimos que al principio es igualmente probable que llueva o no.
prob_inicial = {'Llueve': 0.5, 'No Llueve': 0.5}

# 4. Matriz de Transición (A) - P(X_t | X_{t-1})
#    Representada como un diccionario anidado: A[estado_anterior][estado_siguiente]
matriz_transicion = {
    'Llueve':    {'Llueve': 0.7, 'No Llueve': 0.3}, # Si hoy llueve, 70% prob. de que mañana también
    'No Llueve': {'Llueve': 0.3, 'No Llueve': 0.7}  # Si hoy no llueve, 70% prob. de que mañana tampoco
}

# 5. Matriz de Emisión/Observación (B) - P(E_t | X_t)
#    Representada como un diccionario anidado: B[estado_oculto][observacion]
matriz_emision = {
    'Llueve':    {'Paraguas': 0.9, 'No Paraguas': 0.1}, # Si llueve, 90% prob. de ver paraguas
    'No Llueve': {'Paraguas': 0.2, 'No Paraguas': 0.8}  # Si no llueve, 20% prob. de ver paraguas
}

# Guardar el HMM completo en una estructura
hmm_paraguas = {
    'estados': estados_ocultos,
    'observaciones': observaciones_posibles,
    'prob_inicial': prob_inicial,
    'transicion': matriz_transicion,
    'emision': matriz_emision
}

# Mostrar la definición del HMM
if __name__ == "__main__":
    print("Modelo Oculto de Markov (HMM) para el problema del Paraguas:")
    print(f"  Estados Ocultos: {hmm_paraguas['estados']}")
    print(f"  Observaciones Posibles: {hmm_paraguas['observaciones']}")

    print("\n  Probabilidades Iniciales (π):")
    for estado, prob in hmm_paraguas['prob_inicial'].items():
        print(f"    P(Inicio={estado}) = {prob}")

    print("\n  Matriz de Transición (A):")
    for estado_prev, transiciones in hmm_paraguas['transicion'].items():
        for estado_sig, prob in transiciones.items():
            print(f"    P({estado_sig} | {estado_prev}) = {prob}")

    print("\n  Matriz de Emisión (B):")
    for estado, emisiones in hmm_paraguas['emision'].items():
        for obs, prob in emisiones.items():
            print(f"    P({obs} | {estado}) = {prob}")

    # Este objeto 'hmm_paraguas' sería la entrada para los algoritmos
    # de inferencia como Forward-Backward o Viterbi.