# ======================================================================
# DEFINICIÓN DEL MUNDO (PROBABILIDADES Y UTILIDADES)
# ======================================================================

# Tabla de Utilidad U(Decisión, Resultado)
utilidad_tabla = {
    'Llevar_Paraguas_Si': {'Lluvia_Real_Si': 70, 'Lluvia_Real_No': 20},
    'Llevar_Paraguas_No': {'Lluvia_Real_Si': -100, 'Lluvia_Real_No': 100}
}

# Probabilidades condicionales P(Lluvia | Pronóstico)
P_Lluvia_dado_Pronostico = {
    'Lluvioso': {'Lluvia_Real_Si': 0.7, 'Lluvia_Real_No': 0.3},
    'Soleado':  {'Lluvia_Real_Si': 0.2, 'Lluvia_Real_No': 0.8}
}

# Probabilidades a priori (generales)
P_Pronostico = {'Lluvioso': 0.4, 'Soleado': 0.6}
P_Lluvia_General = {'Lluvia_Real_Si': 0.4, 'Lluvia_Real_No': 0.6} # Ejemplo

# ======================================================================
# CÁLCULO DEL VALOR DE LA INFORMACIÓN
# ======================================================================

def calcular_utilidad_esperada(decision, probabilidades, utilidades):
    """Función genérica para calcular la UE de una decisión."""
    ue = 0
    for resultado, prob in probabilidades.items():
        ue += prob * utilidades[decision][resultado]
    return ue

def calcular_vpi():
    """Calcula el Valor de la Información Perfecta (VPI) para el 'Pronóstico'."""
    decisiones = ['Llevar_Paraguas_Si', 'Llevar_Paraguas_No']
    
    # --- PASO 1: Calcular la MEU *sin* la información del pronóstico ---
    ue_sin_info = []
    for decision in decisiones:
        ue = calcular_utilidad_esperada(decision, P_Lluvia_General, utilidad_tabla)
        ue_sin_info.append(ue)
    
    meu_sin_info = max(ue_sin_info)
    
    # --- PASO 2 y 3: Calcular la MEU *con* la información del pronóstico ---
    # Para cada posible valor de la nueva información (cada pronóstico)...
    meu_con_info_ponderada = 0
    for pronostico, prob_pronostico in P_Pronostico.items():
        # ...calculamos cuál sería la mejor decisión y su utilidad esperada.
        ue_con_info_especifica = []
        probabilidades_resultado = P_Lluvia_dado_Pronostico[pronostico]
        for decision in decisiones:
            ue = calcular_utilidad_esperada(decision, probabilidades_resultado, utilidad_tabla)
            ue_con_info_especifica.append(ue)
        
        # La mejor utilidad que podemos obtener si conocemos ese pronóstico
        meu_para_ese_pronostico = max(ue_con_info_especifica)
        
        # Sumamos al promedio ponderado
        meu_con_info_ponderada += prob_pronostico * meu_para_ese_pronostico

    # --- PASO 4: Calcular el VPI ---
    vpi = meu_con_info_ponderada - meu_sin_info
    
    return meu_sin_info, meu_con_info_ponderada, vpi

# --- Bloque principal ---
if __name__ == "__main__":
    
    print("Calculando el Valor de la Información Perfecta (VPI) para saber el 'Pronóstico'...")
    print("-" * 75)
    
    meu_sin, meu_con, vpi = calcular_vpi()
    
    print(f"Paso 1: Máxima Utilidad Esperada SIN información (decidiendo a ciegas) = {meu_sin:.2f}")
    print(f"Paso 3: Utilidad Esperada promedio CON información (sabiendo el pronóstico) = {meu_con:.2f}")
    print("-" * 75)
    print(f"Paso 4: El Valor de la Información Perfecta (VPI) es la diferencia = {vpi:.2f}")
    
    print("\nConclusión:")
    print(f"Vale la pena 'pagar' hasta {vpi:.2f} unidades de utilidad para obtener la información del pronóstico antes de decidir.")