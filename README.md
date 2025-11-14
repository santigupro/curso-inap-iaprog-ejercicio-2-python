# Generador de Presentaciones LibreOffice

Este proyecto permite generar una presentación de LibreOffice Impress (.odp) a partir de una plantilla, un archivo de contenido en Markdown e imagenes en el directorio input, reemplazando placeholders.

## Requisitos

- Python 3.x
- LibreOffice instalado
- LibreOffice ejecutándose en modo servidor UNO
- Paquete `python3-uno` (Ubuntu) o equivalente UNO para Python

## Estructura del proyecto

```
input/
    contenido.md         # Archivo Markdown con el contenido de la presentación
    template.odp         # Plantilla de presentación LibreOffice Impress
output/
    presentacion-generada.odp # Archivo generado
src/
    generar_presentacion.py   # Script principal
```

## Instalación de dependencias

### Ubuntu

1. Instala LibreOffice y el paquete UNO para Python:

```sh
sudo apt update
sudo apt install libreoffice python3-uno
```

2. (Opcional) Verifica que LibreOffice está instalado:

```sh
libreoffice --version
```

### Windows

1. Instala LibreOffice desde [https://www.libreoffice.org/download/download/](https://www.libreoffice.org/download/download/)

2. Instala Python 3 desde [https://www.python.org/downloads/](https://www.python.org/downloads/)

3. Instala el paquete UNO para Python:
   - Descarga el archivo `pyuno` correspondiente a tu versión de LibreOffice y Python.
   - Consulta la documentación oficial de LibreOffice para detalles: [https://wiki.documentfoundation.org/Documentation/DevGuide/Python_Scripting](https://wiki.documentfoundation.org/Documentation/DevGuide/Python_Scripting)

## Ejecución del script

### Ubuntu

1. Ejecuta el script desde la raíz del proyecto:

```sh
python3 src/generar_presentacion.py
```

El archivo generado estará en `output/presentacion-generada.odp`.

### Windows

1. Abre una terminal (CMD o PowerShell) en la raíz del proyecto.
3. Ejecuta el script:

```sh
python src\generar_presentacion.py
```

El archivo generado estará en `output\presentacion-generada.odp`.

## Notas

- El script inicia LibreOffice en modo servidor si no está corriendo.
- Si tienes problemas con la conexión UNO, asegúrate de que LibreOffice esté ejecutándose con el parámetro:

```sh
soffice --accept=socket,host=localhost,port=2002;urp; --headless --norestore --nofirststartwizard
```

- En Windows, puedes iniciar LibreOffice en modo servidor desde la terminal:

```sh
"C:\Program Files\LibreOffice\program\soffice.exe" --accept=socket,host=localhost,port=2002;urp; --headless --norestore --nofirststartwizard
```

## Personalización

- Modifica `contenido.md` para cambiar el contenido de la presentación.
- Modifica `template.odp` para cambiar el diseño de la presentación.

## Licencia

Este proyecto es de uso educativo y libre.
