import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs # Para generar datos de ejemplo
from sklearn.cluster import KMeans       # Implementación de k-Means

# Generar Datos Sintéticos
# Creamos 300 puntos de datos agrupados alrededor de 3 centros.
# 'X' contendrá las coordenadas (features), 'y_true' las etiquetas reales (que NO usaremos).
X, y_true = make_blobs(n_samples=300, centers=3, cluster_std=0.8, random_state=42)

# Graficar los datos originales (sin colorear por grupo)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], s=30, c='gray', alpha=0.7)
plt.title('Datos Originales (Sin Etiquetas)')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.grid(True)

# Aplicar el Algoritmo k-Means
# Especificamos que queremos encontrar k=3 clústeres.
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10) # n_init ayuda a la estabilidad
kmeans.fit(X) # Aquí es donde el algoritmo "aprende" los grupos

# Obtener las etiquetas asignadas por k-Means y los centroides
y_kmeans = kmeans.predict(X)
centroides = kmeans.cluster_centers_

# Visualizar los Resultados
plt.subplot(1, 2, 2)
# Colorear los puntos según el clúster asignado por k-Means
plt.scatter(X[:, 0], X[:, 1], s=30, c=y_kmeans, cmap='viridis', alpha=0.7)
# Marcar los centroides encontrados
plt.scatter(centroides[:, 0], centroides[:, 1], s=100, c='red', marker='X', label='Centroides')
plt.title('Datos Agrupados por k-Means (k=3)')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("Se generaron datos sintéticos y se aplicó k-Means.")
print("La figura muestra los datos originales y cómo k-Means los agrupó.")
print("Observa cómo los colores asignados por k-Means (derecha) corresponden")
print("generalmente a los grupos visuales en los datos originales (izquierda).")