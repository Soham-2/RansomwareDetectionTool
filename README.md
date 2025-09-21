# Ransomware Detection Tool

## Overview
This project is a Python-based ransomware detection system designed to monitor a specified directory for suspicious file activities. It detects patterns indicative of ransomware, such as rapid file renames and extension changes, and provides immediate alerts.

**Key Features:**
- **Real-time Monitoring:** Continuously watches a target directory for file system events.
- **Ransomware Pattern Detection:** Identifies suspicious bursts of file renaming and extension modification.
- **Desktop Notifications:** Provides Windows popup notifications for both successful program startup and detected ransomware activity.
- **Auditory Alerts:** Plays a custom, alarming sound (`critical_alert.wav`) when potential ransomware is detected.
- **Safe Simulation Tools:** Includes scripts to safely simulate ransomware behavior and manage sample files for testing.

## Project Structure

```
.
├── logs/                         # Stores detection logs (detections.log)
├── src/
│   ├── __init__.py               # Python package initializer
│   ├── actions.py                # Contains potential actions (e.g., kill_process - currently not integrated into detection flow)
│   ├── config.py                 # Configuration settings (monitor path, detection thresholds)
│   ├── detector.py               # Core logic for detecting suspicious file activity
│   ├── logger.py                 # Configures logging for the application
│   └── monitor.py                # Sets up file system monitoring using watchdog
├── tests/                        # Unit tests for detector and monitor
├── victim_files/                 # Directory to monitor and simulate attacks on
│   ├── doc1.pdf                  # Sample PDF file (placeholder)
│   ├── image1.jpg                # Sample JPG image file (placeholder)
│   ├── image2.png                # Sample PNG image file (placeholder)
│   ├── note1.txt                 # Sample text file
│   ├── note2.txt                 # Sample text file
│   └── README.md                 # Information about the sample files
├── critical_alert.wav            # Custom sound file for ransomware detection alerts
├── create_samples.py             # Helper script to generate dummy sample files in victim_files/
├── main.py                       # Main entry point of the detector application
├── README.md                     # This documentation file
├── requirements.txt              # Python dependency list
├── reset_simulator.py            # Helper script to revert changes made by the simulator
└── simulator.py                  # Safe ransomware simulation script
```

## How it Works

1.  **`main.py`**: Initiates the `DirectoryMonitor`, which starts observing the `victim_files` directory. Upon startup, it sends a Windows desktop notification.
2.  **`src/monitor.py`**: Uses `watchdog` to listen for file system events (specifically `on_moved`, which covers both renames and extension changes). When an event occurs, it analyzes whether the file's extension has changed or if it was merely renamed.
3.  **`src/detector.py`**: Receives file events from the monitor. It tracks the frequency of renames and extension changes within a 10-second window. If a predefined threshold (`MAX_RENAMES` or `MAX_EXT_CHANGES` from `src/config.py`) is exceeded, it:
    *   Logs a `WARNING` message to `logs/detections.log` and the console.
    *   Triggers a Windows popup notification titled "Ransomware ALERT!" with details of the suspicious activity.
    *   Plays the `critical_alert.wav` sound file for an audible alert.
4.  **`src/logger.py`**: Ensures all events and warnings are recorded with timestamps, log levels, and detailed messages, both in the terminal and in `detections.log`.
5.  **`src/actions.py`**: Provides a `kill_process` function, which can be integrated for automated responses to detected threats (currently not actively used in the main detection loop).

## Usage (Recommended Demo Workflow)

To test the ransomware detection tool with the included simulator:

1.  **Install Dependencies:**
    Open your terminal in the project's root directory and run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Create Sample Files:**
    Ensure your `victim_files` directory contains the necessary sample files by running:
    ```bash
    python create_samples.py
    ```
    (This will create/re-create `note1.txt`, `note2.txt`, `doc1.pdf`, `image1.jpg`, `image2.png`, and a `README.md` within `victim_files/`).

3.  **Place Custom Alert Sound:**
    Make sure you have an alarming `.wav` audio file named `critical_alert.wav` placed directly in the project's root directory.

4.  **Start the Detector (in Terminal A):**
    Open your primary terminal (Terminal A) in the project's root directory and run the main detector script. You should see a Windows notification pop up confirming monitoring has started.
    ```bash
    python main.py
    ```

5.  **Simulate a Ransomware Attack (in a separate Terminal B):**
    Open a *new* terminal window (Terminal B), navigate to the project's root directory, and run the simulator script. This will rapidly rename files in `victim_files/` by appending `.locked`.
    ```bash
    python simulator.py --folder ./victim_files --delay 0.2 --append .locked
    ```
    *   To test on a smaller set of files, you can add `--limit N` (e.g., `--limit 3`).
    *   To simulate different extension changes, modify the `--append` flag (e.g., `--append .encrypted`).

6.  **Observe Detector Output & Alerts:**
    *   In **Terminal A**, you will see log messages indicating file events and warnings when ransomware-like activity is detected.
    *   You will receive **Windows popup notifications** ("Ransomware ALERT!") for each detection.
    *   You will hear the **`critical_alert.wav` sound** playing with each ransomware detection notification.
    *   For detailed event logs, check `logs/detections.log`.

7.  **Reset Filenames (After Demo):**
    After the simulation, you can revert the renamed files to their original names by running this in **Terminal B**:
    ```bash
    python reset_simulator.py
    ```
    *   Use `--dry` to preview changes first: `python reset_simulator.py --dry`

## Safety Notes
- These scripts are designed for **demonstration purposes ONLY**.
- They act strictly **ONLY inside the specified folder** (default: `./victim_files`).
- **DO NOT run the simulator on important or sensitive directories.**
- The simulator (`simulator.py`) **only renames files**; it does NOT perform encryption, deletion, or content modification of your actual files. 

## Flowchart


```mermaid
flowchart TD
  Start([Start])
  Main[/"main.py\n(start & Windows startup notif)"/]
  Monitor[/"DirectoryMonitor\n(src/monitor.py)\nwatchdog -> on_moved"/]
  Event{File moved/renamed\n(on_moved event)}
  Analyze["src/detector.py\nanalyze event"]
  Type{Extension changed\nor simple rename?}
  ExtCount["Track extension-changes\n(sliding 10s window)"]
  RenCount["Track renames\n(sliding 10s window)"]
  Check{Threshold exceeded?\n(MAX_EXT_CHANGES / MAX_RENAMES)}
  NoLog[/"Log INFO (terminal)\n& continue monitoring"/]
  YesAlert["ALERT: actions\n- log WARNING -> logs/detections.log\n- Windows popup: 'Ransomware ALERT!'\n- play critical_alert.wav\n- (optional) kill_process from src/actions.py"]
  Simulator[/simulator.py\n(safe rapid rename -> .locked)/]
  CreateSamples[/"create_samples.py\n(generate victim_files/)"/]
  ResetSim["reset_simulator.py\n(revert filenames)"]
  End([Monitoring continues])

  Start --> Main --> Monitor
  Monitor --> Event --> Analyze --> Type
  Type -->|extension changed| ExtCount --> Check
  Type -->|renamed| RenCount --> Check
  Check -->|no| NoLog --> End
  Check -->|yes| YesAlert --> End

  %% Auxiliary/test tools
  CreateSamples -.-> Monitor
  Simulator -.-> Monitor
  YesAlert -.-> ResetSim
