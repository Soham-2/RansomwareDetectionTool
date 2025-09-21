import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.detector import RansomwareDetector
from src.logger import logger

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector

    def on_moved(self, event):
        if not event.is_directory:
            old_ext = os.path.splitext(event.src_path)[1]
            new_ext = os.path.splitext(event.dest_path)[1]
            if old_ext != new_ext:
                self.detector.record_event("ext_changed", event.dest_path)
            else:
                self.detector.record_event("renamed", event.dest_path)

class DirectoryMonitor:
    def __init__(self, path):
        self.path = path
        self.detector = RansomwareDetector()
        self.observer = Observer()

    def start(self):
        logger.info(f"🔍 Monitoring started on: {self.path}")
        event_handler = FileEventHandler(self.detector)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join() 