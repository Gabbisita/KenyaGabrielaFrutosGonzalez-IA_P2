from sklearn.neural_network import MLPClassifier

# Definir la Arquitectura de la Red

# hidden_layer_sizes define el número de neuronas en cada capa oculta.
# (100, 50, 20) significa:
#   - Capa oculta 1: 100 neuronas
#   - Capa oculta 2: 50 neuronas
#   - Capa oculta 3: 20 neuronas
# Tener múltiples capas ocultas es lo que la hace "profunda".

# activation especifica la función de activación (ej. 'relu' es común)
# solver es el algoritmo de optimización (ej. 'adam')
# max_iter es el número de épocas de entrenamiento

# Creamos una instancia del clasificador MLP
# (Imagina que tenemos datos con N características de entrada
# y queremos clasificar en M clases de salida)
red_profunda_simple = MLPClassifier(
    hidden_layer_sizes=(100, 50, 20), # Tres capas ocultas
    activation='relu',
    solver='adam',
    max_iter=500, # Número de pasadas de entrenamiento
    random_state=42,
    verbose=True # Para ver el progreso del entrenamiento (si lo hubiera)
)

# (Paso Faltante) Entrenamiento
# Aquí necesitaríamos datos de entrenamiento (X_train, y_train)
# y llamaríamos a red_profunda_simple.fit(X_train, y_train)
# Este paso es donde la red "aprende".

# (Paso Faltante) Predicción
# Después del entrenamiento, usaríamos la red para predecir en nuevos datos
# predicciones = red_profunda_simple.predict(X_nuevos)

print("Se ha definido la estructura de una red neuronal profunda simple (MLP).")
print("Capas ocultas:", red_profunda_simple.hidden_layer_sizes)
print("Función de activación:", red_profunda_simple.activation)