"""
Folder Wiping Module for Secure Wipe
Recursive folder scanning and batch file wiping
"""

import os
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import QMessageBox


class FolderScanner(QObject):
    """Scan folder recursively and collect files"""
    
    progress = pyqtSignal(int, str)  # percent, message
    finished = pyqtSignal(list, int, int)  # files, total_count, total_size
    
    def __init__(self, folder_path, include_hidden=False):
        super().__init__()
        self.folder_path = folder_path
        self.include_hidden = include_hidden
        self.cancelled = False
    
    def run(self):
        """Scan folder and collect all files"""
        try:
            files = []
            total_size = 0
            
            # Walk through directory
            for root, dirs, filenames in os.walk(self.folder_path):
                
                if self.cancelled:
                    break
                
                # Filter hidden folders if needed
                if not self.include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    filenames = [f for f in filenames if not f.startswith('.')]
                
                for filename in filenames:
                    if self.cancelled:
                        break
                    
                    file_path = os.path.join(root, filename)
                    
                    try:
                        # Get file size
                        size = os.path.getsize(file_path)
                        
                        files.append({
                            'path': file_path,
                            'name': filename,
                            'size': size,
                            'relative_path': os.path.relpath(file_path, self.folder_path)
                        })
                        
                        total_size += size
                        
                        # Update progress
                        self.progress.emit(
                            len(files),
                            f"Scanning... Found {len(files)} files"
                        )
                        
                    except (PermissionError, OSError) as e:
                        # Skip files we can't access
                        continue
            
            self.finished.emit(files, len(files), total_size)
            
        except Exception as e:
            self.finished.emit([], 0, 0)
    
    def cancel(self):
        """Cancel scanning"""
        self.cancelled = True


class FolderWiper(QObject):
    """Wipe all files in a folder"""
    
    progress = pyqtSignal(int, int, str)  # current_file, total_files, message
    file_completed = pyqtSignal(str, bool)  # file_path, success
    finished = pyqtSignal(int, int)  # successful, failed
    
    def __init__(self, files, algorithm, wiper_core):
        super().__init__()
        self.files = files
        self.algorithm = algorithm
        self.wiper = wiper_core
        self.cancelled = False
        self.paused = False
    
    def run(self):
        """Wipe all files"""
        successful = 0
        failed = 0
        
        for index, file_info in enumerate(self.files):
            
            # Check if cancelled
            if self.cancelled:
                break
            
            # Check if paused
            while self.paused and not self.cancelled:
                QThread.msleep(100)
            
            file_path = file_info['path']
            file_name = file_info['name']
            
            # Update progress
            self.progress.emit(
                index + 1,
                len(self.files),
                f"Wiping: {file_name}"
            )
            
            # Wipe file
            try:
                self.wiper.set_algorithm(self.algorithm)
                success = self.wiper.wipe_file(file_path)
                
                if success:
                    successful += 1
                    self.file_completed.emit(file_path, True)
                else:
                    failed += 1
                    self.file_completed.emit(file_path, False)
                    
            except Exception as e:
                failed += 1
                self.file_completed.emit(file_path, False)
        
        self.finished.emit(successful, failed)
    
    def cancel(self):
        """Cancel wiping"""
        self.cancelled = True
    
    def pause(self):
        """Pause wiping"""
        self.paused = True
    
    def resume(self):
        """Resume wiping"""
        self.paused = False


class FolderWipeManager:
    """Manager for folder wiping operations"""
    
    @staticmethod
    def scan_folder(folder_path, include_hidden=False):
        """
        Scan folder and get file list
        
        Returns:
            dict: {'files': [...], 'total_count': int, 'total_size': int}
        """
        files = []
        total_size = 0
        
        try:
            for root, dirs, filenames in os.walk(folder_path):
                
                # Filter hidden
                if not include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    filenames = [f for f in filenames if not f.startswith('.')]
                
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    
                    try:
                        size = os.path.getsize(file_path)
                        files.append({
                            'path': file_path,
                            'name': filename,
                            'size': size,
                            'relative_path': os.path.relpath(file_path, folder_path)
                        })
                        total_size += size
                    except:
                        continue
            
            return {
                'files': files,
                'total_count': len(files),
                'total_size': total_size
            }
            
        except Exception as e:
            return {
                'files': [],
                'total_count': 0,
                'total_size': 0,
                'error': str(e)
            }
    
    @staticmethod
    def format_size(bytes_size):
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    @staticmethod
    def get_folder_summary(folder_path):
        """Get quick folder summary"""
        result = FolderWipeManager.scan_folder(folder_path)
        
        return {
            'path': folder_path,
            'total_files': result['total_count'],
            'total_size': result['total_size'],
            'formatted_size': FolderWipeManager.format_size(result['total_size']),
            'has_error': 'error' in result
        }
    
    @staticmethod
    def show_confirmation_dialog(parent, folder_path, file_count, total_size):
        """Show confirmation dialog before folder wipe"""
        formatted_size = FolderWipeManager.format_size(total_size)
        
        reply = QMessageBox.question(
            parent,
            "Confirm Folder Wipe",
            f"⚠️ WARNING: You are about to PERMANENTLY DELETE:\n\n"
            f"📁 Folder: {Path(folder_path).name}\n"
            f"📊 Files: {file_count} files\n"
            f"💾 Total Size: {formatted_size}\n\n"
            f"🔴 This operation CANNOT be undone!\n"
            f"🔴 ALL FILES will be permanently destroyed!\n\n"
            f"Type 'DELETE' to confirm:",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        return reply == QMessageBox.StandardButton.Yes
    
    @staticmethod
    def estimate_time(file_count, total_size_mb, algorithm='dod'):
        """Estimate time for folder wipe"""
        # Simple estimation
        base_speed_mbs = 80  # MB/s
        
        passes = {
            'simple': 1,
            'dod': 3,
            'nist': 1,
            'gutmann': 7,
            'crypto': 1
        }
        
        pass_count = passes.get(algorithm, 3)
        
        # Time for wiping
        wipe_time = (total_size_mb * pass_count) / base_speed_mbs
        
        # Add overhead for each file (0.5 sec per file)
        overhead = file_count * 0.5
        
        total_seconds = wipe_time + overhead
        
        # Format time
        if total_seconds < 60:
            return f"~{int(total_seconds)} seconds"
        elif total_seconds < 3600:
            minutes = int(total_seconds / 60)
            return f"~{minutes} minutes"
        else:
            hours = int(total_seconds / 3600)
            minutes = int((total_seconds % 3600) / 60)
            return f"~{hours}h {minutes}m"


# Convenience functions
def scan_folder_quick(folder_path):
    """Quick folder scan"""
    return FolderWipeManager.scan_folder(folder_path)


def get_folder_info(folder_path):
    """Get folder information"""
    return FolderWipeManager.get_folder_summary(folder_path)
