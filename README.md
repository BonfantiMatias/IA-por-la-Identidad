# IA por la Identidad

El desafío planteado por la la Fundacion Sadosky en colaboración con la Fundación Abuelas de Plaza de Mayo es el de crear un programa que logre interpretar imágenes de diarios, las mismas son recortes, fotos u escaneos de calidades muy diversas.
Estas imágenes deben ser procesadas individualmente para generar un archivo JSON donde se transcriban su partes por separado (Título, Cuerpo, Bajada, Imagen, Epígrafe, Volanta)


# Nuestra solución

Este proyecto ofrece una solución en Python para extraer información de notas y diarios digitalizados. La solución utiliza una segmentación en YOLO para separar las notas y noticias y, posteriormente, analizarlas individualmente mediante una detección en YOLO. La detección en YOLO se encarga de detectar las diferentes partes de la nota, como la volanta, el título, la bajada, el cuerpo y el epígrafe. La salida de esta detección se presentan como bounding box que se procesan con un OCR para generar un archivo JSON. En resumen, la solución en Python utiliza técnicas de segmentación y detección en YOLO para extraer información de notas y diarios digitalizados de manera eficiente.

## Instalación en Windows

[Video Instalcion Windows](https://drive.google.com/file/d/1vS0Ex5zZ-sMXT48S6oynN2BQ6BBfQ6dq/view?usp=sharing)

Descargar los archivos, descomprirlos y abrir la carpeta donde se encuentran los archivos. Una vez en la carpeta reemplazar la ruta que figura en la barra de direcciones por "cmd" y presionar enter para ingresar a nuetra carpeta en la consola de Windows. 

 El primer punto es verificar que tenemos instalado python con el
    siguiente comando 
    
        python --version
    
   Si no tenemos instalado python debemos descargarlo desde la siguiente pagina y al momento de instalar en la primer ventana tildamos la opción de patch.

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
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    #Linux
    #os.environ['TESSDATA_PREFIX'] = './ocr'


Despues

    # Configurar la ruta del ejecutable de Tesseract>
    #Windows
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    #Linux
    os.environ['TESSDATA_PREFIX'] = './ocr'

## Instalación en MacOS

[Video Instalacion MacOs ](https://drive.google.com/file/d/1nUGjTj8aXxeOL6wctxMU1Pz2fOtU6Hoo/view?usp=sharing)
Descargar los archivos, descomprirlos y abrir la carpeta donde se encuentran los archivos. Una vez en la carpeta abrimos una consola con esa ruta.

El primer punto es verificar que tenemos instalado python con el siguiente comando 

    python --version


Si no tenemos instalado python seguimos la sieguiente guia para instalar python y pip.

[Guia instalacion Python ](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux/)

El segundo punto es instalar las librerias necesarias con el siguiente comando. Esto puede demorar unos minutos dependiendo de nuestra conexión a internet.

    pip install -r requirements.txt

En tercer lugar realizamos la Instalación de Tesseract.
La instalación se realiza por medio de MacPorts. MacPorts es un sistema de gestión de paquetes para macOS, que permite instalar y gestionar una amplia variedad de software de código abierto y otros proyectos de software en tu Mac.
Para verificar si MacPorts está instalado en tu Mac, puedes abrir una terminal y ejecutar el siguiente comando:

    port version

Este comando debería mostrar la versión de MacPorts que tienes instalada en tu sistema. Si el comando no se reconoce, es necesario instalarlo desde su sitio web oficial de MacPorts (https://www.macports.org/install.php). La instalación es sencilla y se realiza a través de un archivo .pkg. 

Para instalar el Tesseract ejecutar el siguiente comando en terminal:

    sudo port install tesseract

Para instalar el idioma español ejecutar:

    sudo port install tesseract-spa

Antes de ejutar hay que modificar la ruta del ocr, por defecto esta configurado para windows. Abrir el archivo ocr.py y modificar las siguiente lineas 

Antes

    # Configurar la ruta del ejecutable de Tesseract>
    #Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    #Linux
    #os.environ['TESSDATA_PREFIX'] = './ocr'


Despues

    # Configurar la ruta del ejecutable de Tesseract>
    #Windows
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    #Linux
    os.environ['TESSDATA_PREFIX'] = './ocr'



## Ejecución 

La ejecución la podemos hacer en 4 entornos diferentes
### Windows  
[Video Ejecucion en Windows ](https://drive.google.com/file/d/1kNA8z7yYXVdISCv9EybG5kD52fsjbkx3/view?usp=sharing)
En la consola ingresamos el siguiente comando

    python3 start.py
    
 Al iniciar se procesaran por defecto los archivos guardados en la carpeta "imagenes" y la salida en la carpeta "json". 
Si queremos procesar los arhivos de otra carpeta o cambiar la ruta de salida podemos hacerlo agregando los siguientes argumentos.

    python3 start.py --entrada carpeta_entrada --salida carpeta_salida

### Linux (Docker)  
[Video Instalacion MacOs ](https://drive.google.com/file/d/1i-5vs2D24F_7rJSq0S-9aFOb5lKJHgJT/view?usp=sharing)

Descargamos los archivos y los descomprimimos. Modificar el archivo ocr.py con la ruta de pytesseract para linux, como se mostro en instalacion para linux.
El siguiente paso es abri una consola en la carpeta donde se encuentran los archivos descomprimidos y ejecutar el siguiente codigo para generar una imagen de docker con las librerias necesarias para ejecutar el codigo.

    sudo docker build -t ocr .
    
El siguiente codigo es para ejecutar la imagen con un volumen compartido entre el contenedor y nuestro sistema operativo. Las imagenes a procesar las cargamos en la carpeta imagenes u otra ubicada dentro del directorio compartido

    sudo docker run -it -v ./:/app/ ocr bash

Una vez dentro del container podemos ejecutar el codigo para procesar las imagenes

    python3 start.py --entrada carpeta_entrada --salida carpeta_salida

### Huggingface
En este entorno grafico podemos probar la segmentacion y las detecciones, sin realizar instalaciones. 

[Hugginface](https://huggingface.co/spaces/matiasbonfanti/IA_por_la_Identidad)

### Google Colab

[Video Colab](https://drive.google.com/file/d/1frmwc5Vbu_JlPhe0d5pvgMaRu2gwI7gV/view?usp=sharing)

En este entorno podemos realizar pruebas con gpu. 

[Colab](https://colab.research.google.com/drive/1yX7k2YXZ8ugW0bDXkFKs5xxDUK4rUs6C?usp=sharing)

