# IA por la Identidad

El desafío planteado por la la Fundacion Sadosky en colaboración con la Fundación Abuelas de Plaza de Mayo es el de crear un programa que logre interpretar imágenes de diarios, las mismas son recortes, fotos u escaneos de calidades muy diversas.
Estas imágenes deben ser procesadas y cada imagen debe generar un archivo JSON donde se transcriban su partes por separado (Título, Cuerpo, Bajada, Imagen, Epígrafe, Volanta)


# Nuestra solución

Este proyecto ofrece una solución en Python para extraer información de notas y diarios digitalizados. La solución utiliza una segmentación en YOLO para separar las notas y noticias y, posteriormente, analizarlas individualmente mediante una detección en YOLO. La detección en YOLO se encarga de detectar las diferentes partes de la nota, como la volanta, el título, la bajada, el cuerpo y el epígrafe. La salida de esta detección se presentan como bounding box que se procesan con un OCR para generar un archivo JSON. En resumen, la solución en Python utiliza técnicas de segmentación y detección en YOLO para extraer información de notas y diarios digitalizados de manera eficiente.

## Instalación en Windows

Descargar los archivos, descomprirlos y abrir la carpeta donde se encuentran los archivos. Una vez en la carpeta reemplazar la ruta que figura en la barra de direcciones por cmd y presionar enter para ingresar a nuetra carpeta en la consola de Windows. 

 El primer punto es verificar que tenemos instalado python con el
    siguiente comando 
    
        python --version
    
   Si no tenemos instalado python descargamos desde la siguiente pagina y al momento de instalar en la primer ventana tildamos la opción de patch.

[Descargar Python ](https://www.python.org/downloads/) 
    
Instalación  OCR 

[Descargar Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

El segundo punto es instalar las librerias necesarias con el siguiente comando. Esto puede demorar unos minutos dependiendo de nuestra conexión a internet.
    
        pip install -r requirements.txt

## Instalación en Linux

Descargar los archivos, descomprirlos y abrir la carpeta donde se encuentran los archivos. Una vez en la carpeta abrimos una consola con esa ruta.

El primer punto es verificar que tenemos instalado python con el siguiente comando 

    python --version


Si no tenemos instalado python seguimos la sieguiente guia para instalar python y pip.

[Guia instalacion Python ](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux/)

El segundo punto es instalar las librerias necesarias con el siguiente comando. Esto puede demorar unos minutos dependiendo de nuestra conexión a internet.

    pip install -r requirements.txt

Antes de ejutar hay que modificar la ruta del ocr, por defecto esta configurado para windows. Abrir el archivo ocr.py y modificar las siguiente lineas 

Antes

    # Configurar la ruta del ejecutable de Tesseract>
    #Windows
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    #Linux
    #os.environ['TESSDATA_PREFIX'] = './ocr'


Despues

    # Configurar la ruta del ejecutable de Tesseract>
    #Windows
    #pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    #Linux
    os.environ['TESSDATA_PREFIX'] = './ocr'


## Ejecución 

La ejecución la podemos hacer en 3 entornos diferentes
### Windows y Linux 
En la consola ingresamos el siguiente comando

    python3 start.py
    
 Al iniciar se procesaran por defecto los archivos guardados en la carpeta "imagenes" y la salida en la carpeta "json". 
Si queremos procesar los arhivos de otra carpeta o cambiar la ruta de salida podemos hacerlo agregando los siguientes argumentos.

    python3 start.py --entrada --salida

### Huggingface
En este entorno grafico podemos probar la segmentacion y las detecciones, sin realizar instalaciones. 

[Hugginface](https://huggingface.co/spaces/matiasbonfanti/IA_por_la_Identidad)

### Google Colab
En este entorno podemos realizar pruebas con gpu. 
