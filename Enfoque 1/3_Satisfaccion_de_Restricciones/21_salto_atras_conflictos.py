def busqueda_cbj(asignacion, variables, dominios, restricciones):
    """
    Implementa una versión simplificada del Salto Atrás Dirigido por Conflictos (CBJ).
    
    Devuelve:
        - Un diccionario de solución si tiene éxito.
        - Un conjunto de conflictos si falla.
    """
    # Caso base: si la asignación está completa, es una solución.
    if len(asignacion) == len(variables):
        return asignacion

    # Seleccionar la siguiente variable sin asignar.
    var = [v for v in variables if v not in asignacion][0]
    
    # Probar cada valor en el dominio de la variable actual.
    for valor in dominios[var]:
        
        # 1. Comprobar si el valor actual es consistente.
        consistente = True
        for vecino in restricciones[var]:
            if vecino in asignacion and asignacion[vecino] == valor:
                consistente = False
                break
        
        if consistente:
            # Si el valor es válido, lo asignamos y continuamos la recursión.
            asignacion[var] = valor
            
            resultado = busqueda_cbj(asignacion, variables, dominios, restricciones)
            
            # Si la llamada recursiva encontró una solución, la devolvemos.
            if isinstance(resultado, dict):
                return resultado

            # Logica de salto (BACKJUMP)
            # Si la recursión falló, 'resultado' es un conjunto de conflictos.
            conflicto = resultado
            
            # Si nuestra variable actual no es parte del conflicto...
            if var not in conflicto:
                # ...¡Hacemos el SALTO! Deshacemos nuestra asignación y devolvemos
                # el mismo conjunto de conflictos hacia arriba, sin probar más valores.
                del asignacion[var]
                return conflicto
            # Si nuestra variable SÍ es parte del conflicto, continuamos probando otros valores.

        # Deshacer la asignación para el siguiente bucle o para el retroceso/salto.
        if var in asignacion:
            del asignacion[var]

    # 2. Si probamos todos los valores y ninguno funcionó.
    #    Necesitamos construir el conjunto de conflictos para esta variable.
    conflicto_final = set()
    for vecino in restricciones[var]:
        if vecino in asignacion:
            conflicto_final.add(vecino)
            
    return conflicto_final

if __name__ == "__main__":
    
    # Variables en un orden específico para intentar provocar un salto.
    variables = ['WA', 'Q', 'V', 'T', 'NSW', 'NT', 'SA']
    colores = ['Rojo', 'Verde', 'Azul']
    dominios = {var: colores for var in variables}
    
    restricciones = {
        'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'], 'T': []
    }
    
    print("\n\nResolviendo el problema con Salto Atrás Dirigido por Conflictos (CBJ)")
    
    solucion = busqueda_cbj({}, variables, dominios, restricciones)
    
    print("-" * 40)
    if isinstance(solucion, dict):
        print("\n¡Solución encontrada!")
        for variable, valor in sorted(solucion.items()):
            print(f"  -> {variable}: {valor}")
    else:
        print("\nNo se encontró una solución.")