"""
Test File Generator — Secure Wipe Demo
Creates a large dummy file so you can test the wipe + monitoring panel.
Run: python create_test_file.py
"""

import os
import sys
import time
import random
import argparse

def create_test_file(path: str, size_mb: int = 100):
    size_bytes = size_mb * 1024 * 1024
    chunk      = 1024 * 1024  # 1 MB per write

    print(f"\n{'='*55}")
    print(f"  Creating test file: {path}")
    print(f"  Size: {size_mb} MB  ({size_bytes:,} bytes)")
    print(f"{'='*55}\n")

    start = time.time()
    written = 0

    with open(path, "wb") as f:
        while written < size_bytes:
            to_write = min(chunk, size_bytes - written)
            # Mix of zeros + random bytes so it looks like real data
            data = os.urandom(to_write)
            f.write(data)
            written += to_write

            pct = written / size_bytes * 100
            bar = int(pct / 2)
            print(f"\r  [{('█' * bar).ljust(50)}] {pct:5.1f}%  "
                  f"{written/1024/1024:.1f}/{size_mb} MB", end="", flush=True)

    elapsed = time.time() - start
    speed   = size_mb / elapsed if elapsed > 0 else 0
    print(f"\n\n  ✅ Done in {elapsed:.1f}s  ({speed:.1f} MB/s)")
    print(f"  File: {os.path.abspath(path)}")
    print(f"\n{'='*55}")
    print("  NOW: Open the app → Secure Wipe → Browse → select this file")
    print("       Then go to 📊 Monitoring while the wipe runs!")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a large test file for wipe testing")
    parser.add_argument("--size",  type=int,  default=100,
                        help="Size in MB (default: 100)")
    parser.add_argument("--path",  type=str,  default="test_files/test_wipe_100MB.dat",
                        help="Output file path")
    args = parser.parse_args()

    # Make sure output folder exists
    folder = os.path.dirname(args.path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    create_test_file(args.path, args.size)
