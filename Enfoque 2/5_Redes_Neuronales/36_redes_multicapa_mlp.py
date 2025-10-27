from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification # To generate dummy data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Generar Datos Sintéticos (Pueden ser no lineales)
X, y = make_classification(n_samples=200, n_features=20, # 20 input features
                           n_informative=10, n_redundant=5,
                           n_classes=3, # 3 output classes
                           random_state=42)

# Escalar datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)


# Definir la Arquitectura MLP
# hidden_layer_sizes=(64, 32) means:
#   - First hidden layer: 64 neurons
#   - Second hidden layer: 32 neurons
mlp_clf = MLPClassifier(
    hidden_layer_sizes=(64, 32), # Two hidden layers
    activation='relu',          # ReLU activation function
    solver='adam',              # Optimization algorithm
    max_iter=500,               # Training epochs
    random_state=42,
    early_stopping=True,        # Stop training if validation score doesn't improve
    validation_fraction=0.1,    # Use 10% of training data for validation
    verbose=False               # Set to True to see training progress
)

print("Estructura MLP definida:")
print(f"  Capas Ocultas: {mlp_clf.hidden_layer_sizes}")
print(f"  Función Activación: {mlp_clf.activation}")

# Entrenar el Modelo
print("\nEntrenando el MLP...")
mlp_clf.fit(X_train, y_train)
print("Entrenamiento completado.")

# Evaluar
y_pred = mlp_clf.predict(X_test)
precision = accuracy_score(y_test, y_pred)
print(f"\nPrecisión en el conjunto de prueba: {precision * 100:.2f}%")
print(f"Número de iteraciones realizadas: {mlp_clf.n_iter_}")