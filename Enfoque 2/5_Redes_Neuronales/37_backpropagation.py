# (Reutilizando el código del MLP de #36)
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Datos
X, y = make_classification(n_samples=200, n_features=20, n_informative=10, n_redundant=5, n_classes=3, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Definir MLP
mlp_clf = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam', # 'adam' is an efficient optimizer that USES GRADIENTS calculated by backpropagation
    max_iter=500,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1,
    verbose=False
)

# Entrenamiento
print("Entrenando el MLP...")
# ¡LA MAGIA DE BACKPROPAGATION OCURRE DENTRO DE .fit()!
mlp_clf.fit(X_train, y_train)
print("Entrenamiento completado.")

# Evaluación
y_pred = mlp_clf.predict(X_test)
precision = accuracy_score(y_test, y_pred)
print(f"\nPrecisión: {precision * 100:.2f}%")
print(f"Iteraciones: {mlp_clf.n_iter_}")