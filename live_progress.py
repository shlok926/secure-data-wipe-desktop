"""
Live Time Remaining Counter Module for Secure Wipe
Real-time progress tracking with time estimation and speed calculation
"""

import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class LiveProgressTracker(QObject):
    """Track live progress with time estimation"""
    
    # Signals
    progress_update = pyqtSignal(dict)  # Emits complete progress info
    
    def __init__(self):
        super().__init__()
        
        self.start_time = None
        self.total_bytes = 0
        self.processed_bytes = 0
        self.current_pass = 0
        self.total_passes = 1
        self.is_active = False
        
        # Speed tracking
        self.last_update_time = None
        self.last_processed_bytes = 0
        self.speed_samples = []
        self.max_samples = 10
    
    def start(self, total_bytes, total_passes=1):
        """Start tracking progress"""
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.total_bytes = total_bytes
        self.processed_bytes = 0
        self.current_pass = 1
        self.total_passes = total_passes
        self.is_active = True
        self.last_processed_bytes = 0
        self.speed_samples = []
    
    def update(self, processed_bytes, current_pass=None):
        """Update progress"""
        if not self.is_active:
            return
        
        self.processed_bytes = processed_bytes
        
        if current_pass is not None:
            self.current_pass = current_pass
        
        # Calculate speed
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        
        if time_delta > 0:
            bytes_delta = processed_bytes - self.last_processed_bytes
            speed = bytes_delta / time_delta  # bytes per second
            
            # Store speed sample
            self.speed_samples.append(speed)
            if len(self.speed_samples) > self.max_samples:
                self.speed_samples.pop(0)
            
            self.last_update_time = current_time
            self.last_processed_bytes = processed_bytes
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        
        # Emit update
        self.progress_update.emit(metrics)
    
    def calculate_metrics(self):
        """Calculate all progress metrics"""
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        
        # Calculate average speed
        avg_speed = sum(self.speed_samples) / len(self.speed_samples) if self.speed_samples else 0
        
        # Calculate total work (all passes)
        total_work = self.total_bytes * self.total_passes
        current_work = (self.current_pass - 1) * self.total_bytes + self.processed_bytes
        
        # Overall progress percentage
        if total_work > 0:
            progress_percent = (current_work / total_work) * 100
        else:
            progress_percent = 0
        
        # Current pass progress
        if self.total_bytes > 0:
            pass_percent = (self.processed_bytes / self.total_bytes) * 100
        else:
            pass_percent = 0
        
        # Time remaining estimation
        if avg_speed > 0 and total_work > 0:
            remaining_work = total_work - current_work
            time_remaining = remaining_work / avg_speed
        else:
            time_remaining = 0
        
        return {
            'elapsed_time': elapsed_time,
            'time_remaining': time_remaining,
            'total_time': elapsed_time + time_remaining,
            'progress_percent': progress_percent,
            'pass_percent': pass_percent,
            'current_pass': self.current_pass,
            'total_passes': self.total_passes,
            'speed_bps': avg_speed,
            'speed_mbps': avg_speed / (1024 * 1024),
            'processed_bytes': self.processed_bytes,
            'total_bytes': self.total_bytes,
            'formatted': self.format_metrics(
                elapsed_time, 
                time_remaining, 
                avg_speed,
                progress_percent,
                self.current_pass,
                self.total_passes
            )
        }
    
    def format_metrics(self, elapsed, remaining, speed, progress, current_pass, total_passes):
        """Format metrics into human-readable strings"""
        return {
            'elapsed': self.format_time(elapsed),
            'remaining': self.format_time(remaining),
            'total': self.format_time(elapsed + remaining),
            'speed': self.format_speed(speed),
            'progress': f"{progress:.1f}%",
            'pass_info': f"Pass {current_pass}/{total_passes}"
        }
    
    @staticmethod
    def format_time(seconds):
        """Format seconds to readable time"""
        if seconds < 1:
            return "< 1 sec"
        elif seconds < 60:
            return f"{int(seconds)} sec"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"
    
    @staticmethod
    def format_speed(bytes_per_sec):
        """Format speed to readable string"""
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.0f} B/s"
        elif bytes_per_sec < 1024 * 1024:
            return f"{bytes_per_sec / 1024:.1f} KB/s"
        else:
            return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"
    
    def stop(self):
        """Stop tracking"""
        self.is_active = False


class ProgressDisplay:
    """Helper class for displaying progress in UI"""
    
    @staticmethod
    def create_progress_text(metrics):
        """Create detailed progress text"""
        fmt = metrics['formatted']
        
        text = f"""
⏱️ Elapsed: {fmt['elapsed']}
⏳ Remaining: {fmt['remaining']}
🎯 Total Est: {fmt['total']}
⚡ Speed: {fmt['speed']}
📊 Progress: {fmt['progress']}
🔄 {fmt['pass_info']}
        """
        
        return text.strip()
    
    @staticmethod
    def create_compact_text(metrics):
        """Create compact progress text for status bar"""
        fmt = metrics['formatted']
        return f"{fmt['progress']} | {fmt['pass_info']} | {fmt['remaining']} left | {fmt['speed']}"
    
    @staticmethod
    def create_title_text(metrics):
        """Create text for window title"""
        fmt = metrics['formatted']
        return f"Wiping... {fmt['progress']} - {fmt['remaining']} remaining"


# Convenience functions
def format_bytes(bytes_val):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def format_duration(seconds):
    """Format duration to readable string"""
    return LiveProgressTracker.format_time(seconds)


# Example usage
if __name__ == "__main__":
    import time
    
    tracker = LiveProgressTracker()
    
    # Simulate wiping 100 MB file with 3 passes
    total_size = 100 * 1024 * 1024  # 100 MB
    total_passes = 3
    
    tracker.start(total_size, total_passes)
    
    print("Simulating wipe progress...")
    print("-" * 60)
    
    # Simulate progress
    for pass_num in range(1, total_passes + 1):
        for chunk in range(0, total_size, 1024 * 1024):  # 1 MB chunks
            tracker.update(min(chunk, total_size), pass_num)
            metrics = tracker.calculate_metrics()
            
            print(f"\rPass {pass_num}/{total_passes} | "
                  f"{metrics['formatted']['progress']} | "
                  f"{metrics['formatted']['speed']} | "
                  f"Remaining: {metrics['formatted']['remaining']}", 
                  end='', flush=True)
            
            time.sleep(0.1)  # Simulate work
    
    print("\n" + "-" * 60)
    print("Done!")
