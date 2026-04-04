"""
Scheduled Wiping Module for Secure Wipe
Schedule wipes for specific times, dates, or recurring intervals
"""

from datetime import datetime, timedelta
from enum import Enum
import json
import os
from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class ScheduleType(Enum):
    """Types of schedules"""
    ONCE = "once"           # One-time at specific date/time
    DAILY = "daily"         # Every day at specific time
    WEEKLY = "weekly"       # Every week on specific day
    MONTHLY = "monthly"     # Every month on specific day


class ScheduledTask:
    """A scheduled wipe task"""
    
    def __init__(self, task_id, file_paths, algorithm, schedule_type, schedule_time):
        self.id = task_id
        self.file_paths = file_paths  # List of files to wipe
        self.algorithm = algorithm
        self.schedule_type = schedule_type
        self.schedule_time = schedule_time  # datetime object
        self.created_time = datetime.now()
        self.last_run = None
        self.next_run = schedule_time
        self.enabled = True
        self.run_count = 0
    
    def should_run_now(self):
        """Check if task should run now with 5-second buffer for accuracy"""
        if not self.enabled:
            return False
        
        now = datetime.now()
        
        if self.next_run:
            # Allow 5-second buffer to catch scheduled times
            # (handles cases where check happens a few seconds after scheduled time)
            time_buffer = timedelta(seconds=5)
            if now >= self.next_run and now <= (self.next_run + time_buffer):
                return True
        
        return False
    
    def calculate_next_run(self):
        """Calculate next run time for recurring tasks"""
        if self.schedule_type == ScheduleType.ONCE:
            # One-time task - disable after running
            self.enabled = False
            self.next_run = None
        
        elif self.schedule_type == ScheduleType.DAILY:
            # Run tomorrow at same time
            self.next_run = self.next_run + timedelta(days=1)
        
        elif self.schedule_type == ScheduleType.WEEKLY:
            # Run next week
            self.next_run = self.next_run + timedelta(weeks=1)
        
        elif self.schedule_type == ScheduleType.MONTHLY:
            # Run next month (approximate - 30 days)
            self.next_run = self.next_run + timedelta(days=30)
    
    def mark_completed(self):
        """Mark task as completed"""
        self.last_run = datetime.now()
        self.run_count += 1
        self.calculate_next_run()
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'file_paths': self.file_paths,
            'algorithm': self.algorithm,
            'schedule_type': self.schedule_type.value,
            'schedule_time': self.schedule_time.isoformat() if self.schedule_time else None,
            'created_time': self.created_time.isoformat(),
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'enabled': self.enabled,
            'run_count': self.run_count
        }
    
    @staticmethod
    def from_dict(data):
        """Create task from dictionary"""
        task = ScheduledTask(
            data['id'],
            data['file_paths'],
            data['algorithm'],
            ScheduleType(data['schedule_type']),
            datetime.fromisoformat(data['schedule_time']) if data['schedule_time'] else None
        )
        task.created_time = datetime.fromisoformat(data['created_time'])
        task.last_run = datetime.fromisoformat(data['last_run']) if data['last_run'] else None
        task.next_run = datetime.fromisoformat(data['next_run']) if data['next_run'] else None
        task.enabled = data['enabled']
        task.run_count = data['run_count']
        return task


class ScheduleManager(QObject):
    """Manage scheduled wipe tasks"""
    
    # Signals
    task_triggered = pyqtSignal(str)  # task_id
    task_completed = pyqtSignal(str, bool)  # task_id, success
    
    def __init__(self, storage_file="data/scheduled_tasks.json"):
        super().__init__()
        
        self.storage_file = storage_file
        self.tasks = {}
        self.next_task_id = 1
        
        # Load tasks first
        self.load_tasks()
        
        # ⚠️ CRITICAL: Check for tasks immediately, don't wait
        QTimer.singleShot(0, self.check_tasks)
        
        # Timer to check tasks frequently (every 10 seconds for accuracy)
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_tasks)
        self.check_timer.start(10000)  # ✅ Check every 10 seconds (was 60!)
        
        print("[SCHEDULER] Started with check interval: 10 seconds")
    
    def add_task(self, file_paths_or_task, algorithm=None, schedule_type=None, schedule_time=None):
        """Add new scheduled task - supports both parameter-based and object-based calls"""
        # Check if first argument is a ScheduledTask object
        if isinstance(file_paths_or_task, ScheduledTask):
            # Object-based call
            task = file_paths_or_task
            self.tasks[task.id] = task
        else:
            # Parameter-based call
            task_id = f"task_{self.next_task_id}"
            self.next_task_id += 1
            
            task = ScheduledTask(
                task_id,
                file_paths_or_task,
                algorithm,
                schedule_type,
                schedule_time
            )
            
            self.tasks[task_id] = task
        
        self.save_tasks()
        return task.id
    
    def remove_task(self, task_id):
        """Remove a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False
    
    def get_task(self, task_id):
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self):
        """Get all tasks"""
        return list(self.tasks.values())
    
    def get_upcoming_tasks(self, count=10):
        """Get upcoming tasks sorted by next run time"""
        upcoming = [t for t in self.tasks.values() if t.enabled and t.next_run]
        upcoming.sort(key=lambda x: x.next_run)
        return upcoming[:count]
    
    def enable_task(self, task_id):
        """Enable a task"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True
            self.save_tasks()
    
    def disable_task(self, task_id):
        """Disable a task"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False
            self.save_tasks()
    
    def check_tasks(self):
        """Check if any tasks should run now"""
        now = datetime.now()
        has_tasks = len(self.tasks) > 0
        
        if has_tasks:
            # Debug logging
            print(f"\n[SCHEDULER CHECK] {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Total tasks: {len(self.tasks)}")
        
        for task in self.tasks.values():
            if task.next_run:
                time_until = (task.next_run - now).total_seconds()
                status = "🟢 ENABLED" if task.enabled else "🔴 DISABLED"
                print(f"  Task {task.id}: {task.next_run.strftime('%H:%M:%S')} ({time_until:.0f}s away) {status}")
            
            if task.should_run_now():
                print(f"  ⚡ TRIGGERED: {task.id}")
                self.task_triggered.emit(task.id)
    
    def check_missed_tasks(self):
        """Check for tasks that should have run while app was closed (CRITICAL!)"""
        missed_tasks = []
        now = datetime.now()
        
        for task in self.tasks.values():
            if not task.enabled:
                continue
                
            # Check if task was supposed to run but didn't
            if task.next_run and task.next_run <= now:
                # Task should have run!
                if task.schedule_type == ScheduleType.ONCE:
                    # One-time task that was missed
                    if task.last_run is None:
                        missed_tasks.append(task)
                else:
                    # Recurring task
                    missed_tasks.append(task)
        
        # Trigger all missed tasks
        for task in missed_tasks:
            print(f"[SCHEDULER] Running missed task: {task.id}")
            self.task_triggered.emit(task.id)
        
        return missed_tasks
    
    def mark_task_completed(self, task_id, success=True):
        """Mark task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id].mark_completed()
            self.save_tasks()
            self.task_completed.emit(task_id, success)
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            
            data = {
                'next_task_id': self.next_task_id,
                'tasks': [task.to_dict() for task in self.tasks.values()]
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                
                self.next_task_id = data.get('next_task_id', 1)
                
                for task_data in data.get('tasks', []):
                    task = ScheduledTask.from_dict(task_data)
                    self.tasks[task.id] = task
        except Exception as e:
            print(f"Error loading tasks: {e}")


def format_schedule_time(task):
    """Format schedule time for display"""
    if not task.next_run:
        return "Not scheduled"
    
    now = datetime.now()
    delta = task.next_run - now
    
    if delta.total_seconds() < 0:
        return "Overdue"
    elif delta.total_seconds() < 3600:  # Less than 1 hour
        minutes = int(delta.total_seconds() / 60)
        return f"In {minutes} minute{'s' if minutes != 1 else ''}"
    elif delta.total_seconds() < 86400:  # Less than 1 day
        hours = int(delta.total_seconds() / 3600)
        return f"In {hours} hour{'s' if hours != 1 else ''}"
    else:
        days = int(delta.total_seconds() / 86400)
        return f"In {days} day{'s' if days != 1 else ''}"


# Example usage
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create manager
    manager = ScheduleManager()
    
    # Add a one-time task for tomorrow at 10 AM
    tomorrow_10am = datetime.now().replace(hour=10, minute=0, second=0) + timedelta(days=1)
    task_id = manager.add_task(
        ['file1.txt', 'file2.pdf'],
        'dod',
        ScheduleType.ONCE,
        tomorrow_10am
    )
    
    print(f"Created task: {task_id}")
    print(f"Will run: {format_schedule_time(manager.get_task(task_id))}")
    
    # Add daily task
    daily_task_id = manager.add_task(
        ['temp.log'],
        'simple',
        ScheduleType.DAILY,
        datetime.now().replace(hour=23, minute=0)
    )
    
    print(f"\nCreated daily task: {daily_task_id}")
    print(f"Will run: {format_schedule_time(manager.get_task(daily_task_id))}")
    
    # Show all upcoming tasks
    print("\nUpcoming tasks:")
    for task in manager.get_upcoming_tasks():
        print(f"  {task.id}: {len(task.file_paths)} files - {format_schedule_time(task)}")