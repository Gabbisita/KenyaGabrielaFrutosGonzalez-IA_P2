import sys
try:
    import spacy
except ImportError:
    print("ERROR: La librería 'spacy' no está instalada.")
    print("Por favor, instálala ejecutando: pip install spacy")
    sys.exit()

# Cargar el Modelo de Lenguaje Español
MODELO_ES = "es_core_news_sm"
try:
    nlp = spacy.load(MODELO_ES)
except OSError:
    print(f"ERROR: Modelo '{MODELO_ES}' no encontrado.")
    print(f"Por favor, descárgalo ejecutando: python -m spacy download {MODELO_ES}")
    sys.exit()

# Texto de Ejemplo
texto = "Apple está buscando comprar una startup del Reino Unido por mil millones de dólares según fuentes en Londres."

print(f"Texto original:\n{texto}\n")

# Procesar el Texto con spaCy
doc = nlp(texto)

# Extraer y Mostrar Entidades Nombradas
print("Entidades Nombradas encontradas (NER):")
if doc.ents:
    for entidad in doc.ents:
        print(f"  -> Texto: '{entidad.text}', Etiqueta: {entidad.label_}")
        # Etiquetas comunes: ORG, GPE (Lugar), MONEY, LOC, PER (Persona)
else:
    print("  No se encontraron entidades nombradas.")