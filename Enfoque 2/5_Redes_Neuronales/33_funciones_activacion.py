import numpy as np
import matplotlib.pyplot as plt

# Definición de las Funciones de Activación

def sigmoid(z):
    """Calcula la función sigmoide."""
    return 1 / (1 + np.exp(-z))

def tanh(z):
    """Calcula la función tangente hiperbólica."""
    return np.tanh(z)

def relu(z):
    """Calcula la función ReLU (Rectified Linear Unit)."""
    return np.maximum(0, z)

# Generar datos de entrada
z = np.linspace(-5, 5, 100) # Un rango de valores de entrada

# Calcular las salidas
y_sigmoid = sigmoid(z)
y_tanh = tanh(z)
y_relu = relu(z)

# Graficar los resultados
plt.figure(figsize=(12, 7))

plt.subplot(2, 2, 1)
plt.plot(z, y_sigmoid, label='Sigmoid')
plt.title('Función Sigmoide')
plt.xlabel('Entrada (z)')
plt.ylabel('Salida f(z)')
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(z, y_tanh, label='Tanh', color='orange')
plt.title('Función Tanh')
plt.xlabel('Entrada (z)')
plt.ylabel('Salida f(z)')
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(z, y_relu, label='ReLU', color='green')
plt.title('Función ReLU')
plt.xlabel('Entrada (z)')
plt.ylabel('Salida f(z)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print("Se han graficado las funciones de activación Sigmoid, Tanh y ReLU.")
print("Observa sus diferentes formas y rangos de salida.")