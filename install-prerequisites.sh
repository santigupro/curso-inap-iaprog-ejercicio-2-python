#!/bin/bash

# Clonar repositorio
git clone https://github.com/adobe-fonts/source-code-pro.git

# Crear directorio local de fuentes si no existe
mkdir -p ~/.local/share/fonts

# Copiar archivos .otf a directorio de fuentes
cp source-code-pro/OTF/*.otf ~/.local/share/fonts/

# Actualizar caché de fuentes
fc-cache -f -v

echo "Instalación de Source Code Pro completada."
