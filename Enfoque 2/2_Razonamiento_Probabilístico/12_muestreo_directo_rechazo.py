import random

estructura_bn = {
    'Nublado': [], 'Aspersor': ['Nublado'], 'Lluvia': ['Nublado'],
    'Pasto Mojado': ['Lluvia', 'Aspersor']
}
cpts_bn = {
    'Nublado': {True: 0.5, False: 0.5},
    'Aspersor': {(True,): {True: 0.1, False: 0.9}, (False,): {True: 0.5, False: 0.5}},
    'Lluvia': {(True,): {True: 0.8, False: 0.2}, (False,): {True: 0.2, False: 0.8}},
    'Pasto Mojado': {
        (True, True): {True: 0.99, False: 0.01}, (True, False): {True: 0.90, False: 0.10},
        (False, True): {True: 0.90, False: 0.10}, (False, False): {True: 0.00, False: 1.00}
    }
}
variables_bn = ['Nublado', 'Aspersor', 'Lluvia', 'Pasto Mojado'] # Orden topológico

# Funciones de Muestreo
def elegir_valor_ponderado(distribucion):
    """Elige un valor (True/False) basado en sus probabilidades."""
    valor_aleatorio = random.random()
    suma_acumulada = 0
    for valor, prob in distribucion.items():
        suma_acumulada += prob
        if valor_aleatorio < suma_acumulada:
            return valor
    # Por si acaso hay errores de redondeo, devolver el último
    return list(distribucion.keys())[-1]

def muestreo_directo_una_muestra(estructura, cpts, vars_ordenadas):
    """Genera una única muestra completa de la Red Bayesiana."""
    muestra = {}
    for variable in vars_ordenadas:
        padres = estructura[variable]
        valores_padres = tuple(muestra[p] for p in padres)
        
        cpt = cpts[variable]
        
        if not padres: # Nodo raíz
            distribucion = cpt
        else:
            distribucion = cpt[valores_padres]
            
        valor_elegido = elegir_valor_ponderado(distribucion)
        muestra[variable] = valor_elegido
    return muestra

def muestreo_por_rechazo(query_var, evidencia, estructura, cpts, vars_ordenadas, num_muestras):
    """
    Estima P(Query | Evidencia) usando Muestreo por Rechazo.
    """
    contador_query = {True: 0, False: 0} # Contadores para Query=T y Query=F
    contador_evidencia_ok = 0 # Cuántas muestras coinciden con la evidencia

    for _ in range(num_muestras):
        # 1. Generar una muestra
        muestra = muestreo_directo_una_muestra(estructura, cpts, vars_ordenadas)
        
        # 2. Verificar si coincide con la evidencia
        coincide = True
        for var_ev, val_ev in evidencia.items():
            if muestra[var_ev] != val_ev:
                coincide = False
                break
        
        # 3. Si coincide, contarla
        if coincide:
            contador_evidencia_ok += 1
            valor_query_en_muestra = muestra[query_var]
            contador_query[valor_query_en_muestra] += 1
            
    # 4. Calcular la probabilidad condicionada estimada
    if contador_evidencia_ok == 0:
        print(f"ADVERTENCIA: Ninguna muestra coincidió con la evidencia después de {num_muestras} intentos.")
        return {True: 0.0, False: 0.0} # Evitar división por cero

    prob_estimada = {
        valor: count / contador_evidencia_ok 
        for valor, count in contador_query.items()
    }
    
    print(f"(Se generaron {num_muestras} muestras, {contador_evidencia_ok} coincidieron con la evidencia)")
    return prob_estimada

if __name__ == "__main__":
    
    NUM_MUESTRAS = 10000
    
    # --- Ejemplo 1: Muestreo Directo para P(Pasto Mojado) ---
    print(f"--- Estimando P(Pasto Mojado) con {NUM_MUESTRAS} muestras (Muestreo Directo) ---")
    conteo_pasto_mojado = 0
    for _ in range(NUM_MUESTRAS):
        muestra = muestreo_directo_una_muestra(estructura_bn, cpts_bn, variables_bn)
        if muestra['Pasto Mojado']:
            conteo_pasto_mojado += 1
    prob_pasto_mojado = conteo_pasto_mojado / NUM_MUESTRAS
    print(f"  P(Pasto Mojado = True) ≈ {prob_pasto_mojado:.3f}")
    
    print("\n" + "="*50 + "\n")

    # Ejemplo 2: Muestreo por Rechazo para P(Lluvia | Pasto Mojado = True)
    query = 'Lluvia'
    evidencia = {'Pasto Mojado': True}
    print(f" Estimando P({query} | Pasto Mojado = True) con {NUM_MUESTRAS} muestras (Muestreo por Rechazo) ")
    
    distribucion_rechazo = muestreo_por_rechazo(query, evidencia, estructura_bn, cpts_bn, variables_bn, NUM_MUESTRAS)
    
    print("\nDistribución Condicional Estimada:")
    for valor, prob in distribucion_rechazo.items():
        print(f"  P({query}={valor} | Pasto Mojado = True) ≈ {prob:.3f}")

    # (El resultado exacto de P(L=T|PM=T) es ~0.430)