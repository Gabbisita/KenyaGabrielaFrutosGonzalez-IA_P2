
# Probabilidades Condicionales para el nodo de azar 'Lluvia Real'
# P(Lluvia Real | Pronóstico)
P_Lluvia_dado_Pronostico = {
    'Lluvioso': {'Lluvia_Real_Si': 0.7, 'Lluvia_Real_No': 0.3},
    'Soleado':  {'Lluvia_Real_Si': 0.2, 'Lluvia_Real_No': 0.8}
}

# Tabla de Utilidad para el nodo de 'Satisfacción'
# U(Decisión, Resultado del Azar)
utilidad = {
    'Llevar_Paraguas_Si': {
        'Lluvia_Real_Si': 70,  # Bien: te mantienes seco
        'Lluvia_Real_No': 20   # Malo: cargaste el paraguas sin razón
    },
    'Llevar_Paraguas_No': {
        'Lluvia_Real_Si': -100, # Muy malo: te empapas
        'Lluvia_Real_No': 100  # Excelente: vas ligero y no llueve
    }
}


def calcular_mejor_decision(evidencia):
    """
    Calcula la Máxima Utilidad Esperada (MEU) dadas las evidencias.
    """
    mejor_decision = None
    max_utilidad_esperada = -float('inf')
    
    decisiones_posibles = ['Llevar_Paraguas_Si', 'Llevar_Paraguas_No']
    resultados_posibles = ['Lluvia_Real_Si', 'Lluvia_Real_No']
    
    # 1. Iterar sobre cada posible decisión.
    for decision in decisiones_posibles:
        utilidad_esperada_actual = 0
        
        # 2. Calcular la utilidad esperada para esa decisión.
        for resultado in resultados_posibles:
            # Obtener la probabilidad del resultado, dada la evidencia.
            prob_resultado = P_Lluvia_dado_Pronostico[evidencia['Pronostico']][resultado]
            
            # Obtener la utilidad de esa combinación de decisión y resultado.
            utilidad_resultado = utilidad[decision][resultado]
            
            # Sumar al total ponderado.
            utilidad_esperada_actual += prob_resultado * utilidad_resultado
        
        print(f"  -> Utilidad Esperada si la decisión es '{decision}': {utilidad_esperada_actual:.2f}")

        # 3. Guardar la mejor decisión encontrada hasta ahora.
        if utilidad_esperada_actual > max_utilidad_esperada:
            max_utilidad_esperada = utilidad_esperada_actual
            mejor_decision = decision

    return mejor_decision, max_utilidad_esperada


if __name__ == "__main__":

    # CASO 1: Vemos que el pronóstico es 'Lluvioso'
    evidencia_observada = {'Pronostico': 'Lluvioso'}
    print(f"CASO 1: La evidencia es que el Pronóstico es '{evidencia_observada['Pronostico']}'")
    
    decision, valor = calcular_mejor_decision(evidencia_observada)
    
    print("-" * 25)
    print(f"Mejor Decisión: {decision}")
    print(f"Valor (MEU): {valor:.2f}\n")
    
    print("\n" + "="*50 + "\n")
    
    # CASO 2: Vemos que el pronóstico es 'Soleado'
    evidencia_observada = {'Pronostico': 'Soleado'}
    print(f"CASO 2: La evidencia es que el Pronóstico es '{evidencia_observada['Pronostico']}'")
    
    decision, valor = calcular_mejor_decision(evidencia_observada)
    
    print("-" * 25)
    print(f"Mejor Decisión: {decision}")
    print(f"Valor (MEU): {valor:.2f}")