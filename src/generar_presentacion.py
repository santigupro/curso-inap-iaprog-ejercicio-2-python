#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar presentación de LibreOffice modificando placeholders
"""

import uno
from com.sun.star.beans import PropertyValue
import os
import sys
import re

def create_property(name, value):
    """Crea un objeto PropertyValue para UNO"""
    prop = PropertyValue()
    prop.Name = name
    prop.Value = value
    return prop

def get_desktop():
    """Obtiene el componente desktop de LibreOffice"""
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context
    )
    
    try:
        ctx = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
        )
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        return desktop
    except:
        print("Error: No se pudo conectar con LibreOffice.")
        print("Asegúrate de que LibreOffice está ejecutándose con el servidor UNO.")
        sys.exit(1)

def abrir_documento(desktop, ruta_archivo):
    """Abre un documento de LibreOffice"""
    url = uno.systemPathToFileUrl(os.path.abspath(ruta_archivo))
    props = (create_property("Hidden", False),)
    doc = desktop.loadComponentFromURL(url, "_blank", 0, props)
    return doc

def guardar_como(doc, ruta_destino):
    """Guarda el documento en una nueva ubicación"""
    url = uno.systemPathToFileUrl(os.path.abspath(ruta_destino))
    props = (create_property("FilterName", "impress8"),)
    doc.storeToURL(url, props)

def reemplazar_texto_en_diapositiva(diapositiva, texto_buscar, texto_reemplazo):
    """Reemplaza texto en una diapositiva"""
    # Iterar sobre todas las formas (shapes) en la diapositiva
    for i in range(diapositiva.getCount()):
        shape = diapositiva.getByIndex(i)
        
        # Verificar si la forma tiene texto
        if shape.supportsService("com.sun.star.drawing.Text"):
            try:
                texto_actual = shape.getString()
                if texto_buscar in texto_actual:
                    nuevo_texto = texto_actual.replace(texto_buscar, texto_reemplazo)
                    shape.setString(nuevo_texto)
                    print(f"  ✓ Reemplazado '{texto_buscar}' por '{texto_reemplazo}'")
            except:
                pass

def mostrar_textos_en_diapositiva(diapositiva):
    """Muestra todos los textos en una diapositiva"""
    print("\nTextos encontrados en la diapositiva:")
    for i in range(diapositiva.getCount()):
        shape = diapositiva.getByIndex(i)
        if shape.supportsService("com.sun.star.drawing.Text"):
            try:
                texto_actual = shape.getString()
                print(f"  - {texto_actual}")
            except:
                pass

def obtener_reemplazos_primera_diapositiva(ruta_contenido):
    """Obtiene los placeholders y textos a reemplazar para la primera diapositiva desde contenido.md"""
    with open(ruta_contenido, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    reemplazos = {}
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith('## ${') and linea.endswith('}'):
            placeholder = linea[3:]
            # El texto a reemplazar está en la siguiente línea no vacía
            i += 1
            while i < len(lineas) and not lineas[i].strip():
                i += 1
            if i < len(lineas):
                reemplazos[placeholder] = lineas[i].strip()
        i += 1
        # Solo procesar la primera sección (Portada)
        if '# Índice' in linea:
            break
    return reemplazos

def obtener_reemplazos_por_diapositiva(ruta_contenido):
    """Obtiene los placeholders y textos a reemplazar para cada diapositiva desde contenido.md"""
    with open(ruta_contenido, 'r', encoding='utf-8') as f:
        contenido = f.read()
    # Dividir por secciones principales (cada título de diapositiva)
    secciones = re.split(r'^# ', contenido, flags=re.MULTILINE)[1:]
    reemplazos_por_diapositiva = []
    for seccion in secciones:
        reemplazos = {}
        lineas = seccion.strip().split('\n')
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            if linea.startswith('## ${') and linea.endswith('}'):
                placeholder = linea[3:]
                i += 1
                contenido_placeholder = []
                # Acumular todas las líneas hasta el siguiente subtítulo o título
                while i < len(lineas):
                    siguiente = lineas[i].strip()
                    if siguiente.startswith('## ${') and siguiente.endswith('}'):
                        break
                    if siguiente.startswith('# '):
                        break
                    contenido_placeholder.append(lineas[i].rstrip())
                    i += 1
                # Unir todas las líneas, preservando saltos de línea
                reemplazos[placeholder] = '\n'.join([l for l in contenido_placeholder if l.strip()])
                continue
            i += 1
        reemplazos_por_diapositiva.append(reemplazos)
    return reemplazos_por_diapositiva

def reemplazar_imagen_en_diapositiva(diapositiva, nueva_imagen_path):
    """Reemplaza la imagen en la diapositiva por la indicada en nueva_imagen_path"""
    for i in range(diapositiva.getCount()):
        shape = diapositiva.getByIndex(i)
        # Verificar si la forma es una imagen
        if shape.supportsService("com.sun.star.drawing.GraphicObjectShape"):
            try:
                # Reemplazar la imagen
                url = uno.systemPathToFileUrl(os.path.abspath(nueva_imagen_path))
                shape.GraphicURL = url
                print(f"  ✓ Imagen reemplazada por '{nueva_imagen_path}'")
                return True
            except Exception as e:
                print(f"  ⚠ Error al reemplazar imagen: {e}")
    return False

def main():
    """Función principal"""
    # Rutas de los archivos
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_template = os.path.join(ruta_base, "input", "template.odp")
    ruta_output = os.path.join(ruta_base, "output", "presentacion-generada.odp")
    ruta_contenido = os.path.join(ruta_base, "input", "contenido.md")
    
    # Borrar la presentación generada si existe
    if os.path.exists(ruta_output):
        print(f"Eliminando presentación generada previa: {ruta_output}")
        os.remove(ruta_output)
    
    # Verificar que existe el template
    if not os.path.exists(ruta_template):
        print(f"Error: No se encuentra el archivo {ruta_template}")
        sys.exit(1)
    
    # Crear directorio output si no existe
    os.makedirs(os.path.dirname(ruta_output), exist_ok=True)
    
    print("=" * 70)
    print("GENERADOR DE PRESENTACIÓN - Tu Turno")
    print("=" * 70)
    
    # Conectar con LibreOffice
    print("\n1. Conectando con LibreOffice...")
    desktop = get_desktop()
    print("  ✓ Conexión establecida")
    
    # Abrir template y guardar como nuevo archivo
    print(f"\n2. Abriendo template: {ruta_template}")
    doc_template = abrir_documento(desktop, ruta_template)
    print("  ✓ Template abierto")
    
    print(f"\n3. Guardando como: {ruta_output}")
    guardar_como(doc_template, ruta_output)
    print("  ✓ Archivo guardado")
    
    # Cerrar la plantilla
    if doc_template:
        try:
            doc_template.close(True)
        except Exception:
            pass
    
    # Abrir la presentación generada SOLO para modificar y guardar, luego cerrar
    doc_output = abrir_documento(desktop, ruta_output)
    draw_pages = doc_output.getDrawPages()
    total_diapositivas = draw_pages.getCount()
    
    # Leer todos los reemplazos por diapositiva
    reemplazos_por_diapositiva = obtener_reemplazos_por_diapositiva(ruta_contenido)
    print(f"Procesando {min(len(reemplazos_por_diapositiva), total_diapositivas)} diapositivas...")
    for idx in range(min(len(reemplazos_por_diapositiva), total_diapositivas)):
        print(f"\nDiapositiva {idx+1}:")
        diapositiva = draw_pages.getByIndex(idx)
        mostrar_textos_en_diapositiva(diapositiva)
        reemplazos = reemplazos_por_diapositiva[idx]
        # Reemplazo de texto
        for placeholder, texto in reemplazos.items():
            if placeholder == "${imagen}":
                # Extraer la ruta de la imagen del texto (puede estar en formato markdown ![alt](ruta))
                match = re.search(r'\(([^)]+)\)', texto)
                if match:
                    imagen_path = os.path.join(ruta_base, "input", match.group(1))
                    reemplazar_imagen_en_diapositiva(diapositiva, imagen_path)
                else:
                    print("  ⚠ No se encontró ruta de imagen en el texto de ${imagen}")
            else:
                reemplazar_texto_en_diapositiva(diapositiva, placeholder, texto)
    # Guardar cambios
    doc_output.store()
    print("✓ Reemplazos aplicados en todas las diapositivas desde contenido.md")
    
    # Cerrar la presentación generada
    if doc_output:
        try:
            doc_output.close(True)
        except Exception:
            pass
    
    print("\n" + "=" * 70)
    print("✓ PRESENTACIÓN GENERADA EXITOSAMENTE")
    print("=" * 70)
    print(f"\nArchivo generado: {ruta_output}")
    print("\nLa presentación permanecerá abierta en LibreOffice.")
    print("Cierra LibreOffice manualmente cuando termines de revisarla.")

if __name__ == "__main__":
    main()
