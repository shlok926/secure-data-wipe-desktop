# 🔧 UI_FIXES_COMPLETE.py
# Copy ALL functions below and replace in your secure_wipe_desktop.py

# ====================================
# FIX 1: IMPROVED DARK THEME
# Replace your apply_dark_theme() function with this:
# ====================================

def apply_dark_theme(self):
    """Apply dark theme with improved visibility - ALL UI FIXED"""
    self.setStyleSheet("""
        /* Main Window */
        QMainWindow {
            background-color: #1e1e1e;
        }
        
        /* Main Content Area */
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        /* Sidebar */
        QListWidget {
            background-color: #252526;
            color: #ffffff;
            font-size: 15px;
            font-weight: 500;
            border: none;
            padding: 10px 0;
        }
        
        QListWidget::item {
            padding: 15px 20px;
            border-left: 4px solid transparent;
            color: #cccccc;
        }
        
        QListWidget::item:selected {
            background-color: #2d2d30;
            border-left: 4px solid #007acc;
            color: #ffffff;
        }
        
        QListWidget::item:hover {
            background-color: #2d2d30;
            color: #ffffff;
        }
        
        /* Page Titles */
        QLabel#page-title {
            font-size: 32px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
        }
        
        QLabel#section-title {
            font-size: 17px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }
        
        QLabel#stat-title {
            font-size: 14px;
            color: #cccccc;
            font-weight: 500;
        }
        
        QLabel#stat-value {
            font-size: 36px;
            font-weight: 700;
            color: #ffffff;
        }
        
        QLabel#status-text {
            font-size: 14px;
            color: #cccccc;
            font-style: italic;
        }
        
        QLabel#description-text {
            font-size: 13px;
            color: #e0e0e0;
            padding: 10px;
            background-color: #2d2d30;
            border-radius: 5px;
        }
        
        QLabel {
            color: #ffffff;
        }
        
        /* Cards */
        QFrame#content-card {
            background-color: #252526;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #3e3e42;
        }
        
        /* Buttons */
        QPushButton {
            font-size: 14px;
            font-weight: 600;
            border-radius: 6px;
            padding: 12px 24px;
            border: none;
            color: white;
            min-height: 40px;
        }
        
        QPushButton#primary-btn {
            background-color: #007acc;
            color: white;
        }
        
        QPushButton#primary-btn:hover {
            background-color: #005a9e;
        }
        
        QPushButton#secondary-btn {
            background-color: #3e3e42;
            color: #ffffff;
        }
        
        QPushButton#secondary-btn:hover {
            background-color: #505053;
            color: #ffffff;
        }
        
        QPushButton#danger-btn {
            background-color: #d83b01;
            color: white;
            font-size: 16px;
        }
        
        QPushButton#danger-btn:hover {
            background-color: #a52a00;
        }
        
        QPushButton:disabled {
            background-color: #3e3e42;
            color: #6e6e6e;
        }
        
        /* Input Fields - FIXED! */
        QLineEdit {
            padding: 12px;
            font-size: 14px;
            border: 2px solid #3e3e42;
            border-radius: 6px;
            background-color: #2d2d30;
            color: #ffffff;
            min-height: 35px;
        }
        
        QLineEdit:focus {
            border-color: #007acc;
            background-color: #252526;
        }
        
        QLineEdit::placeholder {
            color: #808080;
            font-style: italic;
        }
        
        QLineEdit:disabled {
            background-color: #2d2d30;
            color: #6e6e6e;
            border-color: #3e3e42;
        }
        
        /* ComboBox - FIXED! */
        QComboBox {
            padding: 10px 15px;
            padding-right: 35px;
            font-size: 14px;
            font-weight: 500;
            border: 2px solid #3e3e42;
            border-radius: 6px;
            background-color: #2d2d30;
            color: #ffffff;
            min-height: 35px;
        }
        
        QComboBox:hover {
            border-color: #007acc;
        }
        
        QComboBox:focus {
            border-color: #007acc;
            background-color: #252526;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: right center;
            width: 30px;
            border: none;
        }
        
        QComboBox::down-arrow {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 7px solid #ffffff;
            margin-right: 8px;
        }
        
        QComboBox::down-arrow:hover {
            border-top-color: #007acc;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2d2d30;
            color: #ffffff;
            selection-background-color: #007acc;
            selection-color: white;
            border: 2px solid #007acc;
            border-radius: 6px;
            padding: 5px;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px;
            min-height: 30px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #3e3e42;
        }
        
        /* Progress Bar */
        QProgressBar {
            border: 1px solid #3e3e42;
            border-radius: 6px;
            background-color: #1e1e1e;
            text-align: center;
            font-weight: 600;
            height: 30px;
            color: #ffffff;
        }
        
        QProgressBar::chunk {
            background-color: #007acc;
            border-radius: 4px;
        }
        
        /* CheckBox - FIXED! */
        QCheckBox {
            color: #ffffff;
            font-size: 14px;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #3e3e42;
            border-radius: 4px;
            background-color: #2d2d30;
        }
        
        QCheckBox::indicator:hover {
            border-color: #007acc;
        }
        
        QCheckBox::indicator:checked {
            background-color: #007acc;
            border-color: #007acc;
        }
        
        /* RadioButton */
        QRadioButton {
            color: #ffffff;
            font-size: 14px;
            spacing: 8px;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #3e3e42;
            border-radius: 9px;
            background-color: #2d2d30;
        }
        
        QRadioButton::indicator:hover {
            border-color: #007acc;
        }
        
        QRadioButton::indicator:checked {
            background-color: #007acc;
            border-color: #007acc;
        }
        
        /* Table */
        QTableWidget {
            background-color: #252526;
            border-radius: 8px;
            border: 1px solid #3e3e42;
            gridline-color: #3e3e42;
            color: #ffffff;
        }
        
        QTableWidget::item {
            padding: 8px;
            color: #ffffff;
        }
        
        QTableWidget::item:selected {
            background-color: #007acc;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #2d2d30;
            padding: 10px;
            border: none;
            font-weight: 600;
            color: #ffffff;
        }
        
        /* Text Edit */
        QTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3e3e42;
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
        }
        
        /* Group Box */
        QGroupBox {
            color: #ffffff;
            border: 2px solid #3e3e42;
            border-radius: 8px;
            margin-top: 10px;
            padding: 15px;
            font-weight: 600;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        /* Scroll Bar */
        QScrollBar:vertical {
            background-color: #1e1e1e;
            width: 12px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3e3e42;
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #505053;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background-color: #1e1e1e;
            height: 12px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3e3e42;
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #505053;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        
        /* DateTimeEdit */
        QDateTimeEdit {
            padding: 10px;
            font-size: 14px;
            border: 2px solid #3e3e42;
            border-radius: 6px;
            background-color: #2d2d30;
            color: #ffffff;
            min-height: 35px;
        }
        
        QDateTimeEdit::up-button, QDateTimeEdit::down-button {
            width: 20px;
            border: none;
            background-color: #3e3e42;
        }
        
        QDateTimeEdit::up-button:hover, QDateTimeEdit::down-button:hover {
            background-color: #505053;
        }
    """)


# ====================================
# FIX 2: CREATE_WIPE_PAGE - BROWSE BUTTON FIX
# Find the line around 353 and replace browse button section:
# ====================================

# FIND THIS:
"""
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("secondary-btn")
        browse_btn.clicked.connect(self.select_file)
"""

# REPLACE WITH THIS:
"""
        browse_btn = QPushButton("📁 Browse")
        browse_btn.setObjectName("secondary-btn")
        browse_btn.setMinimumWidth(120)  # Fix: Prevent text wrapping
        browse_btn.setFixedHeight(45)     # Fix: Consistent height  
        browse_btn.clicked.connect(self.select_file)
"""

# ====================================
# HOW TO APPLY THESE FIXES:
# ====================================

"""
METHOD 1: Replace Function (EASIEST)
1. Open your secure_wipe_desktop.py
2. Find def apply_dark_theme(self):
3. Delete the ENTIRE function (from def to end of stylesheet)
4. Copy-paste the NEW function from above
5. Save and run!

METHOD 2: Find & Replace Browse Button
1. Search for: browse_btn = QPushButton("Browse...")
2. Replace with the fixed version above
3. Save and run!

RESULT:
✅ All text visible (white color)
✅ Algorithm dropdown shows selection
✅ Browse button fully visible
✅ Placeholder text visible (gray)
✅ Labels clear and bold
✅ Dropdown arrow visible
"""
