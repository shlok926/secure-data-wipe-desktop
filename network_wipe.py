"""
Network Wipe — Remote file/folder wiping via SSH
Securely wipes files on remote Linux/macOS machines using 'shred'.
Requires: pip install paramiko
"""

import threading
import time
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTextEdit, QFormLayout,
    QProgressBar, QFrame, QCheckBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QFont

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False


# ---------------------------------------------------------------------------
# Worker thread — runs SSH wipe commands
# ---------------------------------------------------------------------------

class NetworkWipeWorker(QObject):
    log      = pyqtSignal(str)           # single log line
    progress = pyqtSignal(int)           # 0-100
    finished = pyqtSignal(bool, str)     # (success, message)

    def __init__(self, host, port, username, credential,
                 remote_path, algorithm, use_key):
        super().__init__()
        self.host        = host
        self.port        = port
        self.username    = username
        self.credential  = credential   # password OR key file path
        self.remote_path = remote_path
        self.algorithm   = algorithm
        self.use_key     = use_key
        self._stop       = False

    def _ts(self) -> str:
        return datetime.now().strftime('%H:%M:%S')

    def run(self):
        if not PARAMIKO_AVAILABLE:
            self.finished.emit(
                False,
                "paramiko is not installed.\nRun:  pip install paramiko"
            )
            return

        try:
            self.log.emit(
                f"[{self._ts()}] Connecting to "
                f"{self.username}@{self.host}:{self.port}…"
            )
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.use_key:
                client.connect(
                    self.host, port=self.port, username=self.username,
                    key_filename=self.credential, timeout=10
                )
            else:
                client.connect(
                    self.host, port=self.port, username=self.username,
                    password=self.credential, timeout=10
                )

            self.log.emit(f"[{self._ts()}] ✓ Connected")
            self.progress.emit(10)

            # Verify remote path exists
            self.log.emit(f"[{self._ts()}] Checking: {self.remote_path}")
            _, out, _ = client.exec_command(
                f'test -e "{self.remote_path}" && echo EXISTS || echo MISSING'
            )
            if out.read().decode().strip() != "EXISTS":
                client.close()
                self.finished.emit(
                    False, f"Remote path not found: {self.remote_path}"
                )
                return

            self.log.emit(f"[{self._ts()}] ✓ Path confirmed")
            self.progress.emit(25)

            # File or directory?
            _, out, _ = client.exec_command(
                f'[ -d "{self.remote_path}" ] && echo DIR || echo FILE'
            )
            path_type = out.read().decode().strip()

            passes_map = {
                'dod': 7, 'nist': 3, 'gutmann': 35, 'crypto': 1, 'simple': 1
            }
            passes = passes_map.get(self.algorithm, 3)

            if path_type == "DIR":
                _, out, _ = client.exec_command(
                    f'find "{self.remote_path}" -type f | wc -l'
                )
                count = out.read().decode().strip()
                self.log.emit(
                    f"[{self._ts()}] Directory scan: {count} files found"
                )
                self.progress.emit(35)
                cmd = (
                    f'find "{self.remote_path}" -type f '
                    f'-exec shred -uzn {passes} {{}} \\; '
                    f'&& rm -rf "{self.remote_path}"'
                )
            else:
                cmd = f'shred -uzn {passes} "{self.remote_path}"'

            self.log.emit(
                f"[{self._ts()}] Executing {self.algorithm.upper()} "
                f"({passes} passes)…"
            )
            self.progress.emit(40)

            transport = client.get_transport()
            channel = transport.open_session()
            channel.exec_command(cmd)

            poll_pct = 40
            while not channel.exit_status_ready():
                if self._stop:
                    channel.close()
                    client.close()
                    self.finished.emit(False, "Cancelled by user")
                    return
                if channel.recv_ready():
                    data = channel.recv(1024).decode('utf-8', errors='replace').strip()
                    if data:
                        self.log.emit(f"[remote] {data}")
                poll_pct = min(90, poll_pct + 1)
                self.progress.emit(poll_pct)
                time.sleep(0.5)

            exit_code = channel.recv_exit_status()
            stderr_data = ""
            if channel.recv_stderr_ready():
                stderr_data = channel.recv_stderr(4096).decode('utf-8', errors='replace')

            client.close()
            self.progress.emit(100)

            if exit_code == 0:
                self.log.emit(f"[{self._ts()}] ✓ Remote wipe completed")
                self.finished.emit(
                    True,
                    f"Remote wipe of '{self.remote_path}' completed successfully"
                )
            else:
                self.finished.emit(
                    False,
                    f"Remote command failed (exit {exit_code}): {stderr_data}"
                )

        except Exception as e:
            self.finished.emit(False, f"Connection error: {e}")

    def stop(self):
        self._stop = True


# ---------------------------------------------------------------------------
# Page widget
# ---------------------------------------------------------------------------

class NetworkWipePage(QWidget):
    """Network Wipe — remote machine file wiping via SSH."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = None
        self._worker = None
        self._build_ui()

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("🌐 Network Wipe")
        title.setObjectName("page-title")
        layout.addWidget(title)

        desc = QLabel(
            "Securely wipe files on remote Linux/macOS machines over SSH. "
            "Requires SSH access and the 'shred' utility on the remote host (standard on most Linux distros)."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color:#94a3b8; font-size:13px;")
        layout.addWidget(desc)

        if not PARAMIKO_AVAILABLE:
            warn = QLabel(
                "⚠️  paramiko is not installed.\n"
                "   Run in terminal:  pip install paramiko\n"
                "   Then restart the application to enable Network Wipe."
            )
            warn.setStyleSheet(
                "background:#3b1f1f; color:#f87171; padding:12px 16px; "
                "border-radius:8px; border:1px solid #7f1d1d; font-size:13px;"
            )
            layout.addWidget(warn)

        content_row = QHBoxLayout()
        content_row.setSpacing(16)
        content_row.addWidget(self._build_connection_panel(), 1)
        content_row.addWidget(self._build_log_panel(), 1)
        layout.addLayout(content_row, 1)

        # Bottom action bar
        bottom = QHBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setFormat("Ready")
        self.progress_bar.setTextVisible(True)

        self.start_btn = QPushButton("🌐 Start Remote Wipe")
        self.start_btn.setObjectName("primary-btn")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.clicked.connect(self._start_wipe)

        self.stop_btn = QPushButton("⏹ Cancel")
        self.stop_btn.setObjectName("secondary-btn")
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._cancel)

        bottom.addWidget(self.progress_bar, 2)
        bottom.addWidget(self.start_btn)
        bottom.addWidget(self.stop_btn)
        layout.addLayout(bottom)

    def _make_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("color:#8b949e; font-weight:600; min-width:100px; background:transparent;")
        return lbl

    def _build_connection_panel(self) -> QFrame:
        box = QFrame()
        box.setObjectName("content-card")
        outer = QVBoxLayout(box)
        outer.setContentsMargins(16, 14, 16, 16)
        outer.setSpacing(10)

        sec_title = QLabel("SSH Connection")
        sec_title.setObjectName("section-title")
        outer.addWidget(sec_title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("192.168.1.100  or  hostname.local")
        form.addRow(self._make_label("Host:"), self.host_input)

        self.port_input = QLineEdit("22")
        form.addRow(self._make_label("Port:"), self.port_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("username")
        form.addRow(self._make_label("Username:"), self.user_input)

        self.use_key_cb = QCheckBox("Use SSH Key File instead of password")
        self.use_key_cb.setStyleSheet(
            "QCheckBox{color:#c9d1d9; background:transparent;}"
            "QCheckBox::indicator{width:16px;height:16px;border:2px solid #00e676;"
            "border-radius:3px;background:#0a1520;}"
            "QCheckBox::indicator:checked{background:#00e676;}"
        )
        self.use_key_cb.toggled.connect(self._toggle_auth)
        form.addRow("", self.use_key_cb)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow(self._make_label("Password:"), self.pass_input)

        key_row = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Path to .pem / .ppk / .key file")
        self.key_input.setVisible(False)
        self._browse_btn = QPushButton("Browse")
        self._browse_btn.setObjectName("secondary-btn")
        self._browse_btn.setFixedWidth(72)
        self._browse_btn.setVisible(False)
        self._browse_btn.clicked.connect(self._browse_key)
        key_row.addWidget(self.key_input)
        key_row.addWidget(self._browse_btn)
        form.addRow(self._make_label("Key File:"), key_row)

        test_btn = QPushButton("🔌 Test Connection")
        test_btn.setObjectName("secondary-btn")
        test_btn.clicked.connect(self._test_connection)
        form.addRow("", test_btn)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background:#1c3348; max-height:1px;")
        form.addRow(sep)

        self.remote_path_input = QLineEdit()
        self.remote_path_input.setPlaceholderText("/home/user/sensitive_data.txt")
        form.addRow(self._make_label("Remote Path:"), self.remote_path_input)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["dod", "nist", "gutmann", "crypto", "simple"])
        form.addRow(self._make_label("Algorithm:"), self.algo_combo)

        outer.addLayout(form)
        return box

    def _build_log_panel(self) -> QFrame:
        box = QFrame()
        box.setObjectName("content-card")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(16, 14, 16, 16)
        lay.setSpacing(10)

        sec_title = QLabel("Activity Log")
        sec_title.setObjectName("section-title")
        lay.addWidget(sec_title)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 10))
        self.log_output.setStyleSheet(
            "QTextEdit{"
            "background:#0a1520; color:#94a3b8; "
            "border:1px solid #1c3348; border-radius:6px; padding:8px;"
            "}"
        )
        self.log_output.setPlaceholderText("SSH activity log will appear here…")
        lay.addWidget(self.log_output)

        clear_btn = QPushButton("Clear Log")
        clear_btn.setObjectName("secondary-btn")
        clear_btn.setFixedWidth(100)
        clear_btn.clicked.connect(self.log_output.clear)
        lay.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignRight)

        return box

    # -----------------------------------------------------------------------
    # Auth toggle
    # -----------------------------------------------------------------------

    def _toggle_auth(self, use_key: bool):
        self.pass_input.setVisible(not use_key)
        self.key_input.setVisible(use_key)
        self._browse_btn.setVisible(use_key)

    def _browse_key(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select SSH Key File", "",
            "Key Files (*.pem *.ppk *.key);;All Files (*)"
        )
        if path:
            self.key_input.setText(path)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _log(self, msg: str):
        self.log_output.append(msg)

    def _test_connection(self):
        if not PARAMIKO_AVAILABLE:
            self._log("⚠️  Install paramiko first: pip install paramiko")
            return

        host = self.host_input.text().strip()
        user = self.user_input.text().strip()
        if not host or not user:
            QMessageBox.warning(self, "Missing Fields",
                "Enter Host and Username before testing.")
            return

        try:
            port = int(self.port_input.text().strip() or '22')
        except ValueError:
            port = 22

        use_key = self.use_key_cb.isChecked()
        cred    = self.key_input.text() if use_key else self.pass_input.text()
        self._log(
            f"[{datetime.now():%H:%M:%S}] Testing connection to "
            f"{user}@{host}:{port}…"
        )

        def _test():
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                if use_key:
                    client.connect(host, port=port, username=user,
                                   key_filename=cred, timeout=8)
                else:
                    client.connect(host, port=port, username=user,
                                   password=cred, timeout=8)
                client.close()
                self._log(f"[{datetime.now():%H:%M:%S}] ✓ Connection successful!")
            except Exception as e:
                self._log(f"[{datetime.now():%H:%M:%S}] ✗ Failed: {e}")

        threading.Thread(target=_test, daemon=True).start()

    # -----------------------------------------------------------------------
    # Wipe execution
    # -----------------------------------------------------------------------

    def _start_wipe(self):
        host        = self.host_input.text().strip()
        port_txt    = self.port_input.text().strip()
        user        = self.user_input.text().strip()
        remote_path = self.remote_path_input.text().strip()
        algo        = self.algo_combo.currentText()

        if not host or not user or not remote_path:
            QMessageBox.warning(self, "Missing Fields",
                "Please fill in Host, Username, and Remote Path.")
            return

        try:
            port = int(port_txt or '22')
        except ValueError:
            QMessageBox.warning(self, "Invalid Port", "Port must be a number.")
            return

        reply = QMessageBox.warning(
            self, "Confirm Remote Wipe",
            f"Remote wipe:\n"
            f"  Host:      {host}\n"
            f"  Path:      {remote_path}\n"
            f"  Algorithm: {algo}\n\n"
            "This CANNOT be undone on the remote machine.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        use_key = self.use_key_cb.isChecked()
        cred    = self.key_input.text() if use_key else self.pass_input.text()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Connecting…")

        self._thread = QThread()
        self._worker = NetworkWipeWorker(
            host, port, user, cred, remote_path, algo, use_key
        )
        self._worker.moveToThread(self._thread)
        self._worker.log.connect(self._log)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._thread.started.connect(self._worker.run)
        self._thread.start()

    def _on_progress(self, pct: int):
        self.progress_bar.setValue(pct)
        self.progress_bar.setFormat(f"{pct}%")

    def _on_finished(self, success: bool, msg: str):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(100 if success else 0)
        self.progress_bar.setFormat("Complete" if success else "Failed")

        if success:
            self._log(f"\n✅ {msg}")
            QMessageBox.information(self, "Remote Wipe Complete", f"✅ {msg}")
            parent = self.parent()
            if parent and hasattr(parent, '_notify_monitoring'):
                parent._notify_monitoring(True, self.algo_combo.currentText())
        else:
            self._log(f"\n❌ {msg}")
            QMessageBox.critical(self, "Remote Wipe Failed", f"❌ {msg}")

        if self._thread:
            self._thread.quit()

    def _cancel(self):
        if self._worker:
            self._worker.stop()
        self.stop_btn.setEnabled(False)
        self._log(f"[{datetime.now():%H:%M:%S}] Cancellation requested…")
