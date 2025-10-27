from collections import Counter, defaultdict
import re # Para tokenizar de forma simple

# Corpus
corpus_texto = """
el pasto es verde .
las nubes son blancas .
el cielo es azul .
el pasto crece alto .
"""

# Preprocesamiento Súper Básico
# Convertir a minúsculas y dividir por espacios/puntuación
tokens = re.findall(r'\b\w+\b|\.', corpus_texto.lower())

# Calcular Frecuencias
conteo_unigramas = Counter(tokens)

# Añadir marcadores de inicio/fin <s> y </s>
tokens_con_marcadores = ['<s>'] + tokens + ['</s>']
conteo_bigramas = Counter()
for i in range(len(tokens_con_marcadores) - 1):
    bigrama = (tokens_con_marcadores[i], tokens_con_marcadores[i+1])
    conteo_bigramas[bigrama] += 1

# Conteo de unigramas incluyendo <s>
conteo_unigramas_con_inicio = Counter(tokens_con_marcadores)

# Calcular Probabilidades Condicionales
probabilidades_bigramas = defaultdict(lambda: defaultdict(float))

for (w_anterior, w_actual), count in conteo_bigramas.items():
    conteo_palabra_anterior = conteo_unigramas_con_inicio[w_anterior]
    if conteo_palabra_anterior > 0:
        probabilidades_bigramas[w_anterior][w_actual] = count / conteo_palabra_anterior
    else:
         probabilidades_bigramas[w_anterior][w_actual] = 0.0

# Mostrar Resultados
print("Corpus")
print(corpus_texto)
print("\nTokens")
print(tokens)

print("\nConteo de Unigramas (Fragmento)")
print(conteo_unigramas.most_common(5))

print("\nConteo de Bigramas (Fragmento)")
print(conteo_bigramas.most_common(5))

print("\nProbabilidades de Bigramas (Ejemplos)")
palabra_anterior = 'el'
print(f"Probabilidades P(w | '{palabra_anterior}'):")
if palabra_anterior in probabilidades_bigramas:
    for palabra_siguiente, prob in probabilidades_bigramas[palabra_anterior].items():
        print(f"  P({palabra_siguiente} | {palabra_anterior}) = {prob:.2f}")
else:
    print("  (No se encontraron bigramas con esa palabra anterior)")

palabra_anterior = 'pasto'
print(f"\nProbabilidades P(w | '{palabra_anterior}'):")
if palabra_anterior in probabilidades_bigramas:
    for palabra_siguiente, prob in probabilidades_bigramas[palabra_anterior].items():
        print(f"  P({palabra_siguiente} | {palabra_anterior}) = {prob:.2f}")
else:
    print("  (No se encontraron bigramas con esa palabra anterior)")

palabra_anterior = '<s>'
print(f"\nProbabilidades P(w | '{palabra_anterior}'):")
if palabra_anterior in probabilidades_bigramas:
    for palabra_siguiente, prob in probabilidades_bigramas[palabra_anterior].items():
        print(f"  P({palabra_siguiente} | {palabra_anterior}) = {prob:.2f}")
else:
    print("  (No se encontraron bigramas con esa palabra anterior)")