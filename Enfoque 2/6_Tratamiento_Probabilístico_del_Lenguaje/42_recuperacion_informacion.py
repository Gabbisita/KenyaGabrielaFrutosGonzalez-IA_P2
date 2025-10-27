import math

# PCFG Estándar
pcfg_probs = {
    ('S', ('NP', 'VP')): 1.0,
    ('VP', ('V', 'NP')): 0.7,
    ('VP', ('V',)): 0.3, # Regla añadida: Verbo intransitivo (ej. "duerme")
    ('NP', ('Det', 'N')): 0.8,
    ('NP', ('N',)): 0.2, # Regla añadida: Nombre propio o plural sin Det
    ('Det', ('the',)): 1.0, # Simplificado
    ('N', ('cat',)): 0.5,
    ('N', ('dog',)): 0.5,
    ('V', ('saw',)): 0.6, # Verbo "saw"
    ('V', ('slept',)): 0.4 # Verbo "slept"
}

# Probabilidades "Lexicalizadas"
# Estructura: (LHS, RHS): {headword: probability}
# Simulamos cómo la probabilidad de VP->V NP depende del verbo (headword V)
# y cómo NP->Det N depende del sustantivo (headword N).

lpcfg_probs = {
    # Para S -> NP VP, la cabeza es la cabeza de VP
    ('S', ('NP', 'VP')): {'saw': 1.0, 'slept': 1.0}, # No depende mucho de la cabeza aquí

    # Para VP -> V NP, la cabeza es V
    ('VP', ('V', 'NP')): {
        'saw': 0.9,  # 'saw' (ver) es muy probable que tome un objeto NP
        'slept': 0.1 # 'slept' (dormir) es poco probable que tome un objeto NP
    },
    # Para VP -> V, la cabeza es V
    ('VP', ('V',)): {
        'saw': 0.1,  # 'saw' es poco probable que esté solo
        'slept': 0.9 # 'slept' es muy probable que esté solo
    },

    # Para NP -> Det N, la cabeza es N
    ('NP', ('Det', 'N')): {
        'cat': 0.8, # 'cat' comúnmente usa determinante
        'dog': 0.8  # 'dog' comúnmente usa determinante
    },
     # Para NP -> N, la cabeza es N (asumimos que no aplica a cat/dog aquí)
     ('NP', ('N',)): {
         'cat': 0.2,
         'dog': 0.2
     },

    # Reglas terminales (la cabeza es la propia palabra)
    ('Det', ('the',)): {'the': 1.0},
    ('N', ('cat',)): {'cat': 0.5}, # Probabilidad intrínseca de la palabra
    ('N', ('dog',)): {'dog': 0.5},
    ('V', ('saw',)): {'saw': 0.6},
    ('V', ('slept',)): {'slept': 0.4}
}

# Árbol de Análisis y Palabras
# Árbol: (S (NP (Det the) (N cat)) (VP (V saw) (NP (Det the) (N dog))))
# Palabras clave (cabezas simuladas para cada nodo):
# S -> VP(saw)
# VP(saw) -> V(saw) NP(dog)
# NP(cat) -> Det(the) N(cat)
# NP(dog) -> Det(the) N(dog)
# + terminales

reglas_del_arbol = [
    (('S', ('NP', 'VP')), 'saw'), # Cabeza simulada = 'saw'
    (('NP', ('Det', 'N')), 'cat'), # Cabeza simulada = 'cat'
    (('Det', ('the',)), 'the'),
    (('N', ('cat',)), 'cat'),
    (('VP', ('V', 'NP')), 'saw'), # Cabeza simulada = 'saw'
    (('V', ('saw',)), 'saw'),
    (('NP', ('Det', 'N')), 'dog'), # Cabeza simulada = 'dog'
    (('Det', ('the',)), 'the'),
    (('N', ('dog',)), 'dog')
]

# Calcular Probabilidades

prob_pcfg = 1.0
print("Calculando con PCFG Estándar")
for (rule, headword) in reglas_del_arbol:
    prob = pcfg_probs.get(rule, 0.0)
    print(f"  Regla: {rule} -> Prob: {prob:.2f}")
    prob_pcfg *= prob

prob_lpcfg = 1.0
print("\n Calculando con LPCFG")
for (rule, headword) in reglas_del_arbol:
    # Obtener la prob. específica para esa cabeza, o 0 si no está definida
    prob = lpcfg_probs.get(rule, {}).get(headword, 0.0)
    print(f"  Regla: {rule}, Cabeza: '{headword}' -> Prob: {prob:.2f}")
    prob_lpcfg *= prob

print(f"\nProbabilidad PCFG del árbol: {prob_pcfg:.6f}")
print(f"Probabilidad LPCFG (simulada) del árbol: {prob_lpcfg:.6f}")

print("En este caso, como 'saw' prefiere tener un objeto, la regla VP -> V NP tiene")
print("mayor probabilidad en la LPCFG que en la PCFG estándar.")