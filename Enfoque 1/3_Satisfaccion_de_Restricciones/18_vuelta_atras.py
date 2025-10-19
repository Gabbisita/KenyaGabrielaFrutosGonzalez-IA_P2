def es_consistente(variable, valor, asignacion, restricciones):
    """
    Verifica si asignar un 'valor' a una 'variable' es consistente
    con la 'asignacion' actual, dadas las 'restricciones'.
    """
    for vecino in restricciones.get(variable, []):
        if vecino in asignacion and asignacion[vecino] == valor:
            return False
    return True

def busqueda_vuelta_atras(asignacion, variables, dominios, restricciones):
    """
    Implementa el algoritmo de Búsqueda de Vuelta Atrás (Backtracking).
    """
    # Caso base: si todas las variables han sido asignadas, encontramos una solución.
    if len(asignacion) == len(variables):
        return asignacion

    # Seleccionar la siguiente variable sin asignar.
    variable_actual = [v for v in variables if v not in asignacion][0]

    # Iterar sobre todos los posibles valores del dominio para esa variable.
    for valor in dominios[variable_actual]:
        # Verificar si la asignación es válida.
        if es_consistente(variable_actual, valor, asignacion, restricciones):
            # 1. Probar: Asignar el valor.
            asignacion[variable_actual] = valor
            
            # 2. Recurrir: Continuar con la siguiente variable.
            resultado = busqueda_vuelta_atras(asignacion, variables, dominios, restricciones)
            
            # Si la recursión encontró una solución, la devolvemos.
            if resultado is not None:
                return resultado
            
            # 3. Retroceder (Backtrack): Si no se encontró solución, deshacer la asignación.
            del asignacion[variable_actual]

    # Si probamos todos los valores y ninguno funcionó, no hay solución por este camino.
    return None

# --- Bloque principal ---
if __name__ == "__main__":
    
    # 1. Definir las Variables (estados de México)
    variables = ['Jalisco', 'Zacatecas', 'Nayarit', 'Colima', 'Michoacan', 'Aguascalientes']
    
    # 2. Definir los Dominios (colores disponibles para cada estado)
    colores = ['Rojo', 'Verde', 'Azul']
    dominios = {var: colores for var in variables}
    
    # 3. Definir las Restricciones (qué estados son vecinos)
    restricciones = {
        'Jalisco': ['Zacatecas', 'Nayarit', 'Colima', 'Michoacan', 'Aguascalientes'],
        'Zacatecas': ['Jalisco', 'Aguascalientes', 'Nayarit'],
        'Nayarit': ['Jalisco', 'Zacatecas'],
        'Colima': ['Jalisco', 'Michoacan'],
        'Michoacan': ['Jalisco', 'Colima'],
        'Aguascalientes': ['Jalisco', 'Zacatecas']
    }
    
    print("Resolviendo el problema de coloreado de mapa con Backtracking...")
    
    # Empezamos con una asignación vacía
    solucion = busqueda_vuelta_atras({}, variables, dominios, restricciones)
    
    if solucion:
        print("\n¡Solución encontrada!")
        for variable, valor in sorted(solucion.items()):
            print(f"  -> {variable}: {valor}")
    else:
        print("\nNo se encontró una solución.")