import random

def mostrar_tablero(tablero):
    """Muestra el tablero de ajedrez con las reinas."""
    n = len(tablero)
    for fila in range(n):
        linea = ""
        for col in range(n):
            linea += "Q " if tablero[col] == fila else ". "
        print(linea)

def contar_conflictos(tablero):
    """Calcula el número total de pares de reinas que se atacan."""
    n = len(tablero)
    conflictos = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Conflicto en la misma fila
            if tablero[i] == tablero[j]:
                conflictos += 1
            # Conflicto en la diagonal
            if abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1
    return conflictos

def min_conflictos(n, max_iteraciones=1000, seed=None):
    """
    Resuelve el problema de las N-Reinas usando el algoritmo de Mínimos-Conflictos.

    Args:
        n (int): El número de reinas y el tamaño del tablero.
        max_iteraciones (int): Límite de iteraciones de reparación.
        seed (int|None): Semilla aleatoria opcional para reproducibilidad.
    Returns:
        list: Lista de longitud n donde el índice es la columna y el valor la fila.
    """
    if seed is not None:
        random.seed(seed)

    # 1. Inicialización: Generar una asignación completa y aleatoria.
    tablero = [random.randint(0, n - 1) for _ in range(n)]

    print("Tablero inicial (aleatorio):")
    mostrar_tablero(tablero)
    print(f"Conflictos iniciales: {contar_conflictos(tablero)}")
    print("-" * 20)

    # 2. Bucle principal de reparación.
    for i in range(max_iteraciones):
        conflictos_actuales = contar_conflictos(tablero)
        # 3. Comprobar si ya es una solución.
        if conflictos_actuales == 0:
            print(f"¡Solución encontrada en la iteración {i}!")
            return tablero

        # 4. Seleccionar una reina en conflicto al azar.
        columnas_en_conflicto = []
        for col in range(n):
            for otro_col in range(col + 1, n):
                if (tablero[col] == tablero[otro_col] or
                    abs(tablero[col] - tablero[otro_col]) == abs(col - otro_col)):
                    columnas_en_conflicto.append(col)
                    break # Pasamos a la siguiente columna

        # Si por alguna razón no hay columnas detectadas en conflicto,
        # reiniciamos aleatoriamente el tablero y continuamos.
        if not columnas_en_conflicto:
            tablero = [random.randint(0, n - 1) for _ in range(n)]
            continue

        col_a_mover = random.choice(columnas_en_conflicto)

        # 5. Minimizar conflictos para esa reina.
        mejor_fila = tablero[col_a_mover]
        mejor_conf = contar_conflictos(tablero)

        fila_original = tablero[col_a_mover]

        for fila_nueva in range(n):
            tablero[col_a_mover] = fila_nueva
            num_conflictos = contar_conflictos(tablero)
            if num_conflictos < mejor_conf:
                mejor_conf = num_conflictos
                mejor_fila = fila_nueva

        # Restaurar el tablero para la decisión final
        tablero[col_a_mover] = mejor_fila

    print("No se encontró solución en el número máximo de iteraciones.")
    return tablero


if __name__ == "__main__":
    N_REINAS = 8 # Puedes probar con 4, 8, 16, etc.
    solucion = min_conflictos(N_REINAS, max_iteraciones=1000, seed=42)

    print("-" * 20)
    print("Tablero final:")
    mostrar_tablero(solucion)
    print(f"Conflictos finales: {contar_conflictos(solucion)}")