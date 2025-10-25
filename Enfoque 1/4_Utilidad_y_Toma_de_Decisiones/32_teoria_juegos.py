def encontrar_equilibrios_nash(pagos):
    """
    Encuentra los equilibrios de Nash en un juego de 2 jugadores con 2 acciones
    por fuerza bruta.

    """
    acciones_A = list(pagos['A'].keys())
    acciones_B = list(pagos['A'][acciones_A[0]].keys())
    
    equilibrios = []
    
    # Iterar sobre cada posible "perfil de estrategia" (combinación de jugadas)
    for accion_A in acciones_A:
        for accion_B in acciones_B:
            
            # Comprobar si A tiene incentivo para desviarse
            pago_actual_A = pagos['A'][accion_A][accion_B]
            
            incentivo_A = False
            for otra_accion_A in acciones_A:
                if otra_accion_A == accion_A:
                    continue
                # A cambia su jugada
                pago_desviado_A = pagos['A'][otra_accion_A][accion_B]
                if pago_desviado_A > pago_actual_A:
                    incentivo_A = True # ¡A quiere cambiar!
                    break
            
            # Comprobar si B tiene incentivo para desviarse
            # Asumimos que la jugada de A está fija (accion_A)
            pago_actual_B = pagos['B'][accion_A][accion_B]
            
            incentivo_B = False
            for otra_accion_B in acciones_B:
                if otra_accion_B == accion_B:
                    continue
                # B cambia su jugada
                pago_desviado_B = pagos['B'][accion_A][otra_accion_B]
                if pago_desviado_B > pago_actual_B:
                    incentivo_B = True # ¡B quiere cambiar!
                    break
            
            # Conclusión
            # Si NINGÚN jugador tiene incentivo para cambiar, es un Equilibrio de Nash
            if not incentivo_A and not incentivo_B:
                equilibrios.append((accion_A, accion_B))
                
    return equilibrios

if __name__ == "__main__":
    
    # Definición del Dilema del Prisionero
    # (Usamos números positivos para utilidad, 0 es mejor que -10)
    acciones = ['Cooperar', 'Traicionar']
    
    # Pagos (Utilidades) para cada jugador
    pagos_prisionero = {
        'A': { # Pagos de A
            'Cooperar': {'Cooperar': -1, 'Traicionar': -10},
            'Traicionar': {'Cooperar': 0, 'Traicionar': -5}
        },
        'B': { # Pagos de B (matriz transpuesta)
            'Cooperar': {'Cooperar': -1, 'Traicionar': 0},
            'Traicionar': {'Cooperar': -10, 'Traicionar': -5}
        }
    }

    print("1. Juego: Dilema del Prisionero")
    equilibrios_prisionero = encontrar_equilibrios_nash(pagos_prisionero)
    print(f"Acciones posibles: {acciones}")
    print(f"Equilibrios de Nash encontrados: {equilibrios_prisionero}")

    print("\n2. Juego: Batalla de los Sexos")
    # Un juego con dos equilibrios
    pagos_batalla = {
        'A': { # Pagos de A
            'Ópera': {'Ópera': 2, 'Fútbol': 1},
            'Fútbol': {'Ópera': 1, 'Fútbol': 2}
        },
        'B': { # Pagos de B
            'Ópera': {'Ópera': 1, 'Fútbol': 2},
            'Fútbol': {'Ópera': 1, 'Fútbol': 1}
        }
    }
    equilibrios_batalla = encontrar_equilibrios_nash(pagos_batalla)
    print(f"Acciones posibles: {['Ópera', 'Fútbol']}")
    print(f"Equilibrios de Nash encontrados: {equilibrios_batalla}")