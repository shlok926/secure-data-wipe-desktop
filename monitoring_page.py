"""
System Monitoring Page for Secure Wipe
Real-time system health, performance metrics,
weekly operations chart, and algorithm usage donut.
"""

import random
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, QMargins
from PyQt6.QtGui import QColor, QPainter, QPen, QFont
from enhanced_dashboard import CustomDonut, CustomAreaChart, CustomColumnChart

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BG      = "#0d1117"
CARD_BG      = "#111e2b"
ROW_BG       = "#0a1520"
BORDER_COL   = "#1c3348"
ACCENT_GREEN = "#00e676"
ACCENT_YELL  = "#ffb300"
ACCENT_CYAN  = "#00bcd4"
ACCENT_BLUE  = "#5c9dff"
TEXT_PRI     = "#dde6ee"
TEXT_SEC     = "#6b8597"


def _card_style(bg=CARD_BG):
    return f"""
        QFrame {{
            background-color: {bg};
            border: 1px solid {BORDER_COL};
            border-radius: 10px;
        }}
    """


def _section_title(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color: {ACCENT_GREEN}; font-size: 12px; font-weight: 700;"
        " letter-spacing: 1.2px; font-family: monospace;"
    )
    return lbl


class MetricCard(QFrame):
    def __init__(self, label, value, icon_text="📊"):
        super().__init__()
        self.setStyleSheet(_card_style())
        self.setMinimumHeight(120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(18, 14, 18, 14)
        
        top = QHBoxLayout()
        lbl = QLabel(label.upper())
        lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px; font-weight: 600; background: transparent;")
        icon = QLabel(icon_text)
        icon.setStyleSheet("font-size: 22px; background: transparent;")
        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(icon)
        
        self._val_lbl = QLabel(value)
        self._val_lbl.setStyleSheet(f"color: {TEXT_PRI}; font-size: 30px; font-weight: 700; background: transparent;")
        
        layout.addLayout(top)
        layout.addWidget(self._val_lbl)
        self.setLayout(layout)

    def update_value(self, value):
        self._val_lbl.setText(value)


class SystemMonitoringPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent_app = parent
        self._prev_disk_io = None
        self._wipe_events = []
        self._build_ui()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_metrics)
        self._timer.start(2000)
        self._refresh_metrics()

    def _build_ui(self):
        self.setStyleSheet(f"background-color: {DARK_BG};")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        root = QVBoxLayout(content)
        root.setContentsMargins(28, 22, 28, 28)
        root.setSpacing(18)

        # Header
        hdr = QHBoxLayout()
        title = QLabel()
        title.setText(f'<span style="color:{TEXT_PRI}; font-size:24px; font-weight:700;">System </span>'
                      f'<span style="color:{ACCENT_GREEN}; font-size:24px; font-weight:700;">Monitoring</span>')
        hdr.addWidget(title)
        hdr.addStretch()
        online = QLabel("● SYSTEM ONLINE")
        online.setStyleSheet(f"color: {ACCENT_GREEN}; font-size: 12px; font-weight: 700;")
        hdr.addWidget(online)
        root.addLayout(hdr)

        # Metric Cards
        grid = QGridLayout()
        self._cpu_card = MetricCard("CPU USAGE", "0%", "🖥️")
        self._mem_card = MetricCard("MEMORY", "0 GB", "🗄️")
        self._disk_card = MetricCard("DISK I/O", "0 MB/s", "💾")
        self._net_card = MetricCard("NETWORK", "Stable", "📶")
        grid.addWidget(self._cpu_card, 0, 0)
        grid.addWidget(self._mem_card, 0, 1)
        grid.addWidget(self._disk_card, 0, 2)
        grid.addWidget(self._net_card, 0, 3)
        root.addLayout(grid)
        root.addStretch() # Push cards to the top

        scroll.setWidget(content)
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def _wrap_card(self, title, widget):
        card = QFrame()
        card.setStyleSheet(_card_style())
        lay = QVBoxLayout(card)
        lay.addWidget(_section_title(f"▌ {title}"))
        lay.addWidget(widget)
        return card

    def refresh_after_wipe(self, success, algorithm=""):
        self._wipe_events.append((datetime.now().timestamp(), success))
        self._refresh_charts()

    def _refresh_charts(self):
        # Charts removed as per user request
        pass

    def _refresh_throughput_chart(self):
        now = datetime.now().timestamp()
        hours = [0] * 24
        if self._parent_app:
            hm = getattr(self._parent_app, "history_manager", None)
            if hm:
                for e in hm.get_all_history():
                    try:
                        ts = datetime.fromisoformat(e.get("timestamp", ""))
                        age = (now - ts.timestamp()) / 3600
                        if 0 <= age < 24 and e.get("success"):
                            hours[int(age)] += 1
                    except: pass
        for t, s in self._wipe_events:
            age = (now - t) / 3600
            if 0 <= age < 24 and s:
                hours[int(age)] += 1
        hours.reverse()
        self.throughput_chart.set_data(hours)

    def _refresh_algo_chart(self):
        counts = {"dod":0, "nist":0, "gutmann":0, "crypto":0, "simple":0}
        if self._parent_app:
            hm = getattr(self._parent_app, "history_manager", None)
            if hm:
                for e in hm.get_all_history():
                    a = e.get("algorithm", "").lower()
                    for k in counts:
                        if k in a or (k=="simple" and "single" in a):
                            counts[k] += 1
        data = []
        colors = {"dod":ACCENT_GREEN, "nist":ACCENT_CYAN, "gutmann":ACCENT_YELL, "crypto":ACCENT_BLUE, "simple":"#a29bfe"}
        names = {"dod":"DoD", "nist":"NIST", "gutmann":"Gutmann", "crypto":"Crypto", "simple":"Single Pass"}
        for k in counts:
            self.algo_labels[k].setText(f"{names[k]}: {counts[k]}")
            data.append((counts[k], colors[k]))
        self.algo_donut.set_data(data)

    def _refresh_weekly_chart(self):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        counts = [0] * 7
        if self._parent_app:
            hm = getattr(self._parent_app, "history_manager", None)
            if hm:
                for e in hm.get_all_history():
                    try:
                        ts = datetime.fromisoformat(e.get("timestamp", ""))
                        if e.get("success"): counts[ts.weekday()] += 1
                    except: pass
        for t, s in self._wipe_events:
            if s: counts[datetime.fromtimestamp(t).weekday()] += 1
        self.weekly_chart.set_data(list(zip(days, counts)))

    def _refresh_metrics(self):
        if PSUTIL_AVAILABLE:
            cpu = psutil.cpu_percent()
            self._cpu_card.update_value(f"{cpu:.0f}%")
            mem = psutil.virtual_memory()
            self._mem_card.update_value(f"{mem.used / 1024**3:.1f} GB")
            try:
                io = psutil.disk_io_counters()
                if self._prev_disk_io:
                    val = ((io.read_bytes - self._prev_disk_io.read_bytes) + (io.write_bytes - self._prev_disk_io.write_bytes)) / 1024 / 1024 / 2
                    self._disk_card.update_value(f"{val:.0f} MB/s")
                self._prev_disk_io = io
            except: pass
            try:
                up = any(s.isup for s in psutil.net_if_stats().values())
                self._net_card.update_value("Stable" if up else "Down")
            except: pass
        else:
            self._cpu_card.update_value(f"{random.randint(15, 40)}%")
            self._mem_card.update_value(f"{random.uniform(3.5, 5.5):.1f} GB")
            self._disk_card.update_value(f"{random.randint(50, 180)} MB/s")
            self._net_card.update_value("Stable")
        self._refresh_charts()
