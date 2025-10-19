import numpy as np
import random

def funcion_objetivo(x, y):
    """
    Define el "paisaje" que queremos escalar. 
    Tiene un pico alto (máximo global) cerca de (2, 2) y
    un pico más bajo (máximo local) cerca de (-2, -2).
    La función devuelve la "altura" en cualquier punto (x, y).
    """
    # Pico principal (global)
    pico1 = 1 * np.exp(-((x - 2)**2 + (y - 2)**2) / 4)
    # Pico secundario (local)
    pico2 = 0.75 * np.exp(-((x + 2)**2 + (y + 2)**2) / 4)
    return pico1 + pico2

def ascension_colinas(funcion, limites, paso, max_iteraciones):
    """
    Implementa el algoritmo de Búsqueda de Ascensión de Colinas.
    
    Args:
        funcion (function): La función objetivo a maximizar.
        limites (list): Tuplas con los límites para cada variable, ej. [(-5, 5), (-5, 5)].
        paso (float): El tamaño del paso para buscar vecinos.
        max_iteraciones (int): Límite de iteraciones para evitar bucles infinitos.
    """
    # 1. Empezar en un punto aleatorio dentro de los límites.
    solucion_actual = np.array([random.uniform(l[0], l[1]) for l in limites])
    valor_actual = funcion(solucion_actual[0], solucion_actual[1])
    
    print(f"  -> Punto de partida: ({solucion_actual[0]:.2f}, {solucion_actual[1]:.2f}) | Altura inicial: {valor_actual:.4f}")

    # 2. Bucle principal de ascenso.
    for _ in range(max_iteraciones):
        mejor_vecino = None
        mejor_valor_vecino = -np.inf

        # 3. Explorar los vecinos inmediatos (arriba, abajo, izquierda, derecha).
        for dx in [-paso, 0, paso]:
            for dy in [-paso, 0, paso]:
                if dx == 0 and dy == 0:
                    continue # No evaluar el punto actual de nuevo

                vecino_potencial = solucion_actual + np.array([dx, dy])
                
                # Asegurarse de que el vecino está dentro de los límites.
                if not (limites[0][0] <= vecino_potencial[0] <= limites[0][1] and
                        limites[1][0] <= vecino_potencial[1] <= limites[1][1]):
                    continue
                
                valor_vecino = funcion(vecino_potencial[0], vecino_potencial[1])
                
                if valor_vecino > mejor_valor_vecino:
                    mejor_valor_vecino = valor_vecino
                    mejor_vecino = vecino_potencial

        # 4. Decidir si moverse o detenerse.
        if mejor_valor_vecino > valor_actual:
            solucion_actual = mejor_vecino
            valor_actual = mejor_valor_vecino
        else:
            # Si ningún vecino es mejor, hemos llegado a una cima.
            break
            
    return solucion_actual, valor_actual

if __name__ == "__main__":
    
    # Parámetros de la búsqueda
    LIMITES_BUSQUEDA = [(-5, 5), (-5, 5)] # Rango para x e y
    TAMANO_PASO = 0.1
    MAX_ITERACIONES = 1000

    print("Ejecutando la Ascensión de Colinas varias veces para ver su comportamiento.")
    print(f"El máximo global verdadero está cerca de (2, 2) con una altura de ~1.0")
    print("-" * 70)

    # Ejecutamos el algoritmo 5 veces para demostrar cómo el inicio aleatorio
    # afecta el resultado final.
    for i in range(5):
        print(f"Intento #{i + 1}:")
        
        solucion_encontrada, valor_encontrado = ascension_colinas(
            funcion_objetivo, 
            LIMITES_BUSQUEDA, 
            TAMANO_PASO, 
            MAX_ITERACIONES
        )
        
        print(f"  => Cima encontrada en: ({solucion_encontrada[0]:.2f}, {solucion_encontrada[1]:.2f}) | Altura final: {valor_encontrado:.4f}")
        
        # Comprobar si encontró el pico principal o se quedó en el local
        if solucion_encontrada[0] > 0:
            print("  Resultado: ¡Encontró el Máximo Global!")
        else:
            print("  Resultado: Se quedó atascado en un Máximo Local.")
        print("-" * 70)