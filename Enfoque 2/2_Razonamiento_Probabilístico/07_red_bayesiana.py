# Representación de una Red Bayesiana simple:
#   Nublado -> Lluvia
#   Nublado -> Aspersor
#   Lluvia -> Pasto Mojado
#   Aspersor -> Pasto Mojado

# 1. Definir la Estructura (Nodos y sus Padres)
estructura_bn = {
    'Nublado': ['Lluvia', 'Aspersor'],
    'Aspersor': ['Nublado'],
    'Lluvia': ['Nublado'],
    'Pasto Mojado': ['Lluvia', 'Aspersor']
}

# 2. Definir los Parámetros (Tablas de Probabilidad Condicional - CPTs)

# P(Nublado) - Nodo raíz
cpt_nublado = {
    True: 0.5,
    False: 0.5
}

# P(Aspersor | Nublado)
cpt_aspersor = {
    # Si Nublado = True
    (True,): {True: 0.1, False: 0.9}, # Es menos probable que se prenda si está nublado
    # Si Nublado = False
    (False,): {True: 0.5, False: 0.5} # Más probable si no está nublado
}

# P(Lluvia | Nublado)
cpt_lluvia = {
    # Si Nublado = True
    (True,): {True: 0.8, False: 0.2}, # Muy probable que llueva si está nublado
    # Si Nublado = False
    (False,): {True: 0.2, False: 0.8}  # Poco probable si no está nublado
}

# P(Pasto Mojado | Lluvia, Aspersor)
cpt_pasto_mojado = {
    # Lluvia=T, Aspersor=T
    (True, True): {True: 0.99, False: 0.01}, # Casi seguro mojado
    # Lluvia=T, Aspersor=F
    (True, False): {True: 0.90, False: 0.10}, # Probable mojado (por lluvia)
    # Lluvia=F, Aspersor=T
    (False, True): {True: 0.90, False: 0.10}, # Probable mojado (por aspersor)
    # Lluvia=F, Aspersor=F
    (False, False): {True: 0.00, False: 1.00} # Imposible mojado (en este modelo simple)
}

# Juntar las CPTs en un diccionario
cpts_bn = {
    'Nublado': cpt_nublado,
    'Aspersor': cpt_aspersor,
    'Lluvia': cpt_lluvia,
    'Pasto Mojado': cpt_pasto_mojado
}

# Ahora tendríamos la Red Bayesiana definida por 'estructura_bn' y 'cpts_bn'.
# Los siguientes algoritmos (Inferencia por Enumeración, etc.) usarían
# esta representación para responder preguntas.

print("Representación de la Red Bayesiana (estructura y CPTs) definida.")
print("\nEstructura (Nodo: [Padres]):")
for nodo, padres in estructura_bn.items():
    print(f"  {nodo}: {padres}")

# Podríamos imprimir las CPTs también si quisiéramos verificar
# print("\nCPTs:")
# for nodo, cpt in cpts_bn.items():
#     print(f"  CPT para {nodo}: {cpt}")