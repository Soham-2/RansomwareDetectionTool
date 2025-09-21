import os

# Directory to monitor (victim_files folder inside project)
MONITOR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "victim_files")

# Thresholds for suspicious behavior
MAX_RENAMES = 5     # within 10 seconds
MAX_EXT_CHANGES = 5 # within 10 seconds 