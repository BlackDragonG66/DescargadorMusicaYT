"""
Módulo de reproducción de audio
"""
import yt_dlp
import threading
import time
from pathlib import Path


class AudioPlayer:
    """Reproductor de audio desde YouTube"""
    
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.current_url = None
        self.current_process = None
        self.player_thread = None
        
        # Intentar importar pygame para reproducción de audio
        try:
            import pygame
            pygame.mixer.init()
            self.pygame_available = True
        except:
            self.pygame_available = False
            print("⚠️  pygame no disponible, se descargará en temp para reproducir")
    
    def play_preview(self, url, duration_limit=30):
        """
        Reproduce una vista previa de la canción (30 segundos)
        
        Args:
            url (str): URL de YouTube
            duration_limit (int): Duración máxima en segundos
            
        Returns:
            bool: True si se inició la reproducción
        """
        if self.is_playing:
            self.stop()
        
        self.current_url = url
        self.is_playing = True
        self.is_paused = False
        
        # Ejecutar reproducción en un thread separado
        self.player_thread = threading.Thread(
            target=self._play_thread,
            args=(url, duration_limit),
            daemon=True
        )
        self.player_thread.start()
        return True
    
    def _play_thread(self, url, duration_limit):
        """Hilo para reproducir audio"""
        try:
            if self.pygame_available:
                self._play_with_pygame(url, duration_limit)
            else:
                self._play_with_ffmpeg(url, duration_limit)
        except Exception as e:
            print(f"Error reproduciendo: {e}")
            self.is_playing = False
    
    def _play_with_pygame(self, url, duration_limit):
        """Reproduce usando pygame.mixer"""
        try:
            import pygame
            from pathlib import Path
            import tempfile
            
            # Crear directorio temporal si no existe
            Path('temp').mkdir(exist_ok=True)
            
            # Descargar el audio a un archivo temporal
            temp_file = Path('temp/preview_audio.webm')
            
            ydl_opts = {
                'format': 'bestaudio',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'outtmpl': str(temp_file.with_name('preview_audio')),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Encontrar el archivo descargado
                ext = info.get('ext', 'webm')
                temp_file = Path(f'temp/preview_audio.{ext}')
                
                if not temp_file.exists():
                    raise Exception("No se pudo descargar el audio temporal")
                
                # Cargar y reproducir el archivo local
                pygame.mixer.music.load(str(temp_file))
                pygame.mixer.music.play()
                
                # Reproducir durante duration_limit segundos
                elapsed = 0
                while self.is_playing and elapsed < duration_limit:
                    if not self.is_paused:
                        elapsed += 0.1
                    time.sleep(0.1)
                
                pygame.mixer.music.stop()
                
                # Eliminar archivo temporal
                try:
                    temp_file.unlink()
                except:
                    pass
                
                self.is_playing = False
        except Exception as e:
            print(f"Error con pygame: {e}")
            self.is_playing = False
    
    def _play_with_ffmpeg(self, url, duration_limit):
        """Reproducción alternativa con FFmpeg (solo descarga pequeña)"""
        try:
            import subprocess
            
            # Descargar solo los primeros segundos
            ydl_opts = {
                'format': 'bestaudio',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'outtmpl': 'temp/preview.%(ext)s',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_file = Path(f"temp/preview.{info['ext']}")
                
                if audio_file.exists():
                    # Reproducir con ffplay
                    cmd = ['ffplay', '-t', str(duration_limit), '-nodisp', '-autoexit', str(audio_file)]
                    self.current_process = subprocess.Popen(cmd)
                    self.current_process.wait()
                    audio_file.unlink()  # Eliminar archivo temporal
        except Exception as e:
            print(f"Error reproduciendo: {e}")
        finally:
            self.is_playing = False
    
    def pause(self):
        """Pausa la reproducción"""
        if self.pygame_available:
            try:
                import pygame
                if self.is_playing and not self.is_paused:
                    pygame.mixer.music.pause()
                    self.is_paused = True
            except:
                pass
    
    def resume(self):
        """Reanuda la reproducción"""
        if self.pygame_available:
            try:
                import pygame
                if self.is_playing and self.is_paused:
                    pygame.mixer.music.unpause()
                    self.is_paused = False
            except:
                pass
    
    def stop(self):
        """Detiene la reproducción"""
        self.is_playing = False
        self.is_paused = False
        self.current_url = None
        
        if self.pygame_available:
            try:
                import pygame
                pygame.mixer.music.stop()
            except:
                pass
        
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process = None
            except:
                pass
    
    def set_volume(self, volume):
        """
        Establece el volumen (0.0 a 1.0)
        
        Args:
            volume (float): Volumen (0.0 a 1.0)
        """
        if self.pygame_available:
            try:
                import pygame
                volume = max(0.0, min(1.0, volume))
                pygame.mixer.music.set_volume(volume)
            except:
                pass
