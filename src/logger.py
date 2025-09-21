import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "detections.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("RansomwareDetector") 