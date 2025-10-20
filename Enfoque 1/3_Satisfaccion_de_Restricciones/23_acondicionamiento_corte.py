import copy

def es_consistente(variable, valor, asignacion, restricciones):
    for vecino in restricciones.get(variable, []):
        if vecino in asignacion and asignacion[vecino] == valor:
            return False
    return True

def busqueda_vuelta_atras(asignacion, variables, dominios, restricciones):
    if len(asignacion) == len(variables):
        return asignacion
    variable_actual = [v for v in variables if v not in asignacion][0]
    for valor in dominios[variable_actual]:
        if es_consistente(variable_actual, valor, asignacion, restricciones):
            asignacion[variable_actual] = valor
            resultado = busqueda_vuelta_atras(asignacion, variables, dominios, restricciones)
            if resultado is not None:
                return resultado
            del asignacion[variable_actual]
    return None


def acondicionamiento_del_corte(variables, dominios, restricciones):
    """
    Resuelve un CSP usando la estrategia de Acondicionamiento del Corte.
    """
    # 1. Identificar el Conjunto de Corte (lo hacemos manualmente).
    conjunto_corte = ['SA']
    variables_resto = [v for v in variables if v not in conjunto_corte]
    
    print(f"Conjunto de corte identificado: {conjunto_corte}")

    # 2. Iterar sobre todas las posibles asignaciones para el conjunto de corte.
    #    Como nuestro cutset es solo 'SA', probamos cada color para 'SA'.
    for valor in dominios[conjunto_corte[0]]:
        print(f"\n--- Probando a 'fijar' el valor: {conjunto_corte[0]} = {valor} ---")
        
        # Crear la asignación inicial para el subproblema.
        asignacion_inicial = {conjunto_corte[0]: valor}

        # 3. Resolver el subproblema restante (que ahora es más simple).
        #    Usamos nuestro backtracking de confianza para esto.
        print("Resolviendo el subproblema para las variables restantes...")
        solucion_subproblema = busqueda_vuelta_atras(
            asignacion_inicial,
            variables, # Le pasamos todas las variables para la condición de parada
            dominios,
            restricciones
        )
        
        # 4. Si el subproblema tiene solución, la combinamos y terminamos.
        if solucion_subproblema is not None:
            print("¡Subproblema resuelto! Se encontró una solución completa.")
            return solucion_subproblema

    # Si probamos todas las asignaciones del cutset y ninguna funcionó, no hay solución.
    return None

if __name__ == "__main__":
    
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    colores = ['Rojo', 'Verde', 'Azul']
    dominios = {var: colores for var in variables}
    
    restricciones = {
        'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'], 'T': []
    }
    
    print("Resolviendo el problema con Acondicionamiento del Corte...")
    
    solucion = acondicionamiento_del_corte(variables, dominios, restricciones)
    
    print("-" * 40)
    if solucion:
        print("\n¡Solución final encontrada!")
        for variable, valor in sorted(solucion.items()):
            print(f"  -> {variable}: {valor}")
    else:
        print("\nNo se encontró una solución.")