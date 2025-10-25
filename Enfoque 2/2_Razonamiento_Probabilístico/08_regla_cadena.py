# Definición de la Red Bayesiana

estructura_bn = {
    'Nublado': [],
    'Aspersor': ['Nublado'],
    'Lluvia': ['Nublado'],
    'Pasto Mojado': ['Lluvia', 'Aspersor']
}

cpts_bn = {
    'Nublado': {True: 0.5, False: 0.5},
    'Aspersor': {
        (True,): {True: 0.1, False: 0.9},
        (False,): {True: 0.5, False: 0.5}
    },
    'Lluvia': {
        (True,): {True: 0.8, False: 0.2},
        (False,): {True: 0.2, False: 0.8}
    },
    'Pasto Mojado': {
        (True, True): {True: 0.99, False: 0.01},
        (True, False): {True: 0.90, False: 0.10},
        (False, True): {True: 0.90, False: 0.10},
        (False, False): {True: 0.00, False: 1.00}
    }
}

# Función para Calcular la Probabilidad Conjunta usando la Regla de la Cadena

def calcular_prob_conjunta_bn(asignacion, estructura, cpts):
    """
    Calcula la probabilidad conjunta P(N, A, L, PM) para una asignación específica
    usando la Regla de la Cadena para Redes Bayesianas.

    Args:
        asignacion (dict): Un diccionario con los valores para cada variable.
                           Ej: {'Nublado': True, 'Aspersor': False, 'Lluvia': True, 'Pasto Mojado': True}
        estructura (dict): La definición de los padres de cada nodo.
        cpts (dict): Las Tablas de Probabilidad Condicional.
    """
    probabilidad_total = 1.0

    # Iteramos sobre las variables en un orden consistente con la red (ej, padres antes que hijos)
    # En este caso, el orden del diccionario funciona, pero en general se necesita un orden topológico.
    variables_ordenadas = ['Nublado', 'Aspersor', 'Lluvia', 'Pasto Mojado']

    for variable in variables_ordenadas:
        valor_variable = asignacion[variable]
        padres = estructura[variable]

        # Obtener los valores de los padres de la asignación actual
        valores_padres = tuple(asignacion[p] for p in padres)

        # Buscar la probabilidad P(Variable | Padres) en la CPT correspondiente
        cpt_variable = cpts[variable]

        if not padres: # Si no tiene padres (nodo raíz)
            prob_condicional = cpt_variable[valor_variable]
        else:
             # Si tiene padres, buscamos usando la tupla de valores de los padres
             # y luego el valor de la variable actual
             prob_condicional = cpt_variable[valores_padres][valor_variable]

        # Multiplicar usando la regla de la cadena
        probabilidad_total *= prob_condicional

    return probabilidad_total

if __name__ == "__main__":

    # Definimos un escenario específico
    escenario = {
        'Nublado': True,
        'Aspersor': False,
        'Lluvia': True,
        'Pasto Mojado': True
    }

    print(f"Calculando la probabilidad conjunta para el escenario:")
    for var, val in escenario.items():
        print(f"  {var} = {val}")

    # Calculamos la probabilidad usando la función
    probabilidad = calcular_prob_conjunta_bn(escenario, estructura_bn, cpts_bn)

    print("\nAplicando la Regla de la Cadena para Redes Bayesianas:")
    print("P(N=T, A=F, L=T, PM=T) = P(N=T) * P(A=F|N=T) * P(L=T|N=T) * P(PM=T|L=T, A=F)")

    # Mostramos los valores individuales (puedes verificarlos en las CPTs)
    p_n = cpts_bn['Nublado'][True]
    p_a_dado_n = cpts_bn['Aspersor'][(True,)][False]
    p_l_dado_n = cpts_bn['Lluvia'][(True,)][True]
    p_pm_dado_la = cpts_bn['Pasto Mojado'][(True, False)][True]

    print(f"  = {p_n:.2f} * {p_a_dado_n:.2f} * {p_l_dado_n:.2f} * {p_pm_dado_la:.2f}")
    print(f"  = {probabilidad:.4f}")