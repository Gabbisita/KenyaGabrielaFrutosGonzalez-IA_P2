import itertools

# Definir una Tabla de Probabilidad Conjunta
# Creamos una tabla donde A y C son condicionalmente independientes dado B.
# Clave: (Valor_A, Valor_B, Valor_C), Valor: Probabilidad

prob_conjunta = {
    # B = True
    (True,  True,  True):  0.10, # P(A=T,C=T|B=T)=0.10/P(B=T)
    (True,  True,  False): 0.15, # P(A=T,C=F|B=T)=0.15/P(B=T) => P(A=T|B=T)=(0.10+0.15)/P(B=T) = 0.25/P(B=T)
    (False, True,  True):  0.10, # P(A=F,C=T|B=T)=0.10/P(B=T)
    (False, True,  False): 0.15, # P(A=F,C=F|B=T)=0.15/P(B=T) => P(A=F|B=T)=(0.10+0.15)/P(B=T) = 0.25/P(B=T)
                                 # P(C=T|B=T)=(0.10+0.10)/P(B=T)=0.20/P(B=T), P(C=F|B=T)=(0.15+0.15)/P(B=T)=0.30/P(B=T)
                                 # P(B=T) = 0.10+0.15+0.10+0.15 = 0.50
                                 # P(A=T|B=T) = 0.25/0.50 = 0.5; P(C=T|B=T) = 0.20/0.50 = 0.4
                                 # P(A=T,C=T|B=T)=0.10/0.50=0.2. Check: P(A=T|B=T)*P(C=T|B=T)=0.5*0.4=0.2. OK.
    # B = False
    (True,  False, True):  0.12, # P(A=T,C=T|B=F)=0.12/P(B=F)
    (True,  False, False): 0.18, # P(A=T,C=F|B=F)=0.18/P(B=F) => P(A=T|B=F)=(0.12+0.18)/P(B=F) = 0.30/P(B=F)
    (False, False, True):  0.08, # P(A=F,C=T|B=F)=0.08/P(B=F)
    (False, False, False): 0.12, # P(A=F,C=F|B=F)=0.12/P(B=F) => P(A=F|B=F)=(0.08+0.12)/P(B=F) = 0.20/P(B=F)
                                 # P(C=T|B=F)=(0.12+0.08)/P(B=F)=0.20/P(B=F), P(C=F|B=F)=(0.18+0.12)/P(B=F)=0.30/P(B=F)
                                 # P(B=F) = 0.12+0.18+0.08+0.12 = 0.50
                                 # P(A=T|B=F) = 0.30/0.50 = 0.6; P(C=T|B=F) = 0.20/0.50 = 0.4
                                 # P(A=T,C=T|B=F)=0.12/0.50=0.24. Check: P(A=T|B=F)*P(C=T|B=F)=0.6*0.4=0.24. OK.
}

# Verificar que la tabla suma 1
total_prob = sum(prob_conjunta.values())
print(f"Suma de la Probabilidad Conjunta: {total_prob:.2f}")
assert abs(total_prob - 1.0) < 1e-9

# Funciones Auxiliares para Calcular Probabilidades

def prob_marginal(variables, valores, jpt):
    """Calcula la probabilidad marginal P(variables=valores) sumando en la JPT."""
    prob = 0
    # Genera todas las combinaciones posibles para TODAS las variables (A, B, C)
    todas_vars = list(jpt.keys())[0] # Obtiene la estructura (var1, var2, var3)
    num_vars = len(todas_vars)
    indices_fijos = {i for i, v in enumerate(variables)}

    # Itera sobre todas las 2^N combinaciones True/False
    for combo_completo in itertools.product([True, False], repeat=num_vars):
        # Verifica si esta combinación coincide con los valores fijos que buscamos
        coincide = True
        for i, val_fijo in zip(range(num_vars), variables):
            if i in indices_fijos and combo_completo[i] != valores[variables.index(val_fijo)]:
                 coincide = False
                 break
        if coincide:
             # Aquí necesitamos encontrar la clave correcta basada en el orden de jpt
             # Asumimos que el orden en jpt es siempre (A, B, C)
             clave_jpt = tuple(combo_completo)
             prob += jpt.get(clave_jpt, 0) # Suma la probabilidad de esta fila
    return prob

def prob_condicionada(var_objetivo, val_objetivo, evidencia_vars, evidencia_vals, jpt):
    """Calcula P(var_objetivo=val_objetivo | evidencia_vars=evidencia_vals)"""
    # P(A|B) = P(A, B) / P(B)

    # Calcular P(A, B)
    vars_conjunta = [var_objetivo] + evidencia_vars
    vals_conjunta = [val_objetivo] + evidencia_vals
    p_conjunta = prob_marginal(vars_conjunta, vals_conjunta, jpt)

    # Calcular P(B)
    p_evidencia = prob_marginal(evidencia_vars, evidencia_vals, jpt)

    # Calcular P(A|B)
    if p_evidencia == 0:
        return 0 # Evitar división por cero
    return p_conjunta / p_evidencia

# Verificar la Independencia Condicional
# ¿Es P(A=True | B=True, C=True) igual a P(A=True | B=True)?

# Calcular P(A=T | B=T, C=T)
p_A_dado_BC = prob_condicionada(
    'A', True,                           # Objetivo: A=True
    ['B', 'C'], [True, True],            # Evidencia: B=True, C=True
    prob_conjunta
)

# Calcular P(A=T | B=T)
p_A_dado_B = prob_condicionada(
    'A', True,                           # Objetivo: A=True
    ['B'], [True],                       # Evidencia: B=True
    prob_conjunta
)

print(f"\nVerificando si P(A=T | B=T, C=T) == P(A=T | B=T):")
print(f"  P(A=T | B=T, C=T) = {p_A_dado_BC:.2f}")
print(f"  P(A=T | B=T)      = {p_A_dado_B:.2f}")

if abs(p_A_dado_BC - p_A_dado_B) < 1e-9:
    print("\nSon iguales. ¡A y C son condicionalmente independientes dado B!")
else:
    print("\nSon diferentes. A y C NO son condicionalmente independientes dado B.")

# Verifiquemos también con B=False
print("\nVerificando también con B=False:")
p_A_dado_nBC = prob_condicionada('A', True, ['B', 'C'], [False, True], prob_conjunta)
p_A_dado_nB = prob_condicionada('A', True, ['B'], [False], prob_conjunta)
print(f"  P(A=T | B=F, C=T) = {p_A_dado_nBC:.2f}")
print(f"  P(A=T | B=F)      = {p_A_dado_nB:.2f}")
if abs(p_A_dado_nBC - p_A_dado_nB) < 1e-9:
    print("Son iguales. Condicionalmente independientes también cuando B es False.")