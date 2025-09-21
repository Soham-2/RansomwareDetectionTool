import psutil
from src.logger import logger

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        logger.info(f"🔴 Suspicious process killed: PID {pid}")
    except Exception as e:
        logger.error(f"Failed to kill process {pid}: {e}") 