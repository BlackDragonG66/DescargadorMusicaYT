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

# Buscar FFmpeg en rutas comunes de Windows
def find_ffmpeg():
    """Busca FFmpeg en rutas comunes"""
    common_paths = [
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        os.path.expandvars(r"%PROGRAMFILES%\ffmpeg\bin\ffmpeg.exe"),
    ]
    
    # Primero intentar con shutil.which
    ffmpeg = shutil.which('ffmpeg')
    if ffmpeg:
        return ffmpeg
    
    # Si no, buscar en rutas comunes
    for path in common_paths:
        if Path(path).exists():
            return path
    
    return None

FFMPEG_PATH = find_ffmpeg()
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
