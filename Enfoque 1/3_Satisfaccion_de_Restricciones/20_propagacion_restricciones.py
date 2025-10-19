from collections import deque

def ac3(variables, dominios, restricciones):
    """
    Implementa el algoritmo AC-3 para la propagación de restricciones.
    Modifica los dominios para hacerlos arco-consistentes.
    """
    # 1. Inicializar la cola con todos los arcos del problema.
    cola = deque()
    for var in variables:
        for vecino in restricciones.get(var, []):
            cola.append((var, vecino))

    print("Iniciando AC-3 para podar dominios...")
    # 2. Procesar la cola hasta que esté vacía.
    while cola:
        xi, xj = cola.popleft()
        
        # Si logramos reducir el dominio de xi...
        if revisar(xi, xj, dominios, restricciones):
            # ...debemos volver a revisar a todos los vecinos de xi.
            for xk in restricciones.get(xi, []):
                if xk != xj:
                    cola.append((xk, xi))
    return dominios

def revisar(xi, xj, dominios, restricciones):
    """
    Función auxiliar para AC-3. Hace que el arco (xi -> xj) sea consistente.
    Devuelve True si se eliminó algún valor del dominio de xi.
    """
    removido = False
    valores_xi = list(dominios[xi]) # Hacemos una copia para iterar

    for valor_x in valores_xi:
        # Si no hay ningún valor en el dominio de xj que satisfaga la restricción
        # junto con valor_x...
        if not any(valor_x != valor_y for valor_y in dominios[xj]):
            # ...entonces eliminamos valor_x del dominio de xi.
            dominios[xi].remove(valor_x)
            removido = True
            
    return removido

# Copiamos la función de backtracking simple que ya teníamos
def busqueda_vuelta_atras(asignacion, variables, dominios, restricciones):
    if len(asignacion) == len(variables):
        return asignacion
    variable_actual = [v for v in variables if v not in asignacion][0]
    for valor in dominios[variable_actual]:
        # La función de consistencia es la misma
        if es_consistente(variable_actual, valor, asignacion, restricciones):
            asignacion[variable_actual] = valor
            resultado = busqueda_vuelta_atras(asignacion, variables, dominios, restricciones)
            if resultado is not None:
                return resultado
            del asignacion[variable_actual]
    return None

def es_consistente(variable, valor, asignacion, restricciones):
    for vecino in restricciones.get(variable, []):
        if vecino in asignacion and asignacion[vecino] == valor:
            return False
    return True

if __name__ == "__main__":
    
    # Problema: Colorear el mapa, pero con dominios iniciales diferentes
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    # Para hacer el problema más interesante, NT y SA solo pueden ser de dos colores
    dominios = {
        'WA': ['Rojo', 'Verde', 'Azul'], 'Q': ['Rojo', 'Verde', 'Azul'],
        'NSW': ['Rojo', 'Verde', 'Azul'], 'V': ['Rojo', 'Verde', 'Azul'],
        'T': ['Rojo', 'Verde', 'Azul'],
        'NT': ['Verde', 'Azul'],
        'SA': ['Verde', 'Azul']
    }
    
    restricciones = {
        'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'], 'T': []
    }
    
    print("Dominios antes de AC-3")
    for var, dom in dominios.items(): print(f"  {var}: {dom}")

    # 1. PRE-PROCESAMIENTO: Aplicar AC-3 para simplificar el problema
    dominios_podados = ac3(variables, dominios, restricciones)

    print("\nDominios después de AC-3")
    for var, dom in dominios_podados.items(): print(f"  {var}: {dom}")
    
    print("\nIniciando Búsqueda Backtracking sobre los dominios podados")
    # 2. BÚSQUEDA: Resolver el problema ya simplificado
    solucion = busqueda_vuelta_atras({}, variables, dominios_podados, restricciones)
    
    print("-" * 40)
    if solucion:
        print("\n¡Solución encontrada!")
        for variable, valor in sorted(solucion.items()):
            print(f"  -> {variable}: {valor}")
    else:
        print("\nNo se encontró una solución.")