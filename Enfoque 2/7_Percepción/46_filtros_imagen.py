
from PIL import Image, ImageDraw

# Definir Parámetros de la Imagen
ancho_imagen = 200
alto_imagen = 150
color_fondo = (200, 200, 255) # Un azul claro (RGB)
color_forma = (255, 0, 0)     # Rojo (RGB)
nombre_archivo = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg"

# Crear una Imagen Nueva
# Creamos una imagen en blanco con el tamaño y color de fondo especificados
imagen = Image.new('RGB', (ancho_imagen, alto_imagen), color_fondo)

# Preparar para Dibujar
# Creamos un objeto 'Draw' que nos permite dibujar sobre la imagen
dibujo = ImageDraw.Draw(imagen)

# Dibujar una Forma Simple
# Dibujamos un rectángulo rojo en el centro
# Coordenadas: [x0, y0, x1, y1] (esquina superior izquierda, esquina inferior derecha)
x0 = ancho_imagen // 4
y0 = alto_imagen // 4
x1 = ancho_imagen * 3 // 4
y1 = alto_imagen * 3 // 4
dibujo.rectangle([x0, y0, x1, y1], fill=color_forma, outline=(0, 0, 0)) # Relleno rojo, borde negro

# Guardar la Imagen
try:
    imagen.save(nombre_archivo)
    print(f"Imagen '{nombre_archivo}' creada y guardada exitosamente.")
    print("Puedes abrir el archivo para ver el resultado.")
except Exception as e:
    print(f"Error al guardar la imagen: {e}")

# (Opcional) Mostrar la Imagen
# Descomenta las siguientes líneas si quieres que Python intente abrir la imagen
# try:
#     imagen.show()
# except Exception as e:
#     print(f"No se pudo mostrar la imagen automáticamente: {e}")