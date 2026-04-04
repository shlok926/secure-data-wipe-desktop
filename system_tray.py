"""
System Tray and Notifications Module for Secure Wipe
Desktop notifications and system tray integration
"""

import sys
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class SystemTrayManager:
    """Manage system tray icon and notifications"""
    
    def __init__(self, parent):
        self.parent = parent
        self.tray_icon = None
        self.setup_tray()
    
    def setup_tray(self):
        """Setup system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self.parent)
        # Set icon (provide a fallback if icon.png is missing)
        import os
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Use a standard Qt icon as fallback
            from PyQt6.QtGui import QPixmap
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.blue)
            self.tray_icon.setIcon(QIcon(pixmap))
        
        # Create context menu
        menu = QMenu()
        
        show_action = QAction("Show Window", self.parent)
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)
        
        menu.addSeparator()
        
        quit_action = QAction("Quit", self.parent)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.tray_activated)
        
        # Show tray icon
        self.tray_icon.show()
    
    def show_notification(self, title, message, icon_type="info"):
        """
        Show desktop notification
        
        Args:
            title: Notification title
            message: Notification message
            icon_type: "info", "warning", or "critical"
        """
        if not self.tray_icon:
            return
        
        icon_map = {
            "info": QSystemTrayIcon.MessageIcon.Information,
            "warning": QSystemTrayIcon.MessageIcon.Warning,
            "critical": QSystemTrayIcon.MessageIcon.Critical
        }
        
        icon = icon_map.get(icon_type, QSystemTrayIcon.MessageIcon.Information)
        
        self.tray_icon.showMessage(title, message, icon, 5000)
    
    def tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()
    
    def show_window(self):
        """Show main window"""
        self.parent.show()
        self.parent.activateWindow()
        self.parent.raise_()
    
    def quit_app(self):
        """Quit application"""
        QApplication.quit()
    
    def hide_to_tray(self):
        """Hide window to system tray"""
        self.parent.hide()
        self.show_notification(
            "Secure Wipe",
            "Application minimized to system tray",
            "info"
        )


# Notification helper functions
def notify_wipe_complete(tray_manager, file_name):
    """Notify when wipe completes"""
    if tray_manager:
        tray_manager.show_notification(
            "✅ Wipe Complete",
            f"Successfully wiped: {file_name}",
            "info"
        )


def notify_wipe_failed(tray_manager, file_name):
    """Notify when wipe fails"""
    if tray_manager:
        tray_manager.show_notification(
            "❌ Wipe Failed",
            f"Failed to wipe: {file_name}",
            "critical"
        )


def notify_folder_complete(tray_manager, successful, failed):
    """Notify when folder wipe completes"""
    if tray_manager:
        tray_manager.show_notification(
            "📁 Folder Wipe Complete",
            f"✅ {successful} successful, ❌ {failed} failed",
            "info"
        )
