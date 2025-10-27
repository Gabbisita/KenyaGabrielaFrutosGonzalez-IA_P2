import pandas as pd

# Datos de Entrenamiento
# (Ejemplo clásico de Play Tennis)
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain', 'Sunny', 'Overcast', 'Overcast', 'Rain'],
    'Temp':    ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity':['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    'Wind':    ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    'Play':    ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
}
df = pd.DataFrame(data)

# Entrenamiento del Modelo Naïve-Bayes

def entrenar_naive_bayes(dataframe, clase_objetivo):
    """Calcula las probabilidades a priori y condicionales."""
    
    clases = dataframe[clase_objetivo].unique()
    features = dataframe.columns.drop(clase_objetivo)
    
    # a) Calcular Probabilidades a Priori P(Clase)
    prioris = dataframe[clase_objetivo].value_counts(normalize=True).to_dict()
    
    # b) Calcular Probabilidades Condicionales P(Feature | Clase)
    #    Usaremos suavizado de Laplace (alpha=1) para evitar probabilidades cero
    verosimilitudes = {} # {feature: {valor: {clase: prob}}}
    alpha = 1 # Parámetro de suavizado de Laplace

    for feature in features:
        verosimilitudes[feature] = {}
        valores_feature = dataframe[feature].unique()
        for valor in valores_feature:
            verosimilitudes[feature][valor] = {}
            for clase in clases:
                # Contar ocurrencias de (valor, clase)
                subset_clase = dataframe[dataframe[clase_objetivo] == clase]
                conteo_valor_clase = (subset_clase[feature] == valor).sum()
                
                # Calcular probabilidad con suavizado
                # P(valor|clase) = (conteo(valor,clase) + alpha) / (conteo(clase) + alpha * num_valores_feature)
                prob = (conteo_valor_clase + alpha) / (len(subset_clase) + alpha * len(valores_feature))
                verosimilitudes[feature][valor][clase] = prob
                
    return prioris, verosimilitudes

# Predicción

def predecir_naive_bayes(instancia, prioris, verosimilitudes):
    """Predice la clase para una nueva instancia."""
    
    probabilidades_posteriori = {}
    
    for clase, priori in prioris.items():
        prob_posteriori = priori # Empezar con P(Clase)
        
        # Multiplicar por P(Feature_i | Clase) para cada feature
        for feature, valor in instancia.items():
            # Si el valor no se vio en el entrenamiento para este feature,
            # podríamos ignorarlo o asignar una probabilidad muy baja.
            # Aquí lo ignoraremos por simplicidad si no está.
            if feature in verosimilitudes and valor in verosimilitudes[feature]:
                 prob_posteriori *= verosimilitudes[feature][valor][clase]
            else:
                 # Manejo simple: asumir una probabilidad pequeña o ignorar
                 # Para ser más robustos, deberíamos manejar valores desconocidos
                 # durante el entrenamiento (ej. con suavizado).
                 # Aquí simplemente no multiplicamos si el valor es nuevo.
                 pass # O asignar una prob. pequeña: prob_posteriori *= 1e-6

        probabilidades_posteriori[clase] = prob_posteriori
        
    # Elegir la clase con la probabilidad posteriori (proporcional) más alta
    return max(probabilidades_posteriori, key=probabilidades_posteriori.get)

# Ejecución
if __name__ == "__main__":
    
    CLASE_OBJETIVO = 'Play'
    
    # Entrenar el modelo
    prob_priori, prob_condicional = entrenar_naive_bayes(df, CLASE_OBJETIVO)
    
    # Crear una nueva instancia para clasificar
    instancia_nueva = {'Outlook': 'Sunny', 'Temp': 'Cool', 'Humidity': 'High', 'Wind': 'Strong'}
    
    print("Datos de Entrenamiento:")
    print(df)
    print("\nProbabilidades a Priori P(Play):")
    print(prob_priori)
    # print("\nProbabilidades Condicionales P(Feature | Play):") # Descomentar si quieres verlas todas
    # print(prob_condicional)
    
    print(f"\nPrediciendo para la instancia: {instancia_nueva}")
    
    prediccion = predecir_naive_bayes(instancia_nueva, prob_priori, prob_condicional)
    
    print(f"\nPredicción Naïve-Bayes: Play = {prediccion}") 
    # Para esta instancia, la predicción correcta suele ser 'No'