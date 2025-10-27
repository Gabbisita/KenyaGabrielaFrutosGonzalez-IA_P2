# Definimos la tabla de probabilidad conjunta P(DolorDeMuelas, Caries)
#          Caries=True  Caries=False
# Dolor=True    0.04         0.01     -> P(Dolor=True) = 0.05
# Dolor=False   0.01         0.94     -> P(Dolor=False) = 0.95
#              ------       ------
# P(Caries=T)=0.05  P(Caries=F)=0.95

# Representamos la tabla conjunta como un diccionario anidado
# P[dolor][caries]
prob_conjunta = {
    True: {True: 0.04, False: 0.01}, # Probabilidades si Dolor=True
    False: {True: 0.01, False: 0.94} # Probabilidades si Dolor=False
}

# Calcular usando la fórmula directa
# P(Caries=T | Dolor=T) = P(Caries=T y Dolor=T) / P(Dolor=T)

# P(Caries=T y Dolor=T) directamente de la tabla
p_caries_y_dolor = prob_conjunta[True][True]

# P(Dolor=T) se calcula sumando la fila Dolor=True
p_dolor = prob_conjunta[True][True] + prob_conjunta[True][False]

# Calcular P(Caries=T | Dolor=T)
p_caries_dado_dolor = p_caries_y_dolor / p_dolor

print(f"Cálculo usando Fórmula Directa")
print(f"P(Caries=True y Dolor=True) = {p_caries_y_dolor}")
print(f"P(Dolor=True) = {p_dolor}")
print(f"P(Caries=True | Dolor=True) = {p_caries_y_dolor} / {p_dolor} = {p_caries_dado_dolor:.2f}")

# Calcularusando Normalización
# Queremos calcular el vector P(Caries | Dolor=True) = [P(C=T|D=T), P(C=F|D=T)]
# Lo calculamos como α * P(Caries, Dolor=True) = α * [P(C=T, D=T), P(C=F, D=T)]

# Extraemos el vector de la tabla
vector_conjunto_dolor_true = {
    True: prob_conjunta[True][True],  # P(C=T, D=T) = 0.04
    False: prob_conjunta[True][False] # P(C=F, D=T) = 0.01
}

# Calculamos la suma para normalizar
suma_para_normalizar = sum(vector_conjunto_dolor_true.values()) # 0.04 + 0.01 = 0.05

# Normalizamos dividiendo cada elemento por la suma
distribucion_condicionada_normalizada = {
    caries: prob / suma_para_normalizar
    for caries, prob in vector_conjunto_dolor_true.items()
}

print(f"\n Cálculo usando Normalización")
print(f"Vector P(Caries, Dolor=True) = {vector_conjunto_dolor_true}")
print(f"Suma (α = 1/Suma) = {suma_para_normalizar}")
print(f"Distribución P(Caries | Dolor=True) normalizada:")
for caries, prob in distribucion_condicionada_normalizada.items():
    print(f"  P(Caries={caries} | Dolor=True) = {prob:.2f}")

# Comprobamos que el resultado para P(Caries=True | Dolor=True) es el mismo
assert abs(p_caries_dado_dolor - distribucion_condicionada_normalizada[True]) < 1e-9