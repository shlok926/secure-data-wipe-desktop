"""
Sound Manager Module for Secure Wipe
Handles all notification sounds
"""

import os
import sys
from PyQt6.QtCore import QObject
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl


class SoundManager(QObject):
    """Manage notification sounds for the application"""
    
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.sounds = {}
        
        # Try to load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound files"""
        sound_files = {
            'success': 'sounds/success.wav',
            'error': 'sounds/error.wav',
            'notification': 'sounds/notification.wav',
            'complete': 'sounds/complete.wav'
        }
        
        for name, path in sound_files.items():
            self.load_sound(name, path)
        
        # If no custom sounds, use system sounds
        if not self.sounds:
            print("Custom sounds not found, will use system sounds")
    
    def load_sound(self, name, path):
        """Load a single sound file"""
        try:
            if os.path.exists(path):
                sound = QSoundEffect()
                sound.setSource(QUrl.fromLocalFile(os.path.abspath(path)))
                sound.setVolume(0.5)  # 50% volume
                self.sounds[name] = sound
                print(f"Loaded sound: {name}")
            else:
                print(f"Sound file not found: {path}")
        except Exception as e:
            print(f"Could not load sound {name}: {e}")
    
    def play(self, sound_name):
        """Play a sound by name"""
        if not self.enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
        else:
            # Fallback to system beep
            self.play_system_beep()
    
    def play_system_beep(self):
        """Play system beep as fallback"""
        try:
            if sys.platform == 'win32':
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
            else:
                print('\a')  # Terminal bell
        except:
            pass
    
    def play_success(self):
        """Play success sound"""
        self.play('success')
    
    def play_error(self):
        """Play error sound"""
        self.play('error')
    
    def play_notification(self):
        """Play notification sound"""
        self.play('notification')
    
    def play_complete(self):
        """Play completion sound"""
        self.play('complete')
    
    def set_enabled(self, enabled):
        """Enable or disable sounds"""
        self.enabled = enabled
    
    def set_volume(self, volume):
        """Set volume for all sounds (0.0 to 1.0)"""
        for sound in self.sounds.values():
            sound.setVolume(volume)


# Quick test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import time
    
    app = QApplication(sys.argv)
    
    manager = SoundManager()
    
    print("Testing sounds...")
    print("Playing success sound...")
    manager.play_success()
    time.sleep(1)
    
    print("Playing error sound...")
    manager.play_error()
    time.sleep(1)
    
    print("Playing notification...")
    manager.play_notification()
    
    print("Done!")