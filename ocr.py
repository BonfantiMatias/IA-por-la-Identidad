import cv2
#from google.colab.patches import cv2_imshow # Importar la función cv2_imshow para mostrar la imagen en Colab
import matplotlib.pyplot as plt
import pytesseract
import os


# Configurar la ruta del ejecutable de Tesseract
#Windows
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
#Linux
#os.environ['TESSDATA_PREFIX'] = './ocr'

def ocr_segmentado(ruta_imagen,etiquetas,noticia):
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)

    # Obtener las dimensiones de la imagen
    image_height, image_width, _ = imagen.shape
    
    # Obtener el nombre del archivo sin extensión
    file_name = os.path.splitext(os.path.basename(etiquetas))[0]
    os.makedirs(f"textos/{noticia}", exist_ok=True)

    # Leer las detecciones del archivo de texto
    with open(etiquetas, "r") as archivo:
        detecciones = []
        for linea in archivo:
            deteccion = [float(coordenada) for coordenada in linea.strip().split()]
            detecciones.append(deteccion)

    # Crear un diccionario para almacenar las detecciones de cada etiqueta
    detecciones_por_etiqueta = {}

    # Iterar sobre las detecciones y agregarlas al diccionario correspondiente a su etiqueta
    for i, deteccion in enumerate(detecciones):
        label = int(deteccion[0])
        if label == 5:
            continue # Saltar las detecciones con la etiqueta "Imagen"

        # Convertir las coordenadas YOLO a píxeles
        x_center, y_center, box_width, box_height = deteccion[1:]
        x_left = int((x_center - (box_width / 2)) * image_width)
        y_top = int((y_center - (box_height / 2)) * image_height)
        box_width = int(box_width * image_width)
        box_height = int(box_height * image_height)
        x_right = x_left + box_width
        y_bottom = y_top + box_height

        # Recortar el cuadro delimitador de la imagen
        cuadro = imagen[y_top:y_bottom, x_left:x_right]

        # Realizar OCR en el cuadro delimitador
        ocr_text = pytesseract.image_to_string(cuadro, lang='spa', config='--psm 6')

        # Clasificar la etiqueta de la clase
        if label == 1:
            clase = "Titulo"
        elif label == 0:
            clase = "Cuerpo"
        elif label == 2:
            clase = "Volanta"
        elif label == 3:
            clase = "bajada"
        elif label == 4:
            clase = "Epigrafe"

        # Agregar la detección al diccionario correspondiente a su etiqueta
        if clase in detecciones_por_etiqueta:
            detecciones_por_etiqueta[clase].append((i+1, ocr_text))
        else:
            detecciones_por_etiqueta[clase] = [(i+1, ocr_text)]

    # Escribir las detecciones de cada etiqueta en un archivo separado
    for clase, detecciones in detecciones_por_etiqueta.items():
        with open(f"textos/{noticia}/{file_name}_{clase}.txt", "w") as archivo:
            for i, ocr_text in detecciones:
                archivo.write(f"{ocr_text}\n")

    # Convertir la imagen a RGB para mostrarla con matplotlib
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # Mostrar la imagen resultante con matplotlib
    plt.imshow(imagen_rgb)
    plt.axis('off')
    plt.show()
    


def ordenar_etiquetas(directorio):
    etiquetas = [2, 1, 3, 0, 4, 5]  # etiquetas en el orden deseado
    
    # iterar sobre todos los archivos en el directorio
    for archivo in os.listdir(directorio):
        if archivo.endswith(".txt"):
            nombre_archivo = os.path.join(directorio, archivo)
            datos = {}
            
            # abrir el archivo y leer los datos
            with open(nombre_archivo, 'r') as f:
                lineas = f.readlines()
                
            # procesar cada línea del archivo
            for linea in lineas:
                partes = linea.strip().split()  # separar la línea en partes
                etiqueta = int(partes[0])
                coordenadas = [float(x) for x in partes[1:]]  # convertir las coordenadas a números
                
                # si es la primera vez que se encuentra la etiqueta, crear una lista vacía
                if etiqueta not in datos:
                    datos[etiqueta] = []
                
                # agregar las coordenadas a la lista correspondiente
                datos[etiqueta].append(coordenadas)
            
            # ordenar los datos según la etiqueta y las coordenadas de YOLO
            for etiqueta in etiquetas:
                if etiqueta in datos:
                    datos[etiqueta] = sorted(datos[etiqueta], key=lambda x: x[0])
            
            # escribir los datos ordenados en el archivo
            with open(nombre_archivo, 'w') as f:
                for etiqueta in etiquetas:
                    if etiqueta in datos:
                        for coordenadas in datos[etiqueta]:
                            # convertir las coordenadas a texto y escribir en el archivo
                            f.write(f"{etiqueta} {' '.join(str(x) for x in coordenadas)}\n")
                
def formato(ruta):
    with open(ruta, "r") as archivo:
        contenido = archivo.read()
        
    # Eliminar saltos de línea y espacios redundantes
    contenido = contenido.replace("\n", " ").replace("  ", " ")
    
    # Concatenar palabras si la línea termina con "-"
    lineas = contenido.split("-")
    contenido = ""
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if i < len(lineas) - 1:
            if not linea.endswith("."):
                linea += "-"
        contenido += linea
        
    # Agregar un salto de línea después de cada oración
    contenido = contenido.replace(". ", ".\n")
    
    # Eliminar signos "-"
    contenido = contenido.replace("-", "")
    
    # Guardar el contenido formateado en el mismo archivo
    with open(ruta, "w") as archivo:
        archivo.write(contenido)