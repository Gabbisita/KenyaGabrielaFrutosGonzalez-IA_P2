import numpy as np

# Asumimos que tenemos un HMM y datos
estados = ['Llueve', 'No Llueve']
observaciones = ['Paraguas', 'No Paraguas']
observaciones_sec = ['Paraguas', 'Paraguas', 'No Paraguas'] # Datos de entrenamiento
T = len(observaciones_sec)
N = len(estados) # Num estados
M = len(observaciones) # Num observaciones posibles

# Mapeos para índices
estado_a_idx = {s: i for i, s in enumerate(estados)}
obs_a_idx = {o: k for k, o in enumerate(observaciones)}
idx_a_estado = {i: s for i, s in enumerate(estados)}

# Inicialización Aleatoria (o con Suposiciones)
# Necesitamos A (transición), B (emisión), pi (inicial)
A = np.random.rand(N, N)
A /= A.sum(axis=1, keepdims=True) # Normalizar filas

B = np.random.rand(N, M)
B /= B.sum(axis=1, keepdims=True) # Normalizar filas

pi = np.random.rand(N)
pi /= pi.sum()

print(" Parámetros Iniciales (Aleatorios)")
print("Matriz A (Transición):\n", A)
print("Matriz B (Emisión):\n", B)
print("Vector pi (Inicial):\n", pi)

# Simulación del E-Step (Cálculo de Expectativas)
# ESTA PARTE NORMALMENTE USA FORWARD-BACKWARD. AQUÍ USAMOS VALORES FICTICIOS.
# gamma[t, i] = Probabilidad de estar en estado i en tiempo t, dado O
gamma = np.random.rand(T, N)
gamma /= gamma.sum(axis=1, keepdims=True) # Normalizar para cada tiempo t

# xi[t, i, j] = Probabilidad de estar en estado i en t y en j en t+1, dado O
xi = np.random.rand(T - 1, N, N)
# Normalizar xi (más complejo, asegurar P(Xt, Xt+1|O) = sum_j xi[t,i,j])
for t in range(T - 1):
     xi[t] /= xi[t].sum() # Simplificación - normalización real es diferente

print("\n Expectativas del E-Step")
# print("Gamma (P(Xt=i | O)):\n", gamma)
# print("Xi (P(Xt=i, Xt+1=j | O)):\n", xi)

# M-Step (Maximización - Reestimación de Parámetros)

# Reestimar pi
pi_nuevo = gamma[0] # P(X0=i | O)

# Reestimar A
# A[i, j] = Sum_t Xi[t, i, j] / Sum_t Gamma[t, i] (para t=0..T-2)
numerador_A = np.sum(xi, axis=0) # Suma sobre el tiempo t
denominador_A = np.sum(gamma[:-1], axis=0) # Suma sobre t=0..T-2
# Evitar división por cero
denominador_A[denominador_A == 0] = 1e-6
A_nuevo = numerador_A / denominador_A[:, np.newaxis]

# Reestimar B
# B[j, k] = Sum_{t where Ot=k} Gamma[t, j] / Sum_t Gamma[t, j]
numerador_B = np.zeros((N, M))
denominador_B = np.sum(gamma, axis=0) # Suma sobre todo el tiempo t
# Evitar división por cero
denominador_B[denominador_B == 0] = 1e-6

for t in range(T):
    obs_idx = obs_a_idx[observaciones_sec[t]]
    for j in range(N):
        numerador_B[j, obs_idx] += gamma[t, j]
        
B_nuevo = numerador_B / denominador_B[:, np.newaxis]

print("\n Parámetros Reestimados (M-Step)")
print("Nueva Matriz A:\n", A_nuevo)
print("Nueva Matriz B:\n", B_nuevo)
print("Nuevo Vector pi:\n", pi_nuevo)

# En un bucle real, estos A_nuevo, B_nuevo, pi_nuevo se convertirían
# en los parámetros para el siguiente E-Step, repitiendo hasta converger.