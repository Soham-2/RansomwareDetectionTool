import time
import os
from collections import defaultdict
from src.logger import logger
from src.config import MAX_RENAMES, MAX_EXT_CHANGES
from plyer import notification
import winsound

CRITICAL_SOUND_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "critical_alert.wav")

class RansomwareDetector:
    def __init__(self):
        self.file_events = defaultdict(list)

    def record_event(self, event_type, file_path):
        now = time.time()
        self.file_events[event_type].append(now)
        logger.info(f"Event: '{event_type}' on file: {file_path}")
        # Keep only last 10 seconds of events
        self.file_events[event_type] = [t for t in self.file_events[event_type] if now - t <= 10]
        self.analyze(event_type, file_path)

    def analyze(self, event_type, file_path):
        if event_type == "renamed" and len(self.file_events["renamed"]) > MAX_RENAMES:
            message = f"⚠️ Potential ransomware detected: too many renames. Last file: {file_path}"
            logger.warning(message)
            try:
                notification.notify(
                    title='Ransomware ALERT!',
                    message=message,
                    app_name='Ransomware Detector',
                    timeout=30 # seconds
                )
            except Exception as e:
                logger.error(f"Failed to send ransomware detected notification: {e}")
            try:
                winsound.PlaySound(CRITICAL_SOUND_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                logger.error(f"Failed to play critical alert sound: {e}")
        elif event_type == "ext_changed" and len(self.file_events["ext_changed"]) > MAX_EXT_CHANGES:
            message = f"⚠️ Potential ransomware detected: too many extension changes. Last file: {file_path}"
            logger.warning(message)
            try:
                notification.notify(
                    title='Ransomware ALERT!',
                    message=message,
                    app_name='Ransomware Detector',
                    timeout=30 # seconds
                )
            except Exception as e:
                logger.error(f"Failed to send ransomware detected notification: {e}")
            try:
                winsound.PlaySound(CRITICAL_SOUND_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                logger.error(f"Failed to play critical alert sound: {e}") 