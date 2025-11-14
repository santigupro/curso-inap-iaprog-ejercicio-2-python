# Generador de Presentaciones LibreOffice

El script realizado permite generar una presentación de LibreOffice Impress (.odp) a partir de una plantilla, un archivo de contenido en Markdown e imagenes situadas en el directorio input.

Respeta los estilos de las diapositivas de template.odp (que es la que usamos en la Junta de Andalucia) sustituyendo ciertos marcadores por el contenido de contenido.md. Lo que hace es reemplazar cada diapositiva por el titulo en el mismo orden correspondiente de contenido.md, es decir, en la diapositiva 1 se busca el contenido del titulo 1 y su contenido del markdown.
Quería hacer que usasen tipos de plantilla pero de momento llegué hasta aquí... :(
El script lo he probado en dos equipos diferentes pero siempre con Ubuntu.
Habría que instalar libreoffice según se indica en el README.md. Si se quiere ver mejor la presnetacion habría que isntalar las fuentes, incluidas también en input/fuentes aunque no se ve bien mal sin las fuentes.

Después de instalar libreoffice y python con ejecutar el script la raiz del repositorio se debería generar en output la presentación en libreoffice.
```sh
python3 src/generar_presentacion.py
```

# Proceso seguido para realizar el script
- Busqué la plantilla de la Junta de Andalucia
- Generé un markdown con el texto e imagenes de la presentación con Perplexity
- Con Visual Studio Code y GitHub Copilot generé el script en varias fases:
    - Primero lo intenté con Java y el sdk de libreoffice y no salía nada bien.
    - Después investigué un poco y vi que era recomendable usar la API UNO de libreoffice con Python.
    - Hice el script en varias fases, primero susituyendo la portada, después la segunda dipaoistiva y después de manera iterativa.
    - Como hay que tener ejecutandose un servicio de libreoffice, para ser menos molesto añadí también al propio script que arrancase y cerrase el servicio.

# Formato de `contenido.md`

El archivo `contenido.md` contiene el contenido de la presentación en formato Markdown estructurado por secciones. Cada diapositiva se define mediante títulos y variables entre llaves `${...}` que serán reemplazadas por el script. El formato típico incluye:

- Títulos de sección y diapositiva (`#`, `##`)
- Variables como `${titulo-presentacion}`, `${subtitulo-presentacion}`, `${contenido-textual}`
- Listas y texto explicativo
- Imágenes referenciadas con sintaxis Markdown (`![Texto](imagen.png)`)

Ejemplo de estructura:

```
# Portada
## ${titulo-presentacion}
titulo
## ${subtitulo-presentacion}
subtitulo
# Índice
## ${contenido-textual}
- uno
- dos
...
# 1. Introducción al sistema
## ${titulo-diapositiva}
Inotrudccion
## ${contenido-textual}
...
## ${imagen}
url markdown a la imagen local
```

Las variables serán sustituidas por el script para generar cada diapositiva de la presentación.


## Requisitos

- Python 3.x
- LibreOffice instalado
- Fuentes Source Sans Pro para ver bien la presentacion (incluidas en input/fuentes)

## Estructura del proyecto

```
input/
    contenido.md         # Archivo Markdown con el contenido de la presentación
    template.odp         # Plantilla de presentación LibreOffice Impress
    fuentes              # Fuentes a instalar para la presentación
output/
    presentacion-generada.odp # Archivo generado
src/
    generar_presentacion.py   # Script principal
```




## Instalación de dependencias

1. Instala LibreOffice y el paquete UNO para Python:

```sh
sudo apt update
sudo apt install libreoffice
```

2. (Opcional) Verifica que LibreOffice está instalado:

```sh
libreoffice --version
```

## Notas

- El script inicia LibreOffice en modo servidor si no está corriendo.
- Algunas veces si el script da error es que no ha arrancado bien el servicio de libreoffice, pero ejecutar por segunda vez el script lo arranca bien.