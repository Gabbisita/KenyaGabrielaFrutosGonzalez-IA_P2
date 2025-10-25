# 1. S - Definición de Estados
filas, cols = 3, 4
estados = [(f, c) for f in range(filas) for c in range(cols)]
# Estados especiales
terminales = [(0, 3), (1, 3)]
paredes = [(1, 1)]

# 2. A - Definición de Acciones
acciones = ['arriba', 'abajo', 'izquierda', 'derecha']

# 3. R - Definición de Recompensas
#    (Recompensa por *llegar* a un estado)
recompensas = {
    (0, 3): 1,   # Tesoro
    (1, 3): -1,  # Trampa
    'movimiento_normal': -0.04 # Un pequeño costo por cada movimiento
}

# 4. P - Definición del Modelo de Transición P(s' | s, a)
def modelo_transicion(estado, accion):
    """
    Esta función representa la "física" del mundo.
    Devuelve una lista de tuplas: [(probabilidad, estado_siguiente), ...]
    """
    if estado in terminales:
        return [(0.0, estado)] # No hay movimiento desde un terminal
    
    # Costo por movimiento normal
    recompensa_movimiento = recompensas['movimiento_normal']
    
    # Mundo Determinista Simple
    f, c = estado
    f_nuevo, c_nuevo = f, c
    
    if accion == 'arriba': f_nuevo -= 1
    elif accion == 'abajo': f_nuevo += 1
    elif accion == 'izquierda': c_nuevo -= 1
    elif accion == 'derecha': c_nuevo += 1
        
    estado_siguiente = (f_nuevo, c_nuevo)
    
    # Verificar si el movimiento es válido
    if not (0 <= f_nuevo < filas and 0 <= c_nuevo < cols and estado_siguiente not in paredes):
        estado_siguiente = estado # Se queda en su lugar si choca
        
    # La probabilidad del resultado es 1.0
    return [(1.0, estado_siguiente, recompensa_movimiento)]

# 5. γ (Gamma) - Factor de Descuento
gamma = 0.9

# Creamos el objeto 'mdp'
mdp_laberinto = {
    'estados': estados,
    'acciones': acciones,
    'transiciones': modelo_transicion, # P
    'recompensas': recompensas,       # R
    'terminales': terminales,
    'gamma': gamma                    # γ
}

if __name__ == "__main__":
    
    print("Objeto MDP creado exitosamente.")
    print(f"Estados: {len(mdp_laberinto['estados'])}")
    print(f"Acciones: {mdp_laberinto['acciones']}")
    print(f"Factor de Descuento (Gamma): {mdp_laberinto['gamma']}")
    
