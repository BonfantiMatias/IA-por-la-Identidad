import os
import glob
import argparse
import shutil
from procesar import procesar_imagenes, normalizar_nombres_archivos_en_carpeta, generar_json

if __name__ == '__main__':
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Procesar imágenes en una carpeta.')
    parser.add_argument('--entrada', metavar='RUTA', type=str, help='Ruta de la carpeta con las imágenes.')
    parser.add_argument('--salida', metavar='RUTA', type=str, help='Ruta de la carpeta para guardar las imágenes procesadas.')
    parser.add_argument('--borrar_carpeta', metavar='BORRAR', type=str, help='Indica si se debe borrar la carpeta de detecciones al finalizar el programa.', default='n')

    # Parsear los argumentos
    args = parser.parse_args()

    # Seleccionar la carpeta de imágenes
    carpeta_imagenes = args.entrada or 'imagenes'

    # Seleccionar la carpeta de salida
    carpeta_salida = args.salida or 'json'

    # Obtener el número de imágenes en la carpeta
    num_imagenes = len([archivo for archivo in os.listdir(carpeta_imagenes) if archivo.endswith('.jpg') or archivo.endswith('.jpeg') or archivo.endswith('.png') or archivo.endswith('.tif')])

    # Imprimir el número de imágenes
    print(f'Número de imágenes en la carpeta: {num_imagenes}')
    
    #Normalizar nombre archivos
    normalizar_nombres_archivos_en_carpeta(carpeta_imagenes)
    
    # Procesar las imágenes
    procesar_imagenes(carpeta_imagenes)
    
    generar_json('textos',carpeta_salida)

    # Preguntar al usuario si desea borrar la carpeta de detecciones
    respuesta_borrar = input('¿Desea borrar la carpeta de detecciones? (s/n): ').lower()

    if respuesta_borrar == 's':
        # Borrar la carpeta de detecciones
        shutil.rmtree('deteccion')
        shutil.rmtree( 'diarios')
        shutil.rmtree('recorte')
        shutil.rmtree('textos')
        print('Las carpetas de detecciones han sido borradas.')
    else:
        print('Las carpetas de detecciones no han sido borrada.')