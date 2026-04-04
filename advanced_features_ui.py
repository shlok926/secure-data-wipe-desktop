"""
Advanced Features UI Integration
Add these pages/dialogs to your secure_wipe_desktop.py
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QComboBox, QDateTimeEdit, QCheckBox, QProgressBar,
    QTableWidget, QTableWidgetItem, QFrame, QTextEdit, QLineEdit,
    QFileDialog, QMessageBox, QTabWidget, QGroupBox
)
from PyQt6.QtCore import Qt, QDateTime
from pathlib import Path
from datetime import datetime


# ====================================================================
# DIALOG 1: BATCH WIPE DIALOG
# ====================================================================

class BatchWipeDialog(QDialog):
    """Dialog for batch file wiping"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🗂️ Batch Wipe")
        self.setMinimumSize(700, 500)
        self.files = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Batch File Wipe")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # File list
        list_label = QLabel("Selected Files:")
        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(200)
        
        layout.addWidget(list_label)
        layout.addWidget(self.file_list)
        
        # Buttons to add/remove files
        btn_layout = QHBoxLayout()
        
        add_files_btn = QPushButton("➕ Add Files")
        add_files_btn.clicked.connect(self.add_files)
        
        add_folder_btn = QPushButton("📁 Add Folder")
        add_folder_btn.clicked.connect(self.add_folder)
        
        remove_btn = QPushButton("➖ Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.clicked.connect(self.clear_all)
        
        btn_layout.addWidget(add_files_btn)
        btn_layout.addWidget(add_folder_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)
        
        # Algorithm selection
        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        self.algo_combo = QComboBox()
        self.algo_combo.addItem("🛡️ DoD 5220.22-M", "dod")
        self.algo_combo.addItem("⚡ Single Pass", "simple")
        self.algo_combo.addItem("🔒 NIST SP 800-88", "nist")
        self.algo_combo.addItem("🔐 Gutmann", "gutmann")
        
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)
        algo_layout.addStretch()
        layout.addLayout(algo_layout)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Ready to start batch wipe")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Start Batch Wipe")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover { background: #c0392b; }
        """)
        self.start_btn.clicked.connect(self.start_batch_wipe)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        action_layout.addWidget(self.start_btn)
        action_layout.addWidget(cancel_btn)
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
    
    def add_files(self):
        """Add files to batch"""
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "")
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
                self.file_list.addItem(f"📄 {Path(file_path).name}")
        
        self.update_status()
    
    def add_folder(self):
        """Add all files from folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            for file_path in Path(folder).rglob('*'):
                if file_path.is_file():
                    file_str = str(file_path)
                    if file_str not in self.files:
                        self.files.append(file_str)
                        self.file_list.addItem(f"📄 {file_path.name}")
            
            self.update_status()
    
    def remove_selected(self):
        """Remove selected files"""
        for item in self.file_list.selectedItems():
            row = self.file_list.row(item)
            self.file_list.takeItem(row)
            self.files.pop(row)
        
        self.update_status()
    
    def clear_all(self):
        """Clear all files"""
        self.file_list.clear()
        self.files = []
        self.update_status()
    
    def update_status(self):
        """Update status label"""
        count = len(self.files)
        self.status_label.setText(f"Ready to wipe {count} file{'s' if count != 1 else ''}")
    
    def start_batch_wipe(self):
        """Start the batch wipe"""
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add files to wipe")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Batch Wipe",
            f"Wipe {len(self.files)} files?\n\n⚠️ THIS CANNOT BE UNDONE!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.accept()


# ====================================================================
# DIALOG 2: SCHEDULE WIPE DIALOG
# ====================================================================

class ScheduleWipeDialog(QDialog):
    """Dialog for scheduling wipes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⏰ Schedule Wipe")
        self.setMinimumSize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Schedule Secure Wipe")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # File selection
        file_layout = QHBoxLayout()
        file_label = QLabel("File to Wipe:")
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select file...")
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.select_file)
        
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input, 1)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Schedule time
        time_layout = QVBoxLayout()
        time_label = QLabel("Schedule Time:")
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.datetime_edit.setMinimumDateTime(QDateTime.currentDateTime())
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.datetime_edit)
        layout.addLayout(time_layout)
        
        # Recurring option
        self.recurring_checkbox = QCheckBox("Recurring (daily)")
        layout.addWidget(self.recurring_checkbox)
        
        # Algorithm - All available algorithms
        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        self.algo_combo = QComboBox()
        # Add all available wiping algorithms
        self.algo_combo.addItem("⚡ Single Pass (Fastest)", "simple")
        self.algo_combo.addItem("🛡️ DoD 5220.22-M (Recommended)", "dod")
        self.algo_combo.addItem("📋 NIST 800-88", "nist")
        self.algo_combo.addItem("🔄 Gutmann (35-pass)", "gutmann")
        self.algo_combo.addItem("🔐 AES Crypto Erase", "crypto")
        
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo)
        algo_layout.addStretch()
        layout.addLayout(algo_layout)
        
        # Info
        info = QLabel(
            "ℹ️ The file will be securely wiped at the scheduled time.\n"
            "The application must be running for the schedule to execute."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #7f8c8d; font-size: 12px; margin: 10px;")
        layout.addWidget(info)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        schedule_btn = QPushButton("⏰ Schedule Wipe")
        schedule_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background: #2980b9; }
        """)
        schedule_btn.clicked.connect(self.schedule_wipe)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(schedule_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def select_file(self):
        """Select file to schedule"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_input.setText(file_path)
    
    def schedule_wipe(self):
        """Schedule the wipe"""
        if not self.file_input.text():
            QMessageBox.warning(self, "No File", "Please select a file")
            return
        
        try:
            # Import scheduled_wipe module
            from scheduled_wipe import ScheduledTask, ScheduleType
            import uuid
            
            # Get form data
            file_path = self.file_input.text()
            schedule_time = self.datetime_edit.dateTime().toPyDateTime()
            algorithm = self.algo_combo.currentData()
            is_recurring = self.recurring_checkbox.isChecked()
            
            # Determine schedule type
            schedule_type = ScheduleType.DAILY if is_recurring else ScheduleType.ONCE
            
            # Create scheduled task
            task = ScheduledTask(
                task_id=str(uuid.uuid4()),
                file_paths=[file_path],
                algorithm=algorithm,
                schedule_type=schedule_type,
                schedule_time=schedule_time
            )
            
            # Save to scheduler
            if hasattr(self.parent(), 'scheduler'):
                self.parent().scheduler.add_task(task)
                self.parent().scheduler.save_tasks()
            
            # Show success message
            task_type = "recurring daily" if is_recurring else "one-time"
            QMessageBox.information(
                self,
                "✅ Wipe Scheduled Successfully!",
                f"File: {Path(file_path).name}\n"
                f"Algorithm: {self.algo_combo.currentText()}\n"
                f"Type: {task_type}\n"
                f"Scheduled for: {schedule_time.strftime('%Y-%m-%d %H:%M')}\n\n"
                f"⚠️ Note: Keep the application running for schedule to execute."
            )
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Scheduling Failed",
                f"Error scheduling wipe:\n{str(e)}"
            )
            print(f"Schedule error: {e}")


# ====================================================================
# DIALOG 3: ANALYTICS DASHBOARD
# ====================================================================

class AnalyticsDashboard(QDialog):
    """Advanced analytics dashboard"""
    
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 Wipe Analytics")
        self.setMinimumSize(800, 600)
        self.history = history
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Wipe Analytics Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total wipes
        total_card = self.create_stat_card(
            "Total Wipes",
            str(len(self.history)),
            "#3498db"
        )
        
        # Success rate
        successful = sum(1 for h in self.history if h.get('success', False))
        rate = (successful / len(self.history) * 100) if self.history else 0
        rate_card = self.create_stat_card(
            "Success Rate",
            f"{rate:.1f}%",
            "#2ecc71"
        )
        
        # Total data
        total_bytes = sum(h.get('file_size', 0) for h in self.history)
        
        # Format bytes to human-readable format (matching dashboard style)
        if total_bytes < 1024:
            data_str = f"{total_bytes} B"
        elif total_bytes < 1024 * 1024:
            data_str = f"{total_bytes / 1024:.1f} KB"
        elif total_bytes < 1024 * 1024 * 1024:
            data_str = f"{total_bytes / (1024 * 1024):.1f} MB"
        else:
            data_str = f"{total_bytes / (1024 * 1024 * 1024):.2f} GB"
        
        data_card = self.create_stat_card(
            "Data Destroyed",
            data_str,
            "#9b59b6"
        )
        
        stats_layout.addWidget(total_card)
        stats_layout.addWidget(rate_card)
        stats_layout.addWidget(data_card)
        layout.addLayout(stats_layout)
        
        # Algorithm breakdown
        algo_group = QGroupBox("Algorithm Usage")
        algo_layout = QVBoxLayout()
        
        algo_counts = {}
        for entry in self.history:
            algo = entry.get('algorithm', 'Unknown')
            algo_counts[algo] = algo_counts.get(algo, 0) + 1
        
        for algo, count in sorted(algo_counts.items(), key=lambda x: x[1], reverse=True):
            percent = (count / len(self.history) * 100) if self.history else 0
            label = QLabel(f"{algo}: {count} ({percent:.1f}%)")
            algo_layout.addWidget(label)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def create_stat_card(self, title, value, color):
        """Create a stat card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card.setLayout(card_layout)
        
        return card


# ====================================================================
# HOW TO INTEGRATE INTO MAIN APP
# ====================================================================

"""
Add these methods to your SecureWipeApp class:

def show_batch_wipe_dialog(self):
    '''Show batch wipe dialog'''
    dialog = BatchWipeDialog(self)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        # Process batch wipe
        files = dialog.files
        algorithm = dialog.algo_combo.currentData()
        # Start batch processing...

def show_schedule_dialog(self):
    '''Show schedule wipe dialog'''
    dialog = ScheduleWipeDialog(self)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        # Save schedule
        pass

def show_analytics(self):
    '''Show analytics dashboard'''
    if self.history_manager:
        history = self.history_manager.get_all_history()
        dialog = AnalyticsDashboard(history, self)
        dialog.exec()

# Add buttons to dashboard:
batch_btn = QPushButton("🗂️ Batch Wipe")
batch_btn.clicked.connect(self.show_batch_wipe_dialog)

schedule_btn = QPushButton("⏰ Schedule Wipe")
schedule_btn.clicked.connect(self.show_schedule_dialog)

analytics_btn = QPushButton("📊 Analytics")
analytics_btn.clicked.connect(self.show_analytics)
"""
