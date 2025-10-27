import numpy as np

# Frase Origen
frase_origen = "el gato"

# Posibles Traducciones Candidatas
traducciones_candidatas = [
    "the cat",
    "a cat",
    "cat the" # Gramaticalmente incorrecta
]

# Modelo de Traducción (Simplificado) P(Origen | Traducción) 
# Qué tan probable es obtener "el gato" DADA una traducción específica.
# (Valores inventados para ilustrar)
prob_traduccion_modelo = {
    "the cat": 0.8, # Muy probable que "the cat" se traduzca como "el gato"
    "a cat": 0.15, # Menos probable
    "cat the": 0.05 # Muy improbable (mala estructura)
}

# Modelo de Lenguaje (Simplificado) P(Traducción)
# Qué tan fluida/probable es la frase candidata en INGLÉS.
# (Valores inventados)
prob_lenguaje_modelo = {
    "the cat": 0.7, # Frase común y correcta
    "a cat": 0.2, # Frase correcta, quizás menos común en contexto general
    "cat the": 0.1 # Frase agramatical, muy poco probable
}

# Calcular la "Mejor" Traducción
# Buscamos la T que maximiza: P(Origen | T) * P(T)

mejor_traduccion = None
mejor_puntuacion = -1.0

print(f"Traduciendo: '{frase_origen}'")
print("\nEvaluando candidatas:")

for t_candidata in traducciones_candidatas:
    p_origen_dado_t = prob_traduccion_modelo.get(t_candidata, 1e-9) # Usar prob muy baja si no está definida
    p_t = prob_lenguaje_modelo.get(t_candidata, 1e-9)
    
    # Puntuación combinada (proporcional a la probabilidad posterior P(T|Origen))
    puntuacion = p_origen_dado_t * p_t
    
    print(f"  - Candidata: '{t_candidata}'")
    print(f"    P(Origen|T) = {p_origen_dado_t:.2f}")
    print(f"    P(T)        = {p_t:.2f}")
    print(f"    Puntuación  = {p_origen_dado_t:.2f} * {p_t:.2f} = {puntuacion:.4f}")
    
    if puntuacion > mejor_puntuacion:
        mejor_puntuacion = puntuacion
        mejor_traduccion = t_candidata

print("\nResultado")
print(f"La traducción más probable es: '{mejor_traduccion}'")
print(f"Con una puntuación combinada de: {mejor_puntuacion:.4f}")