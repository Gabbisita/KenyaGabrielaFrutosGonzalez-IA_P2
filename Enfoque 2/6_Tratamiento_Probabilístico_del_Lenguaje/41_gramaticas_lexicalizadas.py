from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Corpus de Documentos
documentos = [
    "el cielo es azul",
    "el sol brilla intensamente hoy",
    "el cielo azul es hermoso",
    "el sol es una estrella brillante"
]

# Crear Vectores TF-IDF
# TfidfVectorizer maneja el conteo y cálculo de TF-IDF
vectorizer = TfidfVectorizer()
# Aprende el vocabulario y calcula los vectores TF-IDF para los documentos
tfidf_matrix = vectorizer.fit_transform(documentos)

# Mostrar el vocabulario aprendido (palabras únicas)
# print("Vocabulario:", vectorizer.get_feature_names_out())
# Mostrar la matriz TF-IDF (filas=documentos, columnas=palabras)
# print("\nMatriz TF-IDF:\n", tfidf_matrix.toarray())

# Definir una Consulta
consulta = "cielo azul brillante"

# Convertir la Consulta a Vector TF-IDF
# Usamos el MISMO vectorizer entrenado
consulta_vec = vectorizer.transform([consulta])

# Calcular Similitud del Coseno
# Compara el vector de la consulta con TODOS los vectores de documentos
similitudes = cosine_similarity(consulta_vec, tfidf_matrix)

# El resultado es una matriz de 1xN (N=num_documentos)
# Aplanar para obtener un array simple de similitudes
similitudes_flat = similitudes.flatten()

# Obtener Ranking
# Obtener los índices de los documentos ordenados por similitud (de mayor a menor)
ranking_indices = np.argsort(similitudes_flat)[::-1]

print(f"Consulta: '{consulta}'")
print("\nRanking de Documentos (más a menos similar):")
for i, index in enumerate(ranking_indices):
    print(f"  {i+1}. Documento {index+1}: '{documentos[index]}' (Similitud: {similitudes_flat[index]:.3f})")