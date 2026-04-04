"""
Security Features Implementation
Add to secure_wipe_desktop.py
"""

# ====================================================================
# SECURITY FEATURES - COMPLETE IMPLEMENTATION
# Add these functions to your SecureWipeApp class
# ====================================================================

def start_wipe(self):
    """Start wipe operation with complete security checks"""
    
    file_path = self.file_input.text().strip()
    
    # Basic validation
    if not file_path:
        QMessageBox.warning(
            self,
            "No File Selected",
            "⚠️ Please select a file to wipe."
        )
        return
    
    if not os.path.exists(file_path):
        QMessageBox.warning(
            self,
            "File Not Found",
            f"❌ The selected file does not exist:\n\n{file_path}"
        )
        return
    
    # ===== SECURITY CHECK 1: CONFIRM BEFORE WIPE =====
    if hasattr(self, 'app_settings'):
        confirm_before = self.app_settings.get('security', {}).get('confirm_before_wipe', True)
        
        if confirm_before:
            file_name = Path(file_path).name
            file_size = os.path.getsize(file_path)
            file_size_str = self.format_size(file_size)
            algorithm = self.algo_combo.currentText().split(' - ')[0]
            
            msg = QMessageBox(self)
            msg.setWindowTitle("⚠️ Confirm Secure Wipe")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(
                f"<h3>Are you sure you want to securely wipe this file?</h3>"
            )
            msg.setInformativeText(
                f"<b>File:</b> {file_name}<br>"
                f"<b>Size:</b> {file_size_str}<br>"
                f"<b>Algorithm:</b> {algorithm}<br><br>"
                f"<font color='#e74c3c'><b>⚠️ THIS ACTION CANNOT BE UNDONE!</b></font><br>"
                f"The file will be permanently destroyed."
            )
            msg.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            
            yes_btn = msg.button(QMessageBox.StandardButton.Yes)
            yes_btn.setText("🗑️ Yes, Wipe It")
            no_btn = msg.button(QMessageBox.StandardButton.No)
            no_btn.setText("❌ Cancel")
            
            reply = msg.exec()
            
            if reply == QMessageBox.StandardButton.No:
                self.status_label.setText("Wipe cancelled by user")
                return
    
    # ===== SECURITY CHECK 2: DOUBLE CONFIRM FOR LARGE FILES =====
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_gb = file_size_bytes / (1024**3)
        
        # Get threshold from settings
        threshold_gb = 5.0  # Default
        if hasattr(self, 'app_settings'):
            threshold_str = self.app_settings.get('general', {}).get('large_file_threshold', '5 GB')
            try:
                threshold_gb = float(threshold_str.split()[0])
            except:
                threshold_gb = 5.0
        
        if file_size_gb > threshold_gb:
            if hasattr(self, 'app_settings'):
                double_confirm = self.app_settings.get('security', {}).get('double_confirm_large', True)
                
                if double_confirm:
                    # First confirmation
                    msg1 = QMessageBox(self)
                    msg1.setWindowTitle("🔶 Large File Warning")
                    msg1.setIcon(QMessageBox.Icon.Warning)
                    msg1.setText(
                        f"<h3>This is a LARGE file ({file_size_gb:.1f} GB)!</h3>"
                    )
                    msg1.setInformativeText(
                        f"<b>File:</b> {Path(file_path).name}<br>"
                        f"<b>Size:</b> {file_size_gb:.1f} GB<br><br>"
                        f"⏱️ <b>Estimated time:</b> {self.estimate_wipe_time(file_size_bytes)}<br><br>"
                        f"⚠️ Wiping large files takes significant time.<br>"
                        f"⚠️ The application will be busy during this operation.<br><br>"
                        f"Do you want to continue?"
                    )
                    msg1.setStandardButtons(
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    msg1.setDefaultButton(QMessageBox.StandardButton.No)
                    
                    if msg1.exec() == QMessageBox.StandardButton.No:
                        self.status_label.setText("Large file wipe cancelled")
                        return
                    
                    # Second confirmation (FINAL)
                    msg2 = QMessageBox(self)
                    msg2.setWindowTitle("🔴 FINAL CONFIRMATION")
                    msg2.setIcon(QMessageBox.Icon.Critical)
                    msg2.setText(
                        f"<h3>⚠️⚠️⚠️ LAST CHANCE TO CANCEL! ⚠️⚠️⚠️</h3>"
                    )
                    msg2.setInformativeText(
                        f"<b>File:</b> {Path(file_path).name}<br>"
                        f"<b>Size:</b> {file_size_gb:.1f} GB<br>"
                        f"<b>Algorithm:</b> {self.algo_combo.currentText().split(' - ')[0]}<br><br>"
                        f"<font color='#e74c3c' size='4'><b>THIS CANNOT BE UNDONE!</b></font><br><br>"
                        f"Are you ABSOLUTELY SURE you want to proceed?"
                    )
                    msg2.setStandardButtons(
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    msg2.setDefaultButton(QMessageBox.StandardButton.No)
                    
                    yes_btn = msg2.button(QMessageBox.StandardButton.Yes)
                    yes_btn.setText("🔴 YES, PROCEED")
                    yes_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
                    
                    if msg2.exec() == QMessageBox.StandardButton.No:
                        self.status_label.setText("Large file wipe cancelled (final confirmation)")
                        return
    
    except Exception as e:
        print(f"Error checking file size: {e}")
    
    # ===== ALL CHECKS PASSED - PROCEED WITH WIPE =====
    
    # Disable button
    self.wipe_btn.setEnabled(False)
    self.status_label.setText("Starting secure wipe...")
    
    # Get algorithm
    algorithm = self.algo_combo.currentData()
    
    # Create and start wiper thread
    self.wiper_thread = QThread()
    self.wiper_worker = WipeWorker(file_path, algorithm)
    self.wiper_worker.moveToThread(self.wiper_thread)
    
    # Connect signals
    self.wiper_thread.started.connect(self.wiper_worker.run)
    self.wiper_worker.progress.connect(self.update_progress)
    self.wiper_worker.finished.connect(self.wipe_finished)
    self.wiper_worker.finished.connect(self.wiper_thread.quit)
    self.wiper_worker.finished.connect(self.wiper_worker.deleteLater)
    self.wiper_thread.finished.connect(self.wiper_thread.deleteLater)
    
    # Start
    self.wiper_thread.start()

def estimate_wipe_time(self, file_size_bytes):
    """Estimate wipe time based on file size"""
    # Assume ~50 MB/s write speed (conservative)
    speed_mb_per_sec = 50
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    # Get passes based on algorithm
    algorithm = self.algo_combo.currentData()
    passes = {'simple': 1, 'dod': 3, 'nist': 1, 'gutmann': 7, 'crypto': 1}.get(algorithm, 3)
    
    total_seconds = (file_size_mb / speed_mb_per_sec) * passes
    
    if total_seconds < 60:
        return f"{int(total_seconds)} seconds"
    elif total_seconds < 3600:
        minutes = int(total_seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = int(total_seconds / 3600)
        minutes = int((total_seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

def format_size(self, bytes_size):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


# ====================================================================
# ADD THIS TO wipe_finished() function
# Find your existing wipe_finished and add sound/notification
# ====================================================================

def wipe_finished(self, success, message):
    """Handle wipe completion with notifications"""
    
    # Re-enable button
    self.wipe_btn.setEnabled(True)
    
    # Reset progress
    self.progress_bar.setValue(0)
    self.status_label.setText("Ready to wipe")
    
    file_path = self.file_input.text()
    algorithm = self.algo_combo.currentText()
    
    # ===== PLAY SOUND IF ENABLED =====
    if hasattr(self, 'sound_manager') and self.sound_manager:
        if hasattr(self, 'app_settings'):
            sound_enabled = self.app_settings.get('notifications', {}).get('play_sound', False)
            if sound_enabled:
                if success:
                    self.sound_manager.play_success()
                else:
                    self.sound_manager.play_error()
    
    # ===== ADD NOTIFICATION =====
    if hasattr(self, 'notification_manager') and self.notification_manager:
        if success:
            self.notification_manager.add(
                "✅ Wipe Completed",
                f"Successfully wiped {Path(file_path).name}",
                "success"
            )
        else:
            self.notification_manager.add(
                "❌ Wipe Failed",
                f"Failed to wipe {Path(file_path).name}",
                "error"
            )
        
        # Update bell icon
        if hasattr(self, 'notification_bell_btn'):
            self.update_notification_bell()
    
    # ... rest of your existing wipe_finished code ...
    # (certificate generation, history saving, message boxes, etc.)


# ====================================================================
# USAGE INSTRUCTIONS:
# ====================================================================

"""
1. Find your existing start_wipe() function
2. Replace it with the complete version above
3. Find wipe_finished() function
4. Add the sound/notification code at the beginning
5. Save and test!

SECURITY FEATURES NOW WORK:
✅ Confirmation before every wipe
✅ Double confirmation for large files
✅ Size threshold from settings
✅ Detailed warning dialogs
✅ Estimated time display
✅ Multiple confirmation levels
✅ User-friendly cancellation
"""
