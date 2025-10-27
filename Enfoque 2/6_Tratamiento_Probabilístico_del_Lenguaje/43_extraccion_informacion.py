from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Corpus de Documentos
documentos = [
    "el cielo es azul y hermoso",
    "el sol brilla intensamente en el cielo azul",
    "el sol es una estrella brillante y caliente",
    "las nubes cubren el cielo azul a veces"
]

# Crear Vectores TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documentos)

# Opcional: Ver vocabulario y matriz
# print("Vocabulario:", vectorizer.get_feature_names_out())
# print("\nMatriz TF-IDF (Documentos x Palabras):\n", tfidf_matrix.toarray().round(2))

# Definir una Consulta
consulta = "sol brillante y cielo azul"

# Convertir la Consulta a Vector TF-IDF
consulta_vec = vectorizer.transform([consulta])

# Calcular Similitud del Coseno
similitudes = cosine_similarity(consulta_vec, tfidf_matrix)
similitudes_flat = similitudes.flatten()

# Obtener Ranking
ranking_indices = np.argsort(similitudes_flat)[::-1] # Índices ordenados de mayor a menor

print(f"Consulta: '{consulta}'")
print("\nRanking de Documentos (más a menos similar):")
for i, index in enumerate(ranking_indices):
    print(f"  {i+1}. Doc {index+1}: '{documentos[index]}' (Sim: {similitudes_flat[index]:.3f})")