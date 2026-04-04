"""
Secure Data Wiping System - Desktop Application
Professional Windows Application with Modern UI
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QProgressBar,
    QFileDialog, QMessageBox, QListWidget, QStackedWidget,
    QTableWidget, QTableWidgetItem, QFrame, QTextEdit, QCheckBox,
    QDateTimeEdit, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread, QDateTime
from PyQt6.QtGui import QFont, QIcon

from wiper_core import SecureWiper

# Import new modules
try:
    from certificate_generator import generate_wipe_certificate
    CERTIFICATES_ENABLED = True
except ImportError:
    CERTIFICATES_ENABLED = False
    print("Certificate generation disabled - install reportlab")

try:
    from email_system import EmailReportSystem
    EMAIL_ENABLED = True
except ImportError:
    EMAIL_ENABLED = False
    print("Email system disabled")

try:
    from history_manager import get_history_manager
    HISTORY_ENABLED = True
except ImportError:
    HISTORY_ENABLED = False
    print("History management disabled")

try:
    from verification_module import WipeVerifier, QuickVerifier
    VERIFICATION_ENABLED = True
except ImportError:
    VERIFICATION_ENABLED = False
    print("Verification disabled")

try:
    from scheduled_wipe import ScheduleManager, ScheduledTask, ScheduleType, format_schedule_time
    SCHEDULING_ENABLED = True
except ImportError:
    SCHEDULING_ENABLED = False
    print("Scheduling disabled")

# =========================
# Free Space Wiper Classes
# =========================

class FreeSpaceWiper:
    """Wipes free disk space on a given drive."""

    def __init__(self, drive_path="C:\\", algorithm="dod", passes=3):
        self.drive_path = drive_path
        self.algorithm  = algorithm
        self.passes     = passes
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def wipe_free_space(self, progress_callback=None):
        """Fill free space with random data then delete the fill file."""
        import tempfile, os, random
        try:
            tmp = os.path.join(self.drive_path, "_fsw_tmp.bin")
            chunk = 1024 * 1024  # 1 MB chunks
            written = 0
            # Get available free bytes
            import shutil
            total, used, free = shutil.disk_usage(self.drive_path)
            target = max(0, free - 50 * 1024 * 1024)  # leave 50 MB buffer
            with open(tmp, "wb") as f:
                while written < target and not self._cancelled:
                    size = min(chunk, target - written)
                    f.write(os.urandom(size))
                    written += size
                    if progress_callback and target > 0:
                        progress_callback(int(written * 100 / target), "Wiping free space...")
            if os.path.exists(tmp):
                os.remove(tmp)
            return True, "Free space wiped successfully"
        except Exception as e:
            return False, str(e)


class FreeSpaceManager:
    """Manages free-space wipe jobs and their results."""

    def __init__(self):
        self._jobs = []

    def add_job(self, drive, algorithm="dod"):
        job = FreeSpaceWiper(drive, algorithm)
        self._jobs.append(job)
        return job

    def get_jobs(self):
        return list(self._jobs)

    def clear_jobs(self):
        self._jobs.clear()


FREE_SPACE_ENABLED = True


# =========================
# Worker Thread for Wiping
# =========================

class WipeWorker(QObject):
    """Background worker for file wiping operations"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, file_path, algorithm_key, wiper):
        super().__init__()
        self.file_path = file_path
        self.algorithm_key = algorithm_key
        self.wiper = wiper

    def run(self):
        """Execute the wipe operation"""
        try:
            self.wiper.set_algorithm(self.algorithm_key)
            
            success = self.wiper.wipe_file(
                self.file_path,
                progress_callback=self._update_progress
            )

            if success:
                self.finished.emit(True, "File wiped successfully!")
            else:
                self.finished.emit(False, "Wipe operation failed")

        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")

    def _update_progress(self, percent, status):
        """Update progress during wipe"""
        self.progress.emit(percent, status)


# =========================
# Main Application Window
# =========================

class SecureWipeApp(QMainWindow):
    """Main application window with modern UI"""

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Secure Data Wiping System v2.0")
        self.setMinimumSize(1280, 800)
        
        # Initialize wiper engine
        self.wiper = SecureWiper()
        
        # Worker thread
        self.worker_thread = None
        self.worker = None
        
        # Initialize history manager FIRST
        if HISTORY_ENABLED:
            self.history_manager = get_history_manager()
            # DO NOT load to wipe_history - causes double counting
            self.wipe_history = []  # Keep empty for in-memory only
        else:
            self.history_manager = None
            self.wipe_history = []
        
        # Initialize email system
        if EMAIL_ENABLED:
            self.email_system = EmailReportSystem()
        else:
            self.email_system = None
        
        # Build UI
        self.init_ui()
        
        # Load saved settings
        self.load_settings()
        
        # Apply styles (light theme by default)
        self.apply_styles()
        
        # Check if monthly report should be sent
        if self.email_system and self.email_system.should_send_monthly_report():
            self.send_monthly_report_check()

    # =========================
    # UI Initialization
    # =========================

    def init_ui(self):
        """Initialize the user interface"""
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar Navigation
        self.sidebar = self.create_sidebar()
        
        # Content Pages
        self.pages = QStackedWidget()
        
        self.dashboard_page = self.create_dashboard()
        self.wipe_page = self.create_wipe_page()
        self.audit_page = self.create_audit_page()
        self.settings_page = self.create_settings_page()
        self.about_page = self.create_about_page()
        
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.wipe_page)
        self.pages.addWidget(self.audit_page)
        self.pages.addWidget(self.settings_page)
        self.pages.addWidget(self.about_page)
        
        # Add to layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages, 1)
        
        main_widget.setLayout(main_layout)
        
        # Set default page
        self.sidebar.setCurrentRow(0)

    # =========================
    # Sidebar
    # =========================

    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QListWidget()
        sidebar.setFixedWidth(240)
        
        items = [
            "🏠 Dashboard",
            "🗑️ Secure Wipe",
            "📋 Audit Logs",
            "⚙️ Settings",
            "ℹ️ About"
        ]
        
        sidebar.addItems(items)
        sidebar.currentRowChanged.connect(self.change_page)
        
        return sidebar

    # =========================
    # Dashboard Page
    # =========================

    def create_dashboard(self):
        """Create enhanced dashboard with statistics and charts"""
        # Try to use enhanced dashboard with charts
        try:
            from enhanced_dashboard import EnhancedDashboard
            return EnhancedDashboard(self)
        except ImportError:
            # Fallback to basic dashboard
            return self.create_basic_dashboard()
    
    def create_basic_dashboard(self):
        """Create basic dashboard without charts (fallback)"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Dashboard")
        title.setObjectName("page-title")
        layout.addWidget(title)
        
        # Statistics Cards Container
        self.stats_container = QWidget()
        stats_layout = QHBoxLayout()
        
        # Create stat cards with references
        self.total_card = self.create_stat_card(
            "Total Wipes",
            "0",
            "#3498db"
        )
        self.success_card = self.create_stat_card(
            "Successful",
            "0",
            "#2ecc71"
        )
        self.failed_card = self.create_stat_card(
            "Failed",
            "0",
            "#e74c3c"
        )
        self.data_card = self.create_stat_card(
            "Data Destroyed",
            "0 MB",
            "#9b59b6"
        )
        
        stats_layout.addWidget(self.total_card)
        stats_layout.addWidget(self.success_card)
        stats_layout.addWidget(self.failed_card)
        stats_layout.addWidget(self.data_card)
        
        self.stats_container.setLayout(stats_layout)
        layout.addWidget(self.stats_container)
        
        # Quick Actions
        actions_label = QLabel("Quick Actions")
        actions_label.setObjectName("section-title")
        layout.addWidget(actions_label)
        
        actions_layout = QHBoxLayout()
        
        wipe_btn = QPushButton("Start New Wipe")
        wipe_btn.setObjectName("primary-btn")
        wipe_btn.clicked.connect(lambda: self.sidebar.setCurrentRow(1))
        
        audit_btn = QPushButton("View Audit Logs")
        audit_btn.setObjectName("secondary-btn")
        audit_btn.clicked.connect(lambda: self.sidebar.setCurrentRow(2))
        
        actions_layout.addWidget(wipe_btn)
        actions_layout.addWidget(audit_btn)
        
        layout.addLayout(actions_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName("stat-card")
        card.setStyleSheet(f"""
            QFrame#stat-card {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setObjectName("stat-title")
        
        value_label = QLabel(value)
        value_label.setObjectName("stat-value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card

    # =========================
    # Wipe Page
    # =========================

    def create_wipe_page(self):
        """Create file wiping page"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Secure File Wipe")
        title.setObjectName("page-title")
        layout.addWidget(title)
        
        # File Selection
        file_group = QFrame()
        file_group.setObjectName("content-card")
        file_layout = QVBoxLayout()
        
        file_label = QLabel("Select File to Wipe:")
        file_label.setObjectName("section-title")
        
        file_input_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("No file selected...")
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("secondary-btn")
        browse_btn.clicked.connect(self.select_file)
        
        file_input_layout.addWidget(self.file_input, 1)
        file_input_layout.addWidget(browse_btn)
        
        file_layout.addWidget(file_label)
        file_layout.addLayout(file_input_layout)
        file_group.setLayout(file_layout)
        
        layout.addWidget(file_group)
        
        # Algorithm Selection
        algo_group = QFrame()
        algo_group.setObjectName("content-card")
        algo_layout = QVBoxLayout()
        
        algo_label = QLabel("Wiping Algorithm:")
        algo_label.setObjectName("section-title")
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItem("🛡️ DoD 5220.22-M (3 passes) - Recommended", "dod")
        self.algo_combo.addItem("⚡ Single Pass (Fast)", "simple")
        self.algo_combo.addItem("🔒 NIST SP 800-88 (Modern SSDs)", "nist")
        self.algo_combo.addItem("🔐 Gutmann (7 passes - High Security)", "gutmann")
        self.algo_combo.addItem("🔑 Cryptographic Erase", "crypto")
        
        algo_description = QLabel(
            "DoD 5220.22-M is recommended for most users. "
            "It provides excellent security with reasonable speed."
        )
        algo_description.setObjectName("description-text")
        algo_description.setWordWrap(True)
        
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)
        algo_layout.addWidget(algo_description)
        algo_group.setLayout(algo_layout)
        
        layout.addWidget(algo_group)
        
        # Verification Option (if enabled)
        if VERIFICATION_ENABLED:
            verify_group = QFrame()
            verify_group.setObjectName("content-card")
            verify_layout = QVBoxLayout()
            
            self.verify_checkbox = QCheckBox("🔍 Verify wipe after completion")
            self.verify_checkbox.setChecked(True)  # Enabled by default
            self.verify_checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 14px;
                    font-weight: 600;
                    color: #2c3e50;
                }
            """)
            
            verify_desc = QLabel(
                "Verification checks that the file has been completely erased "
                "and generates a confidence score."
            )
            verify_desc.setObjectName("description-text")
            verify_desc.setWordWrap(True)
            
            verify_layout.addWidget(self.verify_checkbox)
            verify_layout.addWidget(verify_desc)
            verify_group.setLayout(verify_layout)
            
            layout.addWidget(verify_group)
        else:
            self.verify_checkbox = None
        
        # Progress Section
        progress_group = QFrame()
        progress_group.setObjectName("content-card")
        progress_layout = QVBoxLayout()
        
        progress_label = QLabel("Operation Progress:")
        progress_label.setObjectName("section-title")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        
        self.status_label = QLabel("Ready to wipe")
        self.status_label.setObjectName("status-text")
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        progress_group.setLayout(progress_layout)
        
        layout.addWidget(progress_group)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        
        self.wipe_btn = QPushButton("🗑️ START SECURE WIPE")
        self.wipe_btn.setObjectName("danger-btn")
        self.wipe_btn.setMinimumHeight(50)
        self.wipe_btn.clicked.connect(self.start_wipe)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary-btn")
        cancel_btn.setMinimumHeight(50)
        cancel_btn.clicked.connect(self.cancel_wipe)
        
        btn_layout.addWidget(self.wipe_btn, 3)
        btn_layout.addWidget(cancel_btn, 1)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    # =========================
    # Audit Page
    # =========================

    def create_audit_page(self):
        """Create audit logs page"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Audit Logs")
        title.setObjectName("page-title")
        layout.addWidget(title)
        
        # Table
        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(5)
        self.audit_table.setHorizontalHeaderLabels([
            "Timestamp",
            "File Path",
            "Algorithm",
            "Status",
            "Duration"
        ])
        self.audit_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.audit_table)
        
        # Load existing history
        if self.history_manager:
            self.load_audit_history()
        
        # Export Button
        export_btn = QPushButton("📄 Export Logs")
        export_btn.setObjectName("secondary-btn")
        export_btn.clicked.connect(self.export_logs)
        layout.addWidget(export_btn)
        
        widget.setLayout(layout)
        return widget

    # =========================
    # Settings Page
    # =========================

    def create_settings_page(self):
        """Create settings page with full configuration"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Settings")
        title.setObjectName("page-title")
        layout.addWidget(title)
        
        # Scrollable container for settings
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # === GENERAL SETTINGS ===
        general_card = self.create_settings_card(
            "General Settings",
            self.create_general_settings()
        )
        scroll_layout.addWidget(general_card)
        
        # === SECURITY SETTINGS ===
        security_card = self.create_settings_card(
            "Security & Confirmation",
            self.create_security_settings()
        )
        scroll_layout.addWidget(security_card)
        
        # === APPEARANCE SETTINGS ===
        appearance_card = self.create_settings_card(
            "Appearance",
            self.create_appearance_settings()
        )
        scroll_layout.addWidget(appearance_card)
        
        # === NOTIFICATION SETTINGS ===
        notification_card = self.create_settings_card(
            "Notifications",
            self.create_notification_settings()
        )
        scroll_layout.addWidget(notification_card)
        
        # === ADVANCED SETTINGS ===
        advanced_card = self.create_settings_card(
            "Advanced",
            self.create_advanced_settings()
        )
        scroll_layout.addWidget(advanced_card)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setObjectName("primary-btn")
        save_btn.clicked.connect(self.save_settings)
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.setObjectName("secondary-btn")
        reset_btn.clicked.connect(self.reset_settings)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(reset_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_card(self, title, content_widget):
        """Create a settings card container"""
        card = QFrame()
        card.setObjectName("content-card")
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setObjectName("section-title")
        card_layout.addWidget(title_label)
        
        card_layout.addWidget(content_widget)
        card.setLayout(card_layout)
        
        return card
    
    def create_general_settings(self):
        """Create general settings section"""
        from PyQt6.QtWidgets import QCheckBox
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Default Algorithm
        algo_layout = QVBoxLayout()
        algo_label = QLabel("Default Wiping Algorithm:")
        algo_label.setStyleSheet("color: #2c3e50; font-weight: 600;")
        self.settings_algo_combo = QComboBox()
        self.settings_algo_combo.addItem("🛡️ DoD 5220.22-M (Recommended)", "dod")
        self.settings_algo_combo.addItem("⚡ Single Pass (Fast)", "simple")
        self.settings_algo_combo.addItem("🔒 NIST SP 800-88", "nist")
        self.settings_algo_combo.addItem("🔐 Gutmann (High Security)", "gutmann")
        self.settings_algo_combo.addItem("🔑 Cryptographic Erase", "crypto")
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.settings_algo_combo)
        layout.addLayout(algo_layout)
        
        # Large File Warning Threshold
        threshold_layout = QVBoxLayout()
        threshold_label = QLabel("Large File Warning (GB):")
        threshold_label.setStyleSheet("color: #2c3e50; font-weight: 600;")
        self.large_file_threshold = QComboBox()
        self.large_file_threshold.addItems(["1 GB", "5 GB", "10 GB", "20 GB", "50 GB"])
        self.large_file_threshold.setCurrentIndex(1)  # Default 5 GB
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.large_file_threshold)
        layout.addLayout(threshold_layout)
        
        # Checkboxes
        self.auto_close_checkbox = QCheckBox("Auto-close application after wipe")
        self.sound_effects_checkbox = QCheckBox("Enable sound effects")
        self.minimize_to_tray_checkbox = QCheckBox("Minimize to system tray on close")
        
        layout.addWidget(self.auto_close_checkbox)
        layout.addWidget(self.sound_effects_checkbox)
        layout.addWidget(self.minimize_to_tray_checkbox)
        
        widget.setLayout(layout)
        return widget
    
    def create_security_settings(self):
        """Create security settings section"""
        from PyQt6.QtWidgets import QCheckBox
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        self.confirm_before_wipe_checkbox = QCheckBox("Show confirmation dialog before wiping")
        self.confirm_before_wipe_checkbox.setChecked(True)
        
        self.double_confirm_large_checkbox = QCheckBox("Double confirmation for files >5GB")
        self.double_confirm_large_checkbox.setChecked(True)
        
        self.verify_after_wipe_checkbox = QCheckBox("Verify wipe after completion")
        
        self.secure_delete_logs_checkbox = QCheckBox("Securely delete old logs")
        
        layout.addWidget(self.confirm_before_wipe_checkbox)
        layout.addWidget(self.double_confirm_large_checkbox)
        layout.addWidget(self.verify_after_wipe_checkbox)
        layout.addWidget(self.secure_delete_logs_checkbox)
        
        widget.setLayout(layout)
        return widget
    
    def create_appearance_settings(self):
        """Create appearance settings section"""
        from PyQt6.QtWidgets import QCheckBox, QRadioButton, QButtonGroup
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Theme Selection
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-weight: 600; color: #2c3e50;")
        layout.addWidget(theme_label)
        
        self.theme_button_group = QButtonGroup()
        
        self.light_theme_radio = QRadioButton("☀️ Light Mode")
        self.light_theme_radio.setChecked(True)
        self.dark_theme_radio = QRadioButton("🌙 Dark Mode")
        self.auto_theme_radio = QRadioButton("🔄 Auto (System)")
        
        self.theme_button_group.addButton(self.light_theme_radio, 0)
        self.theme_button_group.addButton(self.dark_theme_radio, 1)
        self.theme_button_group.addButton(self.auto_theme_radio, 2)
        
        # Connect theme change
        self.light_theme_radio.toggled.connect(self.on_theme_changed)
        self.dark_theme_radio.toggled.connect(self.on_theme_changed)
        
        layout.addWidget(self.light_theme_radio)
        layout.addWidget(self.dark_theme_radio)
        layout.addWidget(self.auto_theme_radio)
        
        # Font Size
        font_layout = QVBoxLayout()
        font_label = QLabel("Font Size:")
        font_label.setStyleSheet("font-weight: 600; margin-top: 10px; color: #2c3e50;")
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Small", "Medium", "Large"])
        self.font_size_combo.setCurrentIndex(1)  # Default Medium
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_size_combo)
        layout.addLayout(font_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_notification_settings(self):
        """Create notification settings section"""
        from PyQt6.QtWidgets import QCheckBox
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        self.enable_notifications_checkbox = QCheckBox("Enable desktop notifications")
        self.enable_notifications_checkbox.setChecked(True)
        
        self.notify_on_complete_checkbox = QCheckBox("Notify when wipe completes")
        self.notify_on_complete_checkbox.setChecked(True)
        
        self.notify_on_error_checkbox = QCheckBox("Notify on errors")
        self.notify_on_error_checkbox.setChecked(True)
        
        self.play_sound_checkbox = QCheckBox("Play sound on completion")
        
        layout.addWidget(self.enable_notifications_checkbox)
        layout.addWidget(self.notify_on_complete_checkbox)
        layout.addWidget(self.notify_on_error_checkbox)
        layout.addWidget(self.play_sound_checkbox)
        
        widget.setLayout(layout)
        return widget
    
    def create_advanced_settings(self):
        """Create advanced settings section"""
        from PyQt6.QtWidgets import QCheckBox
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Log Retention
        log_layout = QVBoxLayout()
        log_label = QLabel("Log Retention Period:")
        log_label.setStyleSheet("color: #2c3e50; font-weight: 600;")
        self.log_retention_combo = QComboBox()
        self.log_retention_combo.addItems([
            "7 Days",
            "30 Days",
            "90 Days",
            "1 Year",
            "Forever"
        ])
        self.log_retention_combo.setCurrentIndex(2)  # Default 90 days
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.log_retention_combo)
        layout.addLayout(log_layout)
        
        # Advanced Options
        self.auto_export_logs_checkbox = QCheckBox("Auto-export logs monthly")
        self.check_updates_checkbox = QCheckBox("Check for updates on startup")
        self.anonymous_stats_checkbox = QCheckBox("Send anonymous usage statistics")
        
        layout.addWidget(self.auto_export_logs_checkbox)
        layout.addWidget(self.check_updates_checkbox)
        layout.addWidget(self.anonymous_stats_checkbox)
        
        widget.setLayout(layout)
        return widget
    
    def on_theme_changed(self):
        """Handle theme change"""
        if self.dark_theme_radio.isChecked():
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background-color: #1e1e1e;
            }
            
            /* Sidebar */
            QListWidget {
                background-color: #252526;
                color: #cccccc;
                font-size: 15px;
                font-weight: 500;
                border: none;
                padding: 10px 0;
            }
            
            QListWidget::item {
                padding: 15px 20px;
                border-left: 4px solid transparent;
            }
            
            QListWidget::item:selected {
                background-color: #2d2d30;
                border-left: 4px solid #007acc;
            }
            
            QListWidget::item:hover {
                background-color: #2d2d30;
            }
            
            /* Page Titles */
            QLabel#page-title {
                font-size: 32px;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 20px;
            }
            
            QLabel#section-title {
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 10px;
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
                color: #cccccc;
                padding: 10px;
                background-color: #2d2d30;
                border-radius: 5px;
            }
            
            QLabel {
                color: #cccccc;
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
                color: #cccccc;
            }
            
            QPushButton#secondary-btn:hover {
                background-color: #505053;
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
            
            /* Input Fields */
            QLineEdit, QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #3e3e42;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: #cccccc;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border-color: #007acc;
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #252526;
                color: #cccccc;
                selection-background-color: #007acc;
                selection-color: white;
                border: 1px solid #3e3e42;
            }
            
            /* Progress Bar */
            QProgressBar {
                border: 1px solid #3e3e42;
                border-radius: 6px;
                background-color: #1e1e1e;
                text-align: center;
                font-weight: 600;
                height: 30px;
                color: #cccccc;
            }
            
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 4px;
            }
            
            /* Table */
            QTableWidget {
                background-color: #252526;
                border-radius: 8px;
                border: 1px solid #3e3e42;
                gridline-color: #3e3e42;
                color: #cccccc;
            }
            
            QTableWidget::item {
                padding: 8px;
                color: #cccccc;
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
                border: 1px solid #3e3e42;
                border-radius: 8px;
                padding: 15px;
                font-size: 13px;
                color: #cccccc;
            }
            
            /* CheckBox */
            QCheckBox, QRadioButton {
                color: #cccccc;
                spacing: 8px;
                padding: 5px;
            }
            
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid #3e3e42;
                background-color: #1e1e1e;
            }
            
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background-color: #007acc;
                border-color: #007acc;
            }
            
            QCheckBox::indicator:hover, QRadioButton::indicator:hover {
                border-color: #007acc;
            }
            
            /* ScrollArea */
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #3e3e42;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #505053;
            }
        """)
    
    def apply_light_theme(self):
        """Apply light theme (original)"""
        self.apply_styles()  # Call original light theme
    
    def save_settings(self):
        """Save all settings to JSON file and apply them"""
        import json
        
        settings = {
            'general': {
                'default_algorithm': self.settings_algo_combo.currentData(),
                'large_file_threshold': self.large_file_threshold.currentText(),
                'auto_close': self.auto_close_checkbox.isChecked(),
                'sound_effects': self.sound_effects_checkbox.isChecked(),
                'minimize_to_tray': self.minimize_to_tray_checkbox.isChecked()
            },
            'security': {
                'confirm_before_wipe': self.confirm_before_wipe_checkbox.isChecked(),
                'double_confirm_large': self.double_confirm_large_checkbox.isChecked(),
                'verify_after_wipe': self.verify_after_wipe_checkbox.isChecked(),
                'secure_delete_logs': self.secure_delete_logs_checkbox.isChecked()
            },
            'appearance': {
                'theme': 'dark' if self.dark_theme_radio.isChecked() else 'light',
                'font_size': self.font_size_combo.currentText()
            },
            'notifications': {
                'enable_notifications': self.enable_notifications_checkbox.isChecked(),
                'notify_on_complete': self.notify_on_complete_checkbox.isChecked(),
                'notify_on_error': self.notify_on_error_checkbox.isChecked(),
                'play_sound': self.play_sound_checkbox.isChecked()
            },
            'advanced': {
                'log_retention': self.log_retention_combo.currentText(),
                'auto_export_logs': self.auto_export_logs_checkbox.isChecked(),
                'check_updates': self.check_updates_checkbox.isChecked(),
                'anonymous_stats': self.anonymous_stats_checkbox.isChecked()
            }
        }
        
        try:
            os.makedirs('config', exist_ok=True)
            with open('config/settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            
            # Apply settings immediately
            self.apply_saved_settings(settings)
            
            QMessageBox.information(
                self,
                "Settings Saved",
                "✅ Your settings have been saved and applied successfully!"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save Failed",
                f"Error saving settings:\n{str(e)}"
            )
    
    def apply_saved_settings(self, settings):
        """Apply loaded settings to the application"""
        try:
            # Store settings globally for use in wipe operations
            self.app_settings = settings
            
            # Apply default algorithm to wipe page dropdown
            default_algo = settings.get('general', {}).get('default_algorithm', 'dod')
            for i in range(self.algo_combo.count()):
                if self.algo_combo.itemData(i) == default_algo:
                    self.algo_combo.setCurrentIndex(i)
                    break
            
            # Apply theme
            theme = settings.get('appearance', {}).get('theme', 'light')
            if theme == 'dark':
                self.apply_dark_theme()
            else:
                self.apply_light_theme()
                
        except Exception as e:
            print(f"Error applying settings: {e}")
    
    def load_settings(self):
        """Load settings from JSON file and apply them"""
        import json
        
        try:
            if os.path.exists('config/settings.json'):
                with open('config/settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Apply loaded settings
                self.apply_saved_settings(settings)
                
                return settings
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # Return default settings
        return {
            'general': {'default_algorithm': 'dod'},
            'appearance': {'theme': 'light'},
            'notifications': {'enable_notifications': True}
        }
    
    def reset_settings(self):
        """Reset all settings to default"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset to defaults
            self.settings_algo_combo.setCurrentIndex(0)
            self.large_file_threshold.setCurrentIndex(1)
            self.auto_close_checkbox.setChecked(False)
            self.sound_effects_checkbox.setChecked(False)
            self.minimize_to_tray_checkbox.setChecked(False)
            
            self.confirm_before_wipe_checkbox.setChecked(True)
            self.double_confirm_large_checkbox.setChecked(True)
            self.verify_after_wipe_checkbox.setChecked(False)
            self.secure_delete_logs_checkbox.setChecked(False)
            
            self.light_theme_radio.setChecked(True)
            self.font_size_combo.setCurrentIndex(1)
            
            self.enable_notifications_checkbox.setChecked(True)
            self.notify_on_complete_checkbox.setChecked(True)
            self.notify_on_error_checkbox.setChecked(True)
            self.play_sound_checkbox.setChecked(False)
            
            self.log_retention_combo.setCurrentIndex(2)
            self.auto_export_logs_checkbox.setChecked(False)
            self.check_updates_checkbox.setChecked(False)
            self.anonymous_stats_checkbox.setChecked(False)
            
            QMessageBox.information(
                self,
                "Settings Reset",
                "✅ All settings have been reset to default values."
            )

    # =========================
    # About Page
    # =========================

    def create_about_page(self):
        """Create about page"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("About Secure Wipe")
        title.setObjectName("page-title")
        layout.addWidget(title)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 8px;
                padding: 20px;
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        about_text.setHtml("""
            <div style='font-family: Arial, sans-serif; color: #2c3e50;'>
                <h2 style='color: #2c3e50;'>Secure Data Wiping System v2.0</h2>
                <p><b>A professional data destruction tool for end-of-life electronic devices</b></p>
                
                <h3 style='color: #3498db; margin-top: 20px;'>Supported Algorithms:</h3>
                <ul style='line-height: 1.8;'>
                    <li><b>DoD 5220.22-M</b> - US Department of Defense standard (3 passes)</li>
                    <li><b>NIST SP 800-88</b> - Modern storage media sanitization</li>
                    <li><b>Gutmann Method</b> - 7-pass secure overwrite</li>
                    <li><b>Cryptographic Erase</b> - Instant encryption-based wipe</li>
                    <li><b>Single Pass</b> - Quick random overwrite</li>
                </ul>
                
                <h3 style='color: #3498db; margin-top: 20px;'>Compliance:</h3>
                <ul style='line-height: 1.8;'>
                    <li>✅ GDPR Compliant</li>
                    <li>✅ HIPAA Ready</li>
                    <li>✅ PCI-DSS Certified Methods</li>
                </ul>
                
                <h3 style='color: #3498db; margin-top: 20px;'>Features:</h3>
                <ul style='line-height: 1.8;'>
                    <li>✨ Military-grade data destruction</li>
                    <li>📊 Comprehensive audit logging</li>
                    <li>🔒 Secure, tamper-proof operations</li>
                    <li>💼 Enterprise-ready architecture</li>
                </ul>
                
                <p style='margin-top: 30px; color: #7f8c8d;'><i>Copyright © 2024-2025. All rights reserved.</i></p>
            </div>
        """)
        
        layout.addWidget(about_text)
        
        widget.setLayout(layout)
        return widget

    # =========================
    # Navigation
    # =========================

    def change_page(self, index):
        """Change active page"""
        self.pages.setCurrentIndex(index)

    # =========================
    # File Operations
    # =========================

    def select_file(self):
        """Open file selection dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Wipe",
            "",
            "All Files (*.*)"
        )
        
        if file_path:
            self.file_input.setText(file_path)

    def start_wipe(self):
        """Start the wiping operation"""
        file_path = self.file_input.text().strip()
        
        if not file_path:
            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select a file to wipe."
            )
            return
        
        if not os.path.exists(file_path):
            QMessageBox.critical(
                self,
                "File Not Found",
                "The selected file does not exist."
            )
            return
        
        # Confirmation dialog
        file_name = Path(file_path).name
        reply = QMessageBox.question(
            self,
            "Confirm Wipe Operation",
            f"Are you sure you want to PERMANENTLY DELETE:\n\n{file_name}\n\n"
            f"This operation CANNOT be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Disable wipe button
        self.wipe_btn.setEnabled(False)
        
        # Get selected algorithm
        algorithm_key = self.algo_combo.currentData()
        
        # Create worker thread
        self.worker_thread = QThread()
        self.worker = WipeWorker(file_path, algorithm_key, self.wiper)
        
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.wipe_finished)
        self.worker.finished.connect(self.worker_thread.quit)
        
        # Start operation
        self.worker_thread.start()

    def cancel_wipe(self):
        """Cancel ongoing wipe operation"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.status_label.setText("Operation cancelled")
            self.wipe_btn.setEnabled(True)

    def update_progress(self, percent, status):
        """Update progress bar and status"""
        self.progress_bar.setValue(percent)
        self.status_label.setText(status)

    def wipe_finished(self, success, message):
        """Handle wipe completion"""
        # Re-enable button
        self.wipe_btn.setEnabled(True)
        
        # Reset progress
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready to wipe")
        
        file_path = self.file_input.text()
        algorithm = self.algo_combo.currentText()
        
        # Add to audit table
        self.add_audit_entry(file_path, algorithm, "Success" if success else "Failed", success)
        
        if success:
            # Get file size before it's deleted
            try:
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            except:
                file_size = 0
            
            # Generate certificate if enabled
            certificate_path = None
            if CERTIFICATES_ENABLED:
                try:
                    certificate_path = generate_wipe_certificate(
                        file_path=file_path,
                        file_size=file_size,
                        algorithm=algorithm,
                        timestamp=datetime.now(),
                        success=True
                    )
                    
                    # Show certificate generated message
                    cert_msg = f"\n\n📜 Certificate generated:\n{certificate_path}"
                    message += cert_msg
                    
                    # Email certificate if enabled
                    if self.email_system and self.email_system.config.get('auto_send_enabled'):
                        success_email, email_msg = self.email_system.send_instant_certificate(
                            certificate_path,
                            Path(file_path).name
                        )
                        if success_email:
                            message += "\n\n📧 Certificate emailed successfully!"
                        
                except Exception as e:
                    print(f"Certificate generation error: {e}")
            
            # Save to history manager
            if self.history_manager:
                try:
                    self.history_manager.add_wipe_entry(
                        file_path=file_path,
                        file_size=file_size,
                        algorithm=algorithm,
                        success=True,
                        duration=0.0,  # TODO: Track actual duration
                        certificate_path=certificate_path
                    )
                except Exception as e:
                    print(f"History save error: {e}")
            
            # Run verification if enabled
            verification_result = None
            if VERIFICATION_ENABLED and self.verify_checkbox and self.verify_checkbox.isChecked():
                try:
                    verifier = QuickVerifier()
                    verification_result = verifier.verify_and_report(file_path)
                    
                    # Add verification info to message
                    if verification_result['passed']:
                        message += f"\n\n✅ Verification: PASSED"
                        message += f"\n🎯 Confidence: {verification_result['confidence']:.1f}%"
                    else:
                        message += f"\n\n⚠️ Verification: {verification_result['message']}"
                        
                except Exception as e:
                    print(f"Verification error: {e}")
            
            QMessageBox.information(
                self,
                "Success",
                f"✅ {message}\n\nFile has been securely wiped and deleted."
            )
            
            # Clear file input
            self.file_input.clear()
            
            # Update dashboard statistics
            self.update_dashboard_stats()
            
        else:
            # Save failed attempt to history
            if self.history_manager:
                try:
                    self.history_manager.add_wipe_entry(
                        file_path=file_path,
                        file_size=0,
                        algorithm=algorithm,
                        success=False,
                        error_message=message
                    )
                except Exception as e:
                    print(f"History save error: {e}")
            
            QMessageBox.critical(
                self,
                "Error",
                f"❌ {message}\n\nPlease check the file and try again."
            )

    def update_dashboard_stats(self):
        """Update dashboard with latest statistics"""
        try:
            # Get history from history_manager (persistent storage)
            if self.history_manager:
                wipe_history = self.history_manager.get_all_history()
            else:
                # Fallback to in-memory if history_manager not available
                wipe_history = self.wipe_history
            
            # Calculate current statistics
            total = len(wipe_history)
            successful = sum(1 for h in wipe_history if h.get('success', False))
            failed = total - successful
            
            # Calculate total data destroyed
            total_bytes = sum(h.get('file_size', 0) for h in wipe_history)
            if total_bytes < 1024:
                data_str = f"{total_bytes} B"
            elif total_bytes < 1024 * 1024:
                data_str = f"{total_bytes / 1024:.1f} KB"
            elif total_bytes < 1024 * 1024 * 1024:
                data_str = f"{total_bytes / (1024 * 1024):.1f} MB"
            else:
                data_str = f"{total_bytes / (1024 * 1024 * 1024):.2f} GB"
            
            # Update card values
            self.update_stat_card_value(self.total_card, str(total))
            self.update_stat_card_value(self.success_card, str(successful))
            self.update_stat_card_value(self.failed_card, str(failed))
            self.update_stat_card_value(self.data_card, data_str)
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
    
    def update_stat_card_value(self, card, new_value):
        """Update a single stat card's value"""
        try:
            # Find the value label in the card and update it
            layout = card.layout()
            if layout and layout.count() >= 2:
                value_label = layout.itemAt(1).widget()
                if isinstance(value_label, QLabel):
                    value_label.setText(new_value)
        except Exception as e:
            print(f"Error updating card: {e}")
    
    def send_monthly_report_check(self):
        """Check and send monthly report if needed"""
        if not self.email_system:
            return
        
        reply = QMessageBox.question(
            self,
            "Monthly Report",
            "It's time to send the monthly audit report. Send now?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.send_monthly_report()
    
    def send_monthly_report(self):
        """Send monthly report email"""
        if not self.email_system:
            QMessageBox.warning(
                self,
                "Email Not Configured",
                "Please configure email settings first."
            )
            return
        
        if not self.history_manager:
            QMessageBox.warning(
                self,
                "No History",
                "No wipe history available to send."
            )
            return
        
        # Get this month's history
        history = self.history_manager.get_monthly_history()
        
        if not history:
            QMessageBox.information(
                self,
                "No Data",
                "No wipe operations this month to report."
            )
            return
        
        # Send report
        success, message = self.email_system.send_monthly_report(history)
        
        if success:
            QMessageBox.information(
                self,
                "Report Sent",
                "✅ Monthly audit report sent successfully!"
            )
        else:
            QMessageBox.critical(
                self,
                "Send Failed",
                f"❌ Failed to send report:\n{message}"
            )

    def add_audit_entry(self, file_path, algorithm, status, success):
        """Add entry to audit log"""
        timestamp = datetime.now()
        
        # Get file size before it's deleted
        try:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
            else:
                file_size = 0
        except:
            file_size = 0
        
        # Only add to in-memory if history_manager is not available
        # (history_manager.add_wipe_entry() is called in wipe_finished())
        if not self.history_manager:
            self.wipe_history.append({
                'timestamp': timestamp,
                'file_path': file_path,
                'file_size': file_size,
                'algorithm': algorithm,
                'status': status,
                'success': success
            })
        
        # Add to table
        row = self.audit_table.rowCount()
        self.audit_table.insertRow(row)
        
        self.audit_table.setItem(
            row, 0,
            QTableWidgetItem(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.audit_table.setItem(
            row, 1,
            QTableWidgetItem(Path(file_path).name)
        )
        self.audit_table.setItem(
            row, 2,
            QTableWidgetItem(algorithm.split(' - ')[0])
        )
        self.audit_table.setItem(
            row, 3,
            QTableWidgetItem(status)
        )
        self.audit_table.setItem(
            row, 4,
            QTableWidgetItem("< 1 min")
        )

    def load_audit_history(self):
        """Load all history into audit table"""
        if not self.history_manager:
            return
        
        # Get all saved history
        all_history = self.history_manager.get_all_history()
        
        # Clear table first
        self.audit_table.setRowCount(0)
        
        # Add each entry to table
        for entry in all_history:
            row = self.audit_table.rowCount()
            self.audit_table.insertRow(row)
            
            # Timestamp
            timestamp = entry.get('timestamp')
            if isinstance(timestamp, datetime):
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(timestamp, str):
                # Handle ISO format string
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    timestamp_str = timestamp[:19] if len(timestamp) > 19 else timestamp
            else:
                timestamp_str = str(timestamp)
            
            # File path
            file_path = entry.get('file_path', 'Unknown')
            file_name = Path(file_path).name if file_path else 'Unknown'
            
            # Algorithm
            algorithm = entry.get('algorithm', 'Unknown')
            
            # Status
            status = "Success" if entry.get('success', False) else "Failed"
            
            # Duration
            duration = entry.get('duration_seconds', 0)
            if duration > 0:
                duration_str = f"{duration:.1f}s"
            else:
                duration_str = "< 1 min"
            
            # Add to table
            self.audit_table.setItem(row, 0, QTableWidgetItem(timestamp_str))
            self.audit_table.setItem(row, 1, QTableWidgetItem(file_name))
            self.audit_table.setItem(row, 2, QTableWidgetItem(algorithm))
            self.audit_table.setItem(row, 3, QTableWidgetItem(status))
            self.audit_table.setItem(row, 4, QTableWidgetItem(duration_str))
    
    def export_logs(self):
        """Export audit logs to file"""
        if not self.wipe_history:
            QMessageBox.information(
                self,
                "No Data",
                "No audit logs to export."
            )
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Audit Logs",
            f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("SECURE WIPE AUDIT LOG\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for entry in self.wipe_history:
                        f.write(f"Timestamp: {entry['timestamp']}\n")
                        f.write(f"File: {entry['file_path']}\n")
                        f.write(f"Algorithm: {entry['algorithm']}\n")
                        f.write(f"Status: {entry['status']}\n")
                        f.write("-" * 80 + "\n")
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Audit logs exported to:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Error exporting logs:\n{str(e)}"
                )

    # =========================
    # Styling
    # =========================

    def apply_styles(self):
        """Apply modern UI styling"""
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background-color: #f5f7fa;
            }
            
            /* Sidebar */
            QListWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 15px;
                font-weight: 500;
                border: none;
                padding: 10px 0;
            }
            
            QListWidget::item {
                padding: 15px 20px;
                border-left: 4px solid transparent;
            }
            
            QListWidget::item:selected {
                background-color: #34495e;
                border-left: 4px solid #1abc9c;
            }
            
            QListWidget::item:hover {
                background-color: #34495e;
            }
            
            /* Page Titles */
            QLabel#page-title {
                font-size: 32px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 20px;
            }
            
            QLabel#section-title {
                font-size: 16px;
                font-weight: 600;
                color: #34495e;
                margin-bottom: 10px;
            }
            
            QLabel#stat-title {
                font-size: 14px;
                color: #7f8c8d;
                font-weight: 500;
            }
            
            QLabel#stat-value {
                font-size: 36px;
                font-weight: 700;
                color: #2c3e50;
            }
            
            QLabel#status-text {
                font-size: 14px;
                color: #7f8c8d;
                font-style: italic;
            }
            
            QLabel#description-text {
                font-size: 13px;
                color: #7f8c8d;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }
            
            /* Cards */
            QFrame#content-card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            /* Buttons */
            QPushButton {
                font-size: 14px;
                font-weight: 600;
                border-radius: 6px;
                padding: 12px 24px;
                border: none;
            }
            
            QPushButton#primary-btn {
                background-color: #3498db;
                color: white;
            }
            
            QPushButton#primary-btn:hover {
                background-color: #2980b9;
            }
            
            QPushButton#secondary-btn {
                background-color: #95a5a6;
                color: white;
            }
            
            QPushButton#secondary-btn:hover {
                background-color: #7f8c8d;
            }
            
            QPushButton#danger-btn {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
            }
            
            QPushButton#danger-btn:hover {
                background-color: #c0392b;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #ecf0f1;
            }
            
            /* Input Fields */
            QLineEdit, QComboBox {
                padding: 10px;
                font-size: 14px;
                border: 2px solid #dfe4ea;
                border-radius: 6px;
                background-color: white;
                color: #2c3e50;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
            }
            
            /* Progress Bar */
            QProgressBar {
                border: 2px solid #dfe4ea;
                border-radius: 6px;
                background-color: #ecf0f1;
                text-align: center;
                font-weight: 600;
                height: 30px;
            }
            
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
            
            /* Table */
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dfe4ea;
                gridline-color: #ecf0f1;
                color: #2c3e50;
            }
            
            QTableWidget::item {
                padding: 8px;
                color: #2c3e50;
            }
            
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #f5f7fa;
                padding: 10px;
                border: none;
                font-weight: 600;
                color: #2c3e50;
            }
            
            /* Text Edit */
            QTextEdit {
                background-color: white;
                border: 1px solid #dfe4ea;
                border-radius: 8px;
                padding: 15px;
                font-size: 13px;
            }
            
            /* CheckBox and RadioButton - Light Mode */
            QCheckBox, QRadioButton {
                color: #2c3e50;
                spacing: 8px;
                padding: 5px;
                font-size: 14px;
            }
            
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #dfe4ea;
                background-color: white;
            }
            
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
            
            QCheckBox::indicator:hover, QRadioButton::indicator:hover {
                border-color: #3498db;
            }
            
            QRadioButton::indicator {
                border-radius: 9px;
            }
        """)


# =========================
# Entry Point
# =========================

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Secure Wipe")
    app.setOrganizationName("SecureWipe Inc.")
    app.setApplicationVersion("2.0")
    
    # Create and show window
    window = SecureWipeApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()