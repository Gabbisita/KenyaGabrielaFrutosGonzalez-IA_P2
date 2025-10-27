import numpy as np
import matplotlib.pyplot as plt
from minisom import MiniSom # pip install MiniSom

# Generar Datos Sintéticos (Colores RGB)
# Creamos 100 colores aleatorios. Cada color tiene 3 'features' (R, G, B).
num_colores = 100
# Datos: matriz de num_colores x 3 (R, G, B entre 0 y 1)
colores_data = np.random.rand(num_colores, 3)

# Inicializar y Entrenar el SOM
# Tamaño del mapa (rejilla 2D)
map_size_x = 10
map_size_y = 10
# Número de características de entrada (R, G, B)
input_len = 3
# Parámetros del SOM
sigma = 1.0 # Tamaño inicial de la vecindad
learning_rate = 0.5

# Inicializar el SOM
som = MiniSom(map_size_x, map_size_y, input_len, sigma=sigma,
              learning_rate=learning_rate, random_seed=42)

# Inicializar los pesos (opcional, puede ayudar a visualizar)
# som.random_weights_init(colores_data) # O usar PCA init
som.pca_weights_init(colores_data) # Inicialización basada en PCA

print(f"Entrenando SOM de {map_size_x}x{map_size_y} con {num_colores} colores...")
# Entrenar el SOM
num_iteraciones = 1000
som.train_random(colores_data, num_iteraciones)
print("Entrenamiento completado.")

# Visualizar el Mapa Organizado
# Obtenemos los pesos finales de cada neurona (que representan colores)
mapa_pesos = som.get_weights() # Devuelve un array de map_x x map_y x input_len

plt.figure(figsize=(8, 8))
# Mostramos la rejilla donde cada celda tiene el color representado por los pesos de esa neurona
plt.imshow(mapa_pesos, interpolation='none')
plt.title('Mapa Autoorganizado de Kohonen (SOM) para Colores')
plt.xlabel('Coordenada X del Mapa')
plt.ylabel('Coordenada Y del Mapa')
# Ocultar los números de los ejes que no son tan relevantes aquí
plt.xticks([])
plt.yticks([])
plt.show()

print("\nSe ha visualizado el SOM entrenado.")
print("Observa cómo colores similares tienden a agruparse en regiones")
print("cercanas del mapa 2D.")

# Opcional: Mapear datos originales al mapa
# Podemos ver dónde caen los colores originales en el mapa entrenado
mapped_coords = np.array([som.winner(x) for x in colores_data]).T
plt.figure(figsize=(8, 8))
# Graficar el mapa de fondo
plt.pcolor(mapa_pesos[:, :, 0], cmap='Reds', alpha=0.2) # Usar un solo canal como fondo
plt.pcolor(mapa_pesos[:, :, 1], cmap='Greens', alpha=0.2)
plt.pcolor(mapa_pesos[:, :, 2], cmap='Blues', alpha=0.2)
# Graficar los puntos de datos mapeados
plt.scatter(mapped_coords[0] + np.random.rand(num_colores) * 0.8 - 0.4, # Añadir jitter
            mapped_coords[1] + np.random.rand(num_colores) * 0.8 - 0.4,
            c=colores_data, s=50, edgecolors='k', linewidths=0.5)
plt.title('Posición de los Colores Originales en el SOM')
plt.xticks(np.arange(map_size_x))
plt.yticks(np.arange(map_size_y))
plt.grid(True)
plt.show()