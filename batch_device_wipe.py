"""
Batch Device Wipe
Wipe multiple files/folders simultaneously using parallel worker threads.
Each item gets its own thread and progress bar.
"""

import os
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFileDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QMessageBox, QAbstractItemView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QColor


# ---------------------------------------------------------------------------
# Worker thread — wipes a single file or folder
# ---------------------------------------------------------------------------

class BatchItemWorker(QObject):
    progress = pyqtSignal(str, int, str)    # (item_id, percent, status_text)
    finished = pyqtSignal(str, bool, str)   # (item_id, success, message)

    def __init__(self, item_id: str, path: str, algorithm: str):
        super().__init__()
        self.item_id = item_id
        self.path = path
        self.algorithm = algorithm
        self._stop = False

    def run(self):
        try:
            from wiper_core import SecureWiper
            p = Path(self.path)

            if p.is_file():
                wiper = SecureWiper()
                wiper.set_algorithm(self.algorithm)

                def cb(pct, status):
                    self.progress.emit(self.item_id, pct, status)

                ok = wiper.wipe_file(str(p), progress_callback=cb)
                self.finished.emit(self.item_id, ok, "Success" if ok else "Wipe failed")

            elif p.is_dir():
                files = [f for f in p.rglob('*') if f.is_file()]
                total = max(len(files), 1)
                success_count = 0

                for i, f in enumerate(files):
                    if self._stop:
                        break
                    wiper = SecureWiper()
                    wiper.set_algorithm(self.algorithm)
                    file_index = i

                    def cb(pct, status, idx=file_index, tot=total):
                        overall = int((idx + pct / 100) / tot * 100)
                        self.progress.emit(self.item_id, overall, f"File {idx + 1}/{tot}")

                    ok = wiper.wipe_file(str(f), progress_callback=cb)
                    if ok:
                        success_count += 1
                    self.progress.emit(
                        self.item_id,
                        int((i + 1) / total * 100),
                        f"Done {i + 1}/{total}"
                    )

                all_ok = success_count == len(files)
                self.finished.emit(
                    self.item_id, all_ok,
                    f"Wiped {success_count}/{len(files)} files"
                )
            else:
                self.finished.emit(self.item_id, False, "Path not found")

        except Exception as e:
            self.finished.emit(self.item_id, False, str(e))

    def stop(self):
        self._stop = True


# ---------------------------------------------------------------------------
# Page widget
# ---------------------------------------------------------------------------

class BatchDeviceWipePage(QWidget):
    """Batch Wipe — multiple files/folders wiped in parallel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: dict = {}      # item_id -> {path, row, prog, success}
        self._workers: dict = {}    # item_id -> BatchItemWorker
        self._threads: dict = {}    # item_id -> QThread
        self._counter = 0
        self._done_count = 0
        self._total_count = 0
        self._build_ui()

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # Header row
        hdr = QHBoxLayout()
        title = QLabel("⚡ Batch Device Wipe")
        title.setObjectName("page-title")
        hdr.addWidget(title)
        hdr.addStretch()

        for label, slot in [
            ("+ Add Files",   self._add_files),
            ("+ Add Folder",  self._add_folder),
            ("🗑 Clear List", self._clear_list),
        ]:
            btn = QPushButton(label)
            btn.setObjectName("secondary-btn")
            btn.clicked.connect(slot)
            hdr.addWidget(btn)

        layout.addLayout(hdr)

        # Description
        info = QLabel(
            "Add multiple files or folders, choose an algorithm, then wipe them all in parallel. "
            "Each item runs in its own thread with an individual progress bar."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color:#94a3b8; font-size:13px;")
        layout.addWidget(info)

        # Algorithm selector
        algo_row = QHBoxLayout()
        algo_lbl = QLabel("Algorithm:")
        algo_lbl.setStyleSheet("font-weight:bold; font-size:13px;")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["dod", "nist", "gutmann", "crypto", "simple"])
        self.algo_combo.setFixedWidth(180)
        algo_row.addWidget(algo_lbl)
        algo_row.addWidget(self.algo_combo)
        algo_row.addStretch()
        layout.addLayout(algo_row)

        # Queue table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Path", "Type", "Size", "Progress"])
        hv = self.table.horizontalHeader()
        hv.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hv.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hv.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hv.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 200)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)

        # Status label
        self.status_lbl = QLabel("No items queued. Add files or folders to begin.")
        self.status_lbl.setStyleSheet("color:#64748b; font-size:13px;")
        layout.addWidget(self.status_lbl)

        # Action buttons
        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("⚡ Start Batch Wipe")
        self.start_btn.setObjectName("primary-btn")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.clicked.connect(self._start_batch)

        self.stop_btn = QPushButton("⏹ Stop All")
        self.stop_btn.setObjectName("secondary-btn")
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop_all)

        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.stop_btn)
        layout.addLayout(btn_row)

    # -----------------------------------------------------------------------
    # Queue management
    # -----------------------------------------------------------------------

    def _add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Files to Wipe")
        for p in paths:
            self._add_item(p)

    def _add_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder to Wipe")
        if path:
            self._add_item(path)

    def _add_item(self, path: str):
        if any(v['path'] == path for v in self._items.values()):
            return  # skip duplicates

        item_id = f"item_{self._counter}"
        self._counter += 1

        row = self.table.rowCount()
        self.table.insertRow(row)

        p = Path(path)
        if p.is_dir():
            size_str, type_str = "Folder", "📁 Folder"
        else:
            size_bytes = p.stat().st_size if p.exists() else 0
            size_str = self._fmt_size(size_bytes)
            type_str = "📄 File"

        for col, text in enumerate([str(p), type_str, size_str]):
            itm = QTableWidgetItem(text)
            itm.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                if col == 0 else Qt.AlignmentFlag.AlignCenter
            )
            self.table.setItem(row, col, itm)

        prog = QProgressBar()
        prog.setRange(0, 100)
        prog.setValue(0)
        prog.setTextVisible(True)
        prog.setFormat("Waiting")
        prog.setFixedHeight(22)
        prog.setStyleSheet(
            "QProgressBar::chunk{background:#3b82f6;} "
            "QProgressBar{text-align:center;}"
        )
        self.table.setCellWidget(row, 3, prog)

        self._items[item_id] = {'path': path, 'row': row, 'prog': prog, 'success': None}
        self._update_status()

    def _clear_list(self):
        if self._workers:
            QMessageBox.warning(self, "Busy",
                "Wait for current wipe to finish before clearing the list.")
            return
        self.table.setRowCount(0)
        self._items.clear()
        self._update_status()

    def _update_status(self):
        n = len(self._items)
        self.status_lbl.setText(
            f"{n} item(s) queued." if n
            else "No items queued. Add files or folders to begin."
        )

    def _fmt_size(self, b: int) -> str:
        for unit, thresh in [("GB", 1 << 30), ("MB", 1 << 20), ("KB", 1 << 10)]:
            if b >= thresh:
                return f"{b / thresh:.1f} {unit}"
        return f"{b} B"

    # -----------------------------------------------------------------------
    # Batch wipe execution
    # -----------------------------------------------------------------------

    def _start_batch(self):
        if not self._items:
            QMessageBox.information(self, "Empty Queue",
                "Add files or folders to wipe first.")
            return

        algo = self.algo_combo.currentText()
        reply = QMessageBox.warning(
            self, "Confirm Batch Wipe",
            f"Securely wipe {len(self._items)} item(s) using {algo.upper()} algorithm?\n\n"
            "This CANNOT be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self._done_count = 0
        self._total_count = len(self._items)
        self._workers.clear()
        self._threads.clear()

        for item_id, info in self._items.items():
            info['prog'].setValue(0)
            info['prog'].setFormat("Starting…")
            info['prog'].setStyleSheet(
                "QProgressBar::chunk{background:#3b82f6;} "
                "QProgressBar{text-align:center;}"
            )

            thread = QThread()
            worker = BatchItemWorker(item_id, info['path'], algo)
            worker.moveToThread(thread)
            worker.progress.connect(self._on_progress)
            worker.finished.connect(self._on_finished)
            thread.started.connect(worker.run)
            self._workers[item_id] = worker
            self._threads[item_id] = thread
            thread.start()

        self.status_lbl.setText(f"Wiping {self._total_count} item(s) in parallel…")

    def _on_progress(self, item_id: str, pct: int, status: str):
        if item_id in self._items:
            prog = self._items[item_id]['prog']
            prog.setValue(pct)
            prog.setFormat(f"{pct}%  {status[:20]}")

    def _on_finished(self, item_id: str, success: bool, msg: str):
        if item_id in self._items:
            prog = self._items[item_id]['prog']
            self._items[item_id]['success'] = success
            prog.setValue(100)
            if success:
                prog.setFormat("✓ Done")
                prog.setStyleSheet(
                    "QProgressBar::chunk{background:#22c55e;} "
                    "QProgressBar{text-align:center; color:white;}"
                )
            else:
                prog.setFormat("✗ Failed")
                prog.setStyleSheet(
                    "QProgressBar::chunk{background:#ef4444;} "
                    "QProgressBar{text-align:center; color:white;}"
                )

        if item_id in self._threads:
            self._threads[item_id].quit()

        self._done_count += 1
        self.status_lbl.setText(f"Progress: {self._done_count}/{self._total_count} done…")

        if self._done_count >= self._total_count:
            self._batch_complete()

    def _batch_complete(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self._workers.clear()
        self._threads.clear()

        successes = sum(1 for v in self._items.values() if v.get('success'))
        self.status_lbl.setText(
            f"Batch complete: {successes}/{self._total_count} succeeded."
        )

        QMessageBox.information(
            self, "Batch Wipe Complete",
            f"✅ Batch wipe finished!\n\n"
            f"{successes}/{self._total_count} items wiped successfully."
        )

        # Notify monitoring page
        parent = self.parent()
        if parent and hasattr(parent, '_notify_monitoring'):
            for _ in range(successes):
                parent._notify_monitoring(True, self.algo_combo.currentText())

    def _stop_all(self):
        for w in self._workers.values():
            w.stop()
        self.stop_btn.setEnabled(False)
        self.status_lbl.setText("Stop requested — finishing current file operations…")
