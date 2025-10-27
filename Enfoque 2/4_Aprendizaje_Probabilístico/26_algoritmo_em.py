import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Generar Datos Sintéticos
np.random.seed(42) # For reproducibility
n_samples = 300
# Componente 1
mu1_real, sigma1_real, pi1_real = 0, 1, 0.4
data1 = np.random.normal(mu1_real, sigma1_real, int(n_samples * pi1_real))
# Componente 2
mu2_real, sigma2_real, pi2_real = 5, 1.5, 0.6
data2 = np.random.normal(mu2_real, sigma2_real, int(n_samples * pi2_real))
# Mezclar los datos
data = np.concatenate([data1, data2])
np.random.shuffle(data) # Barajar para que no sepamos el origen

# Algoritmo EM para GMM (2 Componentes, 1D)

def em_gmm_1d(data, num_components=2, max_iter=100, tol=1e-4):
    """
    Estima los parámetros de un GMM 1D usando EM.
    """
    n = len(data)
    
    # 1. Inicialización aleatoria de parámetros
    # (Una inicialización más robusta usaría k-Means, pero esto es más simple)
    pis = np.ones(num_components) / num_components
    mus = np.random.choice(data, num_components, replace=False)
    sigmas = np.ones(num_components) * np.std(data) # Usar std dev general al inicio

    log_likelihood_old = -np.inf

    for i in range(max_iter):
        # E-Step (Expectation)
        # Calcular las responsabilidades P(Componente k | data_n, params_actuales)
        responsibilities = np.zeros((n, num_components))
        for k in range(num_components):
            # Usar la PDF (Probability Density Function) de la normal
            responsibilities[:, k] = pis[k] * norm.pdf(data, mus[k], sigmas[k])
        
        # Normalizar las responsabilidades para que sumen 1 para cada punto
        sum_resp = np.sum(responsibilities, axis=1, keepdims=True)
        # Evitar división por cero si alguna probabilidad es muy baja
        sum_resp[sum_resp == 0] = 1e-10
        responsibilities /= sum_resp
        
        # Calcular Log-Likelihood para verificar convergencia
        log_likelihood_new = np.sum(np.log(sum_resp))
        if abs(log_likelihood_new - log_likelihood_old) < tol:
            print(f"Convergencia alcanzada en la iteración {i}")
            break
        log_likelihood_old = log_likelihood_new
        
        # M-Step (Maximization)
        # Actualizar los parámetros usando las responsabilidades
        
        # Nk = suma de responsabilidades para el componente k
        Nks = np.sum(responsibilities, axis=0)
        
        # Actualizar pis (probabilidades de mezcla)
        pis = Nks / n
        
        # Actualizar mus (medias)
        mus = np.sum(data[:, np.newaxis] * responsibilities, axis=0) / Nks
        
        # Actualizar sigmas (desviaciones estándar)
        for k in range(num_components):
             diff_sq = (data - mus[k])**2
             sigmas[k] = np.sqrt(np.sum(diff_sq * responsibilities[:, k]) / Nks[k])
             # Evitar sigmas muy pequeñas
             if sigmas[k] < 1e-6: sigmas[k] = 1e-6

    else: # Si el bucle termina sin break
        print(f"EM no convergió después de {max_iter} iteraciones.")

    return mus, sigmas, pis

# Ejecución y Visualización
if __name__ == "__main__":
    
    print("Ejecutando EM para ajustar un GMM a los datos...")
    
    mu_est, sigma_est, pi_est = em_gmm_1d(data)
    
    print("\nParámetros Reales")
    print(f"Comp 1: mu={mu1_real:.2f}, sigma={sigma1_real:.2f}, pi={pi1_real:.2f}")
    print(f"Comp 2: mu={mu2_real:.2f}, sigma={sigma2_real:.2f}, pi={pi2_real:.2f}")

    print("\n Parámetros Estimados por EM")
    # Ordenar los componentes estimados por media para facilitar comparación
    idx_sorted = np.argsort(mu_est)
    mu_est = mu_est[idx_sorted]
    sigma_est = sigma_est[idx_sorted]
    pi_est = pi_est[idx_sorted]
    for k in range(len(mu_est)):
         print(f"Comp {k+1}: mu={mu_est[k]:.2f}, sigma={sigma_est[k]:.2f}, pi={pi_est[k]:.2f}")

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, density=True, alpha=0.6, label='Datos Observados')
    
    x_axis = np.linspace(data.min(), data.max(), 200)
    for k in range(len(mu_est)):
        plt.plot(x_axis, pi_est[k] * norm.pdf(x_axis, mu_est[k], sigma_est[k]), label=f'Componente {k+1} Estimado')
        
    plt.title('Ajuste de GMM con Algoritmo EM')
    plt.xlabel('Valor')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.show()