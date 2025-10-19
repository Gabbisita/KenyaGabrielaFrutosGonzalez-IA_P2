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

def busqueda_haz_local(funcion, limites, tamano_haz, paso, max_iteraciones):
    """
    Implementa el algoritmo de Búsqueda de Haz Local.
    
    Args:
        tamano_haz (int): El número de estados (k) a mantener en cada paso.
    """
    # 1. Empezar con un haz de 'k' estados aleatorios.
    haz_actual = []
    for _ in range(tamano_haz):
        estado = np.array([random.uniform(l[0], l[1]) for l in limites])
        haz_actual.append(estado)
    
    # Guardar la mejor solución encontrada globalmente.
    valores_haz = [funcion(e[0], e[1]) for e in haz_actual]
    mejor_solucion = haz_actual[np.argmax(valores_haz)]
    mejor_valor = max(valores_haz)

    # 2. Bucle principal de búsqueda.
    for i in range(max_iteraciones):
        todos_los_sucesores = []
        # 3. Generar todos los sucesores de cada estado en el haz.
        for estado_actual in haz_actual:
            for dx in [-paso, 0, paso]:
                for dy in [-paso, 0, paso]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    sucesor = estado_actual + np.array([dx, dy])
                    sucesor = np.clip(sucesor, [l[0] for l in limites], [l[1] for l in limites])
                    todos_los_sucesores.append(sucesor)
        
        # 4. Evaluar a todos los sucesores y ordenarlos.
        sucesores_evaluados = [(funcion(s[0], s[1]), s) for s in todos_los_sucesores]
        sucesores_evaluados.sort(key=lambda x: x[0], reverse=True)
        
        # 5. Formar el nuevo haz con los 'k' mejores sucesores.
        haz_actual = [s[1] for s in sucesores_evaluados[:tamano_haz]]
        
        # 6. Actualizar la mejor solución global.
        valor_actual_mejor = funcion(haz_actual[0][0], haz_actual[0][1])
        if valor_actual_mejor > mejor_valor:
            mejor_valor = valor_actual_mejor
            mejor_solucion = haz_actual[0]
            
        if i % 50 == 0:
            print(f"Iter {i}: Mejor valor en el haz actual: {valor_actual_mejor:.4f}, Mejor global: {mejor_valor:.4f}")

    return mejor_solucion, mejor_valor

if __name__ == "__main__":
    
    LIMITES = [(-5, 5), (-5, 5)]
    TAMANO_PASO = 0.1
    MAX_ITERACIONES = 200
    TAMANO_HAZ = 5 # Nuestro equipo tendrá 5 "escaladores"

    print(f"Ejecutando Búsqueda de Haz Local con un haz de tamaño {TAMANO_HAZ}...")
    print(f"El máximo global verdadero está cerca de (2, 2) con altura ~1.0")
    print("-" * 70)

    solucion, valor = busqueda_haz_local(
        funcion_objetivo, 
        LIMITES, 
        TAMANO_HAZ,
        TAMANO_PASO, 
        MAX_ITERACIONES
    )
    
    print("-" * 70)
    print(f"Búsqueda finalizada.")
    print(f"La mejor solución encontrada fue: ({solucion[0]:.2f}, {solucion[1]:.2f})")
    print(f"Altura máxima encontrada: {valor:.4f}")
    
    if solucion[0] > 0:
        print("Resultado: ¡El haz convergió en el Máximo Global!")
    else:
        print("Resultado: El haz convergió en el Máximo Local.")