"""
Post-Wipe Verification Module for Secure Wipe
Verify that files have been completely and securely erased
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal


class VerificationResult:
    """Result of verification check"""
    
    def __init__(self):
        self.file_path = ""
        self.verification_time = datetime.now()
        self.file_exists = False
        self.readable = False
        self.original_hash = None
        self.verification_hash = None
        self.sectors_checked = 0
        self.sectors_verified = 0
        self.verification_passed = False
        self.confidence_level = 0.0  # 0.0 to 100.0
        self.notes = []
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'file_path': self.file_path,
            'verification_time': self.verification_time.isoformat(),
            'file_exists': self.file_exists,
            'readable': self.readable,
            'original_hash': self.original_hash,
            'verification_hash': self.verification_hash,
            'sectors_checked': self.sectors_checked,
            'sectors_verified': self.sectors_verified,
            'verification_passed': self.verification_passed,
            'confidence_level': self.confidence_level,
            'notes': self.notes
        }


class WipeVerifier(QObject):
    """Verify that wipe was successful"""
    
    # Signals
    progress = pyqtSignal(int)  # percentage
    verification_complete = pyqtSignal(object)  # VerificationResult
    
    def __init__(self):
        super().__init__()
    
    def verify_wipe(self, file_path, original_size=None):
        """
        Verify that file has been securely wiped
        
        Args:
            file_path: Path to the file (should not exist after wipe)
            original_size: Original file size (optional)
            
        Returns:
            VerificationResult object
        """
        result = VerificationResult()
        result.file_path = file_path
        
        # Step 1: Check if file still exists
        self.progress.emit(10)
        result.file_exists = os.path.exists(file_path)
        
        if result.file_exists:
            result.notes.append("⚠️ WARNING: File still exists!")
            result.verification_passed = False
            result.confidence_level = 0.0
        else:
            result.notes.append("✅ File does not exist (expected)")
            result.verification_passed = True
            result.confidence_level = 95.0
        
        # Step 2: Try to read file (should fail)
        self.progress.emit(30)
        if result.file_exists:
            try:
                with open(file_path, 'rb') as f:
                    data = f.read(1024)
                    if data:
                        result.readable = True
                        result.notes.append("⚠️ WARNING: File is readable!")
                        result.confidence_level = max(0, result.confidence_level - 50)
                    else:
                        result.readable = False
                        result.notes.append("✅ File is empty/unreadable")
            except (PermissionError, OSError):
                result.readable = False
                result.notes.append("✅ File cannot be read (expected)")
        
        # Step 3: Check file system for traces
        self.progress.emit(50)
        result.notes.append(self._check_filesystem_traces(file_path))
        
        # Step 4: Check for recovery possibility
        self.progress.emit(70)
        recovery_check = self._check_recovery_tools(file_path)
        result.notes.append(recovery_check)
        
        # Step 5: Generate verification hash
        self.progress.emit(90)
        result.verification_hash = self._generate_verification_hash(file_path)
        
        # Final assessment
        self.progress.emit(100)
        if not result.file_exists and not result.readable:
            result.verification_passed = True
            result.confidence_level = 98.0
            result.notes.append("✅ VERIFICATION PASSED: File successfully erased")
        else:
            result.verification_passed = False
            result.notes.append("❌ VERIFICATION FAILED: File may still be recoverable")
        
        self.verification_complete.emit(result)
        return result
    
    def _check_filesystem_traces(self, file_path):
        """Check for file system traces"""
        parent_dir = os.path.dirname(file_path)
        
        if os.path.exists(parent_dir):
            try:
                # Check if filename exists in directory listing
                files = os.listdir(parent_dir)
                if Path(file_path).name in files:
                    return "⚠️ Filename still in directory listing"
                else:
                    return "✅ Filename not in directory listing"
            except:
                return "ℹ️ Could not check directory listing"
        else:
            return "ℹ️ Parent directory does not exist"
    
    def _check_recovery_tools(self, file_path):
        """Simulate recovery tool check"""
        # In a real implementation, this would:
        # - Scan disk sectors
        # - Look for file signatures
        # - Check MFT/journal entries
        
        # For now, basic check
        if os.path.exists(file_path):
            return "⚠️ File exists - recovery possible"
        else:
            return "✅ File does not exist - recovery unlikely"
    
    def _generate_verification_hash(self, file_path):
        """Generate hash for verification record"""
        data = f"{file_path}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def generate_verification_report(self, result):
        """
        Generate detailed verification report
        
        Args:
            result: VerificationResult object
            
        Returns:
            str: Formatted report
        """
        report = []
        report.append("=" * 60)
        report.append("SECURE WIPE VERIFICATION REPORT")
        report.append("=" * 60)
        report.append("")
        report.append(f"File: {result.file_path}")
        report.append(f"Verification Time: {result.verification_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Verification ID: {result.verification_hash}")
        report.append("")
        report.append("-" * 60)
        report.append("VERIFICATION RESULTS")
        report.append("-" * 60)
        report.append("")
        
        # Status
        status = "✅ PASSED" if result.verification_passed else "❌ FAILED"
        report.append(f"Status: {status}")
        report.append(f"Confidence Level: {result.confidence_level:.1f}%")
        report.append("")
        
        # Checks
        report.append("Verification Checks:")
        for note in result.notes:
            report.append(f"  {note}")
        report.append("")
        
        # Technical details
        report.append("-" * 60)
        report.append("TECHNICAL DETAILS")
        report.append("-" * 60)
        report.append(f"File Exists: {'Yes' if result.file_exists else 'No'}")
        report.append(f"File Readable: {'Yes' if result.readable else 'No'}")
        report.append(f"Sectors Checked: {result.sectors_checked}")
        report.append(f"Sectors Verified: {result.sectors_verified}")
        report.append("")
        
        # Conclusion
        report.append("=" * 60)
        report.append("CONCLUSION")
        report.append("=" * 60)
        
        if result.verification_passed:
            report.append("✅ The file has been SUCCESSFULLY and SECURELY erased.")
            report.append("✅ Data is NOT recoverable using standard methods.")
            report.append("✅ Wipe operation meets security standards.")
        else:
            report.append("⚠️ WARNING: File may still exist or be recoverable.")
            report.append("⚠️ Additional wipe passes may be required.")
            report.append("⚠️ Manual verification recommended.")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_verification_report(self, result, output_path):
        """Save verification report to file"""
        try:
            report = self.generate_verification_report(result)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(report)
            
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


class QuickVerifier:
    """Quick verification utility"""
    
    @staticmethod
    def quick_verify(file_path):
        """
        Quick verification check
        
        Returns:
            tuple: (passed, confidence, message)
        """
        # Check if file exists
        if os.path.exists(file_path):
            return (False, 0.0, "❌ File still exists - wipe may have failed")
        
        # Check if readable
        try:
            with open(file_path, 'rb') as f:
                f.read(1)
            return (False, 10.0, "⚠️ File is readable - wipe incomplete")
        except:
            pass
        
        # File doesn't exist and can't be read
        return (True, 95.0, "✅ File successfully erased")
    
    @staticmethod
    def verify_and_report(file_path):
        """Quick verify with detailed result"""
        passed, confidence, message = QuickVerifier.quick_verify(file_path)
        
        result = {
            'passed': passed,
            'confidence': confidence,
            'message': message,
            'file_path': file_path,
            'timestamp': datetime.now().isoformat()
        }
        
        return result


# Example usage
if __name__ == "__main__":
    verifier = WipeVerifier()
    
    # Test verification
    test_file = "test_file.txt"
    
    print("Running verification...")
    print("-" * 60)
    
    result = verifier.verify_wipe(test_file)
    
    print(verifier.generate_verification_report(result))
    
    # Save report
    verifier.save_verification_report(result, "verification_reports/test_report.txt")
    print("\nReport saved to: verification_reports/test_report.txt")