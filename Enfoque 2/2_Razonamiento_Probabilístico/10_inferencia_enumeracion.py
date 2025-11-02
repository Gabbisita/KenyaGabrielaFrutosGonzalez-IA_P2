import itertools


# Reutilizamos la definición de la Red Bayesiana
estructura_bn = {
    'Nublado': [],
    'Aspersor': ['Nublado'],
    'Lluvia': ['Nublado'],
    'Pasto Mojado': ['Lluvia', 'Aspersor']
}

cpts_bn = {
    'Nublado': {True: 0.5, False: 0.5},
    'Aspersor': {
        (True,): {True: 0.1, False: 0.9}, (False,): {True: 0.5, False: 0.5}
    },
    'Lluvia': {
        (True,): {True: 0.8, False: 0.2}, (False,): {True: 0.2, False: 0.8}
    },
    'Pasto Mojado': {
        (True, True): {True: 0.99, False: 0.01}, (True, False): {True: 0.90, False: 0.10},
        (False, True): {True: 0.90, False: 0.10}, (False, False): {True: 0.00, False: 1.00}
    }
}
variables_bn = ['Nublado', 'Aspersor', 'Lluvia', 'Pasto Mojado'] # En orden topológico

# Algoritmo de Inferencia por Enumeración

def probabilidad_conjunta(evento, estructura, cpts, vars_ordenadas):
    """Calcula la probabilidad conjunta de un evento completo P(N,A,L,PM)."""
    prob = 1.0
    for var in vars_ordenadas:
        valor = evento[var]
        padres = estructura[var]
        valores_padres = tuple(evento[p] for p in padres)
        
        cpt = cpts[var]
        if not padres: # Nodo raíz
            prob_cond = cpt[valor]
        else:
            prob_cond = cpt[valores_padres][valor]
        prob *= prob_cond
    return prob

def enumerate_ask(query_var, evidencia, estructura, cpts, vars_totales):
    """
    Calcula P(Query | Evidencia) usando Inferencia por Enumeración.
    """
    distribucion_Q = {} # Para guardar P(Query=valor, evidencia)
    
    # Iterar sobre cada valor posible de la variable de consulta
    for valor_q in [True, False]:
        
        # Extender la evidencia con la asignación actual de la variable de consulta
        evidencia_extendida = evidencia.copy()
        evidencia_extendida[query_var] = valor_q
        
        variables_ocultas = [v for v in vars_totales if v != query_var and v not in evidencia]
        
        suma_q = 0
        
        # Iterar sobre todas las combinaciones posibles de las variables ocultas
        # itertools.product genera todas las tuplas (True/False, True/False, ...)
        valores_ocultos = list(itertools.product([True, False], repeat=len(variables_ocultas)))
        
        for vals in valores_ocultos:
            # Crear un evento completo (asignación a todas las variables)
            evento_completo = evidencia_extendida.copy()
            for i, var_oculta in enumerate(variables_ocultas):
                evento_completo[var_oculta] = vals[i]
            
            # Calcular la probabilidad conjunta de este evento completo
            p_evento = probabilidad_conjunta(evento_completo, estructura, cpts, vars_totales)
            suma_q += p_evento
            
        distribucion_Q[valor_q] = suma_q

    # Normalizar para obtener P(Query | evidencia)
    total = sum(distribucion_Q.values())
    if total == 0:
        return {val: 0.0 for val in distribucion_Q} # Evitar división por cero
        
    for valor in distribucion_Q:
        distribucion_Q[valor] /= total
        
    return distribucion_Q

if __name__ == "__main__":
    
    query = 'Lluvia'
    evidencia = {'Pasto Mojado': True}

    print(f"Calculando P usando Inferencia por Enumeración")

    distribucion_resultado = enumerate_ask(query, evidencia, estructura_bn, cpts_bn, variables_bn)
    
    print("\nDistribución de Probabilidad Condicional Resultante:")
    for valor, prob in distribucion_resultado.items():
        print(f"  P({query}={valor} | Pasto Mojado = True) = {prob:.3f}")

    # Ejemplo 2: P(Nublado | Lluvia=True, Aspersor=False)
    query2 = 'Nublado'
    evidencia2 = {'Lluvia': True, 'Aspersor': False}
    print(f"\nCalculando P({query2} | Lluvia = True, Aspersor = False)")
    distribucion_resultado2 = enumerate_ask(query2, evidencia2, estructura_bn, cpts_bn, variables_bn)
    print("\nDistribución de Probabilidad Condicional Resultante:")
    for valor, prob in distribucion_resultado2.items():
        print(f"  P({query2}={valor} | Lluvia=T, Aspersor=F) = {prob:.3f}")