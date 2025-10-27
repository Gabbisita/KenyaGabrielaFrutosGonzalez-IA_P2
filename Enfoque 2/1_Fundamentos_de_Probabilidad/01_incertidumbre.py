# Definimos nuestras creencias iniciales (probabilidades a priori)
# sobre el clima de mañana.

# P(Clima = Soleado), P(Clima = Nublado), P(Clima = Lluvioso)
prob_clima_a_priori = {
    'Soleado': 0.6,   # Creemos que es más probable que esté soleado
    'Nublado': 0.3,
    'Lluvioso': 0.1    # Menos probable que llueva
}

# Verificar que las probabilidades suman 1 (o muy cerca debido a decimales)
total_prob = sum(prob_clima_a_priori.values())
print(f"Probabilidades a priori definidas:")
for clima, prob in prob_clima_a_priori.items():
    # Esta línea debe tener 4 espacios al inicio
    print(f"  P(Clima={clima}) = {prob:.2f}")

print(f"\nSuma total de probabilidades: {total_prob:.2f}")
clima_mas_probable_a_priori = max(prob_clima_a_priori, key=prob_clima_a_priori.get)
print(f"\nBasado solo en la probabilidad a priori, el clima más probable es: {clima_mas_probable_a_priori}")