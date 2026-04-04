# 🚀 3 NEW FEATURE IMPLEMENTATIONS

## ✨ Features to Add:
1. ⏱️ **Estimated Time Calculator** - Smart time prediction
2. 💡 **Algorithm Recommendation System** - File/storage based suggestions  
3. 📜 **Certificate Download Button** - After wipe completion

---

## 📝 **IMPLEMENTATION CODE SNIPPETS**

### **Feature 1: Estimated Time Calculator**

Add this function to `SecureWipeApp` class:

```python
def calculate_estimated_time(self, file_size_mb, algorithm):
    """
    Calculate estimated wipe time
    
    Based on:
    - HDD: ~80 MB/s write speed
    - SSD: ~300 MB/s write speed  
    - Conservative estimate: 80 MB/s average
    """
    base_speed_mbs = 80  # MB per second
    
    # Algorithm pass counts
    passes = {
        'simple': 1,
        'dod': 3,
        'nist': 1,
        'gutmann': 7,
        'crypto': 1
    }
    
    pass_count = passes.get(algorithm, 3)
    
    # Time = (file_size * passes) / speed
    estimated_seconds = (file_size_mb * pass_count) / base_speed_mbs
    
    # Add overhead
    estimated_seconds += 2
    
    return max(1, estimated_seconds)

def format_time(self, seconds):
    """Format seconds to readable time"""
    if seconds < 60:
        return f"~{int(seconds)} sec"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"~{minutes} min {secs} sec"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"~{hours} hr {minutes} min"
```

**Update `start_wipe()` function:**

```python
def start_wipe(self):
    """Start the wiping operation"""
    file_path = self.file_input.text().strip()
    
    if not file_path or not os.path.exists(file_path):
        # ... validation code ...
        return
    
    # ===== NEW: Calculate estimated time =====
    try:
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        algorithm_key = self.algo_combo.currentData()
        estimated_seconds = self.calculate_estimated_time(file_size_mb, algorithm_key)
        time_str = self.format_time(estimated_seconds)
        
    except:
        file_size_mb = 0
        time_str = "~0 sec"
    # =========================================
    
    # Updated confirmation dialog
    file_name = Path(file_path).name
    reply = QMessageBox.question(
        self,
        "Confirm Secure Wipe",
        f"📁 File: {file_name}\n"
        f"📊 Size: {file_size_mb:.2f} MB\n"
        f"⏱️ Estimated Time: {time_str}\n\n"
        f"⚠️ This action is IRREVERSIBLE.\n"
        f"Proceed?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    
    if reply != QMessageBox.StandardButton.Yes:
        return
    
    # Show estimated time in status
    self.status_label.setText(f"Starting wipe... Est. time: {time_str}")
    
    # ... rest of code ...
```

---

### **Feature 2: Smart Algorithm Recommendation**

Add this function:

```python
def get_algorithm_recommendation(self, file_path):
    """
    Recommend best algorithm based on:
    - File type
    - Storage device (SSD vs HDD)
    - File size
    """
    
    # Get file extension
    ext = Path(file_path).suffix.lower()
    
    # Get file size
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    except:
        file_size_mb = 0
    
    # Check if on SSD (basic check - can be enhanced)
    drive = Path(file_path).drive or "C:"
    is_ssd = self.is_ssd_drive(drive)
    
    # Recommendation logic
    recommendations = []
    
    # SSD Detection
    if is_ssd:
        recommendations.append({
            'algorithm': 'nist',
            'reason': '🔥 SSD Detected - NIST SP 800-88 recommended (optimized for SSDs)',
            'priority': 10
        })
    
    # Large files
    if file_size_mb > 1000:  # > 1 GB
        recommendations.append({
            'algorithm': 'simple',
            'reason': f'⚡ Large File ({file_size_mb:.0f} MB) - Single Pass for speed',
            'priority': 8
        })
    
    # Sensitive document types
    sensitive_exts = ['.pdf', '.docx', '.xlsx', '.txt', '.csv', '.doc', '.xls']
    if ext in sensitive_exts:
        recommendations.append({
            'algorithm': 'dod',
            'reason': '🔒 Document File - DoD 5220.22-M recommended (3 passes)',
            'priority': 9
        })
    
    # Media files (less sensitive)
    media_exts = ['.mp4', '.avi', '.mkv', '.mp3', '.wav', '.jpg', '.png', '.gif']
    if ext in media_exts:
        recommendations.append({
            'algorithm': 'simple',
            'reason': '🎬 Media File - Single Pass sufficient',
            'priority': 7
        })
    
    # Encrypted files
    encrypted_exts = ['.gpg', '.aes', '.encrypted', '.7z', '.zip']
    if ext in encrypted_exts or 'encrypt' in file_path.lower():
        recommendations.append({
            'algorithm': 'crypto',
            'reason': '🔐 Encrypted File - Cryptographic Erase recommended',
            'priority': 10
        })
    
    # Sort by priority
    recommendations.sort(key=lambda x: x['priority'], reverse=True)
    
    # Return top recommendation or default
    if recommendations:
        return recommendations[0]
    else:
        return {
            'algorithm': 'dod',
            'reason': '🛡️ Default - DoD 5220.22-M (balanced security)',
            'priority': 5
        }

def is_ssd_drive(self, drive_letter):
    """
    Check if drive is SSD (Windows only)
    Basic implementation - can be enhanced
    """
    try:
        import subprocess
        result = subprocess.run(
            ['powershell', '-Command', 
             f'Get-PhysicalDisk | Where-Object {{$_.DeviceID -eq 0}} | Select-Object MediaType'],
            capture_output=True,
            text=True
        )
        return 'SSD' in result.stdout
    except:
        return False  # Assume HDD if can't detect
```

**Add recommendation display in UI:**

```python
def select_file(self):
    """Open file selection dialog"""
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Select File to Wipe",
        "",
        "All Files (*.*)"
    )
    
    if file_path:
        self.file_input.setText(file_path)
        
        # ===== NEW: Show recommendation =====
        recommendation = self.get_algorithm_recommendation(file_path)
        
        # Find and select recommended algorithm
        for i in range(self.algo_combo.count()):
            if self.algo_combo.itemData(i) == recommendation['algorithm']:
                self.algo_combo.setCurrentIndex(i)
                break
        
        # Show recommendation message
        QMessageBox.information(
            self,
            "Algorithm Recommendation",
            f"💡 Smart Recommendation:\n\n"
            f"{recommendation['reason']}\n\n"
            f"You can change the algorithm if needed."
        )
        # ====================================
```

---

### **Feature 3: Certificate Download Button**

**Update `wipe_finished()` to store certificate path:**

```python
def wipe_finished(self, success, message):
    """Handle wipe completion"""
    # ... existing code ...
    
    if success:
        # Generate certificate
        certificate_path = None
        if CERTIFICATES_ENABLED:
            try:
                certificate_path = generate_wipe_certificate(...)
                
                # ===== NEW: Store for download button =====
                self.last_certificate_path = certificate_path
                # =========================================
                
            except Exception as e:
                print(f"Certificate error: {e}")
        
        # ... rest of code ...
        
        # ===== NEW: Show custom success dialog with certificate button =====
        self.show_success_dialog_with_certificate(message, certificate_path)
        # ==================================================================

def show_success_dialog_with_certificate(self, message, cert_path):
    """Show success dialog with certificate download button"""
    from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
    
    dialog = QDialog(self)
    dialog.setWindowTitle("Wipe Successful")
    dialog.setMinimumWidth(400)
    
    layout = QVBoxLayout()
    
    # Success message
    success_label = QLabel(f"✅ {message}\n\nFile has been securely wiped and deleted.")
    success_label.setWordWrap(True)
    layout.addWidget(success_label)
    
    # Certificate info
    if cert_path:
        cert_label = QLabel(f"\n📜 Certificate Generated:\n{Path(cert_path).name}")
        cert_label.setStyleSheet("color: #2ecc71; font-weight: 600;")
        layout.addWidget(cert_label)
    
    # Buttons
    button_layout = QHBoxLayout()
    
    if cert_path:
        # Download/Open Certificate Button
        cert_btn = QPushButton("📥 Download Certificate")
        cert_btn.setObjectName("primary-btn")
        cert_btn.clicked.connect(lambda: self.download_certificate(cert_path))
        button_layout.addWidget(cert_btn)
        
        # Open Folder Button
        folder_btn = QPushButton("📂 Open Folder")
        folder_btn.setObjectName("secondary-btn")
        folder_btn.clicked.connect(lambda: self.open_certificate_folder(cert_path))
        button_layout.addWidget(folder_btn)
    
    # Close Button
    close_btn = QPushButton("Close")
    close_btn.setObjectName("secondary-btn")
    close_btn.clicked.connect(dialog.accept)
    button_layout.addWidget(close_btn)
    
    layout.addLayout(button_layout)
    dialog.setLayout(layout)
    
    dialog.exec()

def download_certificate(self, cert_path):
    """Copy certificate to user-selected location"""
    save_path, _ = QFileDialog.getSaveFileName(
        self,
        "Save Certificate",
        Path(cert_path).name,
        "PDF Files (*.pdf)"
    )
    
    if save_path:
        try:
            import shutil
            shutil.copy2(cert_path, save_path)
            QMessageBox.information(
                self,
                "Certificate Saved",
                f"✅ Certificate saved to:\n{save_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save Failed",
                f"❌ Error saving certificate:\n{str(e)}"
            )

def open_certificate_folder(self, cert_path):
    """Open folder containing the certificate"""
    import subprocess
    folder = str(Path(cert_path).parent)
    
    try:
        if sys.platform == 'win32':
            subprocess.run(['explorer', folder])
        elif sys.platform == 'darwin':
            subprocess.run(['open', folder])
        else:
            subprocess.run(['xdg-open', folder])
    except Exception as e:
        QMessageBox.warning(
            self,
            "Cannot Open",
            f"Could not open folder:\n{str(e)}"
        )
```

---

## 📊 **ALGORITHM RECOMMENDATION TABLE**

| File Type | Size | Storage | Recommended Algorithm | Reason |
|-----------|------|---------|----------------------|---------|
| Documents (.pdf, .docx) | Any | Any | DoD 5220.22-M | Sensitive data, 3 passes |
| Media (.mp4, .jpg) | Any | Any | Single Pass | Less sensitive, speed priority |
| Any | > 1 GB | HDD | Single Pass | Large file, speed priority |
| Any | < 1 GB | SSD | NIST SP 800-88 | SSD optimized |
| Encrypted (.gpg, .aes) | Any | Any | Cryptographic Erase | Pre-encrypted |
| System Files | < 100 MB | Any | DoD 5220.22-M | Security priority |
| Temp Files | Any | Any | Single Pass | Fast cleanup |

---

## 🎯 **TIME ESTIMATION TABLE**

### **File Size Examples:**

| File Size | Algorithm | Estimated Time |
|-----------|-----------|----------------|
| 10 MB | Single Pass | ~1 sec |
| 10 MB | DoD (3 pass) | ~2 sec |
| 10 MB | Gutmann (7 pass) | ~5 sec |
| 100 MB | Single Pass | ~2 sec |
| 100 MB | DoD (3 pass) | ~4 sec |
| 100 MB | Gutmann (7 pass) | ~10 sec |
| 1 GB | Single Pass | ~13 sec |
| 1 GB | DoD (3 pass) | ~40 sec |
| 1 GB | Gutmann (7 pass) | ~90 sec |
| 10 GB | Single Pass | ~2 min |
| 10 GB | DoD (3 pass) | ~6 min |
| 10 GB | Gutmann (7 pass) | ~15 min |

**Formula:** `Time = (Size_MB × Passes) / 80 + 2 seconds`

---

## ✅ **TESTING CHECKLIST**

### **Test Estimated Time:**
- [ ] Small file (10 MB) - shows seconds
- [ ] Medium file (100 MB) - shows seconds/minutes
- [ ] Large file (1 GB+) - shows minutes
- [ ] Very large (10 GB+) - shows hours/minutes
- [ ] Time shown in confirmation dialog
- [ ] Time shown in status label

### **Test Algorithm Recommendation:**
- [ ] PDF file → Recommends DoD
- [ ] Image file → Recommends Single Pass
- [ ] Large file (>1 GB) → Recommends Single Pass
- [ ] Encrypted file → Recommends Crypto
- [ ] SSD detection (if possible)
- [ ] Recommendation shown after file selection

### **Test Certificate Download:**
- [ ] Certificate generated after wipe
- [ ] Custom success dialog appears
- [ ] "Download Certificate" button works
- [ ] "Open Folder" button works
- [ ] Certificate saves to selected location
- [ ] Folder opens correctly

---

## 🚀 **QUICK IMPLEMENTATION GUIDE**

### **Step 1: Add Functions**
Copy these functions into `SecureWipeApp` class:
- `calculate_estimated_time()`
- `format_time()`
- `get_algorithm_recommendation()`
- `is_ssd_drive()`
- `show_success_dialog_with_certificate()`
- `download_certificate()`
- `open_certificate_folder()`

### **Step 2: Update Existing Functions**
Modify:
- `select_file()` - Add recommendation logic
- `start_wipe()` - Add time calculation
- `wipe_finished()` - Add certificate dialog

### **Step 3: Test**
Run app and test all 3 features!

---

## 💡 **USER EXPERIENCE FLOW**

```
1. User clicks "Browse"
   ↓
2. Selects file (test.pdf, 50 MB)
   ↓
3. Popup: "💡 Document File - DoD 5220.22-M recommended"
   ↓
4. Algorithm auto-selected
   ↓
5. User clicks "START SECURE WIPE"
   ↓
6. Confirmation:
   "File: test.pdf
    Size: 50 MB
    Est. Time: ~2 min
    Proceed?"
   ↓
7. Wipe starts
   Status: "Starting wipe... Est. time: ~2 min"
   ↓
8. Wipe completes
   ↓
9. Custom dialog appears:
   "✅ Wipe successful!
    📜 Certificate: wipe_cert_ABC123.pdf
    
    [📥 Download Certificate] [📂 Open Folder] [Close]"
   ↓
10. User clicks "Download Certificate"
    ↓
11. Save dialog opens
    ↓
12. Certificate saved to Downloads/
    ↓
13. Success message: "Certificate saved!"
```

---

**Ready to implement? Copy code snippets into your app!** 🚀
