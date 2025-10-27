import numpy as np
import matplotlib.pyplot as plt # Necesitarás matplotlib: pip install matplotlib

# Definición del Sistema y Parámetros del Filtro

# Modelo de Estado (Lineal)
# x_k = F * x_{k-1} + B * u_k + w_k
# Estado x = [posición, velocidad]' (vector columna)
# Matriz de transición F (cómo evoluciona el estado sin control)
dt = 1.0 # Intervalo de tiempo
F = np.array([[1, dt],
              [0, 1]])
# Matriz de control B (no la usamos aquí, asumimos u_k=0)
B = np.array([[0.5 * dt**2], [dt]]) # Ejemplo si hubiera aceleración
# Ruido del proceso w_k (incertidumbre en el modelo de movimiento)
# Covarianza Q del ruido del proceso
q_val = 0.01
Q = np.array([[0.25 * dt**4, 0.5 * dt**3],
              [0.5 * dt**3, dt**2]]) * q_val # Ejemplo simple

# Modelo de Observación (Lineal)
# z_k = H * x_k + v_k
# Matriz de observación H (solo medimos la posición)
H = np.array([[1, 0]])
# Ruido de la medición v_k (incertidumbre en el sensor)
# Covarianza R del ruido de la medición
r_val = 1.0
R = np.array([[r_val]])

# Implementación del Filtro de Kalman

def prediccion_kalman(x_est, P_est, F, Q):
    """Paso de Predicción del Filtro de Kalman."""
    # Predecir el estado: x_pred = F * x_est
    x_pred = F @ x_est
    # Predecir la covarianza del error: P_pred = F * P_est * F^T + Q
    P_pred = F @ P_est @ F.T + Q
    return x_pred, P_pred

def actualizacion_kalman(x_pred, P_pred, z_med, H, R):
    """Paso de Actualización del Filtro de Kalman."""
    # Calcular la Ganancia de Kalman: K = P_pred * H^T * (H * P_pred * H^T + R)^-1
    innovacion_cov = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(innovacion_cov)
    
    # Actualizar la estimación del estado: x_est = x_pred + K * (z_med - H * x_pred)
    residuo = z_med - H @ x_pred
    x_est = x_pred + K @ residuo
    
    # Actualizar la covarianza del error: P_est = (I - K * H) * P_pred
    I = np.identity(P_pred.shape[0])
    P_est = (I - K @ H) @ P_pred
    
    return x_est, P_est

# Simulación
if __name__ == "__main__":
    
    # Simulación del sistema real (oculto para el filtro)
    num_pasos = 50
    posicion_real = np.zeros(num_pasos)
    velocidad_real = np.full(num_pasos, 2.0) # Velocidad constante
    x_real = np.array([0.0, 2.0]) # Estado inicial real [pos, vel]
    
    # Generar mediciones ruidosas
    mediciones = np.zeros(num_pasos)
    for k in range(1, num_pasos):
        # Mover el objeto real (con algo de ruido de proceso)
        w_k = np.sqrt(Q) @ np.random.randn(2, 1) # Ruido de proceso
        x_real = F @ x_real.reshape(2, 1) # + w_k # Omitimos ruido proceso en real para claridad
        posicion_real[k] = x_real[0, 0]
        
        # Generar medición ruidosa
        v_k = np.sqrt(R) @ np.random.randn(1, 1) # Ruido de medición
        mediciones[k] = (H @ x_real.reshape(2, 1) + v_k)[0, 0]

    # Ejecutar el Filtro de Kalman
    x_estimado = np.zeros((2, num_pasos))
    P_estimado = np.zeros((2, 2, num_pasos))
    
    # Estado inicial estimado y su covarianza (incertidumbre inicial)
    x_est = np.array([0.0, 0.0]).reshape(2, 1) # Empezamos sin saber la velocidad
    P_est = np.diag([1.0, 1.0]) * 10 # Incertidumbre inicial alta

    x_estimado[:, 0] = x_est.flatten()
    P_estimado[:, :, 0] = P_est

    for k in range(1, num_pasos):
        # Predicción
        x_pred, P_pred = prediccion_kalman(x_est, P_est, F, Q)
        # Actualización
        z_med = np.array([[mediciones[k]]])
        x_est, P_est = actualizacion_kalman(x_pred, P_pred, z_med, H, R)
        
        x_estimado[:, k] = x_est.flatten()
        P_estimado[:, :, k] = P_est

    # 4. Graficar Resultados
    plt.figure(figsize=(12, 6))
    plt.plot(posicion_real, 'g-', label='Posición Real')
    plt.plot(mediciones, 'bo', markersize=3, label='Mediciones Ruidosas')
    plt.plot(x_estimado[0, :], 'r-', label='Estimación Kalman (Posición)')
    # Líneas de incertidumbre (+/- 1 desviación estándar)
    std_pos = np.sqrt(P_estimado[0, 0, :])
    plt.fill_between(range(num_pasos), x_estimado[0, :] - std_pos, x_estimado[0, :] + std_pos, color='r', alpha=0.2, label='Incertidumbre (1 std dev)')
    
    plt.title('Filtro de Kalman: Seguimiento 1D')
    plt.xlabel('Paso de Tiempo')
    plt.ylabel('Posición')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Simulación completada. La gráfica muestra:")
    print(" - La trayectoria real (verde).")
    print(" - Las mediciones ruidosas (azul).")
    print(" - La estimación del Filtro de Kalman (rojo), que suaviza el ruido.")
    print(" - La banda roja clara indica la incertidumbre del filtro.")