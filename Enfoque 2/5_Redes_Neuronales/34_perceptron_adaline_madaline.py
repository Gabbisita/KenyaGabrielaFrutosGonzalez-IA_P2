import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification # Generate sample data
from sklearn.linear_model import Perceptron      # Perceptron model
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler # Scaling helps convergence

# Generar Datos Linealmente Separables
X, y = make_classification(n_samples=100, n_features=2, n_informative=2,
                           n_redundant=0, n_repeated=0, n_classes=2,
                           n_clusters_per_class=1,
                           class_sep=1.5, # Ensure good separation
                           random_state=42)

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Entrenar el Modelo Perceptrón
# tol: Criterio de parada
# max_iter: Número máximo de pasadas sobre los datos (épocas)
perceptron_clf = Perceptron(max_iter=100, tol=1e-3, random_state=42)
perceptron_clf.fit(X_train, y_train)

# Evaluar
y_pred = perceptron_clf.predict(X_test)
precision = accuracy_score(y_test, y_pred)
print(f"Modelo Perceptrón Simple")
print(f"Precisión en el conjunto de prueba: {precision * 100:.2f}%")
print(f"Número de iteraciones hasta converger: {perceptron_clf.n_iter_}")

# Visualizar Límite de Decisión
def plot_decision_boundary(clf, X, y, title):
    h = .02 # step size
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    plt.title(title)
    plt.xlabel('Característica 1 (Escalada)')
    plt.ylabel('Característica 2 (Escalada)')
    plt.grid(True)

plt.figure(figsize=(8, 6))
plot_decision_boundary(perceptron_clf, X_scaled, y, f'Límite de Decisión del Perceptrón - Precisión: {precision*100:.1f}%')
plt.show()