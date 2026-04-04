"""
Build Script for Secure Wipe Desktop Application
Creates standalone .exe file for Windows distribution
"""

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Configuration
APP_NAME = "SecureWipe"
VERSION = "2.0.0"
MAIN_SCRIPT = "secure_wipe_desktop.py"

# Build directory cleanup
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

print("=" * 80)
print(f"Building {APP_NAME} v{VERSION}")
print("=" * 80)


# PyInstaller build configuration (avoid empty string in args)
pyi_args = [
    MAIN_SCRIPT,
    '--name=%s' % APP_NAME,
    '--onefile',
    '--windowed',
    '--icon=icon.ico',  # Professional SecureWipe icon
    '--hidden-import=PyQt6',
    '--hidden-import=PyQt6.QtCore',
    '--hidden-import=PyQt6.QtWidgets',
    '--hidden-import=PyQt6.QtGui',
    '--hidden-import=PyQt6.QtCharts',
    '--add-data=wiper_core.py:.',
    '--clean',
    '--optimize=2',
    '--log-level=INFO',
]
if os.path.exists('version_info.txt'):
    pyi_args.append('--version-file=version_info.txt')

PyInstaller.__main__.run(pyi_args)

print("\n" + "=" * 80)
print("BUILD COMPLETE!")
print("=" * 80)
print(f"\nExecutable location: dist/{APP_NAME}.exe")
print(f"File size: ~{os.path.getsize(f'dist/{APP_NAME}.exe') / (1024*1024):.1f} MB" if os.path.exists(f'dist/{APP_NAME}.exe') else "File not found")
print("\nYou can now distribute the .exe file to users!")
print("No Python installation required on target machines.")
