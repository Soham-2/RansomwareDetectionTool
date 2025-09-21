#!/usr/bin/env python3
# create_samples.py
# Creates safe dummy files inside victim_files/ for demo.

from pathlib import Path
import random
import string

SAMPLES_DIR = Path("./victim_files")
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

def random_text(n=64):
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=n))

def create_text_file(name, lines=4):
    p = SAMPLES_DIR / name
    with p.open('w', encoding='utf-8') as f:
        for _ in range(lines):
            f.write(random_text(80) + '\n')
    print('Created', p)

def create_dummy_binary(name, size_kb=1):
    p = SAMPLES_DIR / name
    # create pseudo-binary by writing bytes
    with p.open('wb') as f:
        for _ in range(size_kb * 1024):
            f.write(bytes([random.getrandbits(8)]))
    print('Created', p)

if __name__ == '__main__':
    create_text_file('note1.txt', lines=4)
    create_text_file('note2.txt', lines=3)
    create_text_file('doc1.pdf', lines=2)
    create_dummy_binary('image1.jpg', size_kb=2)
    create_dummy_binary('image2.png', size_kb=2)
    print('Sample files created in', SAMPLES_DIR.resolve())
