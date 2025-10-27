import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

# Creencia Inicial (Prior)
# Representamos nuestra creencia sobre theta (prob. de cara)
# con una distribución Beta(alpha, beta).
# Empezamos con Beta(1, 1), que es una distribución uniforme (no sabemos nada).
alpha_prior = 1
beta_prior = 1

# Simular Datos (Lanzamientos de Moneda)
# Supongamos que la moneda REAL tiene una prob. de cara de 0.7 (sesgada)
prob_real_cara = 0.7
num_lanzamientos = 50
# Generamos una secuencia de lanzamientos (1=Cara, 0=Cruz)
datos_lanzamientos = np.random.binomial(1, prob_real_cara, num_lanzamientos)

# Aprendizaje Bayesiano (Actualización Secuencial)
alpha_actual = alpha_prior
beta_actual = beta_prior

print("Actualización Bayesiana de Creencias")
print(f"Prior: Beta({alpha_actual}, {beta_actual}) - Creencia inicial uniforme.")

# Listas para graficar la evolución de la creencia
puntos_tiempo = [0]
alphas = [alpha_actual]
betas = [beta_actual]

for i, lanzamiento in enumerate(datos_lanzamientos):
    # Actualizar los parámetros de la Beta según el resultado
    if lanzamiento == 1: # Cara
        alpha_actual += 1
    else: # Cruz
        beta_actual += 1

    # Guardar para la gráfica en ciertos puntos
    if (i + 1) in [1, 5, 10, 20, 50]:
        print(f"Después de {i+1} lanzamientos: Posterior = Beta({alpha_actual}, {beta_actual})")
        puntos_tiempo.append(i+1)
        alphas.append(alpha_actual)
        betas.append(beta_actual)

# Visualizar la Evolución de la Creencia
plt.figure(figsize=(10, 6))
x = np.linspace(0, 1, 100) # Rango de posibles valores para theta (prob. de cara)

for i in range(len(puntos_tiempo)):
    # Calcular la PDF de la distribución Beta en cada punto guardado
    pdf = beta.pdf(x, alphas[i], betas[i])
    plt.plot(x, pdf, label=f'Después de {puntos_tiempo[i]} lanzamientos')

plt.title('Aprendizaje Bayesiano: Evolución de la Creencia sobre la Moneda')
plt.xlabel('Probabilidad de Cara (θ)')
plt.ylabel('Densidad de Probabilidad')
plt.legend()
plt.grid(True)
plt.axvline(prob_real_cara, color='r', linestyle='--', label=f'Valor Real ({prob_real_cara})')
plt.legend() # Llamar de nuevo para incluir la línea roja
plt.show()

print("\nObserva cómo la distribución se vuelve más 'picuda' y se centra")
print("alrededor del valor real a medida que vemos más datos.")