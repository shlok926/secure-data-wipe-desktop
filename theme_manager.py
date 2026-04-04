# theme_manager.py
# ══════════════════════════════════════════════════════════
# Theme Manager — Dark & Light Mode for Secure Wipe App
# ══════════════════════════════════════════════════════════

DARK_THEME = """
/* ── Global ── */
QMainWindow, QWidget {
    background-color: #0a0e14;
    color: #cdd6e0;
    font-family: 'Rajdhani', 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

/* ── Sidebar ── */
QFrame#sidebar {
    background-color: #0a0e14;
    border-right: 1px solid #1e2d3d;
}

/* ── Nav Buttons ── */
QPushButton#nav-btn {
    background-color: transparent;
    color: #546e7a;
    border: none;
    border-left: 3px solid transparent;
    padding: 12px 20px;
    text-align: left;
    font-size: 13px;
    border-radius: 0px;
}
QPushButton#nav-btn:hover {
    background-color: rgba(0,230,118,0.05);
    color: #cdd6e0;
    border-left: 3px solid #00e676;
}
QPushButton#nav-btn:checked {
    background-color: rgba(0,230,118,0.08);
    color: #00e676;
    border-left: 3px solid #00e676;
    font-weight: bold;
}

/* ── Page Title ── */
QLabel#page-title {
    font-size: 24px;
    font-weight: bold;
    color: #e0eaf5;
    padding: 4px 0px 16px 0px;
}

/* ── Section Title ── */
QLabel#section-title {
    font-size: 12px;
    font-weight: bold;
    color: #00e676;
    padding: 4px 0px;
    letter-spacing: 1px;
}

/* ── Content Cards ── */
QFrame#content-card {
    background-color: #111820;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    padding: 16px;
}

/* ── File List ── */
QListWidget#file-list {
    background-color: #0f1620;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    padding: 6px;
    min-height: 280px;
    font-size: 13px;
}
QListWidget#file-list::item {
    color: #cdd6e0;
    padding: 8px 12px;
    min-height: 32px;
    border-bottom: 1px solid #1e2d3d;
    border-radius: 2px;
}
QListWidget#file-list::item:hover {
    background-color: #243447;
    color: #cdd6e0;
}
QListWidget#file-list::item:selected {
    background-color: #243447;
    color: #cdd6e0;
    border-left: 3px solid #1e2d3d;
}

/* ── ComboBox ── */
QComboBox {
    background-color: #0f1620;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
}
QComboBox:hover {
    border: 1px solid #1e2d3d;
}
QComboBox:focus {
    border: 1px solid #1e2d3d;
}
QComboBox::drop-down {
    border: none;
    width: 30px;
}
QComboBox QAbstractItemView {
    background-color: #111820;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    selection-background-color: #243447;
    selection-color: #cdd6e0;
    outline: none;
}

/* ── Primary Button ── */
QPushButton#primary-btn {
    background-color: #00c853;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 42px;
}
QPushButton#primary-btn:hover {
    background-color: #00e676;
}
QPushButton#primary-btn:pressed {
    background-color: #009624;
}
QPushButton#primary-btn:disabled {
    background-color: #243447;
    color: #546e7a;
}

/* ── Danger Button ── */
QPushButton#danger-btn {
    background-color: #d32f2f;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 42px;
}
QPushButton#danger-btn:hover {
    background-color: #ef5350;
    box-shadow: 0px 0px 20px rgba(211,47,47,0.35);
}
QPushButton#danger-btn:pressed {
    background-color: #b71c1c;
}

/* ── Secondary Button ── */
QPushButton#secondary-btn {
    background-color: #0f1620;
    color: #cdd6e0;
    border: 1px solid #243447;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 13px;
    min-height: 36px;
}
QPushButton#secondary-btn:hover {
    background-color: #243447;
    color: #cdd6e0;
    border: 1px solid #243447;
}
QPushButton#secondary-btn:pressed {
    background-color: #0a0e14;
}

/* ── Progress Bar ── */
QProgressBar {
    background-color: #0f1620;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    text-align: center;
    color: #00e676;
    font-weight: bold;
    min-height: 24px;
}
QProgressBar::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #00c853, stop:1 #00e676
    );
    border-radius: 4px;
}

/* ── Input / LineEdit ── */
QLineEdit {
    background-color: #0f1620;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
}
QLineEdit:focus {
    border: 1px solid #1e2d3d;
}

/* ── CheckBox ── */
QCheckBox {
    color: #cdd6e0;
    spacing: 8px;
    font-size: 13px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #1e2d3d;
    border-radius: 2px;
    background-color: #0f1620;
}
QCheckBox::indicator:checked {
    background-color: #00e676;
    border: 1px solid #00e676;
}
QCheckBox::indicator:hover {
    border: 1px solid #1e2d3d;
}

/* ── Table ── */
QTableWidget {
    background-color: #0f1620;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    gridline-color: #1e2d3d;
    font-size: 13px;
}
QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1e2d3d;
}
QTableWidget::item:selected {
    background-color: #243447;
    color: #cdd6e0;
}
QHeaderView::section {
    background-color: #0f1620;
    color: #00e676;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #1e2d3d;
    font-weight: bold;
    font-size: 13px;
}

/* ── ScrollBar ── */
QScrollBar:vertical {
    background-color: #0f1620;
    width: 8px;
    border-radius: 2px;
}
QScrollBar::handle:vertical {
    background-color: #243447;
    border-radius: 2px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #1e2d3d;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ── Tooltip ── */
QToolTip {
    background-color: #111820;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    border-radius: 2px;
    padding: 6px;
    font-size: 12px;
}

/* ── Description Text ── */
QLabel#description-text {
    color: #546e7a;
    font-size: 12px;
    font-style: italic;
}

/* ── Status / Info Labels ── */
QLabel#status-success { color: #00e676; font-weight: bold; }
QLabel#status-error   { color: #ef5350; font-weight: bold; }
QLabel#status-warning { color: #ffc107; font-weight: bold; }
QLabel#status-info    { color: #cdd6e0; font-weight: bold; }

/* ── Tab Widget ── */
QTabWidget::pane {
    background-color: #111820;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
}
QTabBar::tab {
    background-color: #0f1620;
    color: #546e7a;
    padding: 8px 20px;
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #111820;
    color: #00e676;
    border-bottom: 2px solid #00e676;
}
QTabBar::tab:hover {
    background-color: #243447;
    color: #cdd6e0;
}

/* ── MessageBox ── */
QMessageBox {
    background-color: #111820;
    color: #cdd6e0;
}
QMessageBox QPushButton {
    background-color: #0f1620;
    color: #cdd6e0;
    border: 1px solid #1e2d3d;
    border-radius: 4px;
    padding: 6px 20px;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background-color: #243447;
    color: #cdd6e0;
}
"""


LIGHT_THEME = """
/* ── Global ── */
QMainWindow, QWidget {
    background-color: #f0f4f8;
    color: #1a2a3a;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

/* ── Sidebar ── */
QFrame#sidebar {
    background-color: #1a2a3a;
    border-right: 2px solid #2a4a6a;
}

/* ── Nav Buttons ── */
QPushButton#nav-btn {
    background-color: transparent;
    color: #8aa8c8;
    border: none;
    border-left: 3px solid transparent;
    padding: 12px 20px;
    text-align: left;
    font-size: 13px;
    border-radius: 0px;
}
QPushButton#nav-btn:hover {
    background-color: #2a4a6a;
    color: #00e5ff;
    border-left: 3px solid #00e5ff;
}
QPushButton#nav-btn:checked {
    background-color: #2a4a6a;
    color: #00ff88;
    border-left: 3px solid #00ff88;
    font-weight: bold;
}

/* ── Page Title ── */
QLabel#page-title {
    font-size: 24px;
    font-weight: bold;
    color: #1a2a3a;
    padding: 4px 0px 16px 0px;
}

/* ── Section Title ── */
QLabel#section-title {
    font-size: 13px;
    font-weight: bold;
    color: #0077aa;
    padding: 4px 0px;
}

/* ── Content Cards ── */
QFrame#content-card {
    background-color: #ffffff;
    border: 1px solid #cdd8e3;
    border-radius: 10px;
    padding: 16px;
}

/* ── File List ── */
QListWidget#file-list {
    background-color: #f8fafc;
    color: #1a2a3a;
    border: 2px solid #0077aa;
    border-radius: 8px;
    padding: 6px;
    min-height: 280px;
    font-size: 13px;
}
QListWidget#file-list::item {
    color: #1a2a3a;
    padding: 8px 12px;
    min-height: 32px;
    border-bottom: 1px solid #e2eaf2;
    border-radius: 4px;
}
QListWidget#file-list::item:hover {
    background-color: #e2eaf2;
    color: #0077aa;
}
QListWidget#file-list::item:selected {
    background-color: #dceefb;
    color: #005580;
    border-left: 3px solid #0077aa;
}

/* ── ComboBox ── */
QComboBox {
    background-color: #ffffff;
    color: #1a2a3a;
    border: 1px solid #cdd8e3;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
}
QComboBox:hover { border: 1px solid #0077aa; }
QComboBox:focus { border: 1px solid #005580; }
QComboBox::drop-down { border: none; width: 30px; }
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1a2a3a;
    border: 1px solid #cdd8e3;
    selection-background-color: #dceefb;
    selection-color: #005580;
    outline: none;
}

/* ── Primary Button ── */
QPushButton#primary-btn {
    background-color: #00897b;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 42px;
}
QPushButton#primary-btn:hover { background-color: #00acc1; }
QPushButton#primary-btn:pressed { background-color: #006064; }
QPushButton#primary-btn:disabled {
    background-color: #cdd8e3;
    color: #8aa8c8;
}

/* ── Danger Button ── */
QPushButton#danger-btn {
    background-color: #d32f2f;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 42px;
}
QPushButton#danger-btn:hover { background-color: #ef5350; }
QPushButton#danger-btn:pressed { background-color: #8e0000; }

/* ── Secondary Button ── */
QPushButton#secondary-btn {
    background-color: #e2eaf2;
    color: #1a2a3a;
    border: 1px solid #cdd8e3;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    min-height: 36px;
}
QPushButton#secondary-btn:hover {
    background-color: #dceefb;
    color: #0077aa;
    border: 1px solid #0077aa;
}
QPushButton#secondary-btn:pressed { background-color: #cdd8e3; }

/* ── Progress Bar ── */
QProgressBar {
    background-color: #e2eaf2;
    border: 1px solid #cdd8e3;
    border-radius: 8px;
    text-align: center;
    color: #1a2a3a;
    font-weight: bold;
    min-height: 24px;
}
QProgressBar::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #00897b, stop:1 #00acc1
    );
    border-radius: 8px;
}

/* ── Input / LineEdit ── */
QLineEdit {
    background-color: #ffffff;
    color: #1a2a3a;
    border: 1px solid #cdd8e3;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
}
QLineEdit:focus { border: 1px solid #0077aa; }

/* ── CheckBox ── */
QCheckBox {
    color: #1a2a3a;
    spacing: 8px;
    font-size: 13px;
}
QCheckBox::indicator {
    width: 18px; height: 18px;
    border: 2px solid #cdd8e3;
    border-radius: 4px;
    background-color: #ffffff;
}
QCheckBox::indicator:checked {
    background-color: #00897b;
    border: 2px solid #00897b;
}
QCheckBox::indicator:hover { border: 2px solid #0077aa; }

/* ── Table ── */
QTableWidget {
    background-color: #ffffff;
    color: #1a2a3a;
    border: 1px solid #cdd8e3;
    border-radius: 8px;
    gridline-color: #e2eaf2;
    font-size: 13px;
}
QTableWidget::item { padding: 8px; border-bottom: 1px solid #e2eaf2; }
QTableWidget::item:selected { background-color: #dceefb; color: #005580; }
QHeaderView::section {
    background-color: #1a2a3a;
    color: #ffffff;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #0077aa;
    font-weight: bold;
    font-size: 13px;
}

/* ── ScrollBar ── */
QScrollBar:vertical {
    background-color: #e2eaf2;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background-color: #cdd8e3;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background-color: #0077aa; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

/* ── Tooltip ── */
QToolTip {
    background-color: #1a2a3a;
    color: #ffffff;
    border: 1px solid #0077aa;
    border-radius: 4px;
    padding: 6px;
    font-size: 12px;
}

/* ── Description Text ── */
QLabel#description-text {
    color: #5a7a9a;
    font-size: 12px;
    font-style: italic;
}

/* ── Status Labels ── */
QLabel#status-success { color: #00897b; font-weight: bold; }
QLabel#status-error   { color: #d32f2f; font-weight: bold; }
QLabel#status-warning { color: #f57c00; font-weight: bold; }
QLabel#status-info    { color: #0077aa; font-weight: bold; }

/* ── Tab Widget ── */
QTabWidget::pane {
    background-color: #ffffff;
    border: 1px solid #cdd8e3;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #e2eaf2;
    color: #5a7a9a;
    padding: 8px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #00897b;
    border-bottom: 2px solid #00897b;
}
QTabBar::tab:hover { background-color: #dceefb; color: #0077aa; }

/* ── MessageBox ── */
QMessageBox { background-color: #ffffff; color: #1a2a3a; }
QMessageBox QPushButton {
    background-color: #e2eaf2;
    color: #1a2a3a;
    border: 1px solid #cdd8e3;
    border-radius: 6px;
    padding: 6px 20px;
    min-width: 80px;
}
QMessageBox QPushButton:hover { background-color: #dceefb; color: #0077aa; }
"""


class ThemeManager:
    """
    Usage:
        self.theme_manager = ThemeManager(app)
        self.theme_manager.apply_dark()   # Default dark
        
        # Toggle button:
        self.theme_manager.toggle()
    """
    def __init__(self, app):
        self.app = app
        self.is_dark = True

    def apply_dark(self):
        self.app.setStyleSheet(DARK_THEME)
        self.is_dark = True

    def apply_light(self):
        self.app.setStyleSheet(LIGHT_THEME)
        self.is_dark = False

    def toggle(self):
        if self.is_dark:
            self.apply_light()
        else:
            self.apply_dark()
        return self.is_dark
