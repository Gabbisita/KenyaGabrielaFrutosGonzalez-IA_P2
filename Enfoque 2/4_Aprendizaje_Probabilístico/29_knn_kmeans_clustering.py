import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification # Para generar datos de ejemplo
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier # Implementación de k-NN
from sklearn.metrics import accuracy_score

# Generar Datos Sintéticos
# Creamos 200 puntos con 2 características, pertenecientes a 2 clases.
X, y = make_classification(n_samples=200, n_features=2, n_informative=2,
                           n_redundant=0, n_clusters_per_class=1, random_state=42)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar (Instanciar) el Clasificador k-NN
# Elegimos k=5 vecinos
k = 5
knn = KNeighborsClassifier(n_neighbors=k)

# En k-NN, "fit" simplemente almacena los datos de entrenamiento
knn.fit(X_train, y_train)

# Realizar Predicciones
y_pred = knn.predict(X_test)

# Evaluar el Rendimiento
precision = accuracy_score(y_test, y_pred)
print(f"Clasificador k-NN con k={k}")
print(f"Precisión en el conjunto de prueba: {precision * 100:.2f}%")

# Visualizar los Resultados
plt.figure(figsize=(10, 6))

# Graficar puntos de entrenamiento
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='viridis',
            marker='o', s=50, alpha=0.7, label='Entrenamiento')

# Graficar puntos de prueba (coloreados por predicción, con borde para real)
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='viridis',
            marker='s', s=70, edgecolors='k', linewidths=1, label='Predicción Prueba')

plt.title(f'Clasificación k-NN (k={k}) - Precisión: {precision*100:.1f}%')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.legend()
plt.grid(True)
plt.show()