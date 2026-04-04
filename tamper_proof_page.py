"""
Tamper-Proof Audit Page
Displays wipe history with SHA-256 hash chain integrity verification.
"""

from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QColor


# ---------------------------------------------------------------------------
# Background worker — runs chain.verify() off the UI thread
# ---------------------------------------------------------------------------

class VerifyWorker(QObject):
    result = pyqtSignal(bool, list, int, int)   # (all_valid, tampered_ids, total, chained)

    def __init__(self, history, chain):
        super().__init__()
        self.history = history
        self.chain = chain

    def run(self):
        valid, tampered = self.chain.verify(self.history)
        self.result.emit(valid, tampered, len(self.history), len(self.chain))


# ---------------------------------------------------------------------------
# Page widget
# ---------------------------------------------------------------------------

class TamperProofAuditPage(QWidget):
    """Tamper-Proof Audit Log — SHA-256 hash chain verification."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = None
        self._worker = None
        self._last_tampered = []
        self._build_ui()
        self._load_entries()

    # -----------------------------------------------------------------------
    # UI construction
    # -----------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        # Title
        title = QLabel("🔒 Tamper-Proof Audit Log")
        title.setObjectName("page-title")
        layout.addWidget(title)

        desc = QLabel(
            "Every wipe entry is hashed with SHA-256 and chained to the previous entry. "
            "Any modification — even a single character — breaks the chain and is flagged instantly."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color:#94a3b8; font-size:13px;")
        layout.addWidget(desc)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        self.card_total   = self._stat_card("Total Entries",  "0",            "#3b82f6")
        self.card_chained = self._stat_card("Chain Length",   "0",            "#8b5cf6")
        self.card_status  = self._stat_card("Chain Status",   "Not Verified", "#64748b")
        self.card_last    = self._stat_card("Last Verified",  "Never",        "#64748b")
        for card in (self.card_total, self.card_chained, self.card_status, self.card_last):
            stats_row.addWidget(card)
        layout.addLayout(stats_row)

        # Buttons
        btn_row = QHBoxLayout()
        self.verify_btn = QPushButton("🔍 Verify Chain Integrity")
        self.verify_btn.setObjectName("primary-btn")
        self.verify_btn.setMinimumHeight(40)
        self.verify_btn.clicked.connect(self._start_verify)

        self.rebuild_btn = QPushButton("🔄 Rebuild Chain")
        self.rebuild_btn.setObjectName("secondary-btn")
        self.rebuild_btn.setMinimumHeight(40)
        self.rebuild_btn.setToolTip("Rebuild chain from current history (use when migrating old logs)")
        self.rebuild_btn.clicked.connect(self._rebuild_chain)

        self.export_btn = QPushButton("📄 Export Report")
        self.export_btn.setObjectName("secondary-btn")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.clicked.connect(self._export_report)

        refresh_btn = QPushButton("↻ Refresh")
        refresh_btn.setObjectName("secondary-btn")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.clicked.connect(self._load_entries)

        for b in (self.verify_btn, self.rebuild_btn, self.export_btn, refresh_btn):
            btn_row.addWidget(b)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Timestamp", "File Name", "Algorithm", "Status", "SHA-256 (first 16)", "Chain"
        ])
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table, 1)

        # Status bar
        self.status_lbl = QLabel("Load history and click Verify to check chain integrity.")
        self.status_lbl.setStyleSheet("color:#64748b; font-size:12px;")
        layout.addWidget(self.status_lbl)

    def _stat_card(self, label: str, value: str, color: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #1e293b; border-radius: 10px;
                border: 1px solid #334155;
            }
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 12)
        lbl = QLabel(label)
        lbl.setStyleSheet("color:#94a3b8; font-size:11px; font-weight:600;")
        val = QLabel(value)
        val.setStyleSheet(f"color:{color}; font-size:22px; font-weight:bold;")
        lay.addWidget(lbl)
        lay.addWidget(val)
        card._value_label = val
        card._color = color
        return card

    # -----------------------------------------------------------------------
    # Data loading
    # -----------------------------------------------------------------------

    def _load_entries(self):
        chain = None
        try:
            from audit_chain import get_audit_chain
            chain = get_audit_chain()
        except Exception:
            pass

        history = []
        try:
            from history_manager import get_history_manager
            history = get_history_manager().get_all_history()
        except Exception:
            pass

        self.table.setRowCount(0)
        for entry in reversed(history):
            row = self.table.rowCount()
            self.table.insertRow(row)

            ts = entry.get('timestamp', '')
            if isinstance(ts, datetime):
                ts = ts.strftime('%Y-%m-%d %H:%M:%S')

            eid = entry.get('id', '')
            stored_hash = chain.get_hash_for(eid) if chain else ''
            status_text = "✅ Success" if entry.get('success') else "❌ Failed"
            chain_text  = "🔗 Chained" if stored_hash else "⚠️ Unchained"
            hash_preview = (stored_hash[:16] + "…") if stored_hash else "—"

            cells = [
                ts,
                entry.get('file_name', entry.get('file_path', '')),
                entry.get('algorithm', ''),
                status_text,
                hash_preview,
                chain_text,
            ]
            for col, text in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                    if col == 1 else
                    Qt.AlignmentFlag.AlignCenter
                )
                self.table.setItem(row, col, item)

        total = len(history)
        chain_len = len(chain) if chain else 0
        self.card_total._value_label.setText(str(total))
        self.card_chained._value_label.setText(str(chain_len))
        self.status_lbl.setText(
            f"Loaded {total} entries. {chain_len} entries in chain. "
            "Click 'Verify Chain Integrity' to check for tampering."
        )

    # -----------------------------------------------------------------------
    # Verification
    # -----------------------------------------------------------------------

    def _start_verify(self):
        try:
            from audit_chain import get_audit_chain
            chain = get_audit_chain()
            from history_manager import get_history_manager
            history = get_history_manager().get_all_history()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot load data: {e}")
            return

        self.verify_btn.setEnabled(False)
        self.verify_btn.setText("🔍 Verifying…")
        self.status_lbl.setText("Verifying chain integrity…")

        self._thread = QThread()
        self._worker = VerifyWorker(history, chain)
        self._worker.moveToThread(self._thread)
        self._worker.result.connect(self._on_verify_result)
        self._thread.started.connect(self._worker.run)
        self._thread.start()

    def _on_verify_result(self, valid: bool, tampered: list, total: int, chained: int):
        self.verify_btn.setEnabled(True)
        self.verify_btn.setText("🔍 Verify Chain Integrity")
        self._last_tampered = tampered
        now_str = datetime.now().strftime('%H:%M:%S')
        self.card_last._value_label.setText(now_str)

        if valid:
            self.card_status._value_label.setText("✅ Valid")
            self.card_status._value_label.setStyleSheet(
                "color:#22c55e; font-size:22px; font-weight:bold;"
            )
            self.status_lbl.setText(
                f"✅  All {chained} chained entries verified — no tampering detected."
            )
            QMessageBox.information(
                self, "Chain Integrity: VALID",
                f"✅ All {chained} chained entries verified.\n\n"
                "No tampering detected. Audit log is authentic."
            )
        else:
            self.card_status._value_label.setText("⚠️ TAMPERED")
            self.card_status._value_label.setStyleSheet(
                "color:#ef4444; font-size:22px; font-weight:bold;"
            )
            self.status_lbl.setText(
                f"⚠️  ALERT: {len(tampered)} tampered entries detected! "
                "Highlighted in red below."
            )
            self._highlight_tampered(tampered)
            QMessageBox.critical(
                self, "Chain Integrity: TAMPERED",
                f"⚠️  TAMPERING DETECTED!\n\n"
                f"{len(tampered)} entries have been modified after original recording.\n\n"
                "These entries no longer match their original SHA-256 hashes.\n"
                "The audit log may have been compromised."
            )

        if self._thread:
            self._thread.quit()

    def _highlight_tampered(self, tampered_ids: list):
        tampered_set = set(tampered_ids)
        try:
            from history_manager import get_history_manager
            history = list(reversed(get_history_manager().get_all_history()))
        except Exception:
            return

        for row in range(self.table.rowCount()):
            if row < len(history):
                eid = history[row].get('id', '')
                if eid in tampered_set:
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item:
                            item.setBackground(QColor("#7f1d1d"))
                            item.setForeground(QColor("#fca5a5"))

    # -----------------------------------------------------------------------
    # Rebuild chain
    # -----------------------------------------------------------------------

    def _rebuild_chain(self):
        reply = QMessageBox.warning(
            self, "Rebuild Chain",
            "This rebuilds the hash chain from current history data.\n\n"
            "Use this to initialize the chain for existing logs, or after "
            "importing records from another system.\n\n"
            "Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            from audit_chain import get_audit_chain
            from history_manager import get_history_manager
            history = get_history_manager().get_all_history()
            history_sorted = sorted(
                history,
                key=lambda x: x.get('timestamp', datetime.min)
            )
            get_audit_chain().rebuild_from_history(history_sorted)
            self._load_entries()
            QMessageBox.information(
                self, "Done",
                f"Chain rebuilt with {len(history_sorted)} entries."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Rebuild failed: {e}")

    # -----------------------------------------------------------------------
    # Export report
    # -----------------------------------------------------------------------

    def _export_report(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Audit Integrity Report",
            "audit_integrity_report.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return

        try:
            from audit_chain import get_audit_chain
            from history_manager import get_history_manager
            chain = get_audit_chain()
            history = get_history_manager().get_all_history()
            valid, tampered = chain.verify(history)
            tampered_set = set(tampered)

            lines = [
                "=" * 72,
                "  TAMPER-PROOF AUDIT LOG INTEGRITY REPORT",
                f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"  Chain Status : {'VALID — No tampering detected' if valid else 'COMPROMISED — Tampering detected'}",
                f"  Total History Entries : {len(history)}",
                f"  Chained Entries       : {len(chain)}",
                f"  Tampered Entries      : {len(tampered)}",
                "=" * 72,
                "",
            ]

            for entry in history:
                eid = entry.get('id', '')
                ts = entry.get('timestamp', '')
                if isinstance(ts, datetime):
                    ts = ts.strftime('%Y-%m-%d %H:%M:%S')
                stored_hash = chain.get_hash_for(eid)
                status = "TAMPERED" if eid in tampered_set else ("VALID" if stored_hash else "UNCHAINED")
                hash_display = (stored_hash[:32] + "…") if stored_hash else "—"
                lines.append(
                    f"[{status:<9}] {ts}  |  {entry.get('file_name', ''):<30}  "
                    f"|  {entry.get('algorithm', ''):<8}  |  {hash_display}"
                )

            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            QMessageBox.information(self, "Exported", f"Report saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))
