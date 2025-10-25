import random
import copy

# Definición del Entorno
FILAS, COLS = 3, 4
ESTADOS = [(f, c) for f in range(FILAS) for c in range(COLS)]
TERMINALES = [(0, 3), (1, 3)]
PAREDES = [(1, 1)]
RECOMPENSAS = {(0, 3): 1, (1, 3): -1, 'movimiento': -0.04}
ACCIONES = ['arriba', 'abajo', 'izquierda', 'derecha']
GAMMA = 0.9

def obtener_transicion_estocastica(estado, accion):
    if estado in TERMINALES: return estado, 0
    acciones_laterales = {'arriba': ['izquierda', 'derecha'], 'abajo': ['izquierda', 'derecha'],
                          'izquierda': ['arriba', 'abajo'], 'derecha': ['arriba', 'abajo']}
    num_aleatorio = random.random()
    if num_aleatorio < 0.8: accion_final = accion
    elif num_aleatorio < 0.9: accion_final = acciones_laterales[accion][0]
    else: accion_final = acciones_laterales[accion][1]
    f, c = estado
    if accion_final == 'arriba': f -= 1
    elif accion_final == 'abajo': f += 1
    elif accion_final == 'izquierda': c -= 1
    elif accion_final == 'derecha': c += 1
    estado_siguiente = (f, c)
    if not (0 <= f < FILAS and 0 <= c < COLS and estado_siguiente not in PAREDES):
        estado_siguiente = estado
    recompensa = RECOMPENSAS.get(estado_siguiente, RECOMPENSAS['movimiento'])
    return estado_siguiente, recompensa

# Funciones para la Búsqueda de Política

def ejecutar_politica(politica, num_episodios=100):
    """Ejecuta la política dada y calcula la recompensa promedio."""
    recompensa_total = 0
    estados_inicio_validos = [s for s in ESTADOS if s not in TERMINALES and s not in PAREDES]
    
    for _ in range(num_episodios):
        estado_actual = random.choice(estados_inicio_validos)
        recompensa_episodio = 0
        pasos = 0
        max_pasos = 100 # Evitar bucles infinitos

        while estado_actual not in TERMINALES and pasos < max_pasos:
            accion = politica[estado_actual]
            estado_siguiente, recompensa = obtener_transicion_estocastica(estado_actual, accion)
            recompensa_episodio += recompensa * (GAMMA ** pasos)
            estado_actual = estado_siguiente
            pasos += 1
        recompensa_total += recompensa_episodio
        
    return recompensa_total / num_episodios

def busqueda_politica_aleatoria(num_iteraciones=1000):
    """
    Busca la mejor política probando cambios aleatorios.
    """
    # 1. Empezar con una política aleatoria
    mejor_politica = {s: random.choice(ACCIONES) for s in ESTADOS if s not in TERMINALES and s not in PAREDES}
    mejor_recompensa = ejecutar_politica(mejor_politica)
    
    print(f"Iter 0: Mejor recompensa = {mejor_recompensa:.3f}")

    # 2. Iterar y probar cambios
    for i in range(1, num_iteraciones + 1):
        # Crear una política vecina modificando una acción al azar
        politica_actual = copy.deepcopy(mejor_politica)
        estado_a_cambiar = random.choice(list(politica_actual.keys()))
        politica_actual[estado_a_cambiar] = random.choice(ACCIONES)
        
        # Evaluar la nueva política
        recompensa_actual = ejecutar_politica(politica_actual)
        
        # Si la nueva política es mejor, la adoptamos
        if recompensa_actual > mejor_recompensa:
            mejor_politica = politica_actual
            mejor_recompensa = recompensa_actual
            print(f"Iter {i}: Nueva mejor recompensa = {mejor_recompensa:.3f}")
            
    return mejor_politica

if __name__ == "__main__":
    
    print("Buscando la política óptima")
    
    politica_optima_encontrada = busqueda_politica_aleatoria()

    print("\nPolítica Óptima Encontrada")
    politica_display = {s: '---' for s in ESTADOS if s in TERMINALES or s in PAREDES}
    politica_display.update(politica_optima_encontrada)
    for f in range(FILAS):
        linea = " | ".join([f"{politica_display.get((f, c), '???'):^9}" for c in range(COLS)])
        print(linea)