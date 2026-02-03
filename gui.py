"""
Interfaz gráfica de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from downloader import YouTubeDownloader
from player import AudioPlayer
from config import AUTO_SELECT_FIRST, DOWNLOADS_DIR
import threading


class MusicDownloaderGUI:
    """Interfaz gráfica del descargador de música"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Música de YouTube")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        self.downloader = YouTubeDownloader()
        self.player = AudioPlayer()
        self.current_results = []
        self.selected_result = None
        self.queue = []
        self.is_downloading = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos para que los elementos se expandan
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(2, weight=2)  # Resultados
        main_frame.rowconfigure(3, weight=2)  # Info
        
        # Título
        title = ttk.Label(main_frame, text="🎵 Descargador de Música YouTube", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Búsqueda", padding="10")
        search_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(search_frame, text="Canción:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.search_entry.bind('<Return>', lambda e: self.search_song())
        
        ttk.Button(search_frame, text="Buscar", command=self.search_song).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Cargar CSV/TXT", command=self.load_playlist).grid(row=0, column=3, padx=5)
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Listbox con scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.results_listbox = tk.Listbox(results_frame, yscrollcommand=scrollbar.set, height=10)
        self.results_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_listbox.bind('<<ListboxSelect>>', self.on_result_select)
        scrollbar.config(command=self.results_listbox.yview)
        
        # Frame de información del resultado seleccionado
        info_frame = ttk.LabelFrame(main_frame, text="Información del Video", padding="10")
        info_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, width=80)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de controles de reproducción
        player_frame = ttk.LabelFrame(main_frame, text="Reproducción", padding="10")
        player_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        self.play_btn = ttk.Button(player_frame, text="▶ Play (30s)", command=self.play_preview, width=15)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(player_frame, text="⏸ Pausa", command=self.pause_player, width=15, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(player_frame, text="⏹ Detener", command=self.stop_player, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(player_frame, text="Volumen:").pack(side=tk.LEFT, padx=5)
        self.volume_slider = ttk.Scale(player_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                       command=self.set_volume, length=150)
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        
        self.player_status = ttk.Label(player_frame, text="Listo", foreground="green")
        self.player_status.pack(side=tk.RIGHT, padx=5)
        
        # Frame de cola de descargas
        queue_frame = ttk.LabelFrame(main_frame, text="Cola de Descargas", padding="10")
        queue_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(queue_frame, text="+ Agregar a Cola", command=self.add_to_queue).pack(side=tk.LEFT, padx=5)
        ttk.Button(queue_frame, text="✓ Descargar Cola", command=self.start_download_queue).pack(side=tk.LEFT, padx=5)
        ttk.Button(queue_frame, text="Limpiar Cola", command=self.clear_queue).pack(side=tk.LEFT, padx=5)
        
        self.queue_label = ttk.Label(queue_frame, text="Canciones en cola: 0")
        self.queue_label.pack(side=tk.RIGHT, padx=5)
        
        # Frame de opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
        options_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(options_frame, text="Ruta de descarga:").grid(row=0, column=0, sticky=tk.W)
        self.download_path = ttk.Entry(options_frame, width=50)
        self.download_path.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.download_path.insert(0, str(DOWNLOADS_DIR))
        
        ttk.Button(options_frame, text="Cambiar", command=self.select_download_path).grid(row=0, column=2, padx=5)
        
        # Frame de estado
        status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
        status_frame.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Listo", foreground="green")
        self.status_label.pack(pady=5)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
    
    def search_song(self):
        """Busca una canción"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Advertencia", "Ingresa un término de búsqueda")
            return
        
        self.update_status("Buscando...", "blue")
        self.progress.start()
        
        def search_thread():
            try:
                self.current_results = self.downloader.search_song(query)
                self.display_results()
                self.update_status("Búsqueda completada", "green")
            except Exception as e:
                messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")
                self.update_status("Error en búsqueda", "red")
            finally:
                self.progress.stop()
        
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def display_results(self):
        """Muestra los resultados en la listbox"""
        self.results_listbox.delete(0, tk.END)
        for i, result in enumerate(self.current_results, 1):
            duration = self._format_duration(result['duration'])
            display_text = f"{i}. {result['title'][:60]} ({duration}) - {result['uploader'][:30]}"
            self.results_listbox.insert(tk.END, display_text)
    
    def _format_duration(self, seconds):
        """Formatea duración en minutos:segundos"""
        if not seconds:
            return "N/A"
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    def on_result_select(self, event):
        """Cuando se selecciona un resultado"""
        selection = self.results_listbox.curselection()
        if selection:
            idx = selection[0]
            self.selected_result = self.current_results[idx]
            self.display_result_info()
    
    def display_result_info(self):
        """Muestra información del resultado seleccionado"""
        if not self.selected_result:
            return
        
        self.info_text.delete(1.0, tk.END)
        info = self.selected_result
        
        text = f"""Título: {info['title']}
Duración: {self._format_duration(info['duration'])}
Uploader: {info['uploader']}
Visualizaciones: {info['views']:,}
URL: {info['url']}"""
        
        self.info_text.insert(tk.END, text)
    
    def play_preview(self):
        """Reproduce una vista previa de 30 segundos"""
        if not self.selected_result:
            messagebox.showwarning("Advertencia", "Selecciona un resultado primero")
            return
        
        # Deshabilitar botones
        self.play_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.update_player_status("Cargando preview...", "blue")
        
        def play_thread():
            try:
                self.player.play_preview(self.selected_result['url'], duration_limit=30)
                
                # Habilitar botones después de que se cargue
                self.play_btn.config(state=tk.NORMAL)
                self.pause_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.NORMAL)
                
                self.update_player_status("Reproduciendo...", "green")
            except Exception as e:
                messagebox.showerror("Error", f"Error reproduciendo: {str(e)}")
                self.update_player_status("Error", "red")
                # Re-habilitar botones aunque falle
                self.play_btn.config(state=tk.NORMAL)
                self.pause_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=play_thread, daemon=True)
        thread.start()
    
    def pause_player(self):
        """Pausa la reproducción"""
        if self.player.is_playing:
            if self.player.is_paused:
                self.player.resume()
                self.update_player_status("Reanudando...", "green")
            else:
                self.player.pause()
                self.update_player_status("Pausado", "orange")
    
    def stop_player(self):
        """Detiene la reproducción"""
        self.player.stop()
        self.update_player_status("Detenido", "red")
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
    
    def set_volume(self, value):
        """Establece el volumen"""
        vol = int(float(value))
        self.player.set_volume(vol / 100.0)
    
    def update_player_status(self, message, color="black"):
        """Actualiza el estado del reproductor"""
        self.player_status.config(text=message, foreground=color)
        self.root.update_idletasks()
    
    def add_to_queue(self):
        """Agrega el resultado seleccionado a la cola"""
        if not self.selected_result:
            messagebox.showwarning("Advertencia", "Selecciona un resultado primero")
            return
        
        self.queue.append(self.selected_result)
        self.update_queue_label()
        messagebox.showinfo("Éxito", f"Agregado: {self.selected_result['title']}")
    
    def update_queue_label(self):
        """Actualiza el label de la cola"""
        self.queue_label.config(text=f"Canciones en cola: {len(self.queue)}")
    
    def clear_queue(self):
        """Limpia la cola de descargas"""
        self.queue = []
        self.update_queue_label()
        messagebox.showinfo("Éxito", "Cola limpiada")
    
    def start_download_queue(self):
        """Inicia la descarga de la cola"""
        if not self.queue:
            messagebox.showwarning("Advertencia", "No hay canciones en la cola")
            return
        
        self.is_downloading = True
        self.progress.start()
        
        def download_thread():
            for i, song in enumerate(self.queue, 1):
                self.update_status(f"Descargando {i}/{len(self.queue)}: {song['title'][:50]}", "blue")
                success, message = self.downloader.download_song(
                    song['url'],
                    self.download_path.get()
                )
                if success:
                    self.update_status(message, "green")
                else:
                    self.update_status(message, "red")
                    messagebox.showerror("Error", message)
            
            self.is_downloading = False
            self.progress.stop()
            self.queue = []
            self.update_queue_label()
            self.update_status("Descargas completadas", "green")
            messagebox.showinfo("Éxito", "Todas las descargas completadas")
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def load_playlist(self):
        """Carga una lista de canciones desde archivo"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            songs = self.downloader.load_playlist_from_file(file_path)
            self.queue = []
            
            self.update_status(f"Buscando {len(songs)} canciones...", "blue")
            self.progress.start()
            
            def load_thread():
                for song_name in songs:
                    try:
                        results = self.downloader.search_song(song_name)
                        if results:
                            if AUTO_SELECT_FIRST:
                                self.queue.append(results[0])
                            else:
                                self.queue.append(results[0])  # Agrega el primero por defecto
                    except Exception as e:
                        print(f"Error buscando {song_name}: {e}")
                
                self.progress.stop()
                self.update_queue_label()
                self.update_status(f"Cargadas {len(self.queue)} canciones", "green")
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.queue)} canciones en la cola")
            
            thread = threading.Thread(target=load_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando archivo: {str(e)}")
    
    def select_download_path(self):
        """Selecciona la ruta de descarga"""
        path = filedialog.askdirectory(title="Selecciona carpeta de descargas")
        if path:
            self.download_path.delete(0, tk.END)
            self.download_path.insert(0, path)
    
    def update_status(self, message, color="black"):
        """Actualiza el estado"""
        self.status_label.config(text=message, foreground=color)
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = MusicDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    
    def setup_ui(self):
        """Configura la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title = ttk.Label(main_frame, text="🎵 Descargador de Música YouTube", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Búsqueda", padding="10")
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(search_frame, text="Canción:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.search_entry.bind('<Return>', lambda e: self.search_song())
        
        ttk.Button(search_frame, text="Buscar", command=self.search_song).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Cargar CSV/TXT", command=self.load_playlist).grid(row=0, column=3, padx=5)
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Listbox con scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.results_listbox = tk.Listbox(results_frame, yscrollcommand=scrollbar.set, height=8)
        self.results_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_listbox.bind('<<ListboxSelect>>', self.on_result_select)
        scrollbar.config(command=self.results_listbox.yview)
        
        # Frame de información del resultado seleccionado
        info_frame = ttk.LabelFrame(main_frame, text="Información del Video", padding="10")
        info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=4, width=80)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de cola de descargas
        queue_frame = ttk.LabelFrame(main_frame, text="Cola de Descargas", padding="10")
        queue_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(queue_frame, text="+ Agregar a Cola", command=self.add_to_queue).pack(side=tk.LEFT, padx=5)
        ttk.Button(queue_frame, text="✓ Descargar Cola", command=self.start_download_queue).pack(side=tk.LEFT, padx=5)
        ttk.Button(queue_frame, text="Limpiar Cola", command=self.clear_queue).pack(side=tk.LEFT, padx=5)
        
        self.queue_label = ttk.Label(queue_frame, text="Canciones en cola: 0")
        self.queue_label.pack(side=tk.RIGHT, padx=5)
        
        # Frame de opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
        options_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(options_frame, text="Ruta de descarga:").grid(row=0, column=0, sticky=tk.W)
        self.download_path = ttk.Entry(options_frame, width=50)
        self.download_path.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.download_path.insert(0, str(DOWNLOADS_DIR))
        
        ttk.Button(options_frame, text="Cambiar", command=self.select_download_path).grid(row=0, column=2, padx=5)
        
        # Frame de estado
        status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
        status_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Listo", foreground="green")
        self.status_label.pack(pady=5)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
    
    def search_song(self):
        """Busca una canción"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Advertencia", "Ingresa un término de búsqueda")
            return
        
        self.update_status("Buscando...", "blue")
        self.progress.start()
        
        def search_thread():
            try:
                self.current_results = self.downloader.search_song(query)
                self.display_results()
                self.update_status("Búsqueda completada", "green")
            except Exception as e:
                messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")
                self.update_status("Error en búsqueda", "red")
            finally:
                self.progress.stop()
        
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def display_results(self):
        """Muestra los resultados en la listbox"""
        self.results_listbox.delete(0, tk.END)
        for i, result in enumerate(self.current_results, 1):
            duration = self._format_duration(result['duration'])
            display_text = f"{i}. {result['title'][:60]} ({duration}) - {result['uploader'][:30]}"
            self.results_listbox.insert(tk.END, display_text)
    
    def _format_duration(self, seconds):
        """Formatea duración en minutos:segundos"""
        if not seconds:
            return "N/A"
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    def on_result_select(self, event):
        """Cuando se selecciona un resultado"""
        selection = self.results_listbox.curselection()
        if selection:
            idx = selection[0]
            self.selected_result = self.current_results[idx]
            self.display_result_info()
    
    def display_result_info(self):
        """Muestra información del resultado seleccionado"""
        if not self.selected_result:
            return
        
        self.info_text.delete(1.0, tk.END)
        info = self.selected_result
        
        text = f"""Título: {info['title']}
Duración: {self._format_duration(info['duration'])}
Uploader: {info['uploader']}
Visualizaciones: {info['views']:,}
URL: {info['url']}"""
        
        self.info_text.insert(tk.END, text)
    
    def add_to_queue(self):
        """Agrega el resultado seleccionado a la cola"""
        if not self.selected_result:
            messagebox.showwarning("Advertencia", "Selecciona un resultado primero")
            return
        
        self.queue.append(self.selected_result)
        self.update_queue_label()
        messagebox.showinfo("Éxito", f"Agregado: {self.selected_result['title']}")
    
    def update_queue_label(self):
        """Actualiza el label de la cola"""
        self.queue_label.config(text=f"Canciones en cola: {len(self.queue)}")
    
    def clear_queue(self):
        """Limpia la cola de descargas"""
        self.queue = []
        self.update_queue_label()
        messagebox.showinfo("Éxito", "Cola limpiada")
    
    def start_download_queue(self):
        """Inicia la descarga de la cola"""
        if not self.queue:
            messagebox.showwarning("Advertencia", "No hay canciones en la cola")
            return
        
        self.is_downloading = True
        self.progress.start()
        
        def download_thread():
            for i, song in enumerate(self.queue, 1):
                self.update_status(f"Descargando {i}/{len(self.queue)}: {song['title'][:50]}", "blue")
                success, message = self.downloader.download_song(
                    song['url'],
                    self.download_path.get()
                )
                if success:
                    self.update_status(message, "green")
                else:
                    self.update_status(message, "red")
                    messagebox.showerror("Error", message)
            
            self.is_downloading = False
            self.progress.stop()
            self.queue = []
            self.update_queue_label()
            self.update_status("Descargas completadas", "green")
            messagebox.showinfo("Éxito", "Todas las descargas completadas")
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def load_playlist(self):
        """Carga una lista de canciones desde archivo"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            songs = self.downloader.load_playlist_from_file(file_path)
            self.queue = []
            
            self.update_status(f"Buscando {len(songs)} canciones...", "blue")
            self.progress.start()
            
            def load_thread():
                for song_name in songs:
                    try:
                        results = self.downloader.search_song(song_name)
                        if results:
                            if AUTO_SELECT_FIRST:
                                self.queue.append(results[0])
                            else:
                                self.queue.append(results[0])  # Agrega el primero por defecto
                    except Exception as e:
                        print(f"Error buscando {song_name}: {e}")
                
                self.progress.stop()
                self.update_queue_label()
                self.update_status(f"Cargadas {len(self.queue)} canciones", "green")
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.queue)} canciones en la cola")
            
            thread = threading.Thread(target=load_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando archivo: {str(e)}")
    
    def select_download_path(self):
        """Selecciona la ruta de descarga"""
        path = filedialog.askdirectory(title="Selecciona carpeta de descargas")
        if path:
            self.download_path.delete(0, tk.END)
            self.download_path.insert(0, path)
    
    def update_status(self, message, color="black"):
        """Actualiza el estado"""
        self.status_label.config(text=message, foreground=color)
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = MusicDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
