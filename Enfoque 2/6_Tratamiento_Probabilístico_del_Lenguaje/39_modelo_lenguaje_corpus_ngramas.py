import numpy as np

# Simulación simple de dos neuronas conectadas
# Neurona de entrada 'i' y neurona de salida 'j'
# Queremos ajustar el peso w_ij

# Tasa de aprendizaje
eta = 0.1

# Peso inicial
w_ij = 0.5

# Datos de entrenamiento (activaciones de las neuronas en diferentes momentos)
# Cada tupla es (activacion_i, activacion_j)
entrenamiento = [
    (1, 1),   # Ambas activas -> Fortalecer
    (0, 1),   # Solo 'j' activa -> Sin cambio (o debilitar, según variante)
    (1, 0),   # Solo 'i' activa -> Sin cambio (o debilitar)
    (0, 0),   # Ninguna activa -> Sin cambio
    (1, 1),   # Ambas activas -> Fortalecer
    (-1, -1), # Ejemplo con activaciones bipolares (-1, 1) - Ambas negativas -> Fortalecer
    (-1, 1)   # Activaciones opuestas -> Debilitar
]

print(f"Regla de Hebb Simple: Δw = η * x_i * y_j")
print(f"Peso inicial w_ij: {w_ij:.2f}")
print("-" * 30)

for t, (x_i, y_j) in enumerate(entrenamiento):
    # Calcular el cambio en el peso según la regla de Hebb básica
    delta_w = eta * x_i * y_j
    
    # Actualizar el peso
    w_ij += delta_w
    
    print(f"Paso {t+1}: x_i={x_i}, y_j={y_j} -> Δw={delta_w:.2f} -> Nuevo w_ij={w_ij:.2f}")

print("-" * 30)
print(f"Peso final w_ij después del aprendizaje: {w_ij:.2f}")