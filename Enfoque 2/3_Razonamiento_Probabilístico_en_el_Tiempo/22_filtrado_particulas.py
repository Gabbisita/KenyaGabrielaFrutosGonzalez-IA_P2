import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import norm # Para la verosimilitud Gaussiana

# Definición del Sistema (No Lineal/No Gaussiano)

# Función de Transición (Movimiento): x_t = f(x_{t-1}) + ruido_proceso
def transition_model(x_prev):
    # Ejemplo: movimiento con velocidad dependiente de la posición + ruido
    return x_prev + 0.1 * x_prev * (5 - x_prev) + np.random.normal(0, 0.5)

# Función de Observación (Sensor): z_t = h(x_t) + ruido_medicion
def observation_model(x_true):
    # Ejemplo: sensor no lineal + ruido
    return x_true**2 / 10.0 + np.random.normal(0, 1.0)

# Verosimilitud de la observación P(z_t | x_t)
# Asumimos ruido Gaussiano en la medición para calcular la verosimilitud
std_dev_medicion = 1.0
def likelihood(z_med, x_particula):
    # Qué tan probable es la medición 'z_med' si el estado real fuera 'x_particula'
    valor_esperado_med = x_particula**2 / 10.0
    # Usamos la PDF (Probability Density Function) de la normal
    prob = norm.pdf(z_med, loc=valor_esperado_med, scale=std_dev_medicion)
    # Evitar pesos cero absolutos (puede causar problemas)
    return prob + 1e-10

# Algoritmo de Filtrado de Partículas

def particle_filter(num_particulas, mediciones, x_inicial_rango):
    """Implementa un Filtro de Partículas básico."""
    
    # 1. Inicialización: Crear partículas distribuidas uniformemente
    particulas = np.random.uniform(x_inicial_rango[0], x_inicial_rango[1], num_particulas)
    pesos = np.ones(num_particulas) / num_particulas # Pesos iguales al inicio
    
    historial_estimaciones = [] # Para guardar la posición estimada en cada paso

    for z_med in mediciones:
        # 2. Predicción (Mover cada partícula)
        particulas = np.array([transition_model(p) for p in particulas])
        
        # 3. Actualización (Pesar cada partícula por la verosimilitud)
        pesos = np.array([likelihood(z_med, p) for p in particulas])
        
        # Normalizar los pesos
        suma_pesos = np.sum(pesos)
        if suma_pesos == 0:
            # Si todos los pesos son cero, re-inicializar (poco probable pero posible)
            particulas = np.random.uniform(x_inicial_rango[0], x_inicial_rango[1], num_particulas)
            pesos = np.ones(num_particulas) / num_particulas
        else:
            pesos /= suma_pesos
            
        # Estimación del estado actual (media ponderada de las partículas)
        estimacion_actual = np.sum(particulas * pesos)
        historial_estimaciones.append(estimacion_actual)

        # 4. Remuestreo (Resampling) - Multinomial Resampling
        indices = np.random.choice(num_particulas, size=num_particulas, p=pesos)
        particulas = particulas[indices]
        # Resetear pesos después del remuestreo
        pesos = np.ones(num_particulas) / num_particulas 
        
    return np.array(historial_estimaciones)

# Simulación
if __name__ == "__main__":
    
    # Simular el sistema real (oculto)
    num_pasos = 50
    x_real = np.zeros(num_pasos)
    x_real[0] = 1.0 # Posición inicial real
    for k in range(1, num_pasos):
        x_real[k] = transition_model(x_real[k-1])

    # Generar mediciones ruidosas
    mediciones = np.array([observation_model(x) for x in x_real])

    # Ejecutar el Filtro de Partículas
    NUM_PARTICULAS = 500
    RANGO_INICIAL = (0, 2)
    estimaciones = particle_filter(NUM_PARTICULAS, mediciones, RANGO_INICIAL)

    # Graficar Resultados
    plt.figure(figsize=(12, 6))
    plt.plot(x_real, 'g-', label='Posición Real')
    plt.plot(mediciones, 'bo', markersize=3, alpha=0.5, label='Mediciones Ruidosas')
    plt.plot(estimaciones, 'r-', label='Estimación Filtro Partículas')
    
    plt.title('Filtro de Partículas: Seguimiento 1D No Lineal')
    plt.xlabel('Paso de Tiempo')
    plt.ylabel('Posición')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Simulación completada. La gráfica muestra:")
    print(" - La trayectoria real (verde).")
    print(" - Las mediciones ruidosas (azul).")
    print(" - La estimación del Filtro de Partículas (rojo), que sigue la tendencia.")