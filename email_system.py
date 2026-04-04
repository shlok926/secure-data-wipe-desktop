"""
Email Automation System for Secure Wipe
Sends monthly audit reports automatically like bank statements
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from pathlib import Path


class EmailReportSystem:
    """Automated email reporting system"""
    
    def __init__(self):
        self.config_file = "config/email_config.json"
        self.load_config()
    
    def load_config(self):
        """Load email configuration"""
        default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "",
            "sender_password": "",
            "recipient_email": "",
            "auto_send_enabled": False,
            "send_day": 1  # Day of month to send (1-28)
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                
                # Decrypt password for RAM usage
                from crypto_utils import CryptoManager
                pw = self.config.get('sender_password', '')
                dec = CryptoManager().decrypt(pw)
                if pw and not dec:
                    dec = pw  # fallback for old plaintext passwords
                self.config['sender_password'] = dec
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
    
    def save_config(self):
        """Save email configuration"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Encrypt before saving
        save_data = self.config.copy()
        from crypto_utils import CryptoManager
        save_data['sender_password'] = CryptoManager().encrypt(save_data.get('sender_password', ''))
        
        with open(self.config_file, 'w') as f:
            json.dump(save_data, f, indent=4)
    
    def update_config(self, smtp_server, smtp_port, sender_email, sender_password, recipient_email):
        """Update email configuration"""
        self.config.update({
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "sender_email": sender_email,
            "sender_password": sender_password,
            "recipient_email": recipient_email
        })
        self.save_config()
    
    def generate_monthly_report_html(self, wipe_history):
        """Generate HTML monthly report"""
        
        # Calculate statistics
        total_wipes = len(wipe_history)
        successful = sum(1 for w in wipe_history if w.get('success', False))
        failed = total_wipes - successful
        total_size = sum(w.get('file_size', 0) for w in wipe_history)
        
        # Group by algorithm
        algo_usage = {}
        for wipe in wipe_history:
            algo = wipe.get('algorithm', 'Unknown')
            algo_usage[algo] = algo_usage.get(algo, 0) + 1
        
        # Generate HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }}
                .stat-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }}
                .stat-number {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 14px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th {{
                    background: #667eea;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background: #f5f5f5;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #eee;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔒 Secure Wipe Monthly Report</h1>
                <p>{datetime.now().strftime('%B %Y')}</p>
            </div>
            
            <div class="summary">
                <div class="stat-card">
                    <div class="stat-number">{total_wipes}</div>
                    <div class="stat-label">Total Wipes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{successful}</div>
                    <div class="stat-label">Successful</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_size / (1024**3):.2f} GB</div>
                    <div class="stat-label">Data Destroyed</div>
                </div>
            </div>
            
            <h2>📊 Algorithm Usage</h2>
            <table>
                <tr>
                    <th>Algorithm</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
        """
        
        for algo, count in algo_usage.items():
            percentage = (count / total_wipes * 100) if total_wipes > 0 else 0
            html += f"""
                <tr>
                    <td>{algo}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>📋 Recent Operations</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>File</th>
                    <th>Algorithm</th>
                    <th>Status</th>
                </tr>
        """
        
        # Show last 10 wipes
        for wipe in wipe_history[-10:]:
            timestamp = wipe.get('timestamp', datetime.now())
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            
            file_name = Path(wipe.get('file_path', 'Unknown')).name
            algorithm = wipe.get('algorithm', 'Unknown')
            status = "✅ Success" if wipe.get('success', False) else "❌ Failed"
            
            html += f"""
                <tr>
                    <td>{timestamp.strftime('%Y-%m-%d %H:%M')}</td>
                    <td>{file_name}</td>
                    <td>{algorithm}</td>
                    <td>{status}</td>
                </tr>
            """
        
        html += f"""
            </table>
            
            <div class="footer">
                <p><strong>Secure Data Wiping System v2.0</strong></p>
                <p>This is an automated monthly report. Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
                <p>For support or questions, please contact your system administrator.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_monthly_report(self, wipe_history, attachment_path=None):
        """Send monthly report email"""
        
        if not self.config.get('sender_email') or not self.config.get('recipient_email'):
            return False, "Email configuration incomplete"
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            msg['Subject'] = f"🔒 Secure Wipe Monthly Report - {datetime.now().strftime('%B %Y')}"
            
            # Generate HTML report
            html_content = self.generate_monthly_report_html(wipe_history)
            
            # Attach HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Attach file if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(attachment_path)}'
                    )
                    msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.send_message(msg)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, str(e)
    
    def should_send_monthly_report(self):
        """Check if it's time to send monthly report"""
        if not self.config.get('auto_send_enabled', False):
            return False
        
        today = datetime.now().day
        send_day = self.config.get('send_day', 1)
        
        # Check if we're on the designated day
        return today == send_day
    
    def send_instant_certificate(self, certificate_path, file_name):
        """Send wipe certificate immediately after operation"""
        
        if not self.config.get('sender_email') or not self.config.get('recipient_email'):
            return False, "Email configuration incomplete"
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            msg['Subject'] = f"✅ Wipe Certificate - {file_name}"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>Secure Wipe Certificate</h2>
                <p>A file has been securely wiped and a certificate has been generated.</p>
                <p><strong>File:</strong> {file_name}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Please find the attached certificate for your records.</p>
                <br>
                <p><i>This is an automated message from Secure Wipe System.</i></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach certificate
            with open(certificate_path, 'rb') as f:
                part = MIMEBase('application', 'pdf')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(certificate_path)}'
                )
                msg.attach(part)
            
            # Send
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.send_message(msg)
            
            return True, "Certificate emailed successfully"
            
        except Exception as e:
            return False, str(e)


# Convenience functions
def setup_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email):
    """Setup email configuration"""
    system = EmailReportSystem()
    system.update_config(smtp_server, smtp_port, sender_email, sender_password, recipient_email)
    return True

def send_monthly_audit_report(wipe_history):
    """Send monthly audit report"""
    system = EmailReportSystem()
    return system.send_monthly_report(wipe_history)
