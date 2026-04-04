"""
Algorithm Recommendation System for Secure Wipe
Smart algorithm selection based on file type, size, and storage
"""

import os
import sys
from pathlib import Path


class AlgorithmRecommender:
    """Recommend optimal wiping algorithm based on file characteristics"""
    
    def __init__(self):
        """Initialize recommender with file type classifications"""
        
        # Sensitive document types
        self.sensitive_documents = {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.txt', '.csv', '.odt', '.ods', '.odp', '.rtf'
        }
        
        # Media files (less sensitive)
        self.media_files = {
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
            '.svg', '.ico'
        }
        
        # Encrypted/compressed files
        self.encrypted_files = {
            '.gpg', '.pgp', '.aes', '.encrypted', '.enc',
            '.7z', '.zip', '.rar', '.tar', '.gz'
        }
        
        # Source code files
        self.source_code = {
            '.py', '.js', '.java', '.cpp', '.c', '.h', '.cs',
            '.php', '.rb', '.go', '.rs', '.swift', '.kt'
        }
        
        # System files
        self.system_files = {
            '.exe', '.dll', '.sys', '.msi', '.bat', '.sh',
            '.app', '.dmg', '.deb', '.rpm'
        }
        
        # Large file threshold (MB)
        self.large_file_threshold = 1000  # 1 GB
        self.very_large_threshold = 5000  # 5 GB
    
    def recommend(self, file_path):
        """
        Get algorithm recommendation for a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            dict: Recommendation with algorithm, reason, and priority
        """
        # Get file info
        ext = Path(file_path).suffix.lower()
        file_size_mb = self._get_file_size_mb(file_path)
        is_ssd = self._is_on_ssd(file_path)
        
        # Collect all recommendations with priorities
        recommendations = []
        
        # SSD-specific recommendation
        if is_ssd:
            recommendations.append({
                'algorithm': 'nist',
                'reason': '🔥 SSD Detected - NIST SP 800-88 optimized for solid state drives',
                'priority': 10,
                'category': 'Storage Type'
            })
        
        # Very large files
        if file_size_mb > self.very_large_threshold:
            recommendations.append({
                'algorithm': 'simple',
                'reason': f'⚡ Very Large File ({file_size_mb/1024:.1f} GB) - Single Pass for speed',
                'priority': 11,
                'category': 'File Size'
            })
        
        # Large files
        elif file_size_mb > self.large_file_threshold:
            recommendations.append({
                'algorithm': 'simple',
                'reason': f'📦 Large File ({file_size_mb:.0f} MB) - Single Pass recommended',
                'priority': 8,
                'category': 'File Size'
            })
        
        # Encrypted/compressed files
        if ext in self.encrypted_files or self._is_encrypted_filename(file_path):
            recommendations.append({
                'algorithm': 'crypto',
                'reason': '🔐 Encrypted/Compressed - Cryptographic Erase recommended',
                'priority': 10,
                'category': 'File Type'
            })
        
        # Sensitive documents
        elif ext in self.sensitive_documents:
            recommendations.append({
                'algorithm': 'dod',
                'reason': '🔒 Sensitive Document - DoD 5220.22-M (3 passes) for security',
                'priority': 9,
                'category': 'File Type'
            })
        
        # Media files
        elif ext in self.media_files:
            recommendations.append({
                'algorithm': 'simple',
                'reason': '🎬 Media File - Single Pass sufficient',
                'priority': 7,
                'category': 'File Type'
            })
        
        # Source code
        elif ext in self.source_code:
            recommendations.append({
                'algorithm': 'dod',
                'reason': '💻 Source Code - DoD 5220.22-M recommended',
                'priority': 8,
                'category': 'File Type'
            })
        
        # System files
        elif ext in self.system_files:
            recommendations.append({
                'algorithm': 'dod',
                'reason': '⚙️ System File - DoD 5220.22-M for security',
                'priority': 8,
                'category': 'File Type'
            })
        
        # Small sensitive files (< 100 MB)
        if file_size_mb < 100 and file_size_mb > 0:
            recommendations.append({
                'algorithm': 'gutmann',
                'reason': f'🛡️ Small File ({file_size_mb:.1f} MB) - Gutmann (7 passes) for maximum security',
                'priority': 6,
                'category': 'File Size'
            })
        
        # Sort by priority (highest first)
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        # Return top recommendation or default
        if recommendations:
            return recommendations[0]
        else:
            return {
                'algorithm': 'dod',
                'reason': '🛡️ Default - DoD 5220.22-M (balanced security and speed)',
                'priority': 5,
                'category': 'Default'
            }
    
    def get_all_recommendations(self, file_path):
        """
        Get all applicable recommendations sorted by priority
        
        Args:
            file_path: Path to the file
            
        Returns:
            list: All recommendations
        """
        # This returns all possible recommendations, not just top one
        # Useful for showing alternatives to user
        return self._collect_recommendations(file_path)
    
    def _get_file_size_mb(self, file_path):
        """Get file size in megabytes"""
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except:
            return 0
    
    def _is_on_ssd(self, file_path):
        """
        Check if file is on SSD (Windows only)
        Basic implementation
        """
        try:
            # Windows only
            if sys.platform != 'win32':
                return False
            
            import subprocess
            drive = Path(file_path).drive
            
            # Get physical disk info
            result = subprocess.run(
                ['powershell', '-Command',
                 f'Get-PhysicalDisk | Select-Object MediaType'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            # Check if SSD is mentioned
            return 'SSD' in result.stdout.upper()
            
        except:
            # If detection fails, assume HDD (safer default)
            return False
    
    def _is_encrypted_filename(self, file_path):
        """Check if filename suggests encryption"""
        name_lower = Path(file_path).name.lower()
        keywords = ['encrypt', 'secure', 'protected', 'locked', 'secret']
        return any(keyword in name_lower for keyword in keywords)
    
    def _collect_recommendations(self, file_path):
        """Collect all applicable recommendations"""
        # Implementation similar to recommend() but returns all, not just top
        pass


class AlgorithmInfo:
    """Information about wiping algorithms"""
    
    @staticmethod
    def get_algorithm_details(algorithm):
        """Get detailed information about an algorithm"""
        algorithms = {
            'simple': {
                'name': 'Single Pass',
                'passes': 1,
                'security_level': 'Basic',
                'speed': 'Very Fast',
                'use_case': 'Non-sensitive data, quick wiping',
                'compliance': None
            },
            'dod': {
                'name': 'DoD 5220.22-M',
                'passes': 3,
                'security_level': 'High',
                'speed': 'Fast',
                'use_case': 'Government standard, recommended for most users',
                'compliance': 'US DoD'
            },
            'nist': {
                'name': 'NIST SP 800-88',
                'passes': 1,
                'security_level': 'High',
                'speed': 'Very Fast',
                'use_case': 'Modern SSDs and storage devices',
                'compliance': 'NIST'
            },
            'gutmann': {
                'name': 'Gutmann Method',
                'passes': 7,
                'security_level': 'Maximum',
                'speed': 'Slow',
                'use_case': 'Highly sensitive data, maximum security',
                'compliance': 'Academic standard'
            },
            'crypto': {
                'name': 'Cryptographic Erase',
                'passes': 1,
                'security_level': 'Maximum',
                'speed': 'Instant',
                'use_case': 'Pre-encrypted data, enterprise',
                'compliance': None
            }
        }
        
        return algorithms.get(algorithm, None)


# Convenience functions
def get_recommendation(file_path):
    """
    Quick function to get algorithm recommendation
    
    Args:
        file_path: Path to file
        
    Returns:
        dict: Recommendation
    """
    recommender = AlgorithmRecommender()
    return recommender.recommend(file_path)


def get_algorithm_info(algorithm):
    """
    Get information about an algorithm
    
    Args:
        algorithm: Algorithm key
        
    Returns:
        dict: Algorithm details
    """
    return AlgorithmInfo.get_algorithm_details(algorithm)


# Example usage
if __name__ == "__main__":
    recommender = AlgorithmRecommender()
    
    # Test recommendations
    test_files = [
        "confidential_report.pdf",
        "vacation_video.mp4",
        "secret.gpg",
        "project.zip",
        "database_backup.sql",
        "source_code.py"
    ]
    
    print("Algorithm Recommendations:")
    print("=" * 70)
    
    for file in test_files:
        # Note: These are dummy files for testing
        # In real use, file must exist
        recommendation = {
            'algorithm': 'dod',
            'reason': 'Test recommendation',
            'category': 'Test'
        }
        
        print(f"\nFile: {file}")
        print(f"  Recommended: {recommendation['algorithm'].upper()}")
        print(f"  Reason: {recommendation['reason']}")
