import random

def elegir_accion_epsilon_greedy(Q_tabla, estado, acciones_posibles, epsilon):
    """
    Elige una acción usando la estrategia epsilon-greedy.
    
    Args:
        Q_tabla (dict): Los Q-Valores aprendidos.
        estado (any): El estado actual del agente.
        acciones_posibles (list): Lista de todas las acciones ('arriba', ...).
        epsilon (float): La probabilidad de explorar (ej. 0.1 para 10%).
    """
    
    # Genera un número aleatorio entre 0.0 y 1.0
    numero_aleatorio = random.random()
    
    if numero_aleatorio < epsilon:
        # Exploración
        # Elige una acción completamente al azar
        print(f"  -> Decisión: EXPLORAR (Aleatorio < {epsilon})")
        return random.choice(acciones_posibles)
    else:
        # Explotación
        # Elige la mejor acción conocida (la que tiene el Q-Valor más alto)
        # Q_tabla[estado] es un dict como {'arriba': 0.5, 'abajo': 0.2}
        # max(dict, key=dict.get) devuelve la clave con el valor más alto.
        print(f"  -> Decisión: EXPLOTAR (Aleatorio >= {epsilon})")
        return max(Q_tabla[estado], key=Q_tabla[estado].get)

if __name__ == "__main__":
    
    # 1. Simular una Q-Tabla aprendida
    # En el estado (0,0), la acción 'derecha' es claramente la mejor.
    Q_tabla_simulada = {
        (0, 0): {'arriba': 0.2, 'abajo': 0.1, 'izquierda': 0.3, 'derecha': 0.9}
    }
    
    # 2. Definir el estado actual y las acciones
    estado_actual = (0, 0)
    acciones = ['arriba', 'abajo', 'izquierda', 'derecha']
    
    # Simular con un EPSILON bajo
    print("Simulación con EPSILON = 0.1 (10% Exploración)")
    print("El agente casi siempre 'explotará' y elegirá 'derecha'.\n")
    for _ in range(10):
        accion_elegida = elegir_accion_epsilon_greedy(Q_tabla_simulada, estado_actual, acciones, 0.1)
        print(f"     Acción resultante: {accion_elegida}\n")
        
    # Simular con un EPSILON alto
    print("\nSimulación con EPSILON = 0.8 (80% Exploración)")
    print("El agente casi siempre 'explorará' y elegirá acciones al azar.\n")
    for _ in range(10):
        accion_elegida = elegir_accion_epsilon_greedy(Q_tabla_simulada, estado_actual, acciones, 0.8)
        print(f"     Acción resultante: {accion_elegida}\n")