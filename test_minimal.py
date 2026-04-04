"""Minimal test to isolate crash in secure_wipe_desktop.py"""
import sys
import os
os.environ["QT_OPENGL"] = "software"

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)
win = QMainWindow()
win.setWindowTitle("Test")
win.setGeometry(100, 100, 400, 300)
label = QLabel("If you see this, PyQt6 rendering works!")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
win.setCentralWidget(label)
print("[1] About to show...", flush=True)
win.show()
print("[2] Window shown!", flush=True)
sys.exit(app.exec())
