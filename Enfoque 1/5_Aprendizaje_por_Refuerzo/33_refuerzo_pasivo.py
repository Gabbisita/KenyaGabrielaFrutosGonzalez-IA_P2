import random

# Definición del Entorno

FILAS, COLS = 3, 4
ESTADOS = [(f, c) for f in range(FILAS) for c in range(COLS)]
TERMINALES = [(0, 3), (1, 3)]
PAREDES = [(1, 1)]
RECOMPENSAS = {(0, 3): 1, (1, 3): -1}
GAMMA = 0.9
ALPHA = 0.1 # Tasa de aprendizaje
NUM_EPISODIOS = 10000 # Cuántas veces el agente "practica" la ruta

# La Política Fija del Agente Pasivo (π)
politica_fija = {
    (0, 0): 'derecha', (0, 1): 'derecha', (0, 2): 'derecha',
    (1, 0): 'arriba',  (1, 2): 'arriba',
    (2, 0): 'arriba', (2, 1): 'derecha', (2, 2): 'arriba', (2, 3): 'izquierda'
}

def obtener_transicion_estocastica(estado, accion):
    """
    Simula el mundo aleatorio. El agente intenta 'accion', 
    pero puede resbalar.
    """
    if estado in TERMINALES:
        return estado, 0 # Se queda en el terminal, sin recompensa

    # Acciones ortogonales (resbalones)
    acciones_laterales = {
        'arriba': ['izquierda', 'derecha'],
        'abajo': ['izquierda', 'derecha'],
        'izquierda': ['arriba', 'abajo'],
        'derecha': ['arriba', 'abajo']
    }
    
    # Elige el resultado basado en las probabilidades
    num_aleatorio = random.random()
    if num_aleatorio < 0.8:
        accion_final = accion
    elif num_aleatorio < 0.9:
        accion_final = acciones_laterales[accion][0]
    else:
        accion_final = acciones_laterales[accion][1]
        
    # Calcula el estado siguiente basado en la acción final
    f, c = estado
    if accion_final == 'arriba': f -= 1
    elif accion_final == 'abajo': f += 1
    elif accion_final == 'izquierda': c -= 1
    elif accion_final == 'derecha': c += 1
        
    estado_siguiente = (f, c)
    
    # Si choca o es inválido, se queda en su lugar
    if not (0 <= f < FILAS and 0 <= c < COLS and estado_siguiente not in PAREDES):
        estado_siguiente = estado
        
    # Obtener la recompensa (es 0 para todos los estados no terminales)
    recompensa = RECOMPENSAS.get(estado_siguiente, 0)
    return estado_siguiente, recompensa

# Algoritmo de Aprendizaje Pasivo TD

def aprendizaje_pasivo_td(politica, num_episodios, alpha, gamma):
    """
    Aprende el valor U(s) de cada estado siguiendo una política fija (π).
    """
    utilidades = {s: 0.0 for s in ESTADOS}
    

    # Creamos una lista de estados válidos para empezar (ni terminales ni paredes)
    estados_inicio_validos = [s for s in ESTADOS if s not in TERMINALES and s not in PAREDES]

    for _ in range(num_episodios):
        
        # Empezar un nuevo episodio desde una posición aleatoria VÁLIDA
        estado_actual = random.choice(estados_inicio_validos)

        while estado_actual not in TERMINALES:
            accion = politica[estado_actual]
            estado_siguiente, recompensa = obtener_transicion_estocastica(estado_actual, accion)
            
            viejo_valor = utilidades[estado_actual]
            valor_siguiente = utilidades[estado_siguiente]
            nueva_estimacion = recompensa + gamma * valor_siguiente
            
            utilidades[estado_actual] = viejo_valor + alpha * (nueva_estimacion - viejo_valor)
            
            estado_actual = estado_siguiente
            
    return utilidades

if __name__ == "__main__":
    
    print("Política Fija")
    
    utilidades_aprendidas = aprendizaje_pasivo_td(politica_fija, NUM_EPISODIOS, ALPHA, GAMMA)
    
    print("\nUtilidades Aprendidas")
    for f in range(FILAS):
        linea = " | ".join([f"{utilidades_aprendidas.get((f, c), 0):.2f}" for c in range(COLS)])
        print(linea)