import numpy as np
import random


def funcion_aptitud(x, y):
    """
    Mide qué tan "buena" es una solución.
    """
    pico1 = 1 * np.exp(-((x - 2)**2 + (y - 2)**2) / 4)
    pico2 = 0.75 * np.exp(-((x + 2)**2 + (y + 2)**2) / 4)
    return pico1 + pico2

# Parámetros del problema
LIMITES = [(-5, 5), (-5, 5)]


def crear_individuo(limites):
    """Crea una solución candidata (un 'individuo') al azar."""
    return np.array([random.uniform(l[0], l[1]) for l in limites])

def seleccionar_padres(poblacion, aptitudes):
    """Elige dos padres de la población. Los más aptos tienen más probabilidad de ser elegidos."""
    # Se suman todas las aptitudes para normalizarlas a probabilidades
    total_aptitud = sum(aptitudes)
    probabilidades = [apt / total_aptitud for apt in aptitudes]
    # Se eligen dos padres basados en esas probabilidades
    indices_padres = np.random.choice(len(poblacion), size=2, p=probabilidades, replace=False)
    return poblacion[indices_padres[0]], poblacion[indices_padres[1]]

def cruce(padre1, padre2):
    """Crea un 'hijo' combinando los 'genes' (coordenadas) de los padres."""
    # Usamos un cruce simple promediando las coordenadas de los padres
    hijo = (padre1 + padre2) / 2
    return hijo

def mutar(individuo, limites, prob_mutacion, magnitud_mutacion):
    """Aplica un pequeño cambio aleatorio al 'hijo'."""
    if random.random() < prob_mutacion:
        mutacion = np.random.uniform(-magnitud_mutacion, magnitud_mutacion, size=individuo.shape)
        individuo += mutacion
        # Asegurarse de que la mutación no saque al individuo de los límites
        individuo = np.clip(individuo, [l[0] for l in limites], [l[1] for l in limites])
    return individuo


def algoritmo_genetico(tamano_poblacion, num_generaciones, prob_mutacion, magnitud_mutacion):
    # 1. Inicialización: Crear la población inicial
    poblacion = [crear_individuo(LIMITES) for _ in range(tamano_poblacion)]
    mejor_individuo = None
    mejor_aptitud = -np.inf

    # 2. Bucle de Generaciones
    for gen in range(num_generaciones):
        # Evaluar la aptitud de la población actual
        aptitudes = np.array([funcion_aptitud(ind[0], ind[1]) for ind in poblacion])

        # Guardar el mejor individuo encontrado hasta ahora
        max_aptitud_actual = np.max(aptitudes)
        if max_aptitud_actual > mejor_aptitud:
            mejor_aptitud = max_aptitud_actual
            mejor_individuo = poblacion[np.argmax(aptitudes)]

        # Crear la siguiente generación
        siguiente_generacion = []
        for _ in range(tamano_poblacion):
            # Selección de padres
            padre1, padre2 = seleccionar_padres(poblacion, aptitudes)
            # Cruce para crear un hijo
            hijo = cruce(padre1, padre2)
            # Mutación del hijo
            hijo_mutado = mutar(hijo, LIMITES, prob_mutacion, magnitud_mutacion)
            siguiente_generacion.append(hijo_mutado)
        
        # Reemplazo: la nueva generación se convierte en la población actual
        poblacion = siguiente_generacion
        
        if gen % 20 == 0:
            print(f"Generación {gen}: Mejor aptitud = {mejor_aptitud:.4f}")
            
    return mejor_individuo, mejor_aptitud


if __name__ == "__main__":
    
    # Parámetros del algoritmo genético
    TAMANO_POBLACION = 100
    NUM_GENERACIONES = 100
    PROBABILIDAD_MUTACION = 0.1
    MAGNITUD_MUTACION = 0.5

    print(f"Ejecutando Algoritmo Genético con una población de {TAMANO_POBLACION} individuos...")
    print(f"El máximo global verdadero está cerca de (2, 2) con altura ~1.0")
    print("-" * 70)

    solucion, valor = algoritmo_genetico(TAMANO_POBLACION, NUM_GENERACIONES, PROBABILIDAD_MUTACION, MAGNITUD_MUTACION)
    
    print("-" * 70)
    print(f"Búsqueda finalizada.")
    print(f"La mejor solución encontrada fue: ({solucion[0]:.2f}, {solucion[1]:.2f})")
    print(f"Aptitud máxima encontrada: {valor:.4f}")
    
    if solucion[0] > 0:
        print("Resultado: ¡La población evolucionó hacia el Máximo Global!")
    else:
        print("Resultado: La población convergió en el Máximo Local.")