# pip install scikit-image matplotlib

import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color # Para cargar imagen y convertir a gris
from skimage.feature import local_binary_pattern # Para calcular LBP
import os

# Definir Nombres de Archivo
archivo_entrada = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg"
if not os.path.exists(archivo_entrada):
    print(f"Error: No se encontró '{archivo_entrada}'. Coloca una imagen con ese nombre.")
    exit()

try:
    # Cargar y Preprocesar Imagen
    imagen_color = io.imread(archivo_entrada)
    imagen_gris = color.rgb2gray(imagen_color) # LBP usualmente se aplica a escala de grises
    print(f"Imagen '{archivo_entrada}' cargada y convertida a escala de grises.")

    # Calcular Patrones Binarios Locales (LBP)
    radius = 3 # Radio de la vecindad
    n_points = 8 * radius # Número de puntos vecinos a considerar
    metodo = 'uniform' # Método 'uniform' es robusto a rotaciones

    # Calcular la imagen LBP
    lbp = local_binary_pattern(imagen_gris, n_points, radius, method=metodo)
    print("Imagen LBP calculada.")

    # Calcular Histograma de LBP (Descriptor de Textura)
    # El histograma de los valores LBP es una forma común de representar la textura
    # El número de bins depende del método ('uniform' reduce el número de patrones)
    n_bins = int(lbp.max() + 1)
    hist_lbp, _ = np.histogram(lbp.ravel(), density=True, bins=n_bins, range=(0, n_bins))
    print("Histograma LBP calculado.")

    # Visualizar Resultados
    plt.figure(figsize=(12, 6))

    # Imagen Original en Gris
    plt.subplot(1, 3, 1)
    plt.imshow(imagen_gris, cmap='gray')
    plt.title('Imagen Original (Gris)')
    plt.axis('off')

    # Imagen LBP
    plt.subplot(1, 3, 2)
    # Mostramos la imagen LBP (representa patrones locales)
    plt.imshow(lbp, cmap='gray')
    plt.title('Patrones Binarios Locales (LBP)')
    plt.axis('off')

    # Histograma LBP
    plt.subplot(1, 3, 3)
    plt.plot(hist_lbp)
    plt.title('Histograma LBP (Descriptor)')
    plt.xlabel('Valor del Patrón LBP')
    plt.ylabel('Proporción')
    plt.ylim(bottom=0) # Asegurar que el eje Y empiece en 0

    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'.")
except Exception as e:
    print(f"Ocurrió un error: {e}")