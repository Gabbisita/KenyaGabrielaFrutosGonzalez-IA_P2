# pip install torch torchvision Pillow requests

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests # To download ImageNet labels
import os

# Definir Archivo y Cargar Modelo Pre-entrenado
archivo_entrada = "/workspaces/KenyaGabrielaFrutosGonzalez-IA_P2/Enfoque 2/7_Percepción/Gato.jpg"
if not os.path.exists(archivo_entrada):
    print(f"Error: No se encontró '{archivo_entrada}'. Coloca una imagen.")
    exit()

# Cargar un modelo ResNet pre-entrenado en ImageNet
# 'weights=models.ResNet50_Weights.DEFAULT' usa los pesos más recientes
try:
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.eval() # Poner el modelo en modo de evaluación (importante)
    print("Modelo ResNet50 pre-entrenado cargado.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    print("Asegúrate de tener conexión a internet la primera vez.")
    exit()

# Preprocesar la Imagen
# Las redes pre-entrenadas esperan imágenes de un tamaño específico
# y normalizadas de cierta manera.
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

try:
    img = Image.open(archivo_entrada).convert('RGB') # Asegurar que sea RGB
    img_t = preprocess(img)
    # Añadir una dimensión 'batch' (el modelo espera lotes de imágenes)
    batch_t = torch.unsqueeze(img_t, 0)
    print("Imagen preprocesada.")
except FileNotFoundError:
    print(f"Error: No se pudo encontrar '{archivo_entrada}'.")
    exit()
except Exception as e:
    print(f"Error al procesar la imagen: {e}")
    exit()

# Realizar la Predicción
with torch.no_grad(): # No necesitamos calcular gradientes para inferencia
    out = model(batch_t)
print("Predicción realizada.")

# Interpretar los Resultados
# Descargar las etiquetas de ImageNet
try:
    LABELS_URL = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
    labels_file = requests.get(LABELS_URL).text
    labels = [line.strip() for line in labels_file.split('\n')]
except Exception as e:
    print(f"Error al descargar las etiquetas de ImageNet: {e}")
    labels = [f"Clase {i}" for i in range(1000)] # Fallback

# Obtener las probabilidades (aplicar Softmax)
probabilities = torch.nn.functional.softmax(out[0], dim=0)

# Mostrar las 5 clases más probables
top5_prob, top5_catid = torch.topk(probabilities, 5)

print("\n Predicciones Top 5")
for i in range(top5_prob.size(0)):
    prob = top5_prob[i].item()
    cat_id = top5_catid[i].item()
    label = labels[cat_id]
    print(f"  {i+1}. Clase: {label:<20} | Probabilidad: {prob*100:.2f}%")

# (Opcional) Mostrar la imagen original
# img.show()