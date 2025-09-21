#!/usr/bin/env python3
# reset_simulator.py
# Reverts filenames that were renamed by simulator.py by removing the appended suffix.
# Usage:
#    python reset_simulator.py --folder ./victim_files --suffix .locked --dry

from pathlib import Path
import argparse

ORIGINAL_EXTENSIONS = {'.txt', '.pdf', '.jpg', '.png', '.md'}

def reset(folder: str = './victim_files', dry_run: bool = False):
    p = Path(folder)
    if not p.exists():
        print('Folder does not exist:', folder)
        return

    # Collect files that have an original extension followed by an appended suffix
    files_to_reset = []
    for f in p.rglob('*'):
        if f.is_file():
            parts = f.name.split('.')
            if len(parts) > 2 and f'.{parts[-2]}' in ORIGINAL_EXTENSIONS:
                original_ext = f'.{parts[-2]}'
                # Reconstruct original name by taking parts up to the original extension
                orig_name_parts = parts[:-1] # Remove the appended suffix
                original_filename = '.'.join(orig_name_parts)
                files_to_reset.append((f, original_filename))

    print(f'Found {len(files_to_reset)} files with appended suffixes.')

    for f, original_filename in files_to_reset:
        target = f.with_name(original_filename)
        print(f"{'Would rename' if dry_run else 'Renaming'}: {f.name} -> {target.name}")
        if not dry_run:
            try:
                f.rename(target)
            except Exception as e:
                print('Failed to rename', f, e)
    print('Reset complete.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', default='./victim_files', help='Folder to reset')
    parser.add_argument('--dry', action='store_true', help='Dry run (do not rename)')
    args = parser.parse_args()
    reset(args.folder, args.dry)
