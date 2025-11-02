# Definimos una distribución de probabilidad para la variable 'Clima'
# P(Clima)
distribucion_clima = {
    'Soleado': 0.6,
    'Nublado': 0.3,
    'Lluvioso': 0.1
}

print("Distribución de Probabilidad:")
for valor, probabilidad in distribucion_clima.items():
    print(f"  P(Clima={valor}) = {probabilidad:.2f}")

# Verificar que las probabilidades suman 1
suma_probabilidades = sum(distribucion_clima.values())

print(f"\nSuma de las probabilidades: {suma_probabilidades:.2f}")

if abs(suma_probabilidades - 1.0) < 1e-9:
    print("La distribución es válida (las probabilidades suman 1).")
else:
    print("¡Error! La distribución no es válida (las probabilidades no suman 1).")

# Esta distribución podría representar nuestra probabilidad a priori del clima,
# o podría ser una probabilidad condicionada P(Clima | Evidencia).