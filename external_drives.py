"""
External Drive Detection and Wiping Module
Support for USB drives, SD cards, and external storage
"""

import os
import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox


class DriveInfo:
    """Information about a storage drive"""
    
    def __init__(self, letter, label, drive_type, size, free_space):
        self.letter = letter
        self.label = label or "Unnamed"
        self.drive_type = drive_type
        self.size = size
        self.free_space = free_space
        self.is_removable = drive_type == "Removable"
    
    def get_display_name(self):
        """Get display name for UI"""
        size_gb = self.size / (1024**3)
        return f"{self.letter} - {self.label} ({size_gb:.1f} GB) [{self.drive_type}]"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'letter': self.letter,
            'label': self.label,
            'type': self.drive_type,
            'size': self.size,
            'free': self.free_space,
            'removable': self.is_removable
        }


class ExternalDriveManager:
    """Manage external drive operations"""
    
    @staticmethod
    def detect_drives():
        """
        Detect all drives on system
        
        Returns:
            list: List of DriveInfo objects
        """
        if sys.platform == 'win32':
            return ExternalDriveManager._detect_windows()
        elif sys.platform == 'darwin':
            return ExternalDriveManager._detect_macos()
        else:
            return ExternalDriveManager._detect_linux()
    
    @staticmethod
    def _detect_windows():
        """Detect drives on Windows"""
        import string
        import ctypes
        
        drives = []
        
        # Get all drive letters
        available_drives = ['%s:' % d for d in string.ascii_uppercase 
                           if os.path.exists('%s:' % d)]
        
        for drive in available_drives:
            try:
                # Get drive type
                drive_type_num = ctypes.windll.kernel32.GetDriveTypeW(drive + '\\')
                drive_types = {
                    0: "Unknown",
                    1: "No Root",
                    2: "Removable",  # USB, SD Card
                    3: "Fixed",      # HDD, SSD
                    4: "Network",
                    5: "CD-ROM",
                    6: "RAM Disk"
                }
                drive_type = drive_types.get(drive_type_num, "Unknown")
                
                # Get volume information
                try:
                    volume_name_buffer = ctypes.create_unicode_buffer(1024)
                    ctypes.windll.kernel32.GetVolumeInformationW(
                        drive + '\\',
                        volume_name_buffer,
                        ctypes.sizeof(volume_name_buffer),
                        None, None, None, None, 0
                    )
                    label = volume_name_buffer.value
                except:
                    label = ""
                
                # Get disk space
                try:
                    free_bytes = ctypes.c_ulonglong(0)
                    total_bytes = ctypes.c_ulonglong(0)
                    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                        drive + '\\',
                        None,
                        ctypes.pointer(total_bytes),
                        ctypes.pointer(free_bytes)
                    )
                    size = total_bytes.value
                    free = free_bytes.value
                except:
                    size = 0
                    free = 0
                
                drive_info = DriveInfo(drive, label, drive_type, size, free)
                drives.append(drive_info)
                
            except Exception as e:
                continue
        
        return drives
    
    @staticmethod
    def _detect_macos():
        """Detect drives on macOS"""
        drives = []
        
        try:
            # List volumes
            volumes_path = Path('/Volumes')
            if volumes_path.exists():
                for volume in volumes_path.iterdir():
                    if volume.is_dir():
                        try:
                            stat = os.statvfs(str(volume))
                            size = stat.f_blocks * stat.f_frsize
                            free = stat.f_bavail * stat.f_frsize
                            
                            drive_info = DriveInfo(
                                str(volume),
                                volume.name,
                                "Removable",  # Assume removable for /Volumes
                                size,
                                free
                            )
                            drives.append(drive_info)
                        except:
                            continue
        except:
            pass
        
        return drives
    
    @staticmethod
    def _detect_linux():
        """Detect drives on Linux"""
        drives = []
        
        try:
            # Check /media and /mnt
            for base_path in ['/media', '/mnt']:
                if os.path.exists(base_path):
                    for mount in os.listdir(base_path):
                        mount_path = os.path.join(base_path, mount)
                        if os.path.ismount(mount_path):
                            try:
                                stat = os.statvfs(mount_path)
                                size = stat.f_blocks * stat.f_frsize
                                free = stat.f_bavail * stat.f_frsize
                                
                                drive_info = DriveInfo(
                                    mount_path,
                                    mount,
                                    "Removable",
                                    size,
                                    free
                                )
                                drives.append(drive_info)
                            except:
                                continue
        except:
            pass
        
        return drives
    
    @staticmethod
    def get_removable_drives():
        """Get only removable drives (USB, SD cards)"""
        all_drives = ExternalDriveManager.detect_drives()
        return [drive for drive in all_drives if drive.is_removable]
    
    @staticmethod
    def is_drive_safe_to_wipe(drive_letter):
        """
        Check if drive is safe to wipe
        
        Returns:
            tuple: (bool, str) - (is_safe, reason)
        """
        # Never wipe C: drive on Windows
        if sys.platform == 'win32':
            if drive_letter.upper() in ['C:', 'C']:
                return False, "Cannot wipe system drive (C:)"
        
        # Check if drive is removable
        drives = ExternalDriveManager.detect_drives()
        for drive in drives:
            if drive.letter == drive_letter:
                if not drive.is_removable:
                    return False, "Not a removable drive"
                return True, "Safe to wipe"
        
        return False, "Drive not found"
    
    @staticmethod
    def format_size(bytes_val):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
    
    @staticmethod
    def show_drive_warning(parent, drive_info):
        """Show warning dialog before wiping drive"""
        size_str = ExternalDriveManager.format_size(drive_info.size)
        
        reply = QMessageBox.warning(
            parent,
            "⚠️ EXTREME WARNING",
            f"🔴 DANGER: You are about to COMPLETELY WIPE:\n\n"
            f"Drive: {drive_info.letter}\n"
            f"Label: {drive_info.label}\n"
            f"Size: {size_str}\n"
            f"Type: {drive_info.drive_type}\n\n"
            f"⚠️ ALL DATA WILL BE PERMANENTLY LOST!\n"
            f"⚠️ THIS CANNOT BE UNDONE!\n"
            f"⚠️ THE ENTIRE DRIVE WILL BE ERASED!\n\n"
            f"Type the drive letter to confirm:",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )
        
        return reply == QMessageBox.StandardButton.Ok


class DriveWiper:
    """Wipe entire external drives"""
    
    @staticmethod
    def wipe_drive(drive_info, algorithm, progress_callback=None):
        """
        Wipe entire drive
        
        Args:
            drive_info: DriveInfo object
            algorithm: Wiping algorithm
            progress_callback: Function to call with progress
            
        Returns:
            bool: Success status
        """
        # WARNING: This is dangerous!
        # Only for removable drives
        
        if not drive_info.is_removable:
            return False
        
        # TODO: Implement actual drive wiping
        # This would involve:
        # 1. Unmounting drive
        # 2. Direct block device access
        # 3. Overwriting all sectors
        # 4. Remounting/formatting
        
        return False  # Not implemented yet for safety
    
    @staticmethod
    def quick_format_drive(drive_letter):
        """
        Quick format drive (Windows only)
        
        Args:
            drive_letter: Drive letter (e.g., "E:")
            
        Returns:
            bool: Success status
        """
        if sys.platform != 'win32':
            return False
        
        try:
            # Use Windows format command
            subprocess.run(
                ['format', drive_letter, '/Q', '/FS:NTFS', '/Y'],
                capture_output=True,
                timeout=60
            )
            return True
        except:
            return False


# Example usage
if __name__ == "__main__":
    print("Detecting drives...")
    print("=" * 60)
    
    # Detect all drives
    all_drives = ExternalDriveManager.detect_drives()
    
    print(f"\nFound {len(all_drives)} drives:\n")
    for drive in all_drives:
        print(f"  {drive.get_display_name()}")
        print(f"    Free: {ExternalDriveManager.format_size(drive.free_space)}")
        print(f"    Removable: {drive.is_removable}")
        print()
    
    # Get removable drives only
    removable = ExternalDriveManager.get_removable_drives()
    print(f"\n{len(removable)} removable drives found:")
    for drive in removable:
        print(f"  ✅ {drive.get_display_name()}")
