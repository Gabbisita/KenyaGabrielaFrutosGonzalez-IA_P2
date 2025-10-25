# Definir las Probabilidades Conocidas

# P(H) - Probabilidad a Priori de la enfermedad
# La enfermedad es rara, afecta al 1% de la población.
p_enfermedad_priori = 0.01

# P(E|H) - Probabilidad de dar positivo SI tienes la enfermedad (Sensibilidad de la prueba)
# La prueba detecta correctamente la enfermedad el 90% de las veces.
p_positivo_dado_enfermedad = 0.90

# P(E|¬H) - Probabilidad de dar positivo SI NO tienes la enfermedad (Tasa de Falsos Positivos)
# La prueba da un falso positivo el 8% de las veces.
p_positivo_dado_sano = 0.08

# Aplicar la Regla de Bayes 
# P(H|E) = [ P(E|H) * P(H) ] / P(E)

# Calculamos el Numerador: P(Positivo | Enfermedad) * P(Enfermedad)
numerador = p_positivo_dado_enfermedad * p_enfermedad_priori

# Calculamos el Denominador P(E) usando la Ley de Probabilidad Total:
# P(Positivo) = P(Positivo|Enfermo)*P(Enfermo) + P(Positivo|Sano)*P(Sano)
p_sano_priori = 1 - p_enfermedad_priori
p_positivo_total = (p_positivo_dado_enfermedad * p_enfermedad_priori) + \
                   (p_positivo_dado_sano * p_sano_priori)

# Calcular la Probabilidad a Posteriori
p_enfermedad_dado_positivo = numerador / p_positivo_total

# Resultados
print("Probabilidades Iniciales")
print(f"P(Enfermedad) = {p_enfermedad_priori:.3f} (A priori)")
print(f"P(Positivo | Enfermedad) = {p_positivo_dado_enfermedad:.2f} (Sensibilidad)")
print(f"P(Positivo | Sano) = {p_positivo_dado_sano:.2f} (Falsos Positivos)")

print("\nAplicando Regla de Bayes")
print(f"P(Positivo) = {p_positivo_total:.4f} (Probabilidad total de dar positivo)")
print(f"P(Enfermedad | Positivo) = {p_enfermedad_dado_positivo:.3f} (A posteriori)")

print("\nConclusión")
print(f"A pesar de dar positivo en la prueba, la probabilidad de tener realmente")
print(f"la enfermedad rara es solo del {p_enfermedad_dado_positivo*100:.1f}%.")
print("Esto se debe a que la enfermedad es muy rara (baja probabilidad a priori).")