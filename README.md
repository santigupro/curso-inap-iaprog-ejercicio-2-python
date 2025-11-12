# Generador de Presentaciones LibreOffice con Python UNO

Este proyecto automatiza la generación de presentaciones de LibreOffice Impress utilizando Python y el módulo UNO (Universal Network Objects) que viene integrado con LibreOffice.

## Descripción

El script `generar_presentacion.py` realiza las siguientes operaciones:
- Abre una presentación plantilla (`input/template.odp`)
- La guarda como `output/presentacion-generada.odp`
- Modifica placeholders en la primera diapositiva:
  - `${titulo-presentacion}` → **Tu Turno**
  - `${subtitulo-presentacion}` → **Sistema de gestión de citas previas de la Junta de Andalucía**

## Requisitos

### Software necesario
- **LibreOffice** (versión 7.0 o superior recomendada)
- **Python 3** (el que viene con LibreOffice es suficiente)

### Instalación de LibreOffice
En sistemas Linux basados en Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install libreoffice libreoffice-script-provider-python
```

En Fedora/RHEL:
```bash
sudo dnf install libreoffice libreoffice-pyuno
```

### Archivo requerido
Debes tener un archivo `input/template.odp` que contenga los placeholders `${titulo-presentacion}` y `${subtitulo-presentacion}` en la primera diapositiva.

## Estructura del proyecto

```
.
├── README.md
├── input/
│   └── template.odp          # Plantilla de presentación
├── output/
│   └── presentacion-generada.odp  # Presentación generada (se crea automáticamente)
└── src/
    └── generar_presentacion.py    # Script principal
```

## Uso

### Paso 1: Iniciar LibreOffice en modo servidor

Antes de ejecutar el script, debes iniciar LibreOffice en modo escucha para conexiones UNO:

```bash
soffice --accept="socket,host=localhost,port=2002;urp;" --headless --norestore --nofirststartwizard
```

**Nota:** Mantén esta terminal abierta mientras ejecutas el script. Puedes ejecutarla en segundo plano agregando `&` al final.

Para ejecutar en segundo plano:
```bash
soffice --accept="socket,host=localhost,port=2002;urp;" --headless --norestore --nofirststartwizard &
```

### Paso 2: Ejecutar el script

Abre una nueva terminal y ejecuta:

```bash
python3 src/generar_presentacion.py
```

O si quieres usar el Python de LibreOffice directamente:

```bash
/usr/bin/python3 src/generar_presentacion.py
```

### Detener el servidor de LibreOffice

Cuando termines, puedes detener el servidor de LibreOffice:

```bash
pkill -f "soffice.*accept"
```

## Resultado esperado

Al ejecutar el script correctamente, verás una salida similar a:

```
======================================================================
GENERADOR DE PRESENTACIÓN - Tu Turno
======================================================================

1. Conectando con LibreOffice...
  ✓ Conexión establecida

2. Abriendo template: /ruta/al/proyecto/input/template.odp
  ✓ Template abierto

3. Guardando como: /ruta/al/proyecto/output/presentacion-generada.odp
  ✓ Archivo guardado

4. Abriendo documento generado: /ruta/al/proyecto/output/presentacion-generada.odp
  ✓ Documento abierto

5. Modificando primera diapositiva...
  ✓ Reemplazado '${titulo-presentacion}' por 'Tu Turno'
  ✓ Reemplazado '${subtitulo-presentacion}' por 'Sistema de gestión de citas previas de la Junta de Andalucía'

6. Guardando cambios...
  ✓ Cambios guardados

======================================================================
✓ PRESENTACIÓN GENERADA EXITOSAMENTE
======================================================================

Archivo generado: /ruta/al/proyecto/output/presentacion-generada.odp

La presentación permanecerá abierta en LibreOffice.
Cierra LibreOffice manualmente cuando termines de revisarla.
```

## Solución de problemas

### Error: No se pudo conectar con LibreOffice

**Causa:** El servidor UNO de LibreOffice no está ejecutándose.

**Solución:** Asegúrate de haber iniciado LibreOffice en modo servidor (Paso 1).

### Error: ModuleNotFoundError: No module named 'uno'

**Causa:** El módulo UNO no está disponible en tu instalación de Python.

**Solución:** Usa el Python que viene con LibreOffice:
```bash
/usr/lib/libreoffice/program/python src/generar_presentacion.py
```

La ubicación puede variar según tu sistema:
- Ubuntu/Debian: `/usr/lib/libreoffice/program/python`
- Fedora: `/usr/lib64/libreoffice/program/python`
- Arch Linux: `/usr/lib/libreoffice/program/python`

### El puerto 2002 ya está en uso

**Causa:** Ya hay una instancia de LibreOffice ejecutándose en ese puerto.

**Solución:** Detén todas las instancias y vuelve a iniciar:
```bash
pkill -f soffice
soffice --accept="socket,host=localhost,port=2002;urp;" --headless --norestore --nofirststartwizard &
```

## Notas adicionales

- El script crea automáticamente el directorio `output/` si no existe
- La presentación generada permanece abierta en LibreOffice para que puedas revisarla
- Puedes modificar los valores de reemplazo editando el archivo `src/generar_presentacion.py`
- El script utiliza el formato nativo de LibreOffice Impress (`.odp`)

## Licencia

Proyecto educativo para el curso INAP de Inteligencia Artificial.