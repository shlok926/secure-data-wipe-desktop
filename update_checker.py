"""
Update Checker Module for Secure Wipe
Check for updates from GitHub releases
"""

import json
import urllib.request
import urllib.error
from datetime import datetime


class UpdateChecker:
    """Check for application updates"""
    
    def __init__(self, current_version="2.0"):
        self.current_version = current_version
        self.github_api = "https://api.github.com/repos/yourusername/securewipe/releases/latest"
        self.update_available = False
        self.latest_version = None
        self.download_url = None
    
    def check_for_updates(self):
        """Check if update is available"""
        try:
            # Make API request
            req = urllib.request.Request(self.github_api)
            req.add_header('User-Agent', 'SecureWipe/2.0')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
            
            # Get latest version
            self.latest_version = data.get('tag_name', '').lstrip('v')
            self.download_url = data.get('html_url')
            
            # Compare versions
            if self.latest_version and self.compare_versions(self.latest_version, self.current_version):
                self.update_available = True
                return True, self.latest_version, self.download_url
            else:
                return False, self.current_version, None
        
        except urllib.error.URLError:
            # No internet or GitHub unreachable
            return None, "Unable to check", None
        except Exception as e:
            print(f"Error checking updates: {e}")
            return None, "Error checking", None
    
    def compare_versions(self, version1, version2):
        """Compare two version strings"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Pad with zeros
            while len(v1_parts) < 3:
                v1_parts.append(0)
            while len(v2_parts) < 3:
                v2_parts.append(0)
            
            return v1_parts > v2_parts
        except:
            return False
    
    def get_update_info(self):
        """Get update information"""
        return {
            'available': self.update_available,
            'current': self.current_version,
            'latest': self.latest_version,
            'download_url': self.download_url
        }


# For testing without internet
class MockUpdateChecker:
    """Mock update checker for testing"""
    
    def __init__(self, current_version="2.0"):
        self.current_version = current_version
        self.update_available = False
    
    def check_for_updates(self):
        """Simulate update check"""
        import random
        
        # 30% chance of update available
        if random.random() < 0.3:
            return True, "2.1", "https://github.com/yourusername/securewipe/releases"
        else:
            return False, self.current_version, None
    
    def get_update_info(self):
        return {
            'available': self.update_available,
            'current': self.current_version,
            'latest': None,
            'download_url': None
        }
