from pathlib import Path
from shutil import * 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

path_to_watch = str(Path.home() / "Downloads")

file_list = {
    "Imagens": ['.jpeg', '.png', '.jpg', '.svg'],
    "Vídeos": ['.avi', '.mp4', '.mov', '.mkv'],
    "Documentos": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    "Músicas": ['.mp3', '.ogg', '.wav', '.amr'],
    "Compactados": ['.zip', '.gz', '.tar', '.rar'],
    "Executaveis": ['.exe', '.msi', '.sh', '.rpm', '.appImage'] 
}

class HandlerOrganizer(FileSystemEventHandler):
    def on_modified(self, event):
        filename = Path(event.src_path).name
        if filename.startswith('.'):
            return
        
        if event.is_directory:
            return
        
        if event.src_path.endswith(('crdownload', 'pm1hps', 'part', 'tmp', 'partial', 'download', '.filepart', '.partialdownload')):
            return
        
        file_extension = Path(event.src_path).suffix.lower()
        file_path = Path(event.src_path)
        
        print(f"Detected file: {file_path.name} with extension: {file_extension}")
        
        category = self.descover_category(file_extension)
        print(f"File categorized under: {category}")
        
        if category == "Others":
            target_dir = Path(path_to_watch) / "Others"
        else:
            target_dir = Path.home() / category
        
        target_dir.mkdir(exist_ok=True)
        final_path = target_dir / file_path.name
        
        cont = 1
        while final_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            
            new_name = f"{stem}({cont}){suffix}"
            final_path = target_dir / new_name
            cont += 1
        
        move(str(file_path), str(final_path))
        print(f"Moved file to: {final_path}")
        
    def descover_category(self, extension):
        for category, list_of_extensions in file_list.items():
            if extension in list_of_extensions:
                return category
        return "Others"

if __name__ == "__main__":
    event_handler = HandlerOrganizer()
    Observer = Observer()
    Observer.schedule(event_handler, path=path_to_watch, recursive=False)
    Observer.start()
    
    print(f"Monitoring started on: {path_to_watch}")
    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        Observer.stop()
    Observer.join()