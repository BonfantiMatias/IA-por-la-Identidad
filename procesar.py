import os
import re
import json
import unicodedata
from PIL import Image
from yolo import recortar_notas, noticias
from ocr import ocr_segmentado, formato, ordenar_etiquetas





def procesar_imagenes(source):
    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(source)
    
    # Recorrer la lista de archivos
    for archivo in archivos:
        # Comprobar que el archivo es una imagen
        if archivo.endswith('.jpg') or archivo.endswith('.jpeg') or archivo.endswith('.png') or archivo.endswith('.tif'):
            # Abrir la imagen con PIL
            imagen = Image.open(os.path.join(source, archivo))
            carpeta = os.path.splitext(archivo)[0]
            
            
             
            try:
                # Pasar la imagen a una función
                recortar_notas(imagen)
            except:
                print(f"no se detectaron noticias en {archivo}.")
                continue
            try:
                # Detectar partes de las noticias
                noticias(carpeta)
            except:
                print(f"Ocurrio un Error al preocesar las partes de {archivo}.")
                continue
            
            ordenar_etiquetas(f"deteccion/{carpeta}/predict/labels/")
             # Obtener la lista de recortes
            recortes_carpeta = f"recorte/{carpeta}"
            recortes_list = os.listdir(recortes_carpeta)
            etiquetas_carpeta = f"deteccion/{carpeta}/predict/labels/"
           
            for nota in recortes_list:
                # Comprobar que el archivo es una imagen
                if nota.endswith('.jpg') or nota.endswith('.jpeg') or nota.endswith('.png') or nota.endswith('.tif'):
                    ruta_imagen = os.path.join(recortes_carpeta, nota)
                    label= os.path.splitext(os.path.basename(nota))[0]
                    ruta_etiquetas = os.path.join(etiquetas_carpeta, f"{label}.txt")
                    try:
                        # Detectar partes de las noticias
                        ocr_segmentado(ruta_imagen,ruta_etiquetas,carpeta)
                    except:
                        print(f"Ocurrio un Error al preocesar las partes de {nota}, VERIFICAR INSTALACION OCR.")
                        continue
                    
            # Definir la ruta de la carpeta a procesar
            ruta_carpeta = f'textos/{carpeta}/'
            print(ruta_carpeta)
            for nombre_archivo in os.listdir(ruta_carpeta):
                # Comprobar si el archivo es un archivo .txt
                if nombre_archivo.endswith('.txt'):
                    # Obtener la ruta completa al archivo
                    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
                    # Aplicar la función al archivo
                    formato(ruta_completa)
                    
def normalizar_nombre_archivo(nombre):
    # Eliminar espacios consecutivos y reemplazarlos por un único espacio
    nombre = re.sub('\s{2,}', ' ', nombre)
    
    # Eliminar puntos al inicio o al final del nombre
    nombre = re.sub('^\.', '', nombre)
    nombre = re.sub('\.$', '', nombre)
    
    # Reemplazar puntos que no forman parte de la extensión del archivo
    nombre = re.sub('\.(?!\w+$)', '', nombre)
    nombre = ''.join((c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn'))
    
    return nombre

def normalizar_nombres_archivos_en_carpeta(ruta_carpeta):
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            nuevo_nombre = normalizar_nombre_archivo(nombre_archivo)
            nuevo_nombre_ruta = os.path.join(ruta_carpeta, nuevo_nombre)
            if nuevo_nombre != nombre_archivo:
                os.rename(ruta_archivo, nuevo_nombre_ruta)
                print(f"Se cambió el nombre de '{nombre_archivo}' a '{nuevo_nombre}'.")
                

def generar_json(dir_raiz, dir_salida):
    for carpeta in os.listdir(dir_raiz):
        if carpeta.startswith("Pag 12"):
            nombre_diario = "Pagina 12"
        else:
            nombre_diario_match = re.search(r'([^\d]+)', carpeta)
            if nombre_diario_match:
                nombre_diario = nombre_diario_match.group(1).strip()
            else:
                nombre_diario = ' '.join(carpeta.split()[:2])
        fecha_match = re.search(r'(\d{4}-\d{2}(-\d{2})?)', carpeta)
        fecha = fecha_match.group(1) if fecha_match else 'sin fecha'

        notas = {}
        i = 0
        while True:
            nota = {}
            volanta_file = f'nota {i}_Volanta.txt'
            titulo_file = f'nota {i}_Titulo.txt'
            bajada_file = f'nota {i}_Bajada.txt'
            cuerpo_file = f'nota {i}_Cuerpo.txt'
            epigrafe_file = f'nota {i}_Epigrafe.txt'

            if os.path.isfile(os.path.join(dir_raiz, carpeta, volanta_file)):
                with open(os.path.join(dir_raiz, carpeta, volanta_file), 'r') as f:
                    volanta = f.read().strip()
                nota['volanta'] = volanta
            if os.path.isfile(os.path.join(dir_raiz, carpeta, titulo_file)):
                with open(os.path.join(dir_raiz, carpeta, titulo_file), 'r') as f:
                    titulo = f.read().strip()
                nota['titulo'] = titulo
            if os.path.isfile(os.path.join(dir_raiz, carpeta, bajada_file)):
                with open(os.path.join(dir_raiz, carpeta, bajada_file), 'r') as f:
                    bajada = f.read().strip()
                nota['bajada'] = bajada
            if os.path.isfile(os.path.join(dir_raiz, carpeta, cuerpo_file)):
                with open(os.path.join(dir_raiz, carpeta, cuerpo_file), 'r') as f:
                    cuerpo = f.read().strip()
                nota['cuerpo'] = cuerpo
            if os.path.isfile(os.path.join(dir_raiz, carpeta, epigrafe_file)):
                with open(os.path.join(dir_raiz, carpeta, epigrafe_file), 'r') as f:
                    epigrafe = f.read().strip()
                nota['epigrafe'] = epigrafe

            if not nota:
                break

            notas[f'nota {i}'] = nota
            i += 1

        resultado = {
            'diario': nombre_diario,
            'fecha': fecha,
        }
        resultado.update(notas)

        nombre_archivo = os.path.join(dir_salida, f"{carpeta}.json")
        with open(nombre_archivo, 'w') as f:
            json.dump(resultado, f)