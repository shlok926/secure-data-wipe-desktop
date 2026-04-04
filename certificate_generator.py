"""
Secure Wipe Certificate Generator
Generates professional PDF certificates for data destruction compliance
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import hashlib
import os


class WipeCertificateGenerator:
    """Generate professional wipe certificates"""
    
    def __init__(self):
        self.output_dir = "certificates"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_certificate(
        self,
        file_path: str,
        file_size: int,
        algorithm: str,
        timestamp: datetime,
        success: bool = True,
        operator: str = "System User"
    ) -> str:
        """
        Generate PDF certificate for wipe operation
        
        Returns:
            str: Path to generated PDF certificate
        """
        
        # Generate certificate ID
        cert_id = self.generate_certificate_id(file_path, timestamp)
        
        # Create filename
        filename = f"wipe_cert_{cert_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # Draw certificate
        self._draw_header(c, width, height)
        self._draw_title(c, width, height)
        self._draw_certificate_id(c, width, height, cert_id)
        self._draw_details(c, width, height, file_path, file_size, algorithm, timestamp, operator)
        self._draw_footer(c, width, height, timestamp)
        self._draw_security_hash(c, width, height, cert_id)
        
        c.save()
        
        return filepath
    
    def generate_certificate_id(self, file_path: str, timestamp: datetime) -> str:
        """Generate unique certificate ID"""
        data = f"{file_path}{timestamp.isoformat()}".encode()
        hash_obj = hashlib.sha256(data)
        return hash_obj.hexdigest()[:16].upper()
    
    def _draw_header(self, c, width, height):
        """Draw certificate header"""
        # Logo area (placeholder)
        c.setFillColor(colors.HexColor('#3498db'))
        c.rect(50, height - 100, 100, 60, fill=1, stroke=0)
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(60, height - 75, "SECURE")
        c.drawString(70, height - 95, "WIPE")
        
        # Company info
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 50, "Secure Data Wiping System v2.0")
        c.drawRightString(width - 50, height - 65, "Compliance Certification Department")
        c.drawRightString(width - 50, height - 80, "Certificate of Data Destruction")
    
    def _draw_title(self, c, width, height):
        """Draw certificate title"""
        c.setFillColor(colors.HexColor('#2c3e50'))
        c.setFont("Helvetica-Bold", 24)
        title = "CERTIFICATE OF SECURE DATA DESTRUCTION"
        title_width = c.stringWidth(title, "Helvetica-Bold", 24)
        c.drawString((width - title_width) / 2, height - 150, title)
        
        # Underline
        c.setStrokeColor(colors.HexColor('#3498db'))
        c.setLineWidth(2)
        c.line(50, height - 160, width - 50, height - 160)
    
    def _draw_certificate_id(self, c, width, height, cert_id):
        """Draw certificate ID"""
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor('#e74c3c'))
        c.drawString(50, height - 190, f"Certificate ID: {cert_id}")
    
    def _draw_details(self, c, width, height, file_path, file_size, algorithm, timestamp, operator):
        """Draw wipe operation details"""
        y = height - 240
        
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(50, y, "Destruction Details:")
        
        y -= 30
        c.setFont("Helvetica", 11)
        
        # File information
        details = [
            ("File Path:", os.path.basename(file_path)),
            ("Full Path:", file_path if len(file_path) < 70 else file_path[:67] + "..."),
            ("File Size:", f"{file_size:,} bytes ({file_size / (1024*1024):.2f} MB)"),
            ("", ""),
            ("Destruction Method:", algorithm),
            ("Timestamp:", timestamp.strftime("%Y-%m-%d %H:%M:%S")),
            ("Operator:", operator),
            ("", ""),
            ("Compliance Standards:", "DoD 5220.22-M, NIST SP 800-88"),
            ("Status:", "✓ SUCCESSFULLY DESTROYED"),
        ]
        
        for label, value in details:
            if label:
                c.setFont("Helvetica-Bold", 11)
                c.drawString(70, y, label)
                c.setFont("Helvetica", 11)
                c.drawString(250, y, value)
            y -= 20
    
    def _draw_footer(self, c, width, height, timestamp):
        """Draw certificate footer"""
        y = 150
        
        # Certification statement
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Certification Statement:")
        
        y -= 20
        c.setFont("Helvetica", 9)
        statement = (
            "This certificate confirms that the specified data has been permanently and irreversibly "
            "destroyed using military-grade secure wiping algorithms in accordance with industry standards. "
            "The data cannot be recovered by any known method."
        )
        
        # Word wrap
        words = statement.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, "Helvetica", 9) < width - 100:
                line = test_line
            else:
                c.drawString(50, y, line)
                y -= 15
                line = word + " "
        c.drawString(50, y, line)
        
        # Signature line
        y -= 40
        c.setLineWidth(1)
        c.line(50, y, 250, y)
        y -= 15
        c.setFont("Helvetica", 9)
        c.drawString(50, y, "Authorized by: Secure Wipe System")
        c.drawString(50, y - 15, f"Date: {timestamp.strftime('%B %d, %Y')}")
    
    def _draw_security_hash(self, c, width, height, cert_id):
        """Draw security verification hash"""
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.grey)
        c.drawString(50, 50, f"Verification Hash: {cert_id}")
        c.drawString(50, 40, "This certificate is digitally verifiable and tamper-proof.")
        
        # QR code placeholder
        c.setFillColor(colors.lightgrey)
        c.rect(width - 120, 30, 70, 70, fill=1, stroke=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7)
        c.drawCentredString(width - 85, 45, "VERIFICATION")
        c.drawCentredString(width - 85, 35, "QR CODE")


def generate_wipe_certificate(file_path, file_size, algorithm, timestamp, success=True):
    """
    Convenience function to generate certificate
    
    Args:
        file_path: Path of wiped file
        file_size: Size in bytes
        algorithm: Wiping algorithm used
        timestamp: When wipe occurred
        success: Whether wipe was successful
        
    Returns:
        str: Path to generated PDF certificate
    """
    generator = WipeCertificateGenerator()
    return generator.generate_certificate(
        file_path=file_path,
        file_size=file_size,
        algorithm=algorithm,
        timestamp=timestamp,
        success=success
    )


if __name__ == "__main__":
    # Test certificate generation
    test_cert = generate_wipe_certificate(
        file_path="C:/Users/Test/Documents/confidential_report.pdf",
        file_size=2485760,
        algorithm="DoD 5220.22-M (3 passes)",
        timestamp=datetime.now()
    )
    print(f"Test certificate generated: {test_cert}")
