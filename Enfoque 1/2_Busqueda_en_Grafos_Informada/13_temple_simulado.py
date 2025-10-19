import numpy as np
import random
import math

def funcion_objetivo(x, y):
    """
    Define el "paisaje" con un pico alto (global) en (2, 2)
    y un pico más bajo (local) en (-2, -2).
    """
    pico1 = 1 * np.exp(-((x - 2)**2 + (y - 2)**2) / 4)
    pico2 = 0.75 * np.exp(-((x + 2)**2 + (y + 2)**2) / 4)
    return pico1 + pico2

def temple_simulado(funcion, limites, temp_inicial, temp_final, factor_enfriamiento):
    """
    Implementa el algoritmo de Temple Simulado (Simulated Annealing).
    """
    solucion_actual = np.array([random.uniform(l[0], l[1]) for l in limites])
    valor_actual = funcion(solucion_actual[0], solucion_actual[1])
    
    mejor_solucion = np.copy(solucion_actual)
    mejor_valor = valor_actual
    
    temperatura = temp_inicial

    while temperatura > temp_final:
        vecino = solucion_actual + np.random.uniform(-0.5, 0.5, size=2)
        vecino = np.clip(vecino, [l[0] for l in limites], [l[1] for l in limites])
        
        valor_vecino = funcion(vecino[0], vecino[1])
        delta_e = valor_vecino - valor_actual

        if delta_e > 0 or random.random() < math.exp(delta_e / temperatura):
            solucion_actual = vecino
            valor_actual = valor_vecino
        
        if valor_actual > mejor_valor:
            mejor_solucion = np.copy(solucion_actual)
            mejor_valor = valor_actual
        
        temperatura *= factor_enfriamiento
        
    return mejor_solucion, mejor_valor

if __name__ == "__main__":
    
    # --- Parámetros 'más pacientes' para una búsqueda más exhaustiva ---
    LIMITES = [(-5, 5), (-5, 5)]
    TEMP_INICIAL = 1000.0          # Empezar un poco más caliente
    TEMP_FINAL = 0.01
    FACTOR_ENFRIAMIENTO = 0.995    # ¡Este es el cambio clave! Enfriamiento más lento.

    print("Ejecutando Temple Simulado con enfriamiento lento...")
    print(f"El máximo global verdadero está cerca de (2, 2) con altura ~1.0")
    print("-" * 70)

    solucion, valor = temple_simulado(
        funcion_objetivo, 
        LIMITES, 
        TEMP_INICIAL, 
        TEMP_FINAL, 
        FACTOR_ENFRIAMIENTO
    )
    
    print("-" * 70)
    print(f"Búsqueda finalizada.")
    print(f"La mejor solución encontrada fue: ({solucion[0]:.2f}, {solucion[1]:.2f})")
    print(f"Altura máxima encontrada: {valor:.4f}")
    
    if solucion[0] > 0:
        print("Resultado: ¡Se encontró el Máximo Global!")
    else:
        print("Resultado: La búsqueda terminó en el Máximo Local.")