import logging
from src.monitor import DirectoryMonitor
from src.config import MONITOR_PATH
from plyer import notification
from src.logger import logger

if __name__ == "__main__":
    monitor = DirectoryMonitor(MONITOR_PATH)
    try:
        notification.notify(
            title='Ransomware Detector',
            message=f'🔍 Monitoring started on: {MONITOR_PATH}',
            app_name='Ransomware Detector',
            timeout=30 # seconds
        )
    except Exception as e:
        logger.error(f"Failed to send startup notification: {e}")
    monitor.start() 