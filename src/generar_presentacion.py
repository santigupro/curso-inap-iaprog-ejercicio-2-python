#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar presentación de LibreOffice modificando placeholders
"""

import uno
from com.sun.star.beans import PropertyValue
import os
import sys

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

def main():
    """Función principal"""
    # Rutas de los archivos
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_template = os.path.join(ruta_base, "input", "template.odp")
    ruta_output = os.path.join(ruta_base, "output", "presentacion-generada.odp")
    ruta_contenido = os.path.join(ruta_base, "input", "contenido.md")
    
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
    
    # Abrir template
    print(f"\n2. Abriendo template: {ruta_template}")
    doc = abrir_documento(desktop, ruta_template)
    print("  ✓ Template abierto")
    
    # Guardar como nuevo archivo
    print(f"\n3. Guardando como: {ruta_output}")
    guardar_como(doc, ruta_output)
    print("  ✓ Archivo guardado")
    
    # Cerrar el documento template
    doc.close(True)
    
    # Abrir el documento generado
    print(f"\n4. Abriendo documento generado: {ruta_output}")
    doc = abrir_documento(desktop, ruta_output)
    print("  ✓ Documento abierto")
    
    # Obtener la primera diapositiva
    print("\n5. Modificando primera diapositiva...")
    draw_pages = doc.getDrawPages()
    primera_diapositiva = draw_pages.getByIndex(0)

    # Mostrar textos encontrados
    mostrar_textos_en_diapositiva(primera_diapositiva)

    # Leer reemplazos de contenido.md para la primera diapositiva
    reemplazos = obtener_reemplazos_primera_diapositiva(ruta_contenido)
    for placeholder, texto in reemplazos.items():
        reemplazar_texto_en_diapositiva(primera_diapositiva, placeholder, texto)
    
    # Guardar cambios
    print("\n6. Guardando cambios...")
    doc.store()
    print("  ✓ Cambios guardados")
    
    print("\n" + "=" * 70)
    print("✓ PRESENTACIÓN GENERADA EXITOSAMENTE")
    print("=" * 70)
    print(f"\nArchivo generado: {ruta_output}")
    print("\nLa presentación permanecerá abierta en LibreOffice.")
    print("Cierra LibreOffice manualmente cuando termines de revisarla.")

if __name__ == "__main__":
    main()
