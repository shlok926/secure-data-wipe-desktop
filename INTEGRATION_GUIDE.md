# 🔌 FEATURE MODULES INTEGRATION GUIDE

## 📦 New Modular Files Created:

1. **time_estimator.py** - Time calculation module
2. **algorithm_recommender.py** - Smart algorithm recommendations
3. **certificate_ui.py** - Certificate download UI

---

## 🚀 HOW TO USE THESE MODULES

### **Step 1: Copy Files to Your Project**

```
Your Project Folder:
├── secure_wipe_desktop.py
├── wiper_core.py
├── time_estimator.py           ← NEW
├── algorithm_recommender.py    ← NEW
├── certificate_ui.py            ← NEW
├── certificate_generator.py
├── email_system.py
├── history_manager.py
```

---

## ⏱️ **Feature 1: Time Estimation**

### **Import:**
```python
from time_estimator import WipeTimeEstimator, estimate_wipe_time
```

### **Usage in secure_wipe_desktop.py:**

```python
class SecureWipeApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # ... existing code ...
        
        # Initialize time estimator
        self.time_estimator = WipeTimeEstimator()
    
    def start_wipe(self):
        """Start the wiping operation"""
        file_path = self.file_input.text().strip()
        
        if not file_path or not os.path.exists(file_path):
            # validation...
            return
        
        # ===== USE TIME ESTIMATOR =====
        try:
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            algorithm_key = self.algo_combo.currentData()
            
            # Calculate time
            estimated_seconds = self.time_estimator.calculate_time(
                file_size_mb, 
                algorithm_key
            )
            time_str = self.time_estimator.format_time(estimated_seconds)
            
        except:
            time_str = "~0 sec"
        # ==============================
        
        # Show in confirmation dialog
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
        
        # Update status with time
        self.status_label.setText(f"Starting wipe... Est: {time_str}")
        
        # ... rest of wipe code ...
```

### **Quick Function:**
```python
# Quick time estimate
time_str = estimate_wipe_time(file_size_mb=100, algorithm='dod')
# Returns: "~4 sec"
```

---

## 💡 **Feature 2: Algorithm Recommendation**

### **Import:**
```python
from algorithm_recommender import AlgorithmRecommender, get_recommendation
```

### **Usage in secure_wipe_desktop.py:**

```python
class SecureWipeApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # ... existing code ...
        
        # Initialize recommender
        self.recommender = AlgorithmRecommender()
    
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
            
            # ===== USE RECOMMENDER =====
            recommendation = self.recommender.recommend(file_path)
            
            # Auto-select recommended algorithm
            for i in range(self.algo_combo.count()):
                if self.algo_combo.itemData(i) == recommendation['algorithm']:
                    self.algo_combo.setCurrentIndex(i)
                    break
            
            # Show recommendation to user
            QMessageBox.information(
                self,
                "💡 Smart Recommendation",
                f"{recommendation['reason']}\n\n"
                f"Category: {recommendation['category']}\n\n"
                f"You can change the algorithm if needed."
            )
            # ===========================
```

### **Quick Function:**
```python
# Quick recommendation
rec = get_recommendation("important_document.pdf")
# Returns: {'algorithm': 'dod', 'reason': '🔒 Sensitive Document...', ...}
```

---

## 📜 **Feature 3: Certificate Download UI**

### **Import:**
```python
from certificate_ui import CertificateManager, show_certificate_dialog
```

### **Usage in secure_wipe_desktop.py:**

```python
def wipe_finished(self, success, message):
    """Handle wipe completion"""
    # ... existing code ...
    
    if success:
        # Generate certificate
        certificate_path = None
        if CERTIFICATES_ENABLED:
            try:
                certificate_path = generate_wipe_certificate(
                    file_path=file_path,
                    file_size=file_size,
                    algorithm=algorithm,
                    timestamp=datetime.now(),
                    success=True
                )
            except Exception as e:
                print(f"Certificate error: {e}")
        
        # ===== USE CERTIFICATE UI =====
        # Show custom dialog with certificate actions
        show_certificate_dialog(
            parent=self,
            message=message,
            cert_path=certificate_path
        )
        # ==============================
        
        # Update dashboard
        self.update_dashboard_stats()
        
        # Clear input
        self.file_input.clear()
```

### **Alternative - Quick Save:**
```python
from certificate_ui import save_certificate_quick

# Quick save to Downloads folder
if certificate_path:
    save_certificate_quick(self, certificate_path)
```

---

## 🔗 **Complete Integration Example**

### **Add to imports at top of secure_wipe_desktop.py:**

```python
# Add these imports
try:
    from time_estimator import WipeTimeEstimator
    TIME_ESTIMATION_ENABLED = True
except ImportError:
    TIME_ESTIMATION_ENABLED = False

try:
    from algorithm_recommender import AlgorithmRecommender
    RECOMMENDATION_ENABLED = True
except ImportError:
    RECOMMENDATION_ENABLED = False

try:
    from certificate_ui import show_certificate_dialog
    CERTIFICATE_UI_ENABLED = True
except ImportError:
    CERTIFICATE_UI_ENABLED = False
```

### **Initialize in __init__:**

```python
def __init__(self):
    super().__init__()
    
    # ... existing initializations ...
    
    # Initialize new features
    if TIME_ESTIMATION_ENABLED:
        self.time_estimator = WipeTimeEstimator()
    
    if RECOMMENDATION_ENABLED:
        self.recommender = AlgorithmRecommender()
    
    # ... rest of init ...
```

### **Use in select_file:**

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
        
        # Get recommendation
        if RECOMMENDATION_ENABLED:
            recommendation = self.recommender.recommend(file_path)
            
            # Auto-select
            for i in range(self.algo_combo.count()):
                if self.algo_combo.itemData(i) == recommendation['algorithm']:
                    self.algo_combo.setCurrentIndex(i)
                    break
            
            # Show popup
            QMessageBox.information(
                self,
                "💡 Smart Recommendation",
                recommendation['reason']
            )
```

### **Use in start_wipe:**

```python
def start_wipe(self):
    """Start the wiping operation"""
    file_path = self.file_input.text().strip()
    
    # ... validation ...
    
    # Calculate time
    time_str = "~0 sec"
    if TIME_ESTIMATION_ENABLED:
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            algorithm_key = self.algo_combo.currentData()
            
            seconds = self.time_estimator.calculate_time(file_size_mb, algorithm_key)
            time_str = self.time_estimator.format_time(seconds)
        except:
            pass
    
    # Show in confirmation
    reply = QMessageBox.question(
        self,
        "Confirm Secure Wipe",
        f"📁 File: {Path(file_path).name}\n"
        f"⏱️ Estimated Time: {time_str}\n\n"
        f"Proceed?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    
    # ... rest of wipe code ...
```

### **Use in wipe_finished:**

```python
def wipe_finished(self, success, message):
    """Handle wipe completion"""
    # ... existing code ...
    
    if success:
        certificate_path = None
        
        # Generate certificate
        if CERTIFICATES_ENABLED:
            try:
                certificate_path = generate_wipe_certificate(...)
            except:
                pass
        
        # Show certificate dialog
        if CERTIFICATE_UI_ENABLED and certificate_path:
            show_certificate_dialog(self, message, certificate_path)
        else:
            # Fallback to regular message
            QMessageBox.information(self, "Success", message)
        
        # Update dashboard
        self.update_dashboard_stats()
```

---

## ✅ **Testing Checklist**

### **Test Time Estimation:**
- [ ] Small file (10 MB) shows seconds
- [ ] Large file (1 GB) shows minutes
- [ ] Time shown in confirmation dialog
- [ ] Different algorithms show different times

### **Test Recommendations:**
- [ ] PDF file → Recommends DoD
- [ ] MP4 file → Recommends Single Pass
- [ ] Large file → Recommends Single Pass
- [ ] Small file → May recommend Gutmann
- [ ] Algorithm auto-selected after file selection

### **Test Certificate UI:**
- [ ] Custom dialog appears after wipe
- [ ] "Download Certificate" button works
- [ ] "Open Folder" button opens folder
- [ ] "View" button opens PDF
- [ ] Certificate saves to chosen location

---

## 🎯 **Benefits of Modular Approach:**

✅ **Clean Code** - Separated concerns
✅ **Easy Testing** - Test modules independently
✅ **Reusable** - Use in other projects
✅ **Maintainable** - Easy to update
✅ **Optional** - Can enable/disable features
✅ **No Breaking Changes** - Graceful fallbacks

---

## 🐛 **Troubleshooting:**

### **Import Error:**
```python
# Add error handling
try:
    from time_estimator import WipeTimeEstimator
    time_est = WipeTimeEstimator()
except ImportError:
    print("Time estimation module not found")
    time_est = None
```

### **Module Not Found:**
- Check file is in same directory
- Check filename matches exactly
- Check for typos in import statement

### **Feature Not Working:**
- Check if module imported successfully
- Check if feature is enabled (flags)
- Check console for error messages

---

## 📝 **Quick Reference:**

### **Time Estimator:**
```python
estimator = WipeTimeEstimator()
seconds = estimator.calculate_time(file_size_mb, algorithm)
formatted = estimator.format_time(seconds)
```

### **Algorithm Recommender:**
```python
recommender = AlgorithmRecommender()
rec = recommender.recommend(file_path)
algorithm = rec['algorithm']
reason = rec['reason']
```

### **Certificate UI:**
```python
show_certificate_dialog(parent, message, cert_path)
# or
save_certificate_quick(parent, cert_path)
```

---

## 🚀 **You're Ready!**

1. Copy 3 new modules to project folder
2. Add imports to secure_wipe_desktop.py
3. Initialize in __init__
4. Use in appropriate functions
5. Test all features!

**All modules work independently - can enable/disable as needed!** 💪
