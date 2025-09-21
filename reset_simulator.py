#!/usr/bin/env python3
# reset_simulator.py
# Reverts filenames that were renamed by simulator.py by removing the appended suffix.
# Usage:
#    python reset_simulator.py --folder ./victim_files --suffix .locked --dry

from pathlib import Path
import argparse

def reset(folder: str = './victim_files', suffix: str = '.locked', dry_run: bool = False):
    p = Path(folder)
    if not p.exists():
        print('Folder does not exist:', folder)
        return
    matches = [f for f in p.rglob(f'*{suffix}') if f.is_file()]
    print(f'Found {len(matches)} files with suffix "{suffix}"')
    for f in matches:
        if f.name.endswith(suffix):
            orig_name = f.name[:-len(suffix)]
            target = f.with_name(orig_name)
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
    parser.add_argument('--suffix', default='.locked', help='Suffix to remove')
    parser.add_argument('--dry', action='store_true', help='Dry run (do not rename)')
    args = parser.parse_args()
    reset(args.folder, args.suffix, args.dry)
