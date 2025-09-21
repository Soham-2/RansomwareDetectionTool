import time
from src.detector import RansomwareDetector

def test_rename_detection():
    detector = RansomwareDetector()
    for _ in range(6):
        detector.record_event("renamed", "file.txt")
        time.sleep(1)

def test_ext_change_detection():
    detector = RansomwareDetector()
    for _ in range(6):
        detector.record_event("ext_changed", "file.locked")
        time.sleep(1) 