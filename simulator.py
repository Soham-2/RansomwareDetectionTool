#!/usr/bin/env python3
"""
simulator.py

SAFE RANSOMWARE SIMULATOR (DEMO ONLY)

This script simulates ransomware behavior by *renaming* files inside the specified folder
by appending a suffix (default: .locked). It does NOT encrypt, delete, or modify file content.

Usage:
    python simulator.py --folder ./victim_files --delay 0.2 --append .locked --limit 0

Flags:
    --folder  : target folder (default: ./victim_files)
    --delay   : seconds to wait between renames (float, default 0.2)
    --append  : suffix to append to filenames (default .locked)
    --limit   : maximum number of files to rename (0 or omitted means all files)

Safety:
- Script only acts on files inside the provided folder.
- Use LIMIT to test on a small number first.
"""

import time
from pathlib import Path
import argparse

def simulate_ransomware(folder: str, delay: float = 0.2, append: str = ".locked", limit: int = 0):
    p = Path(folder)
    if not p.exists():
        print("Error: folder does not exist:", folder)
        return
    # collect files (skip files that already have the suffix)
    files = [f for f in p.rglob("*") if f.is_file() and not f.name.endswith(append)]
    if limit and limit > 0:
        files = files[:limit]
    print(f"Simulating ransomware on {len(files)} files in {p.resolve()} (delay={delay}, append='{append}')")
    for f in files:
        try:
            new_name = f.with_name(f.name + append)
            f.rename(new_name)
            print(f"Renamed: {f.name} -> {new_name.name}")
        except Exception as e:
            print(f"Failed to rename {f}: {e}")
        time.sleep(delay)
    print("Simulation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Safe ransomware simulator (renames files only)")
    parser.add_argument("--folder", default="./victim_files", help="Folder to simulate ransomware")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay between renames in seconds")
    parser.add_argument("--append", default=".locked", help="Suffix to append to filenames")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to rename (0 for all)")
    args = parser.parse_args()
    simulate_ransomware(args.folder, args.delay, args.append, args.limit)
