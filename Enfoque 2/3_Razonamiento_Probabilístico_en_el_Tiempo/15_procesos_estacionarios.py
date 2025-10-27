import numpy as np
import matplotlib.pyplot as plt # Necesitarás matplotlib: pip install matplotlib

def generar_ruido_blanco(n_puntos, media=0, std_dev=1):
    """Genera una serie de ruido blanco (estacionaria)."""
    return np.random.normal(loc=media, scale=std_dev, size=n_puntos)

def generar_camino_aleatorio(n_puntos, inicio=0, std_dev_paso=1):
    """Genera una serie de camino aleatorio (no estacionaria)."""
    pasos = np.random.normal(loc=0, scale=std_dev_paso, size=n_puntos)
    # np.cumsum calcula la suma acumulada de los pasos
    return inicio + np.cumsum(pasos)

# Parámetros
NUM_PUNTOS = 200

# Generar las series
serie_estacionaria = generar_ruido_blanco(NUM_PUNTOS)
serie_no_estacionaria = generar_camino_aleatorio(NUM_PUNTOS)

# Graficar para visualizar
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(serie_estacionaria)
plt.title('Proceso Estacionario (Ruido Blanco)')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.axhline(np.mean(serie_estacionaria), color='r', linestyle='--', label=f'Media={np.mean(serie_estacionaria):.2f}')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(serie_no_estacionaria)
plt.title('Proceso No Estacionario (Camino Aleatorio)')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
# Nota: La media de un camino aleatorio cambia con el tiempo, no es constante.

plt.tight_layout()
plt.show()

print("Se han generado y graficado ejemplos de series temporales.")
print("Observa cómo el Ruido Blanco fluctúa alrededor de una media constante,")
print("mientras que el Camino Aleatorio tiende a 'vagar' sin una media fija.")