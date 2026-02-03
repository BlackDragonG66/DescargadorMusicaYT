"""
Configuración de la aplicación
"""
import os
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "descargas"
TEMP_DIR = BASE_DIR / "temp"

# Crear directorios si no existen
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Configuración de yt-dlp
YTDLP_CONFIG = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),
    'quiet': False,
    'no_warnings': False,
    'socket_timeout': 30,
}

# Configuración de búsqueda
SEARCH_LIMIT = 5  # Máximo de resultados a mostrar
AUTO_SELECT_FIRST = False  # Si es True, descarga automáticamente el primer resultado
