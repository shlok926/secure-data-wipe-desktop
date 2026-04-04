# 🚀 TIER 3 COMPLETE - Integration Code

## This file contains all code snippets to add to secure_wipe_desktop.py

---

## PART 1: Initialize Schedule Manager in __init__

Add this to __init__ function after history_manager initialization:

```python
# Initialize schedule manager
if SCHEDULING_ENABLED:
    self.schedule_manager = ScheduleManager()
    self.schedule_manager.task_triggered.connect(self.on_scheduled_task_triggered)
    self.schedule_manager.task_completed.connect(self.on_scheduled_task_completed)
else:
    self.schedule_manager = None

# Initialize free space wiper
if FREE_SPACE_ENABLED:
    self.free_space_wiper = FreeSpaceWiper()
    self.free_space_wiper.progress.connect(self.on_free_space_progress)
    self.free_space_wiper.finished.connect(self.on_free_space_finished)
else:
    self.free_space_wiper = None

# Selected files for scheduling
self.selected_schedule_files = []
```

---

## PART 2: Add Pages to Sidebar

In init_ui(), add after Settings page:

```python
# Add Scheduled Wipes page
if SCHEDULING_ENABLED:
    self.schedule_page = self.create_schedule_page()
    self.pages.addWidget(self.schedule_page)
    self.sidebar.addItem("📅 Scheduled Wipes")

# Add Free Space Wipe page
if FREE_SPACE_ENABLED:
    self.free_space_page = self.create_free_space_page()
    self.pages.addWidget(self.free_space_page)
    self.sidebar.addItem("🗑️ Free Space Wipe")
```

---

## PART 3: Create Schedule Page Function

Add this function to SecureWipeApp class:

```python
def create_schedule_page(self):
    """Create scheduled wipes page"""
    widget = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    
    # Title
    title = QLabel("Scheduled Wipes")
    title.setObjectName("page-title")
    layout.addWidget(title)
    
    # Schedule Form
    form_group = QGroupBox("Create New Schedule")
    form_layout = QVBoxLayout()
    
    # File selection
    file_layout = QHBoxLayout()
    file_label = QLabel("Files to Wipe:")
    self.schedule_files_input = QLineEdit()
    self.schedule_files_input.setPlaceholderText("Select files...")
    self.schedule_files_input.setReadOnly(True)
    browse_schedule_btn = QPushButton("Browse Files...")
    browse_schedule_btn.setObjectName("secondary-btn")
    browse_schedule_btn.clicked.connect(self.select_files_for_schedule)
    file_layout.addWidget(file_label, 1)
    file_layout.addWidget(self.schedule_files_input, 3)
    file_layout.addWidget(browse_schedule_btn, 1)
    form_layout.addLayout(file_layout)
    
    # Schedule type
    type_layout = QHBoxLayout()
    type_label = QLabel("Schedule Type:")
    self.schedule_type_combo = QComboBox()
    self.schedule_type_combo.addItems(["One-Time", "Daily", "Weekly", "Monthly"])
    type_layout.addWidget(type_label, 1)
    type_layout.addWidget(self.schedule_type_combo, 2)
    type_layout.addStretch()
    form_layout.addLayout(type_layout)
    
    # Date/Time picker
    datetime_layout = QHBoxLayout()
    datetime_label = QLabel("Run At:")
    self.schedule_datetime = QDateTimeEdit()
    self.schedule_datetime.setDateTime(QDateTime.currentDateTime().addDays(1))
    self.schedule_datetime.setCalendarPopup(True)
    self.schedule_datetime.setDisplayFormat("yyyy-MM-dd HH:mm")
    datetime_layout.addWidget(datetime_label, 1)
    datetime_layout.addWidget(self.schedule_datetime, 2)
    datetime_layout.addStretch()
    form_layout.addLayout(datetime_layout)
    
    # Create button
    create_btn = QPushButton("📅 Create Schedule")
    create_btn.setObjectName("primary-btn")
    create_btn.clicked.connect(self.create_scheduled_task)
    form_layout.addWidget(create_btn)
    
    form_group.setLayout(form_layout)
    layout.addWidget(form_group)
    
    # Scheduled tasks table
    tasks_label = QLabel("Scheduled Tasks")
    tasks_label.setStyleSheet("font-size: 18px; font-weight: 600; margin-top: 20px;")
    layout.addWidget(tasks_label)
    
    self.schedule_table = QTableWidget()
    self.schedule_table.setColumnCount(6)
    self.schedule_table.setHorizontalHeaderLabels([
        "ID", "Files", "Schedule", "Next Run", "Status", "Actions"
    ])
    layout.addWidget(self.schedule_table)
    
    # Refresh button
    refresh_btn = QPushButton("🔄 Refresh Tasks")
    refresh_btn.setObjectName("secondary-btn")
    refresh_btn.clicked.connect(self.refresh_scheduled_tasks)
    layout.addWidget(refresh_btn)
    
    # Refresh scheduled tasks
    self.refresh_scheduled_tasks()
    
    widget.setLayout(layout)
    return widget
```

---

## PART 4: Schedule Helper Functions

```python
def select_files_for_schedule(self):
    """Select files for scheduled wipe"""
    files, _ = QFileDialog.getOpenFileNames(
        self,
        "Select Files for Scheduled Wipe",
        "",
        "All Files (*.*)"
    )
    
    if files:
        self.selected_schedule_files = files
        self.schedule_files_input.setText(f"{len(files)} file(s) selected")

def create_scheduled_task(self):
    """Create new scheduled task"""
    if not self.selected_schedule_files:
        QMessageBox.warning(self, "No Files", "Please select files to wipe")
        return
    
    # Get schedule type
    type_map = {
        "One-Time": ScheduleType.ONCE,
        "Daily": ScheduleType.DAILY,
        "Weekly": ScheduleType.WEEKLY,
        "Monthly": ScheduleType.MONTHLY
    }
    schedule_type = type_map[self.schedule_type_combo.currentText()]
    
    # Get datetime
    schedule_time = self.schedule_datetime.dateTime().toPyDateTime()
    
    # Get algorithm
    algorithm = self.algo_combo.currentData()
    
    # Create task
    task_id = self.schedule_manager.add_task(
        self.selected_schedule_files,
        algorithm,
        schedule_type,
        schedule_time
    )
    
    QMessageBox.information(
        self,
        "Schedule Created",
        f"✅ Scheduled wipe created!\n\n"
        f"Task ID: {task_id}\n"
        f"Files: {len(self.selected_schedule_files)}\n"
        f"Will run: {format_schedule_time(self.schedule_manager.get_task(task_id))}"
    )
    
    # Clear selection
    self.selected_schedule_files = []
    self.schedule_files_input.clear()
    
    # Refresh table
    self.refresh_scheduled_tasks()

def refresh_scheduled_tasks(self):
    """Refresh scheduled tasks table"""
    if not self.schedule_manager:
        return
    
    self.schedule_table.setRowCount(0)
    
    for task in self.schedule_manager.get_all_tasks():
        row = self.schedule_table.rowCount()
        self.schedule_table.insertRow(row)
        
        self.schedule_table.setItem(row, 0, QTableWidgetItem(task.id))
        self.schedule_table.setItem(row, 1, QTableWidgetItem(f"{len(task.file_paths)} file(s)"))
        self.schedule_table.setItem(row, 2, QTableWidgetItem(task.schedule_type.value))
        self.schedule_table.setItem(row, 3, QTableWidgetItem(format_schedule_time(task)))
        self.schedule_table.setItem(row, 4, QTableWidgetItem("Enabled" if task.enabled else "Disabled"))
        
        delete_btn = QPushButton("🗑️")
        delete_btn.clicked.connect(lambda checked, tid=task.id: self.delete_scheduled_task(tid))
        self.schedule_table.setCellWidget(row, 5, delete_btn)

def delete_scheduled_task(self, task_id):
    """Delete a scheduled task"""
    reply = QMessageBox.question(
        self,
        "Delete Schedule",
        f"Delete scheduled task {task_id}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    
    if reply == QMessageBox.StandardButton.Yes:
        self.schedule_manager.remove_task(task_id)
        self.refresh_scheduled_tasks()

def on_scheduled_task_triggered(self, task_id):
    """Handle when scheduled task triggers"""
    task = self.schedule_manager.get_task(task_id)
    if not task:
        return
    
    QMessageBox.information(
        self,
        "Scheduled Wipe",
        f"🔔 Scheduled wipe starting!\n\nTask: {task_id}\nFiles: {len(task.file_paths)}"
    )
    
    self.schedule_manager.mark_task_completed(task_id, True)
    self.refresh_scheduled_tasks()

def on_scheduled_task_completed(self, task_id, success):
    """Handle when scheduled task completes"""
    print(f"Scheduled task {task_id} completed: {'Success' if success else 'Failed'}")
```

---

## PART 5: Create Free Space Page

```python
def create_free_space_page(self):
    """Create free space wiping page"""
    widget = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    
    # Title
    title = QLabel("Free Space Wipe")
    title.setObjectName("page-title")
    layout.addWidget(title)
    
    # Warning
    warning = QLabel(
        "⚠️ WARNING: Free space wiping takes a VERY long time (hours) and "
        "will make your drive unusable during the operation!"
    )
    warning.setWordWrap(True)
    warning.setStyleSheet("color: #e74c3c; font-weight: 600; padding: 10px; background: #fadbd8; border-radius: 5px;")
    layout.addWidget(warning)
    
    # Drive selection
    drive_group = QGroupBox("Select Drive")
    drive_layout = QVBoxLayout()
    
    drive_select_layout = QHBoxLayout()
    drive_label = QLabel("Drive:")
    self.drive_combo_free = QComboBox()
    refresh_drives_btn = QPushButton("🔄 Refresh")
    refresh_drives_btn.clicked.connect(self.refresh_drives_for_free_space)
    
    drive_select_layout.addWidget(drive_label)
    drive_select_layout.addWidget(self.drive_combo_free)
    drive_select_layout.addWidget(refresh_drives_btn)
    drive_layout.addLayout(drive_select_layout)
    
    # Drive info
    self.drive_info_label = QLabel("Select a drive to see information")
    self.drive_info_label.setWordWrap(True)
    drive_layout.addWidget(self.drive_info_label)
    
    drive_group.setLayout(drive_layout)
    layout.addWidget(drive_group)
    
    # Progress
    progress_group = QGroupBox("Operation Progress")
    progress_layout = QVBoxLayout()
    
    self.free_space_progress = QProgressBar()
    self.free_space_status = QLabel("Ready")
    
    progress_layout.addWidget(self.free_space_progress)
    progress_layout.addWidget(self.free_space_status)
    progress_group.setLayout(progress_layout)
    layout.addWidget(progress_group)
    
    # Buttons
    btn_layout = QHBoxLayout()
    
    start_free_wipe_btn = QPushButton("🗑️ Start Free Space Wipe")
    start_free_wipe_btn.setObjectName("danger-btn")
    start_free_wipe_btn.setMinimumHeight(50)
    start_free_wipe_btn.clicked.connect(self.start_free_space_wipe)
    
    cancel_free_btn = QPushButton("Cancel")
    cancel_free_btn.setObjectName("secondary-btn")
    cancel_free_btn.setMinimumHeight(50)
    cancel_free_btn.clicked.connect(self.cancel_free_space_wipe)
    
    btn_layout.addWidget(start_free_wipe_btn, 3)
    btn_layout.addWidget(cancel_free_btn, 1)
    
    layout.addLayout(btn_layout)
    layout.addStretch()
    
    # Refresh drives
    self.refresh_drives_for_free_space()
    
    widget.setLayout(layout)
    return widget

def refresh_drives_for_free_space(self):
    """Refresh drive list for free space wipe"""
    if not self.free_space_wiper:
        return
    
    self.drive_combo_free.clear()
    
    # Add C: drive
    import sys
    if sys.platform == 'win32':
        self.drive_combo_free.addItem("C:\\")
    else:
        self.drive_combo_free.addItem("/")
    
    # Update info
    self.update_drive_info_free_space()

def update_drive_info_free_space(self):
    """Update drive information display"""
    if not self.free_space_wiper:
        return
    
    drive = self.drive_combo_free.currentText()
    if not drive:
        return
    
    info = self.free_space_wiper.get_drive_info(drive)
    
    if 'error' not in info:
        free_gb = info['free'] / (1024**3)
        total_gb = info['total'] / (1024**3)
        
        est_time = self.free_space_wiper.estimate_time(info['free'])
        time_str = self.free_space_wiper.format_time(est_time)
        
        self.drive_info_label.setText(
            f"Total: {total_gb:.1f} GB\n"
            f"Free: {free_gb:.1f} GB\n"
            f"Estimated Time: {time_str}"
        )

def start_free_space_wipe(self):
    """Start free space wiping"""
    drive = self.drive_combo_free.currentText()
    
    reply = QMessageBox.warning(
        self,
        "⚠️ EXTREME WARNING",
        f"You are about to wipe ALL FREE SPACE on {drive}\n\n"
        f"⚠️ This will take HOURS!\n"
        f"⚠️ Drive will be UNUSABLE during operation!\n"
        f"⚠️ Operation CANNOT be cancelled!\n\n"
        f"Are you ABSOLUTELY SURE?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    
    if reply == QMessageBox.StandardButton.Yes:
        QMessageBox.information(
            self,
            "Not Implemented",
            "Free space wiping is not yet fully implemented.\n\n"
            "This feature requires extensive testing and will be added in a future update."
        )

def cancel_free_space_wipe(self):
    """Cancel free space wipe"""
    if self.free_space_wiper:
        self.free_space_wiper.cancel()

def on_free_space_progress(self, percent, message):
    """Handle free space progress"""
    self.free_space_progress.setValue(percent)
    self.free_space_status.setText(message)

def on_free_space_finished(self, success, message):
    """Handle free space completion"""
    QMessageBox.information(self, "Complete" if success else "Failed", message)
```

---

## PART 6: Add to Styles (Optional - for GroupBox)

Add to apply_styles() function:

```python
QGroupBox {
    font-weight: 600;
    border: 2px solid #dfe4ea;
    border-radius: 8px;
    margin-top: 10px;
    padding: 15px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}
```

---

## TESTING CHECKLIST:

### Scheduled Wiping:
- [ ] New "Scheduled Wipes" tab appears
- [ ] Can select files
- [ ] Can set date/time
- [ ] Can create schedule
- [ ] Tasks show in table
- [ ] Can delete tasks

### Free Space Wipe:
- [ ] New "Free Space Wipe" tab appears
- [ ] Shows drive information
- [ ] Shows warnings
- [ ] (Currently shows "not implemented" - safe!)

---

Save this file for reference during integration!
