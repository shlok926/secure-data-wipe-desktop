"""
Auth Manager - Handles App Lock, PIN Setup, and Verification
"""
import hashlib
import os
import time
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QWidget, QApplication, QFrame
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon, QFont

class AuthManager:
    """Manages authentication state and PIN validation"""
    def __init__(self):
        self.settings = QSettings("SecureWipeInc", "SecureWipeApp")
        
    def is_pin_set(self):
        # Tamper Resistance: Check both registry and local encrypted file
        reg_has = self.settings.contains("app_pin_hash")
        file_has = os.path.exists("config/.auth_state")
        
        if reg_has and not file_has:
            # Heal file
            self._save_to_file(self.settings.value("app_pin_hash", ""))
        elif file_has and not reg_has:
            # Heal registry (bypassed registry!)
            hash_val = self._read_from_file()
            if hash_val:
                self.settings.setValue("app_pin_hash", hash_val)
                reg_has = True
                print("🚨 Security Alert: Registry tamper detected and healed.")
                
        return reg_has or file_has
        
    def _save_to_file(self, pin_hash):
        try:
            os.makedirs("config", exist_ok=True)
            from crypto_utils import CryptoManager
            encrypted = CryptoManager().encrypt(pin_hash)
            with open("config/.auth_state", "w") as f:
                f.write(encrypted)
        except: pass
        
    def _read_from_file(self):
        try:
            if os.path.exists("config/.auth_state"):
                with open("config/.auth_state", "r") as f:
                    encrypted = f.read().strip()
                from crypto_utils import CryptoManager
                return CryptoManager().decrypt(encrypted)
        except: pass
        return None
        
    def verify_pin(self, pin):
        # Read from either source to ensure resilience
        stored_hash = self.settings.value("app_pin_hash", "")
        if not stored_hash:
            stored_hash = self._read_from_file() or ""
            
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        return stored_hash == pin_hash
        
    def set_pin(self, new_pin):
        pin_hash = hashlib.sha256(new_pin.encode()).hexdigest()
        self.settings.setValue("app_pin_hash", pin_hash)
        self._save_to_file(pin_hash)
        
    def remove_pin(self):
        self.settings.remove("app_pin_hash")
        if os.path.exists("config/.auth_state"):
            try: os.remove("config/.auth_state")
            except: pass
        self.reset_attempts()

    def get_lockout_status(self):
        """Returns (is_locked, seconds_remaining, attempts)"""
        attempts = int(self.settings.value("pin_attempts", 0) or 0)
        lockout_time = float(self.settings.value("pin_lockout_time", 0.0) or 0.0)
        
        current_time = time.time()
        if current_time < lockout_time:
            return True, int(lockout_time - current_time), attempts
        return False, 0, attempts
        
    def record_failed_attempt(self):
        """Record a failure and lock out if > 5 attempts."""
        attempts = int(self.settings.value("pin_attempts", 0) or 0) + 1
        self.settings.setValue("pin_attempts", attempts)
        if attempts >= 5:
            self.settings.setValue("pin_lockout_time", time.time() + 30)
        return attempts
        
    def reset_attempts(self):
        self.settings.remove("pin_attempts")
        self.settings.remove("pin_lockout_time")



class SetupPinDialog(QDialog):
    """Dialog shown on first launch to setup a PIN, or from Settings to change PIN"""
    def __init__(self, parent=None, is_change=False):
        super().__init__(parent)
        self.setWindowTitle("Set Master PIN" if not is_change else "Change Master PIN")
        self.setFixedSize(400, 300)
        self.setModal(True)
        self.is_change = is_change
        self.auth_manager = AuthManager()
        
        # Styles
        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; color: #c9d1d9; }
            QLabel { color: #c9d1d9; font-size: 14px; }
            QLineEdit { 
                padding: 10px; font-size: 24px; border: 1px solid #3e3e42; 
                border-radius: 6px; background-color: #0a1520; color: #00e676; 
                letter-spacing: 5px; text-align: center;
            }
            QPushButton { 
                padding: 10px; font-size: 14px; font-weight: bold;
                border-radius: 6px; border: none; 
            }
            QPushButton#primary-btn { background-color: #007acc; color: white; }
            QPushButton#primary-btn:hover { background-color: #005a9e; }
            QPushButton#secondary-btn { background-color: #3e3e42; color: #cccccc; }
            QPushButton#secondary-btn:hover { background-color: #505053; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("🔐 Secure Your App")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #00e676;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        desc = QLabel("Set a 4 to 8 digit PIN to restrict access to the application." if not is_change else "Enter a new PIN to update your security settings.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # PIN Input
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(8)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setPlaceholderText("••••")
        layout.addWidget(self.pin_input)
        
        # Confirm Input
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setMaxLength(8)
        self.confirm_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.confirm_input.setPlaceholderText("Confirm ••••")
        layout.addWidget(self.confirm_input)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        # Only allow skipping if we are setting it up for the first time
        if not is_change:
            skip_btn = QPushButton("Skip For Now")
            skip_btn.setObjectName("secondary-btn")
            skip_btn.clicked.connect(self.reject)
            btn_layout.addWidget(skip_btn)
            
        save_btn = QPushButton("Save PIN")
        save_btn.setObjectName("primary-btn")
        save_btn.clicked.connect(self.save_pin)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
    def save_pin(self):
        pin = self.pin_input.text()
        confirm = self.confirm_input.text()
        
        if not pin.isdigit() or len(pin) < 4:
            QMessageBox.warning(self, "Invalid PIN", "PIN must be between 4 and 8 digits.")
            return
            
        if pin != confirm:
            QMessageBox.warning(self, "Mismatch", "PINs do not match. Please try again.")
            return
            
        self.auth_manager.set_pin(pin)
        QMessageBox.information(self, "Success", "Master PIN has been set successfully!")
        self.accept()


class LoginDialog(QDialog):
    """Professional lock screen dialog shown on app launch if PIN is enabled"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Secure Wipe - Authentication")
        self.setFixedSize(500, 650)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        self.auth_manager = AuthManager()
        
        # Professional styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #0a0e14, stop:1 #0f1620);
                color: #cdd6e0;
            }
            QLabel {
                color: #cdd6e0;
                background: transparent;
            }
            QLineEdit {
                padding: 16px;
                font-size: 24px;
                border: 2px solid #1e2d3d;
                border-radius: 10px;
                background-color: #111820;
                color: #00e676;
                letter-spacing: 6px;
                text-align: center;
                font-weight: bold;
                font-family: 'Segoe UI', 'Courier New', monospace;
            }
            QLineEdit:focus {
                border: 2px solid #00e676;
                background-color: #0f1620;
            }
            QPushButton {
                padding: 14px;
                font-size: 15px;
                font-weight: 600;
                border-radius: 8px;
                border: none;
            }
            QPushButton#unlock-btn {
                background-color: #00e676;
                color: #0a0e14;
                min-height: 45px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#unlock-btn:hover {
                background-color: #00c853;
            }
            QPushButton#unlock-btn:pressed {
                background-color: #00b84d;
            }
            QPushButton#exit-btn {
                background-color: transparent;
                color: #ff6b6b;
                text-decoration: underline;
                font-size: 13px;
                padding: 8px;
            }
            QPushButton#exit-btn:hover {
                color: #ff5252;
            }
            QFrame {
                background-color: #111820;
                border: 1px solid #1e2d3d;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Top section with padding
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(25)
        top_layout.setContentsMargins(50, 60, 50, 40)
        
        # Lock icon - Large and centered
        icon_container = QWidget()
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_lbl = QLabel("🔒")
        icon_lbl.setStyleSheet("font-size: 80px; background: transparent;")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_lbl)
        icon_container.setLayout(icon_layout)
        top_layout.addWidget(icon_container)
        
        # Title - Professional heading
        title = QLabel("Authentication Required")
        title_font = QFont("Segoe UI")
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff; background: transparent; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(title)
        
        # Subtitle with description
        subtitle = QLabel("Enter your Master PIN to continue")
        subtitle_font = QFont("Segoe UI")
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #7f8c8d; background: transparent; margin-bottom: 10px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        top_layout.addWidget(subtitle)
        
        # Info box - Professional styling
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setStyleSheet("""
            QFrame#infoFrame {
                background-color: #111820;
                border: 1px solid #1e2d3d;
                border-radius: 8px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(12, 8, 12, 8)
        
        info_text = QLabel("ℹ️ This application is protected by PIN authentication")
        info_text.setStyleSheet("color: #90a4ae; font-size: 12px; background: transparent;")
        info_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(info_text)
        info_frame.setLayout(info_layout)
        top_layout.addWidget(info_frame)
        
        # Spacer
        top_layout.addSpacing(10)
        
        # PIN Input section with label
        pin_label = QLabel("Master PIN")
        pin_label.setStyleSheet("color: #90a4ae; font-size: 12px; font-weight: 600; background: transparent;")
        top_layout.addWidget(pin_label)
        
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(8)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.returnPressed.connect(self.verify)
        self.pin_input.setPlaceholderText("●●●●")
        top_layout.addWidget(self.pin_input)
        
        # Error message - Professional styling
        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet("""
            color: #ff6b6b;
            font-size: 13px;
            font-weight: 600;
            background: transparent;
            padding: 8px;
            border-radius: 5px;
        """)
        self.error_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_lbl.setWordWrap(True)
        self.error_lbl.setVisible(False)  # Hide initially
        top_layout.addWidget(self.error_lbl)
        
        # Attempt counter
        self.attempt_lbl = QLabel("")
        self.attempt_lbl.setStyleSheet("color: #ff9100; font-size: 11px; background: transparent;")
        self.attempt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.attempt_lbl.setVisible(False)  # Hide initially
        top_layout.addWidget(self.attempt_lbl)
        
        top_layout.addStretch()
        top_widget.setLayout(top_layout)
        layout.addWidget(top_widget)
        
        # Bottom section - Action buttons
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setSpacing(12)
        bottom_layout.setContentsMargins(50, 20, 50, 40)
        
        # Unlock Button
        unlock_btn = QPushButton("🔓 Unlock")
        unlock_btn.setObjectName("unlock-btn")
        unlock_btn.clicked.connect(self.verify)
        bottom_layout.addWidget(unlock_btn)
        
        # Exit Button
        exit_btn = QPushButton("✕ Exit Application")
        exit_btn.setObjectName("exit-btn")
        exit_btn.clicked.connect(self.reject)
        bottom_layout.addWidget(exit_btn)
        
        bottom_widget.setLayout(bottom_layout)
        layout.addWidget(bottom_widget)
        
        self.setLayout(layout)
        
        # Focus on PIN input
        self.pin_input.setFocus()
        
        # Attempt tracking
        self.attempt_count = 0
        self.max_attempts = 5
        
    def verify(self):
        pin = self.pin_input.text()
        if not pin:
            self.show_error("Please enter PIN")
            return
        
        # Attempt tracking
        self.attempt_count += 1
        
        if self.auth_manager.verify_pin(pin):
            self.accept()
        else:
            remaining = self.max_attempts - self.attempt_count
            if remaining > 0:
                self.show_error("❌ Incorrect PIN")
                self.attempt_lbl.setText(f"Attempts remaining: {remaining}")
                self.attempt_lbl.setVisible(True)
                self.pin_input.clear()
                self.pin_input.setFocus()
                
                # Shake animation
                self.shake_animation()
            else:
                self.show_error("❌ Too many failed attempts. Exiting...")
                self.attempt_lbl.setText("Application will close...")
                self.attempt_lbl.setVisible(True)
                import time
                QApplication.instance().processEvents()
                time.sleep(2)
                self.reject()
    
    def show_error(self, message):
        self.error_lbl.setText(message)
        self.error_lbl.setVisible(True)
    
    def shake_animation(self):
        """Subtle shake animation for wrong PIN"""
        for _ in range(3):
            self.move(self.x() + 5, self.y())
            QApplication.instance().processEvents()
            import time
            time.sleep(0.05)
            self.move(self.x() - 10, self.y())
            QApplication.instance().processEvents()
            time.sleep(0.05)
        self.move(self.x() + 5, self.y())
        QApplication.instance().processEvents()
            
        # Check lockout
        is_locked, remaining, attempts = self.auth_manager.get_lockout_status()
        if is_locked:
            self.error_lbl.setText(f"Locked out. Try again in {remaining}s.")
            self.pin_input.clear()
            return
            
        if self.auth_manager.verify_pin(pin):
            self.auth_manager.reset_attempts()
            self.accept()
        else:
            attempts = self.auth_manager.record_failed_attempt()
            if attempts >= 5:
                self.error_lbl.setText("Too many attempts. Locked out for 30s.")
            else:
                self.error_lbl.setText(f"Incorrect PIN. {5 - attempts} attempts left.")
            self.pin_input.clear()
            self.pin_input.setFocus()
            
            # Add a slight delay/shake effect in a real app, keeping it simple here
