# pip install Pillow

from PIL import Image, ImageFilter
import os # To check if file exists

# Definir Nombres de Archivo
archivo_entrada = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg" # Asegúrate de tener una imagen con este nombre
archivo_salida_blur = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg"

# Verificar si la imagen de entrada existe
if not os.path.exists(archivo_entrada):
    print(f"Error: No se encontró el archivo de imagen '{archivo_entrada}'.")
    print("Por favor, coloca una imagen con ese nombre en el mismo directorio.")
    exit()

try:
    # Cargar la Imagen
    imagen_original = Image.open(archivo_entrada)
    print(f"Imagen '{archivo_entrada}' cargada.")
    print(f"  Formato: {imagen_original.format}, Modo: {imagen_original.mode}, Tamaño: {imagen_original.size}")

    # Aplicar un Filtro (Box Blur)
    # ImageFilter.BLUR es un filtro predefinido que promedia una vecindad 3x3
    # Para un blur más fuerte, puedes usar BoxBlur(radius)
    imagen_blur = imagen_original.filter(ImageFilter.BLUR)
    # Ejemplo de blur más fuerte:
    # imagen_blur_fuerte = imagen_original.filter(ImageFilter.BoxBlur(radius=5))

    # Guardar la Imagen Filtrada
    imagen_blur.save(archivo_salida_blur)
    print(f"Imagen con filtro blur guardada como '{archivo_salida_blur}'.")

    # (Opcional) Mostrar Imágenes
    # imagen_original.show(title="Imagen Original")
    # imagen_blur.show(title="Imagen con Blur")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'.")
except Exception as e:
    print(f"Ocurrió un error: {e}")