# Descargador de Música de YouTube

Herramienta para descargar música desde YouTube de forma rápida y sencilla.

## Características

- 🎵 **Búsqueda de canciones:** Busca en YouTube directamente
- 📁 **Carga de listas:** Importa CSV/TXT con múltiples canciones
- ▶️ **Preview:** Escucha 30 segundos antes de descargar
- 💾 **Descarga en MP3:** Convierte automáticamente a MP3 192kbps
- 🎚️ **Control de volumen:** Ajusta el volumen en tiempo real
- 🖥️ **Interfaz gráfica:** Interfaz moderna y fácil de usar

## Requisitos Previos

- Python 3.10+
- FFmpeg instalado
- pip (gestor de paquetes de Python)

## Instalación

### Opción 1: Desde el código fuente

```bash
# Clonar el repositorio
git clone https://github.com/BlackDragonG66/DescargadorMusicaYT.git
cd DescargadorMusicaYT

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

### Opción 2: Usar el .exe (Windows)

1. Descarga el archivo `DescargadorMusicaYT.exe` desde [Releases](https://github.com/BlackDragonG66/DescargadorMusicaYT/releases)
2. Asegúrate de tener FFmpeg instalado:
   ```bash
   winget install FFmpeg
   ```
3. Ejecuta el .exe

## Uso

1. **Buscar canción:**
   - Escribe el nombre en el campo "Canción"
   - Presiona Enter o haz clic en "Buscar"
   
2. **Escuchar preview:**
   - Selecciona un resultado
   - Haz clic en "▶ Play (30s)"
   - Ajusta el volumen si necesitas

3. **Descargar:**
   - Haz clic en "+ Agregar a Cola"
   - Repite para más canciones
   - Haz clic en "✓ Descargar Cola"

4. **Cargar lista:**
   - Prepara un archivo CSV o TXT con nombres de canciones (uno por línea)
   - Haz clic en "Cargar CSV/TXT"
   - La app buscará y agregará todas a la cola automáticamente

## Formatos soportados

- **Entrada:** CSV, TXT
- **Salida:** MP3 (192kbps)
- **Fuente:** YouTube

## Construcción del .exe

Si quieres compilar el .exe por tu cuenta:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
pyinstaller build.spec

# El .exe estará en: dist/DescargadorMusicaYT.exe
```

## Estructura del proyecto

```
DescargadorMusicaYT/
├── main.py              # Punto de entrada
├── gui.py               # Interfaz gráfica
├── downloader.py        # Lógica de descarga
├── player.py            # Reproducción de audio
├── config.py            # Configuración
├── requirements.txt     # Dependencias
├── build.spec           # Configuración PyInstaller
└── README.md            # Este archivo
```

## Requisitos del sistema

- **RAM:** 512MB mínimo, 1GB+ recomendado
- **Espacio:** Depende de las canciones descargadas
- **Conexión:** Internet estable para descargar

## Solución de problemas

### FFmpeg no encontrado
```bash
winget install FFmpeg
```
O descárgalo desde: https://ffmpeg.org/download.html

### Error al descargar
- Verifica tu conexión a Internet
- Intenta con otra canción
- Asegúrate de que YouTube no esté bloqueado

### El preview no reproduce
- Verifica que pygame esté instalado
- Intenta reiniciar la aplicación

## Licencia

Este proyecto es de código abierto. Úsalo libremente.

## Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de hacer fork y enviar pull requests.

## Contacto

Para reportar bugs o sugerencias, abre un issue en GitHub.
