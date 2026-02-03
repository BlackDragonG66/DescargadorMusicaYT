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
        # Limpiar previamente si hay algo en reproducción
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
        temp_file = None
        wav_file = None
        
        try:
            import pygame
            from pathlib import Path
            import subprocess
            import time
            
            # Crear directorio temporal si no existe
            Path('temp').mkdir(exist_ok=True)
            
            # Limpiar archivos temporales previos
            self._cleanup_temp_files()
            time.sleep(0.2)  # Esperar a que se liberen
            
            # Descargar el audio en PEOR CALIDAD (más rápido para preview)
            ydl_opts = {
                'format': 'worstaudio/worst',  # Audio de peor calidad
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': 30,
                'outtmpl': 'temp/preview_audio',
            }
            
            print("Descargando preview...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                ext = info.get('ext', 'webm')
                print(f"Extensión detectada: {ext}")
                
                # Buscar el archivo descargado
                temp_folder = Path('temp')
                temp_file = None
                
                # Buscar archivos que comiencen con preview_audio
                for file in temp_folder.glob('preview_audio*'):
                    if file.is_file():
                        temp_file = file
                        print(f"Archivo encontrado: {temp_file}")
                        break
                
                if not temp_file or not temp_file.exists():
                    print(f"Error: No se encontró archivo en temp. Archivos: {list(temp_folder.glob('*'))}")
                    raise Exception("No se pudo descargar el audio temporal")
                
                # Convertir a WAV si no es formato compatible
                wav_file = temp_folder / 'preview_audio.wav'
                if temp_file.suffix.lower() not in ['.wav', '.mp3', '.ogg']:
                    print(f"Convirtiendo {temp_file.suffix} a WAV...")
                    try:
                        # Usar ffmpeg para convertir
                        cmd = ['ffmpeg', '-i', str(temp_file), '-q:a', '9', '-y', str(wav_file)]
                        result = subprocess.run(cmd, capture_output=True, timeout=30)
                        if result.returncode != 0:
                            print(f"Error en conversión: {result.stderr.decode()}")
                        
                        if wav_file.exists():
                            try:
                                temp_file.unlink()  # Eliminar original
                            except:
                                pass
                            temp_file = wav_file
                            print(f"Conversión completada: {wav_file}")
                    except Exception as e:
                        print(f"Error convirtiendo: {e}")
                        # Continuar con el archivo original
                
                print(f"Cargando: {temp_file}")
                
                # Cargar y reproducir
                try:
                    pygame.mixer.music.load(str(temp_file))
                    pygame.mixer.music.play()
                    print("Reproduciendo...")
                    
                    # Reproducir durante duration_limit segundos
                    elapsed = 0
                    while self.is_playing and elapsed < duration_limit:
                        if not self.is_paused:
                            elapsed += 0.1
                        time.sleep(0.1)
                except pygame.error as e:
                    print(f"Error pygame: {e}")
                    raise
                finally:
                    # Asegurar que se detiene
                    try:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                    except:
                        pass
                
                print("Reproducción completada")
                
        except Exception as e:
            print(f"Error con pygame: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_playing = False
            
            # Limpiar archivos con reintentos
            if temp_file and temp_file.exists():
                for attempt in range(5):
                    try:
                        temp_file.unlink()
                        print(f"Archivo temporal eliminado: {temp_file}")
                        break
                    except PermissionError:
                        print(f"Archivo en uso, reintentando... ({attempt+1}/5)")
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Error eliminando {temp_file}: {e}")
                        break
            
            if wav_file and wav_file.exists():
                for attempt in range(5):
                    try:
                        wav_file.unlink()
                        print(f"Archivo WAV eliminado: {wav_file}")
                        break
                    except PermissionError:
                        print(f"Archivo WAV en uso, reintentando... ({attempt+1}/5)")
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Error eliminando {wav_file}: {e}")
                        break
    
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
                pygame.mixer.music.unload()  # Descargar para liberar archivo
            except:
                pass
        
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process = None
            except:
                pass
        
        # Limpiar archivos temporales
        self._cleanup_temp_files()
    
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
    
    def _cleanup_temp_files(self):
        """Limpia archivos temporales de forma segura"""
        from pathlib import Path
        import time
        
        temp_folder = Path('temp')
        if not temp_folder.exists():
            return
        
        # Archivos a limpiar
        patterns = ['preview_audio*']
        
        for pattern in patterns:
            for file in temp_folder.glob(pattern):
                if file.is_file():
                    try:
                        # Esperar a que se libere el archivo
                        for attempt in range(5):
                            try:
                                file.unlink()
                                print(f"Archivo temporal eliminado: {file}")
                                break
                            except PermissionError:
                                print(f"Archivo en uso, reintentando... ({attempt+1}/5)")
                                time.sleep(0.5)
                            except Exception as e:
                                print(f"Error eliminando {file}: {e}")
                                break
                    except Exception as e:
                        print(f"No se pudo limpiar {file}: {e}")
