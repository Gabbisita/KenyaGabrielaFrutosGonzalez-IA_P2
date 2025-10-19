import copy

def busqueda_con_forward_checking(asignacion, variables, dominios, restricciones):

    if len(asignacion) == len(variables):
        return asignacion

    variable_actual = [v for v in variables if v not in asignacion][0]

    for valor in dominios[variable_actual]:
        # Hacemos una copia profunda de los dominios para poder modificarlos temporalmente.
        dominios_locales = copy.deepcopy(dominios)
        
        # 1. Probar: Asignamos el valor.
        asignacion[variable_actual] = valor
        print(f"Probando: {variable_actual} = {valor}")
        
        # Comprobación
        poda_exitosa = True
        # Para cada vecino de la variable que acabamos de asignar
        for vecino in restricciones.get(variable_actual, []):
            if vecino not in asignacion:
                # Intentamos eliminar el valor actual de su dominio.
                if valor in dominios_locales[vecino]:
                    dominios_locales[vecino].remove(valor)
                
                # Si un dominio de un vecino se queda vacío, esta ruta no es válida.
                if not dominios_locales[vecino]:
                    poda_exitosa = False
                    print(f"  -> Poda fallida: Asignar {valor} a {variable_actual} deja a {vecino} sin opciones.")
                    break # Salimos del bucle de vecinos
        
        # 2. Recurrir: Si la poda fue exitosa, continuamos con los dominios reducidos.
        if poda_exitosa:
            resultado = busqueda_con_forward_checking(asignacion, variables, dominios_locales, restricciones)
            if resultado is not None:
                return resultado
        
        # 3. Retroceder (Backtrack): Deshacemos la asignación.
        #    No necesitamos restaurar los dominios porque usamos una copia.
        print(f"Retrocediendo... quitando {valor} de {variable_actual}")
        del asignacion[variable_actual]
        
    return None

if __name__ == "__main__":
    
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    colores = ['Rojo', 'Verde', 'Azul']
    dominios = {var: colores[:] for var in variables} # Usar [:] para crear copias
    
    restricciones = {
        'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'], 'T': []
    }
    
    solucion = busqueda_con_forward_checking({}, variables, dominios, restricciones)
    
    print("-" * 40)
    if solucion:
        print("\n¡Solución encontrada!")
        for variable, valor in sorted(solucion.items()):
            print(f"  -> {variable}: {valor}")
    else:
        print("\nNo se encontró una solución.")