"""
Certificate UI Handler Module for Secure Wipe
Handles certificate download, viewing, and management UI
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt


class CertificateDialog(QDialog):
    """Custom dialog for wipe success with certificate actions"""
    
    def __init__(self, parent=None, message="", certificate_path=None):
        super().__init__(parent)
        
        self.certificate_path = certificate_path
        self.setWindowTitle("Wipe Successful")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self.init_ui(message)
        self.apply_styles()
    
    def init_ui(self, message):
        """Initialize the dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Success icon and message
        success_label = QLabel("✅ Wipe Completed Successfully!")
        success_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2ecc71;
            margin-bottom: 10px;
        """)
        layout.addWidget(success_label)
        
        # Detailed message
        detail_label = QLabel(message)
        detail_label.setWordWrap(True)
        detail_label.setStyleSheet("font-size: 14px; color: #2c3e50;")
        layout.addWidget(detail_label)
        
        # Certificate info section
        if self.certificate_path:
            cert_frame = self._create_certificate_section()
            layout.addWidget(cert_frame)
        
        # Buttons
        button_layout = self._create_button_layout()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_certificate_section(self):
        """Create certificate information section"""
        from PyQt6.QtWidgets import QFrame
        
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #2ecc71;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Certificate header
        cert_header = QLabel("📜 Certificate Generated")
        cert_header.setStyleSheet("font-size: 16px; font-weight: 600; color: #2c3e50;")
        layout.addWidget(cert_header)
        
        # Certificate filename
        cert_name = Path(self.certificate_path).name
        cert_label = QLabel(f"<b>File:</b> {cert_name}")
        cert_label.setStyleSheet("font-size: 13px; color: #555; margin-top: 5px;")
        layout.addWidget(cert_label)
        
        # Certificate path
        cert_path = QLabel(f"<b>Location:</b> {self.certificate_path}")
        cert_path.setStyleSheet("font-size: 11px; color: #777; margin-top: 5px;")
        cert_path.setWordWrap(True)
        layout.addWidget(cert_path)
        
        frame.setLayout(layout)
        return frame
    
    def _create_button_layout(self):
        """Create button layout"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        if self.certificate_path:
            # Download/Save Certificate button
            download_btn = QPushButton("📥 Download Certificate")
            download_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            download_btn.clicked.connect(self.download_certificate)
            button_layout.addWidget(download_btn)
            
            # Open Folder button
            folder_btn = QPushButton("📂 Open Folder")
            folder_btn.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)
            folder_btn.clicked.connect(self.open_certificate_folder)
            button_layout.addWidget(folder_btn)
            
            # View Certificate button (opens PDF)
            view_btn = QPushButton("👁️ View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9b59b6;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #8e44ad;
                }
            """)
            view_btn.clicked.connect(self.view_certificate)
            button_layout.addWidget(view_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #bdc3c7;
            }
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        return button_layout
    
    def download_certificate(self):
        """Download/Save certificate to user-selected location"""
        if not self.certificate_path or not os.path.exists(self.certificate_path):
            QMessageBox.warning(
                self,
                "Certificate Not Found",
                "Certificate file does not exist."
            )
            return
        
        # Get save location from user
        default_name = Path(self.certificate_path).name
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Certificate",
            default_name,
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if save_path:
            try:
                # Copy certificate to selected location
                shutil.copy2(self.certificate_path, save_path)
                
                QMessageBox.information(
                    self,
                    "Certificate Saved",
                    f"✅ Certificate successfully saved to:\n\n{save_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Save Failed",
                    f"❌ Error saving certificate:\n\n{str(e)}"
                )
    
    def open_certificate_folder(self):
        """Open folder containing the certificate"""
        if not self.certificate_path:
            return
        
        folder_path = str(Path(self.certificate_path).parent.absolute())
        
        try:
            if sys.platform == 'win32':
                # Windows - open Explorer and select file
                subprocess.run(['explorer', '/select,', self.certificate_path])
            elif sys.platform == 'darwin':
                # macOS - open Finder
                subprocess.run(['open', '-R', self.certificate_path])
            else:
                # Linux - open file manager
                subprocess.run(['xdg-open', folder_path])
                
        except Exception as e:
            QMessageBox.warning(
                self,
                "Cannot Open Folder",
                f"Could not open folder:\n\n{str(e)}\n\nFolder: {folder_path}"
            )
    
    def view_certificate(self):
        """Open certificate in default PDF viewer"""
        if not self.certificate_path or not os.path.exists(self.certificate_path):
            QMessageBox.warning(
                self,
                "Certificate Not Found",
                "Certificate file does not exist."
            )
            return
        
        try:
            if sys.platform == 'win32':
                # Windows - open with default application
                os.startfile(self.certificate_path)
            elif sys.platform == 'darwin':
                # macOS - open with default application
                subprocess.run(['open', self.certificate_path])
            else:
                # Linux - open with default application
                subprocess.run(['xdg-open', self.certificate_path])
                
        except Exception as e:
            QMessageBox.warning(
                self,
                "Cannot Open Certificate",
                f"Could not open certificate:\n\n{str(e)}"
            )
    
    def apply_styles(self):
        """Apply dialog styles"""
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)


class CertificateManager:
    """Manage certificate operations"""
    
    @staticmethod
    def show_success_dialog(parent, message, certificate_path=None):
        """
        Show success dialog with certificate actions
        
        Args:
            parent: Parent widget
            message: Success message
            certificate_path: Path to certificate PDF
            
        Returns:
            QDialog.DialogCode: Dialog result
        """
        dialog = CertificateDialog(parent, message, certificate_path)
        return dialog.exec()
    
    @staticmethod
    def quick_save_certificate(parent, certificate_path):
        """
        Quick save certificate to Downloads folder
        
        Args:
            parent: Parent widget
            certificate_path: Path to certificate
            
        Returns:
            bool: True if saved successfully
        """
        if not certificate_path or not os.path.exists(certificate_path):
            return False
        
        try:
            # Get Downloads folder
            downloads = Path.home() / "Downloads"
            downloads.mkdir(exist_ok=True)
            
            # Copy certificate
            dest = downloads / Path(certificate_path).name
            shutil.copy2(certificate_path, dest)
            
            QMessageBox.information(
                parent,
                "Certificate Saved",
                f"✅ Certificate saved to Downloads:\n\n{dest.name}"
            )
            return True
            
        except Exception as e:
            QMessageBox.critical(
                parent,
                "Save Failed",
                f"❌ Error saving certificate:\n\n{str(e)}"
            )
            return False
    
    @staticmethod
    def email_certificate(parent, certificate_path, email_system=None):
        """
        Email certificate (requires email_system module)
        
        Args:
            parent: Parent widget
            certificate_path: Path to certificate
            email_system: EmailReportSystem instance
            
        Returns:
            bool: True if sent successfully
        """
        if not email_system:
            QMessageBox.warning(
                parent,
                "Email Not Configured",
                "Email system is not configured.\n\nPlease configure email settings first."
            )
            return False
        
        try:
            file_name = Path(certificate_path).name
            success, message = email_system.send_instant_certificate(
                certificate_path,
                file_name
            )
            
            if success:
                QMessageBox.information(
                    parent,
                    "Certificate Emailed",
                    f"✅ Certificate emailed successfully!\n\n{message}"
                )
            else:
                QMessageBox.warning(
                    parent,
                    "Email Failed",
                    f"❌ Failed to email certificate:\n\n{message}"
                )
            
            return success
            
        except Exception as e:
            QMessageBox.critical(
                parent,
                "Email Error",
                f"❌ Error emailing certificate:\n\n{str(e)}"
            )
            return False


# Convenience functions
def show_certificate_dialog(parent, message, cert_path=None):
    """Show certificate success dialog"""
    return CertificateManager.show_success_dialog(parent, message, cert_path)


def save_certificate_quick(parent, cert_path):
    """Quick save to Downloads"""
    return CertificateManager.quick_save_certificate(parent, cert_path)


# Example usage
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Test dialog
    test_cert = "certificates/wipe_cert_TEST123.pdf"
    dialog = CertificateDialog(
        None,
        "File has been securely wiped and deleted.",
        test_cert
    )
    dialog.exec()
