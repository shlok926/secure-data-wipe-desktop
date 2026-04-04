"""
Enhanced Dashboard Module for Secure Wipe
Simplified layout matching the user's screenshot with metric cards and quick actions.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QPushButton, QGridLayout, QScrollArea,
    QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush, QLinearGradient, QPolygonF
from datetime import datetime, timedelta
import random

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class CustomDonut(QWidget):
    def __init__(self, bg_color="#111e2b", parent=None):
        super().__init__(parent)
        self.segments = []
        self.bg_color = bg_color
        self.setMinimumSize(140, 140)

    def set_data(self, data):
        self.segments = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        size = min(rect.width(), rect.height()) - 10
        x, y = (rect.width() - size) / 2.0, (rect.height() - size) / 2.0
        pie_rect = QRectF(float(x), float(y), float(size), float(size))

        total = sum(v for v, c in self.segments)
        if total == 0:
            painter.setBrush(QColor("#1c3348"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(pie_rect)
        else:
            start_angle = 90 * 16
            for value, color in self.segments:
                if value == 0: continue
                span_angle = int(round((value / total) * 360 * 16))
                painter.setBrush(QColor(color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawPie(pie_rect, int(start_angle), -span_angle)
                start_angle -= span_angle

        hole_size = size * 0.70
        hole_x, hole_y = x + (size - hole_size) / 2.0, y + (size - hole_size) / 2.0
        hole_rect = QRectF(float(hole_x), float(hole_y), float(hole_size), float(hole_size))
        painter.setBrush(QColor(self.bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(hole_rect)

        if total > 0:
            painter.setPen(QColor("#e6edf3"))
            font = painter.font(); font.setPointSize(14); font.setBold(True); painter.setFont(font)
            painter.drawText(hole_rect, Qt.AlignmentFlag.AlignCenter, str(int(total)))


class CustomAreaChart(QWidget):
    def __init__(self, color="#3b82f6", parent=None):
        super().__init__(parent)
        self.data = []
        self.labels = []
        self.color = color
        self.setMinimumHeight(150)

    def set_data(self, data, labels=None):
        self.data = data
        self.labels = labels
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.data: return

        rect = self.rect()
        w, h = float(rect.width()), float(rect.height())
        mx, my = 30.0, 30.0
        dw = (w - 2 * mx) / (len(self.data) - 1 if len(self.data) > 1 else 1)
        max_val = float(max(self.data + [1]))
        
        points = []
        for i, val in enumerate(self.data):
            px = mx + i * dw
            py = h - my - (val / max_val) * (h - 2 * my)
            points.append(QPointF(px, py))

        # Sharp Area
        path = QPolygonF()
        path.append(QPointF(mx, h - my))
        for p in points: path.append(p)
        path.append(QPointF(mx + (len(self.data)-1)*dw, h - my))
        
        grad = QLinearGradient(0, 0, 0, h)
        c = QColor(self.color); c.setAlpha(80); grad.setColorAt(0, c)
        c.setAlpha(10); grad.setColorAt(1, c)
        painter.setBrush(QBrush(grad)); painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(path)

        # Sharp Line
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(self.color), 2))
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i+1])

        if self.labels and len(self.labels) == len(self.data):
            painter.setPen(QColor("#8b949e"))
            font = painter.font(); font.setPointSize(9); painter.setFont(font)
            for i, lbl in enumerate(self.labels):
                lx = mx + i * dw - 20
                painter.drawText(QRectF(lx, h - 25, 40, 20), Qt.AlignmentFlag.AlignCenter, lbl)


class CustomColumnChart(QWidget):
    def __init__(self, color="#3b82f6", parent=None):
        super().__init__(parent)
        self.data = []
        self.color = color
        self.setMinimumHeight(120)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.data: return

        rect = self.rect()
        w, h = float(rect.width()), float(rect.height())
        mx, my = 35.0, 30.0
        bw = (w - 2 * mx) / len(self.data)
        max_val = float(max([v for l,v in self.data] + [1]))

        for i, (label, val) in enumerate(self.data):
            bar_h = (val / max_val) * (h - 2 * my - 20)
            target_bw = bw * 0.6
            bx, by = mx + i * bw + (bw - target_bw)/2.0, h - my - 15 - bar_h
            painter.setBrush(QColor(self.color)); painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(bx, by, target_bw, bar_h), 2, 2)
            painter.setPen(QColor("#8b949e"))
            font = painter.font(); font.setPointSize(9); painter.setFont(font)
            painter.drawText(QRectF(bx - 10, h - 25, target_bw + 20, 20), Qt.AlignmentFlag.AlignCenter, label)
            if val > 0:
                painter.setPen(QColor("#e6edf3"))
                painter.drawText(QRectF(bx - 10, by - 20, target_bw + 20, 20), Qt.AlignmentFlag.AlignCenter, str(int(val)))


class StatCard(QFrame):
    def __init__(self, title, value, color="#3498db", icon="📊", parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.color = color
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet(f"QFrame {{ background: #111e2b; border: 1px solid #1c3348; border-radius: 12px; padding: 20px; }}")
        layout = QVBoxLayout(self)
        t_lbl = QLabel(self.title.upper())
        t_lbl.setStyleSheet("color: #8b949e; font-size: 11px; font-weight: 700;")
        self.val_lbl = QLabel(str(self.value))
        self.val_lbl.setStyleSheet("color: #e6edf3; font-size: 32px; font-weight: 800;")
        layout.addWidget(t_lbl); layout.addSpacing(10); layout.addWidget(self.val_lbl)

    def update_value(self, new_val):
        self.val_lbl.setText(str(new_val))


class MetricCard(QFrame):
    """System monitoring metric card (CPU, Memory, Disk, Network)"""
    def __init__(self, label, value, icon_text="📊", parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame { background-color: #111e2b; border: 1px solid #1c3348; border-radius: 10px; }")
        self.setMinimumHeight(110)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Top row: Label + Icon
        top = QHBoxLayout()
        lbl = QLabel(label.upper())
        lbl.setStyleSheet("color: #6b8597; font-size: 10px; font-weight: 600; background: transparent;")
        icon = QLabel(icon_text)
        icon.setStyleSheet("font-size: 20px; background: transparent;")
        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(icon)
        
        # Value label
        self._val_lbl = QLabel(value)
        self._val_lbl.setStyleSheet("color: #dde6ee; font-size: 28px; font-weight: 700; background: transparent;")
        
        layout.addLayout(top)
        layout.addWidget(self._val_lbl)
        self.setLayout(layout)

    def update_value(self, value):
        """Update the displayed metric value"""
        self._val_lbl.setText(value)


class EnhancedDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self._prev_disk_io = None  # For disk I/O calculation
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("background-color: #0d1117;")
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(35, 35, 35, 35); main_lay.setSpacing(30)

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: 800; color: #e6edf3;")
        main_lay.addWidget(title)

        # ──── Statistics Cards ────
        cards = QHBoxLayout()
        self.total_card = StatCard("Total Wipes", "0", "#3b82f6")
        self.success_card = StatCard("Successful", "0", "#22c55e")
        self.failed_card = StatCard("Failed", "0", "#ef4444")
        self.data_card = StatCard("Data Destroyed", "0 MB", "#eab308")
        cards.addWidget(self.total_card); cards.addWidget(self.success_card)
        cards.addWidget(self.failed_card); cards.addWidget(self.data_card)
        main_lay.addLayout(cards)

        # ──── System Monitoring Cards (MOVED HERE - ABOVE Quick Actions) ────
        mon_title = QLabel("SYSTEM MONITORING")
        mon_title.setStyleSheet("color: #00e676; font-size: 12px; font-weight: 800; letter-spacing: 1px; margin-top: 10px;")
        main_lay.addWidget(mon_title)

        mon_grid = QGridLayout()
        mon_grid.setSpacing(15)
        self.cpu_card = MetricCard("CPU Usage", "0%", "🖥️")
        self.mem_card = MetricCard("Memory", "0 GB", "🗄️")
        self.disk_card = MetricCard("Disk I/O", "0 MB/s", "💾")
        self.net_card = MetricCard("Network", "Stable", "📶")
        mon_grid.addWidget(self.cpu_card, 0, 0)
        mon_grid.addWidget(self.mem_card, 0, 1)
        mon_grid.addWidget(self.disk_card, 0, 2)
        mon_grid.addWidget(self.net_card, 0, 3)
        main_lay.addLayout(mon_grid)

        # ──── Quick Actions ────
        qa_title = QLabel("QUICK ACTIONS")
        qa_title.setStyleSheet("color: #00e676; font-size: 12px; font-weight: 800; letter-spacing: 1px;")
        main_lay.addWidget(qa_title)

        btns = QHBoxLayout()
        btns.setSpacing(15)
        actions = [
            ("Start New Wipe", "#00e676", "🧹", 1),  # Row 1: Secure Wipe
            ("View Audit Logs", "#1c3348", "📋", 3),  # Row 3: Audit Logs
            ("Batch Wipe", "#00e676", "📁", 8),       # Row 8: Batch Wipe (changed from 9)
            ("Schedule", "#1c3348", "⏰", None),      # No direct row - show dialog
            ("Analytics", "#1c3348", "📊", None)      # No direct row - show dialog
        ]
        for text, bg, icon, row in actions:
            b = QPushButton(f"{icon} {text}")
            b.setStyleSheet(f"QPushButton {{ background: {bg}; color: {'#0d1117' if bg=='#00e676' else '#e6edf3'}; border: none; border-radius: 6px; padding: 12px 25px; font-weight: 700; }}")
            
            # Add click handlers based on action
            if row is not None:
                b.clicked.connect(lambda checked, r=row: self.parent_app.sidebar.setCurrentRow(r) if self.parent_app else None)
            elif "Schedule" in text:
                b.clicked.connect(self.show_schedule_dialog)
            elif "Analytics" in text:
                b.clicked.connect(self.show_analytics)
            
            btns.addWidget(b)
        main_lay.addLayout(btns)

        main_lay.addStretch()

        # ──── Timers ────
        # Wipe statistics refresh (5 seconds)
        self.timer = QTimer(); self.timer.timeout.connect(self.refresh_dashboard)
        self.timer.start(5000); self.refresh_dashboard()
        
        # System monitoring refresh (2 seconds)
        self.monitor_timer = QTimer(); self.monitor_timer.timeout.connect(self.refresh_monitoring)
        self.monitor_timer.start(2000); self.refresh_monitoring()

    def refresh_dashboard(self):
        if not self.parent_app: return
        hm = getattr(self.parent_app, "history_manager", None)
        if not hm: return
        hist = hm.get_all_history()
        ok = sum(1 for e in hist if e.get("success"))
        self.total_card.update_value(len(hist))
        self.success_card.update_value(ok)
        self.failed_card.update_value(len(hist) - ok)
        bytes_val = sum(e.get("file_size",0) for e in hist)
        if bytes_val < 1024**2: ds = f"{bytes_val/1024:.1f} KB"
        elif bytes_val < 1024**3: ds = f"{bytes_val/(1024**2):.1f} MB"
        else: ds = f"{bytes_val/(1024**3):.2f} GB"
        self.data_card.update_value(ds)

    def refresh_monitoring(self):
        """Refresh system monitoring metrics (CPU, Memory, Disk, Network)"""
        if PSUTIL_AVAILABLE:
            # CPU Usage
            try:
                cpu = psutil.cpu_percent(interval=0.1)
                self.cpu_card.update_value(f"{cpu:.0f}%")
            except:
                self.cpu_card.update_value("N/A")
            
            # Memory Usage
            try:
                mem = psutil.virtual_memory()
                self.mem_card.update_value(f"{mem.used / 1024**3:.1f} GB")
            except:
                self.mem_card.update_value("N/A")
            
            # Disk I/O
            try:
                io = psutil.disk_io_counters()
                if self._prev_disk_io:
                    read_delta = io.read_bytes - self._prev_disk_io.read_bytes
                    write_delta = io.write_bytes - self._prev_disk_io.write_bytes
                    total_delta = (read_delta + write_delta) / 1024 / 1024 / 2  # Convert to MB/s
                    self.disk_card.update_value(f"{total_delta:.0f} MB/s")
                self._prev_disk_io = io
            except:
                self.disk_card.update_value("N/A")
            
            # Network Status
            try:
                net_stats = psutil.net_if_stats()
                is_up = any(s.isup for s in net_stats.values())
                self.net_card.update_value("Stable" if is_up else "Down")
            except:
                self.net_card.update_value("N/A")
        else:
            # Fallback to mock data if psutil not available
            self.cpu_card.update_value(f"{random.randint(15, 40)}%")
            self.mem_card.update_value(f"{random.uniform(3.5, 5.5):.1f} GB")
            self.disk_card.update_value(f"{random.randint(50, 180)} MB/s")
            self.net_card.update_value("Stable")

    def show_schedule_dialog(self):
        """Show schedule/task creation dialog"""
        if self.parent_app and hasattr(self.parent_app, 'show_schedule_dialog'):
            self.parent_app.show_schedule_dialog()
        else:
            QMessageBox.information(self, "Schedule", "Open the Scheduled Tasks page to create new schedules.")

    def show_analytics(self):
        """Show analytics dashboard"""
        if self.parent_app and hasattr(self.parent_app, 'show_analytics'):
            self.parent_app.show_analytics()
        else:
            QMessageBox.information(self, "Analytics", "Analytics feature is not yet available.")