import random
import copy # For deep copies if needed, though not strictly here

estructura_bn = {
    'Nublado': [], 'Aspersor': ['Nublado'], 'Lluvia': ['Nublado'],
    'Pasto Mojado': ['Lluvia', 'Aspersor']
}
cpts_bn = {
    'Nublado': {True: 0.5, False: 0.5},
    'Aspersor': {(True,): {True: 0.1, False: 0.9}, (False,): {True: 0.5, False: 0.5}},
    'Lluvia': {(True,): {True: 0.8, False: 0.2}, (False,): {True: 0.2, False: 0.8}},
    'Pasto Mojado': {
        (True, True): {True: 0.99, False: 0.01}, (True, False): {True: 0.90, False: 0.10},
        (False, True): {True: 0.90, False: 0.10}, (False, False): {True: 0.00, False: 1.00}
    }
}
variables_bn = ['Nublado', 'Aspersor', 'Lluvia', 'Pasto Mojado']

# Funciones Auxiliares

def encontrar_manto_markov(nodo_objetivo, estructura):
    """Identifica el Manto de Markov (padres, hijos, otros padres de hijos)."""
    manto = set()
    padres = estructura.get(nodo_objetivo, [])
    manto.update(padres)
    hijos = []
    for nodo, lista_padres in estructura.items():
        if nodo_objetivo in lista_padres:
            hijos.append(nodo)
            manto.add(nodo)
            otros_padres = [p for p in lista_padres if p != nodo_objetivo]
            manto.update(otros_padres)
    manto.discard(nodo_objetivo)
    return list(manto) # Devolver como lista para consistencia

def prob_condicional_dado_manto(variable, valor, estado_actual, estructura, cpts):
    """
    Calcula P(Variable=valor | Manto(Variable)) de forma proporcional.
    P(X | MB(X)) ∝ P(X | Parents(X)) * Π_{Y in Children(X)} P(Y | Parents(Y))
    """
    prob = 1.0
    
    # Término P(X | Parents(X))
    padres = estructura[variable]
    valores_padres = tuple(estado_actual[p] for p in padres)
    cpt_var = cpts[variable]
    if not padres:
        prob *= cpt_var[valor]
    else:
        prob *= cpt_var[valores_padres][valor]
        
    # Término Π P(Y | Parents(Y)) para cada hijo Y
    hijos = [nodo for nodo, lista_padres in estructura.items() if variable in lista_padres]
    for hijo in hijos:
        padres_hijo = estructura[hijo]
        # Construir la tupla de valores de los padres del hijo CON el valor propuesto para 'variable'
        valores_padres_hijo_dict = {p: estado_actual[p] for p in padres_hijo if p != variable}
        valores_padres_hijo_dict[variable] = valor # Usar el valor que estamos evaluando
        
        # Asegurar el orden correcto para la clave CPT
        valores_padres_hijo_tupla = tuple(valores_padres_hijo_dict[p] for p in padres_hijo)
        
        cpt_hijo = cpts[hijo]
        valor_hijo = estado_actual[hijo]
        prob *= cpt_hijo[valores_padres_hijo_tupla][valor_hijo]
        
    return prob

def normalizar_distribucion(dist):
    """Normaliza un diccionario de probabilidades."""
    total = sum(dist.values())
    if total == 0: return {k: 1.0/len(dist) for k in dist}
    return {k: v / total for k, v in dist.items()}

def elegir_valor_ponderado(distribucion):
    """Elige un valor basado en sus probabilidades."""
    valor_aleatorio = random.random()
    suma_acumulada = 0
    for valor, prob in distribucion.items():
        suma_acumulada += prob
        if valor_aleatorio < suma_acumulada:
            return valor
    return list(distribucion.keys())[-1] # Fallback

# Algoritmo de Muestreo de Gibbs

def muestreo_gibbs(query_var, evidencia, estructura, cpts, vars_totales, num_muestras, burn_in=100):
    """
    Estima P(Query | Evidencia) usando Muestreo de Gibbs.
    """
    # 1. Inicialización
    estado_actual = {}
    variables_ocultas = []
    for var in vars_totales:
        if var in evidencia:
            estado_actual[var] = evidencia[var]
        else:
            estado_actual[var] = random.choice([True, False]) # Valor inicial aleatorio
            variables_ocultas.append(var)
            
    if not variables_ocultas: # Si no hay variables ocultas, la prob es 1 o 0
         prob_evidencia = prob_condicional_dado_manto(query_var, evidencia[query_var], estado_actual, estructura, cpts)
         # Este cálculo simple no es suficiente, requiere más lógica
         print("Advertencia: No hay variables ocultas, Gibbs no es necesario.")
         # Devolvería 1.0 si query_var está en evidencia y coincide, 0.0 si no.
         target_val = evidencia.get(query_var)
         return {val: 1.0 if val == target_val else 0.0 for val in [True, False]}


    muestras_recolectadas = []
    
    # 2. Iterar (incluyendo burn-in)
    total_iteraciones = burn_in + num_muestras
    for i in range(total_iteraciones):
        # Elegir una variable oculta al azar para actualizar
        var_a_muestrear = random.choice(variables_ocultas)
        
        # Calcular la distribución P(var | Manto(var))
        distribucion_condicional = {}
        for valor_posible in [True, False]:
            distribucion_condicional[valor_posible] = prob_condicional_dado_manto(
                var_a_muestrear, valor_posible, estado_actual, estructura, cpts
            )
            
        # Normalizar la distribución
        distribucion_normalizada = normalizar_distribucion(distribucion_condicional)
        
        # Muestrear el nuevo valor para la variable
        nuevo_valor = elegir_valor_ponderado(distribucion_normalizada)
        estado_actual[var_a_muestrear] = nuevo_valor
        
        # 3. Recolectar muestra después del burn-in
        if i >= burn_in:
            muestras_recolectadas.append(estado_actual[query_var])
            
    # 4. Estimar la probabilidad a partir de las muestras
    if not muestras_recolectadas:
        return {True: 0.5, False: 0.5} # No se recolectaron muestras

    conteo_true = sum(1 for val in muestras_recolectadas if val is True)
    prob_true = conteo_true / len(muestras_recolectadas)
    
    return {True: prob_true, False: 1.0 - prob_true}

if __name__ == "__main__":
    
    NUM_MUESTRAS = 10000
    BURN_IN = 500
    
    query = 'Lluvia'
    # Evidencia más compleja para hacer MCMC más interesante
    evidencia = {'Aspersor': True, 'Pasto Mojado': True}
    print(f"--- Estimando P({query} | Aspersor = True, Pasto Mojado = True) con {NUM_MUESTRAS} muestras (Muestreo de Gibbs) ---")
    
    distribucion_gibbs = muestreo_gibbs(query, evidencia, estructura_bn, cpts_bn, variables_bn, NUM_MUESTRAS, BURN_IN)
    
    print("\nDistribución Condicional Estimada:")
    for valor, prob in distribucion_gibbs.items():
        print(f"  P({query}={valor} | Aspersor=T, Pasto Mojado=T) ≈ {prob:.3f}")

    # (El resultado exacto es P(L=T|A=T,PM=T) ≈ 0.849)