"""
Configuración de la aplicación
"""
import os
import shutil
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "descargas"
TEMP_DIR = BASE_DIR / "temp"

# Crear directorios si no existen
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Verificar FFmpeg
FFMPEG_PATH = shutil.which('ffmpeg')
FFPROBE_PATH = shutil.which('ffprobe')

if not FFMPEG_PATH:
    print("⚠️  Advertencia: FFmpeg no se encontró en el PATH")
    print("Descárgalo desde: https://ffmpeg.org/download.html")

# Configuración de yt-dlp con FFmpeg explícito
YTDLP_CONFIG = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        'nopostoverwrites': False,
    }],
    'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),
    'quiet': False,
    'no_warnings': False,
    'socket_timeout': 30,
    'progress_hooks': [],
    'ffmpeg_location': FFMPEG_PATH if FFMPEG_PATH else None,
}

# Configuración de búsqueda
SEARCH_LIMIT = 5  # Máximo de resultados a mostrar
AUTO_SELECT_FIRST = False  # Si es True, descarga automáticamente el primer resultado
