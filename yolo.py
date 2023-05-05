from typing import List
from ultralytics import YOLO
import cv2
import numpy as np
import os

def recortar_notas(imagen_path: str) -> int:
    model = YOLO("final-seg-l.pt")

    results = model.predict(source=imagen_path, save=True, save_txt=True, project="diarios", classes=0, conf=0.70) 

    # cargar imagen tif
    image = cv2.imread(results[0].path)

    # crear una carpeta para guardar los recortes
    filename = os.path.splitext(os.path.basename(results[0].path))[0]
    foldername = os.path.splitext(filename)[0]
    if not os.path.exists(f"recorte/{foldername}"):
        os.makedirs(f"recorte/{foldername}")

    datos = results[0].masks.xy

    num_notas = 0

    for i, coords in enumerate(datos): 
        # coordenadas de segmentación
        coordenadas = np.array(coords)

        # crear una máscara vacía
        mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

        # dibujar un polígono en la máscara
        cv2.fillPoly(mask, [coordenadas.astype(np.int32)], 255)

        # aplicar la máscara a la imagen
        masked = cv2.bitwise_and(image, image, mask=mask)

        # recortar la imagen utilizando la caja delimitadora de la máscara
        x, y, w, h = cv2.boundingRect(mask)
        recorte = masked[y:y+h, x:x+w]

        # guardar el recorte como una imagen
        recorte_path = os.path.join(f"recorte/{foldername}", f"nota {i}.jpg")
        cv2.imwrite(recorte_path, recorte)

        num_notas += 1

    return print(f"Se proceso la imagen '{filename}' y se obtuvieron {num_notas} recortes") 


def noticias(carpeta):
    nombre = carpeta
    model = YOLO("detect-n.pt")
    results = model.predict(source=f"recorte/{nombre}", save=True, save_txt=True,project=f"deteccion/{nombre}", conf=0.75)  # save plotted images
    return print(f"Imagen {nombre} procesada correctamente")