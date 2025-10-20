def calcular_utilidad_esperada(opcion, funcion_utilidad):
    """
    Calcula la Utilidad Esperada (UE) para una sola opción.
    UE = Suma de (probabilidad_de_resultado * utilidad_de_resultado)
    """
    utilidad_total = 0
    for resultado in opcion['resultados']:
        nombre_resultado = resultado['nombre']
        probabilidad = resultado['probabilidad']
        utilidad = funcion_utilidad[nombre_resultado]
        
        utilidad_total += probabilidad * utilidad
        
    return utilidad_total

def tomar_decision_racional(opciones, funcion_utilidad):
    """
    Evalúa todas las opciones y elige la que maximiza la Utilidad Esperada.
    """
    mejor_opcion = None
    max_utilidad_esperada = -float('inf')
    
    # Evaluar cada opción disponible
    for opcion in opciones:
        utilidad_esperada = calcular_utilidad_esperada(opcion, funcion_utilidad)
        print(f"  -> Utilidad Esperada para '{opcion['nombre']}': {utilidad_esperada:.2f}")
        
        if utilidad_esperada > max_utilidad_esperada:
            max_utilidad_esperada = utilidad_esperada
            mejor_opcion = opcion
            
    return mejor_opcion, max_utilidad_esperada

if __name__ == "__main__":

    # 1. Definir la Función de Utilidad del agente.
    #    Mide cuánta "felicidad" le da cada resultado.
    funcion_utilidad = {
        'tacos_increibles': 150,
        'tacos_buenos': 80,
        'tacos_malos': -20
    }

    # 2. Definir las Opciones y sus resultados inciertos.
    opciones = [
        {
            'nombre': 'Taquería Nueva',
            'resultados': [
                {'nombre': 'tacos_increibles', 'probabilidad': 0.60},
                {'nombre': 'tacos_malos', 'probabilidad': 0.40}
            ]
        },
        {
            'nombre': 'Puesto de Siempre',
            'resultados': [
                {'nombre': 'tacos_buenos', 'probabilidad': 1.0}
            ]
        },
        {
            'nombre': 'Probar un Food Truck',
            'resultados': [
                {'nombre': 'tacos_increibles', 'probabilidad': 0.20},
                {'nombre': 'tacos_buenos', 'probabilidad': 0.50},
                {'nombre': 'tacos_malos', 'probabilidad': 0.30}
            ]
        }
    ]

    print("El agente está decidiendo dónde cenar...")
    print("Calculando la Utilidad Esperada para cada opción...")
    
    # 3. El agente toma la decisión.
    decision, valor = tomar_decision_racional(opciones, funcion_utilidad)
    
    print("-" * 40)
    print(f"La decisión racional es: '{decision['nombre']}'")
    print(f"Ofrece una utilidad esperada de: {valor:.2f}")