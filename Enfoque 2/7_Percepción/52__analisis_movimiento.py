# Definir la Estructura del Dibujo
# Nodos (vértices/uniones) y Líneas (aristas)
# Usaremos letras para los vértices visibles y números para las líneas

# Vértices (Uniones)
uniones = {
    'A': ['L1', 'L2', 'L3'],   # Unión tipo Flecha
    'B': ['L1', 'L4', 'L5'],   # Unión tipo Flecha
    'C': ['L2', 'L6', 'L7'],   # Unión tipo Flecha
    'D': ['L3', 'L8', 'L9'],   # Unión tipo Flecha (atrás)
    'E': ['L4', 'L6', 'L10'],  # Unión tipo Flecha
    'F': ['L5', 'L7', 'L11'],  # Unión tipo Flecha
    'G': ['L8', 'L10', 'L12'], # Unión tipo Flecha (atrás)
    # H (atrás, invisible)
    # I (atrás, invisible)
}

# Líneas (Variables a etiquetar)
lineas = [f'L{i}' for i in range(1, 13)]

# Dominio de Etiquetas
etiquetas_posibles = ['+', '-', '>'] # Convexo, Cóncavo, Límite (solo usamos >)

# Catálogo de Uniones Válidas
# Definimos algunas uniones tipo FLECHA válidas para un cubo convexo
# (Las flechas '>' indican bordes oclusivos del contorno)
# (La orientación real de '>' depende de la vista, aquí simplificamos)

uniones_validas = {
    # Flecha simple convexa (3 bordes convexos)
    ('+', '+', '+'),
    # Flecha con un límite (contorno)
    ('+', '+', '>'), ('+', '>', '+'), ('>', '+', '+'),
    # Flecha con dos límites (contorno)
    ('+', '>', '>'), ('>', '+', '>'), ('>', '>', '+'),
    # Flecha con tres límites (contorno exterior)
    ('>', '>', '>')
}
# Nota: Faltarían tipos L, T, Horquilla y las variantes cóncavas para un catálogo completo.

# Algoritmo de Backtracking para Etiquetado

def es_consistente_union(union_id, asignacion_actual):
    """Verifica si las etiquetas asignadas a las líneas de una unión son válidas."""
    lineas_union = uniones[union_id]

    # Solo verificar si todas las líneas de la unión ya tienen etiqueta
    if not all(l in asignacion_actual for l in lineas_union):
        return True # Aún no podemos verificarla completamente

    # Obtener las etiquetas asignadas (en un orden consistente, ej. alfabético)
    etiquetas_asignadas = tuple(sorted([asignacion_actual[l] for l in lineas_union]))

    # Simplificación: Asumimos que todas son Flecha y verificamos contra el catálogo
    # En un sistema real, determinaríamos el tipo de unión (L, T, Flecha...)
    # y buscaríamos en el sub-catálogo correspondiente.
    # También necesitaríamos manejar la orientación de las flechas '>'.
    
    # Buscamos permutaciones porque el orden en uniones_validas es fijo
    from itertools import permutations
    for p in permutations(etiquetas_asignadas):
        if p in uniones_validas:
             return True # Encontramos una combinación válida

    # print(f"  -> Inconsistencia en unión {union_id} con etiquetas {etiquetas_asignadas}")
    return False # Ninguna permutación fue válida

def etiquetar_lineas_backtracking(asignacion, lineas_restantes):
    """Intenta encontrar una asignación de etiquetas consistente."""
    # Caso base: Todas las líneas asignadas
    if not lineas_restantes:
        return asignacion # ¡Solución encontrada!

    linea_actual = lineas_restantes[0]
    resto = lineas_restantes[1:]

    for etiqueta in etiquetas_posibles:
        asignacion[linea_actual] = etiqueta
        # print(f"Probando: {linea_actual} = {etiqueta}") # Descomentar para depurar

        # Verificar consistencia con TODAS las uniones afectadas
        consistente = True
        for union_id, lineas_en_union in uniones.items():
            if linea_actual in lineas_en_union:
                if not es_consistente_union(union_id, asignacion):
                    consistente = False
                    break # Esta etiqueta no funciona para esta línea

        if consistente:
            # Si es consistente hasta ahora, continuar recursivamente
            resultado = etiquetar_lineas_backtracking(asignacion, resto)
            if resultado is not None:
                return resultado # Propagar la solución encontrada

        # Si la etiqueta no funcionó o la recursión falló, retroceder
        # print(f"Retrocediendo... quitando {etiqueta} de {linea_actual}") # Descomentar
        del asignacion[linea_actual]

    # Si probamos todas las etiquetas y ninguna funcionó
    return None


if __name__ == "__main__":
    print("Buscando un etiquetado de líneas consistente para el cubo...")
    
    asignacion_inicial = {}
    solucion = etiquetar_lineas_backtracking(asignacion_inicial, lineas)
    
    print("-" * 40)
    if solucion:
        print("¡Etiquetado Consistente Encontrado!")
        # Ordenar por nombre de línea para mostrar
        for linea, etiqueta in sorted(solucion.items(), key=lambda item: int(item[0][1:])):
            print(f"  -> {linea}: {etiqueta}")
    else:
        print("No se encontró un etiquetado consistente (o el catálogo es incompleto).")