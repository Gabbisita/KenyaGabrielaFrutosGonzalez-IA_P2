# pip install Pillow

from PIL import Image, ImageFilter
import os # To check if file exists

# Definir Nombres de Archivo
archivo_entrada = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg" # Asegúrate de tener una imagen con este nombre
archivo_salida_edges = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg"

# Verificar si la imagen de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"Error: No se encontró el archivo de imagen '{archivo_entrada}'.")
    print("Por favor, coloca una imagen con ese nombre en el mismo directorio.")
    exit()

try:
    # Cargar la Imagen y Convertir a Escala de Grises
    imagen_original = Image.open(archivo_entrada)
    imagen_gris = imagen_original.convert("L") # 'L' mode is grayscale
    print(f"Imagen '{archivo_entrada}' cargada y convertida a escala de grises.")

    # Aplicar Filtro de Detección de Aristas
    # ImageFilter.FIND_EDGES aplica un filtro similar a Sobel
    imagen_bordes = imagen_gris.filter(ImageFilter.FIND_EDGES)

    # Guardar la Imagen de Bordes
    imagen_bordes.save(archivo_salida_edges)
    print(f"Imagen con bordes detectados guardada como '{archivo_salida_edges}'.")

    # (Opcional) Mostrar Imágenes 
    # imagen_original.show(title="Imagen Original")
    # imagen_bordes.show(title="Bordes Detectados (Sobel)")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'.")
except Exception as e:
    print(f"Ocurrió un error: {e}")