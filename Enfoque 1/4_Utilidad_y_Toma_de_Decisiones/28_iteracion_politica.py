import random
import copy

# Definición del Entorno (MDP)
FILAS, COLS = 3, 4
ESTADOS = tuple((f, c) for f in range(FILAS) for c in range(COLS))
# Definir explícitamente estados válidos (no paredes, no terminales)
PAREDES = ((1, 1),)
TERMINALES = ((0, 3), (1, 3))
ESTADOS_ACTIVOS = tuple(s for s in ESTADOS if s not in PAREDES and s not in TERMINALES)
ACCIONES = ('arriba', 'abajo', 'izquierda', 'derecha')
RECOMPENSAS = {(0, 3): 1.0, (1, 3): -1.0} # Recompensas en estados terminales
COSTO_MOVIMIENTO = -0.04 # Costo por cada paso
GAMMA = 0.9 # Factor de descuento

def transiciones(estado, accion):
    """Modelo de transición determinista."""
    if estado in TERMINALES:
        return [(1.0, estado)] # Se queda en el terminal

    f, c = estado
    df, dc = 0, 0
    if accion == 'arriba': df = -1
    elif accion == 'abajo': df = 1
    elif accion == 'izquierda': dc = -1
    elif accion == 'derecha': dc = 1

    estado_siguiente = (f + df, c + dc)

    # Verificar límites y paredes
    if not (0 <= estado_siguiente[0] < FILAS and \
            0 <= estado_siguiente[1] < COLS and \
            estado_siguiente not in PAREDES):
        estado_siguiente = estado # Choca, se queda donde está

    return [(1.0, estado_siguiente)]

# Algoritmo de Iteración de Políticas

def iteracion_de_politicas(estados, acciones, terminales, transiciones, recompensas, costo_movimiento, gamma, epsilon=0.001):
    """Encuentra la política óptima usando Iteración de Políticas."""

    # Inicializar una política aleatoria para estados activos
    politica = {s: random.choice(acciones) for s in ESTADOS_ACTIVOS}
    utilidades = {s: 0.0 for s in estados} # Utilidades iniciales = 0

    while True:
        # Evaluación de Política (iterativa hasta convergencia)
        while True:
            nuevas_utilidades = utilidades.copy()
            delta = 0
            for s in ESTADOS_ACTIVOS: # Solo calcular para estados activos
                accion_actual = politica[s]
                valor_q = 0
                # Calcular Q(s, pi(s))
                for (prob, s_prime) in transiciones(s, accion_actual):
                    recompensa = recompensas.get(s_prime, costo_movimiento) # Recompensa al llegar a s_prime
                    valor_q += prob * (recompensa + gamma * utilidades[s_prime])

                nuevas_utilidades[s] = valor_q
                delta = max(delta, abs(nuevas_utilidades[s] - utilidades[s]))

            utilidades = nuevas_utilidades
            if delta < epsilon * (1 - gamma) / gamma:
                break # Convergencia de la evaluación

        # Mejora de Política
        politica_estable = True
        for s in ESTADOS_ACTIVOS:
            accion_antigua = politica[s]
            mejor_accion = None
            max_valor_q = -float('inf')

            # Encontrar la acción que maximiza la utilidad esperada
            for accion in acciones:
                valor_q = 0
                for (prob, s_prime) in transiciones(s, accion):
                    recompensa = recompensas.get(s_prime, costo_movimiento)
                    valor_q += prob * (recompensa + gamma * utilidades[s_prime])

                if valor_q > max_valor_q:
                    max_valor_q = valor_q
                    mejor_accion = accion

            politica[s] = mejor_accion
            if accion_antigua != politica[s]:
                politica_estable = False

        # Si la política no cambió, hemos terminado
        if politica_estable:
            return politica, utilidades

# Ejecución y Visualización

def mostrar_utilidades(utilidades, filas, cols):
    print("Utilidades Óptimas")
    for f in range(filas):
        linea = " | ".join([f"{utilidades.get((f, c), 0):6.2f}" if (f, c) not in PAREDES else "######" for c in range(cols)])
        print(linea)

def mostrar_politica(politica, filas, cols):
    print("\nPolítica Óptima")
    simbolos_acciones = {'arriba': '^', 'abajo': 'v', 'izquierda': '<', 'derecha': '>'}
    for f in range(filas):
        linea = " | ".join([f"  {simbolos_acciones.get(politica.get((f, c)), ' ')}   " if (f, c) not in PAREDES + TERMINALES else "Term  " if (f,c) in TERMINALES else "######" for c in range(cols)])
        print(linea)

if __name__ == "__main__":
    politica_optima, utilidades_optimas = iteracion_de_politicas(
        ESTADOS, ACCIONES, TERMINALES, transiciones, RECOMPENSAS, COSTO_MOVIMIENTO, GAMMA
    )

    mostrar_utilidades(utilidades_optimas, FILAS, COLS)
    mostrar_politica(politica_optima, FILAS, COLS)