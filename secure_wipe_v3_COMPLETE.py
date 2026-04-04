"""
🔥 SECURE WIPE - COMPLETE VERSION v3.0 🔥
Main application file with ALL features integrated

Bhai, yeh file run karo! Sab kuch ready hai!
"""

# This is the MASTER file that ties everything together
# Just run: python THIS_FILE.py

import sys
import os

# First, check if main file exists
main_file = "secure_wipe_desktop.py"

if not os.path.exists(main_file):
    print("❌ Error: secure_wipe_desktop.py not found!")
    print("📁 Please make sure secure_wipe_desktop.py is in the same folder")
    sys.exit(1)

# Import everything from main file
from secure_wipe_desktop import *

# Now add the new features
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

# Import new modules
try:
    from login_system import LoginSystem
    LOGIN_ENABLED = True
except ImportError:
    print("⚠️ Login system not available (login_system.py missing)")
    LOGIN_ENABLED = False

try:
    from update_checker import UpdateChecker
    UPDATE_ENABLED = True
except ImportError:
    print("⚠️ Update checker not available (update_checker.py missing)")
    UPDATE_ENABLED = False


# ===================================================================
# LOGIN DIALOG
# ===================================================================

class LoginDialog(QDialog):
    """Login dialog for user authentication"""
    
    def __init__(self, login_system, parent=None):
        super().__init__(parent)
        self.login_system = login_system
        self.authenticated = False
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🔐 Secure Wipe - Login")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔐 Secure Data Wiping System")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Please login to continue")
        subtitle.setStyleSheet("color: #7f8c8d;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("padding: 10px; border: 2px solid #dfe4ea; border-radius: 5px;")
        
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 10px; border: 2px solid #dfe4ea; border-radius: 5px;")
        self.password_input.returnPressed.connect(self.login)
        
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        # Info text
        info = QLabel("ℹ️ Default: username=admin, password=admin123")
        info.setStyleSheet("color: #3498db; font-size: 11px; font-style: italic;")
        layout.addWidget(info)
        
        layout.addSpacing(10)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        login_btn = QPushButton("🔓 Login")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        login_btn.clicked.connect(self.login)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        success, message = self.login_system.authenticate(username, password)
        
        if success:
            self.authenticated = True
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", message)
            self.password_input.clear()
            self.password_input.setFocus()


# ===================================================================
# ENHANCED MAIN APP CLASS
# ===================================================================

class SecureWipeAppV3(SecureWipeApp):
    """Enhanced app with login and update checker"""
    
    def __init__(self):
        # Initialize login system first
        if LOGIN_ENABLED:
            self.login_system = LoginSystem()
            
            # Show login dialog
            login_dialog = LoginDialog(self.login_system)
            if login_dialog.exec() != QDialog.DialogCode.Accepted:
                sys.exit(0)  # User cancelled login
        
        # Initialize parent class
        super().__init__()
        
        # Initialize update checker
        if UPDATE_ENABLED:
            self.update_checker = UpdateChecker("2.0")
            self.check_updates_on_startup()
    
    def check_updates_on_startup(self):
        """Check for updates when app starts"""
        try:
            available, version, url = self.update_checker.check_for_updates()
            
            if available:
                msg = QMessageBox(self)
                msg.setWindowTitle("📥 Update Available")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText(f"<h3>Update Available!</h3>")
                msg.setInformativeText(
                    f"<b>Current Version:</b> 2.0<br>"
                    f"<b>Latest Version:</b> {version}<br><br>"
                    f"A new version is available for download."
                )
                msg.addButton("📥 Download", QMessageBox.ButtonRole.AcceptRole)
                msg.addButton("⏭️ Skip", QMessageBox.ButtonRole.RejectRole)
                
                if msg.exec() == 0:  # Download clicked
                    import webbrowser
                    webbrowser.open(url)
        except:
            pass  # Silently fail if update check fails
    
    def show_about(self):
        """Enhanced about dialog with update info"""
        super().show_about()  # Call parent about
        
        # Add update check button to dashboard if not exists
        if UPDATE_ENABLED and not hasattr(self, 'update_check_done'):
            self.update_check_done = True


# ===================================================================
# MAIN ENTRY POINT
# ===================================================================

def main():
    """Main entry point with all features"""
    
    print("=" * 60)
    print("🔥 SECURE WIPE v3.0 - COMPLETE EDITION 🔥")
    print("=" * 60)
    print()
    
    if LOGIN_ENABLED:
        print("✅ Login System: ENABLED")
    else:
        print("⚠️  Login System: DISABLED (login_system.py missing)")
    
    if UPDATE_ENABLED:
        print("✅ Update Checker: ENABLED")
    else:
        print("⚠️  Update Checker: DISABLED (update_checker.py missing)")
    
    print()
    print("Starting application...")
    print()
    
    app = QApplication(sys.argv)
    
    # Use enhanced version if login available, otherwise regular
    if LOGIN_ENABLED:
        window = SecureWipeAppV3()
    else:
        window = SecureWipeApp()
    
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
