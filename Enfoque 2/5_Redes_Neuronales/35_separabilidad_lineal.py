import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

# Generar Datos NO Linealmente Separables (XOR)
# Entradas: (0,0), (0,1), (1,0), (1,1)
# Salidas XOR: 0, 1, 1, 0
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

# Intentar Entrenar el Perceptrón
perceptron_xor = Perceptron(max_iter=100, tol=1e-3, random_state=42)
perceptron_xor.fit(X_xor, y_xor)

# Evaluar
y_pred_xor = perceptron_xor.predict(X_xor)
precision_xor = accuracy_score(y_xor, y_pred_xor)
print(f"Intentando resolver XOR con un Perceptrón Simple:")
print(f"  Precisión obtenida: {precision_xor * 100:.2f}%")
print("  (Un Perceptrón simple NO PUEDE resolver XOR perfectamente)")

# Visualizar (Datos XOR y Límite)
plt.figure(figsize=(6, 5))
plt.scatter(X_xor[:, 0], X_xor[:, 1], c=y_xor, cmap=plt.cm.coolwarm, s=100, edgecolors='k')

# Dibujar el límite de decisión encontrado (que será incorrecto)
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()
xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 50),
                     np.linspace(ylim[0], ylim[1], 50))
Z = perceptron_xor.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)

plt.title(f'Perceptrón intentando separar XOR (Falla)')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.xticks([0, 1])
plt.yticks([0, 1])
plt.grid(True)
plt.show()