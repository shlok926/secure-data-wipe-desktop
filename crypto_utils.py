"""
crypto_utils.py - Handles encryption and decryption of sensitive settings.
Provides secure storage for the email sender password and other secrets.
"""
from cryptography.fernet import Fernet
from PyQt6.QtCore import QSettings

class CryptoManager:
    """Manages encryption and decryption of sensitive data."""
    def __init__(self):
        self.settings = QSettings("SecureWipeInc", "SecureWipeApp")
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)
        
    def _get_or_create_key(self):
        key = self.settings.value("encryption_key", "")
        if not key:
            key = Fernet.generate_key().decode('utf-8')
            self.settings.setValue("encryption_key", key)
        return key.encode('utf-8')
        
    def encrypt(self, plain_text: str) -> str:
        """Encrypt plain text and return hex/string."""
        if not plain_text:
            return ""
        try:
            return self.fernet.encrypt(plain_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return ""
        
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt string back to plain text. Returns empty string on failure."""
        if not encrypted_text:
            return ""
        try:
            return self.fernet.decrypt(encrypted_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            print(f"Decryption error (could be plain text or invalid key): {e}")
            return ""
