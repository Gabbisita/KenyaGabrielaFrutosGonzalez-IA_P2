import numpy as np

# Definición del Mundo
# Un mundo simple de 1x4: [ (0,0), (0,1), (0,2), (0,3) ]
# (0,3) es un estado terminal (Tesoro)
estados = [(0, 0), (0, 1), (0, 2), (0, 3)]
acciones = ['izquierda', 'derecha']
terminales = [(0, 3)]

def transiciones(estado, accion):
    """Modelo de Transición P(s' | s, a) - Determinista por simplicidad"""
    if estado in terminales:
        return estado
    f, c = estado
    if accion == 'derecha':
        c_nuevo = min(c + 1, 3)
    elif accion == 'izquierda':
        c_nuevo = max(c - 1, 0)
    return (f, c_nuevo)

# Definición del POMDP
observaciones = ['ve_pared', 've_abierto']

def modelo_observacion(estado):
    """Modelo de Observación P(o | s) - Qué tan 'ruidosos' son los sensores"""
    # (0,0) es una esquina (ve pared a la izquierda)
    # (0,3) es una esquina (ve pared a la derecha)
    # (0,1) y (0,2) son pasillos abiertos
    
    if estado == (0, 0) or estado == (0, 3):
        # 80% de probabilidad de ver la pared, 20% de error
        return {'ve_pared': 0.8, 've_abierto': 0.2}
    else: # (0,1) o (0,2)
        # 90% de probabilidad de ver abierto, 10% de error
        return {'ve_pared': 0.1, 've_abierto': 0.9}

def actualizar_creencia(creencia_anterior, accion, observacion):
    """
    Actualiza el estado de creencia usando el filtro de Bayes.
    Esta es la función central de un POMDP.
    """
    nueva_creencia = {s: 0.0 for s in estados}
    
    # 1. Bucle sobre todos los estados posibles (s')
    for estado_siguiente in estados:
        
        # 1a. Paso de PREDICCIÓN (Movimiento)
        # Suma de [ P(s'|s,a) * P_anterior(s) ] para todos los estados 's'
        prob_predicha = 0
        for estado_actual in estados:
            if transiciones(estado_actual, accion) == estado_siguiente:
                prob_predicha += 1.0 * creencia_anterior[estado_actual]
        
        # 1b. Paso de ACTUALIZACIÓN (Observación)
        # P(o | s') * P(s' predicha)
        prob_observacion = modelo_observacion(estado_siguiente)[observacion]
        nueva_creencia[estado_siguiente] = prob_observacion * prob_predicha

    # 2. Normalización
    total = sum(nueva_creencia.values())
    if total == 0:
        return {s: 1.0 / len(estados) for s in estados} # Reiniciar si es imposible
    
    for estado in nueva_creencia:
        nueva_creencia[estado] /= total
        
    return nueva_creencia

def imprimir_creencia(creencia):
    """Función auxiliar para mostrar la creencia de forma clara."""
    print("Estado de Creencia actual:")
    for estado in estados:
        prob = creencia.get(estado, 0)
        print(f"  P(Estar en {estado}) = {prob * 100:.1f}%")

# Ejecución de la Simulación
if __name__ == "__main__":
    
    # Creencia inicial: El agente no sabe dónde está (distribución uniforme)
    creencia = {s: 1.0 / len(estados) for s in estados}
    imprimir_creencia(creencia)
    
    # Simulación Paso a Paso
    print("\nPASO 1")
    print("Acción: 'derecha'")
    print("Observación: 've_abierto'")
    creencia = actualizar_creencia(creencia, 'derecha', 've_abierto')
    imprimir_creencia(creencia)
    
    print("\nPASO 2")
    print("Acción: 'derecha'")
    print("Observación: 've_abierto'")
    creencia = actualizar_creencia(creencia, 'derecha', 've_abierto')
    imprimir_creencia(creencia)
    
    print("\nPASO 3")
    print("Acción: 'derecha'")
    print("Observación: 've_pared'")
    creencia = actualizar_creencia(creencia, 'derecha', 've_pared')
    imprimir_creencia(creencia)