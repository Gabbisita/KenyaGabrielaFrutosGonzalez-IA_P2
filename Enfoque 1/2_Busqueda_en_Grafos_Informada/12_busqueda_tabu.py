import numpy as np
import random

def funcion_objetivo(x, y):
    """
    Define el "paisaje" con un pico alto (global) en (2, 2)
    y un pico más bajo (local) en (-2, -2).
    """
    pico1 = 1 * np.exp(-((x - 2)**2 + (y - 2)**2) / 4)
    pico2 = 0.75 * np.exp(-((x + 2)**2 + (y + 2)**2) / 4)
    return pico1 + pico2

def ascension_colinas_simple(funcion, limites, paso, max_iteraciones):
    """
    Implementa el algoritmo simple de Ascensión de Colinas desde un único punto de partida.
    """
    # Empezar en un punto aleatorio dentro de los límites.
    solucion_actual = np.array([random.uniform(l[0], l[1]) for l in limites])
    
    for _ in range(max_iteraciones):
        valor_actual = funcion(solucion_actual[0], solucion_actual[1])
        mejor_vecino = None
        mejor_valor_vecino = valor_actual

        # Explorar los vecinos inmediatos
        for dx in [-paso, 0, paso]:
            for dy in [-paso, 0, paso]:
                if dx == 0 and dy == 0:
                    continue

                vecino_potencial = solucion_actual + np.array([dx, dy])
                if not (limites[0][0] <= vecino_potencial[0] <= limites[0][1] and
                        limites[1][0] <= vecino_potencial[1] <= limites[1][1]):
                    continue
                
                valor_vecino = funcion(vecino_potencial[0], vecino_potencial[1])
                if valor_vecino > mejor_valor_vecino:
                    mejor_valor_vecino = valor_vecino
                    mejor_vecino = vecino_potencial

        # Si ningún vecino es mejor, hemos llegado a una cima.
        if mejor_vecino is None:
            break
        else:
            solucion_actual = mejor_vecino
            
    return solucion_actual, funcion(solucion_actual[0], solucion_actual[1])

def busqueda_con_reinicios(numero_de_intentos):
    """
    Ejecuta la Ascensión de Colinas múltiples veces y devuelve el mejor resultado global.
    """
    mejor_solucion_global = None
    mejor_valor_global = -np.inf

    for i in range(numero_de_intentos):
        # Cada intento empieza desde un nuevo punto aleatorio.
        solucion_local, valor_local = ascension_colinas_simple(
            funcion_objetivo, 
            [(-5, 5), (-5, 5)], 
            0.1, 
            1000
        )
        
        print(f"Intento #{i+1}: Encontró un pico en ({solucion_local[0]:.2f}, {solucion_local[1]:.2f}) con altura {valor_local:.4f}")
        
        # Si este intento encontró una solución mejor que la global, la guardamos.
        if valor_local > mejor_valor_global:
            mejor_valor_global = valor_local
            mejor_solucion_global = solucion_local
            
    return mejor_solucion_global, mejor_valor_global

if __name__ == "__main__":
    
    NUMERO_DE_INTENTOS = 20 # Realizar 20 búsquedas independientes

    print(f"Ejecutando Ascensión de Colinas con {NUMERO_DE_INTENTOS} Reinicios Aleatorios...")
    print(f"El máximo global verdadero está cerca de (2, 2) con altura ~1.0")
    print("-" * 70)

    solucion, valor = busqueda_con_reinicios(NUMERO_DE_INTENTOS)
    
    print("-" * 70)
    print(f"Búsqueda finalizada.")
    print(f"La MEJOR solución encontrada entre todos los intentos fue: ({solucion[0]:.2f}, {solucion[1]:.2f})")
    print(f"Altura máxima encontrada: {valor:.4f}")
    
    if solucion[0] > 0:
        print("Resultado: ¡Se encontró el Máximo Global!")
    else:
        print("Resultado: El mejor resultado fue un Máximo Local.")