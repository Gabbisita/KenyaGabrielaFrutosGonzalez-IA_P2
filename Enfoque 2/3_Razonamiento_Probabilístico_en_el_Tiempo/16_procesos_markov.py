import random
import numpy as np # Necesitarás NumPy: pip install numpy

# Definir la Cadena de Markov

# Estados posibles
estados = ['Soleado', 'Lluvioso']

# Matriz de Transición P(Estado_mañana | Estado_hoy)
#           Mañana=Soleado  Mañana=Lluvioso
# Hoy=Soleado      0.9            0.1
# Hoy=Lluvioso     0.3            0.7
matriz_transicion = {
    'Soleado': {'Soleado': 0.9, 'Lluvioso': 0.1},
    'Lluvioso': {'Soleado': 0.3, 'Lluvioso': 0.7}
}

# Verificar que las filas de la matriz sumen 1
for estado_actual, transiciones in matriz_transicion.items():
    suma = sum(transiciones.values())
    if abs(suma - 1.0) > 1e-9:
        print(f"¡Error! Las probabilidades para el estado '{estado_actual}' no suman 1.")

# Simular la Cadena de Markov

def simular_cadena_markov(estado_inicial, matriz, num_pasos):
    """Simula una secuencia de estados."""
    historial_estados = [estado_inicial]
    estado_actual = estado_inicial

    for _ in range(num_pasos):
        # Obtener las probabilidades de transición desde el estado actual
        probabilidades = matriz[estado_actual]
        
        # Elegir el siguiente estado basado en esas probabilidades
        estado_siguiente = np.random.choice(
            list(probabilidades.keys()),
            p=list(probabilidades.values())
        )
        
        historial_estados.append(estado_siguiente)
        estado_actual = estado_siguiente
        
    return historial_estados

# Ejecución
if __name__ == "__main__":
    
    ESTADO_INICIAL = 'Soleado'
    NUM_DIAS_A_SIMULAR = 15

    print(f"Simulando el clima durante {NUM_DIAS_A_SIMULAR} días, empezando en '{ESTADO_INICIAL}'...")
    
    secuencia_clima = simular_cadena_markov(ESTADO_INICIAL, matriz_transicion, NUM_DIAS_A_SIMULAR)
    
    print("\nSecuencia del clima simulada:")
    print(" -> ".join(secuencia_clima))

    # También podemos calcular la distribución de probabilidad a largo plazo (distribución estacionaria)
    # (Esto requiere álgebra lineal más avanzada, pero es una propiedad clave de muchas Cadenas de Markov)