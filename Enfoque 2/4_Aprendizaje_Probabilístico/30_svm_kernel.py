import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons # Para generar datos no separables linealmente
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC # Support Vector Classifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler # Es bueno escalar los datos para SVM

# Generar Datos Sintéticos (Forma de Lunas)
X, y = make_moons(n_samples=200, noise=0.15, random_state=42)

# Escalar los datos (importante para SVM)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Entrenar el Modelo SVM
# Usamos el kernel RBF (predeterminado), que es bueno para datos no lineales
# C es el parámetro de regularización (controla el trade-off entre margen y error)
svm_clf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_clf.fit(X_train, y_train)

# Realizar Predicciones
y_pred = svm_clf.predict(X_test)

# Evaluar el Rendimiento
precision = accuracy_score(y_test, y_pred)
print(f"Clasificador SVM con kernel RBF")
print(f"Precisión en el conjunto de prueba: {precision * 100:.2f}%")

# Visualizar el Límite de Decisión
def plot_decision_boundary(clf, X, y, title):
    h = .02 # step size in the mesh
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # Predecir para cada punto en la malla
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    plt.title(title)
    plt.xlabel('Característica 1 (Escalada)')
    plt.ylabel('Característica 2 (Escalada)')
    plt.grid(True)


plt.figure(figsize=(8, 6))
plot_decision_boundary(svm_clf, X_scaled, y, f'Límite de Decisión SVM (RBF) - Precisión: {precision*100:.1f}%')
plt.show()