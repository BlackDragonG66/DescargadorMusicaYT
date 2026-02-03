"""
Módulo de descarga de música desde YouTube
"""
import yt_dlp
import csv
from pathlib import Path
from config import YTDLP_CONFIG, DOWNLOADS_DIR, FFMPEG_PATH


class YouTubeDownloader:
    """Descargador de música desde YouTube"""
    
    def __init__(self):
        self.ydl_opts = YTDLP_CONFIG.copy()
    
    def search_song(self, query):
        """
        Busca una canción en YouTube y retorna los resultados
        
        Args:
            query (str): Término de búsqueda
            
        Returns:
            list: Lista de diccionarios con info de resultados
        """
        try:
            search_query = f"ytsearch5:{query}"
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(search_query, download=False)
                results = []
                for entry in info.get('entries', []):
                    results.append({
                        'url': entry['webpage_url'],
                        'title': entry.get('title', 'Sin título'),
                        'duration': entry.get('duration', 0),
                        'uploader': entry.get('uploader', 'Desconocido'),
                        'views': entry.get('view_count', 0),
                    })
                return results
        except Exception as e:
            raise Exception(f"Error en la búsqueda: {str(e)}")
    
    def download_song(self, url, output_path=None):
        """
        Descarga una canción desde YouTube
        
        Args:
            url (str): URL de YouTube
            output_path (str): Ruta de salida (opcional)
            
        Returns:
            tuple: (True, mensaje) o (False, error)
        """
        try:
            opts = self.ydl_opts.copy()
            if output_path:
                opts['outtmpl'] = str(Path(output_path) / '%(title)s.%(ext)s')
            
            # Verificar FFmpeg
            if not FFMPEG_PATH:
                raise Exception("FFmpeg no está instalado. Por favor instálalo desde https://ffmpeg.org/download.html")
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return True, f"✓ Descargado: {info.get('title', 'Sin título')}"
        except Exception as e:
            return False, f"✗ Error: {str(e)}"
    
    def load_playlist_from_file(self, file_path):
        """
        Carga una lista de canciones desde un archivo CSV o TXT
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            list: Lista de canciones
        """
        songs = []
        file_path = Path(file_path)
        
        try:
            if file_path.suffix.lower() == '.csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row:  # Si la fila no está vacía
                            songs.append(row[0].strip())  # Primera columna
            elif file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        song = line.strip()
                        if song:  # Si la línea no está vacía
                            songs.append(song)
            else:
                raise ValueError("Formato no soportado. Use .txt o .csv")
            
            return songs
        except Exception as e:
            raise Exception(f"Error cargando archivo: {str(e)}")
    
    def get_downloads_folder(self):
        """Retorna la carpeta de descargas"""
        return str(DOWNLOADS_DIR)
