"""
Advanced Batch Processing Module for Secure Wipe
Queue management, pause/resume, priority handling
"""

from enum import Enum
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
from pathlib import Path


class QueueItemStatus(Enum):
    """Status of queue items"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class QueueItem:
    """Single item in wipe queue"""
    
    def __init__(self, file_path, algorithm="dod", priority=0):
        self.id = self._generate_id()
        self.file_path = file_path
        self.file_name = Path(file_path).name
        self.algorithm = algorithm
        self.priority = priority
        self.status = QueueItemStatus.PENDING
        self.added_time = datetime.now()
        self.start_time = None
        self.end_time = None
        self.error_message = None
        self.file_size = 0
        
        # Get file size
        try:
            import os
            self.file_size = os.path.getsize(file_path)
        except:
            self.file_size = 0
    
    def _generate_id(self):
        """Generate unique ID"""
        import hashlib
        data = f"{datetime.now().isoformat()}{id(self)}".encode()
        return hashlib.md5(data).hexdigest()[:12].upper()
    
    def start_processing(self):
        """Mark as processing"""
        self.status = QueueItemStatus.PROCESSING
        self.start_time = datetime.now()
    
    def mark_completed(self):
        """Mark as completed"""
        self.status = QueueItemStatus.COMPLETED
        self.end_time = datetime.now()
    
    def mark_failed(self, error_msg):
        """Mark as failed"""
        self.status = QueueItemStatus.FAILED
        self.end_time = datetime.now()
        self.error_message = error_msg
    
    def mark_cancelled(self):
        """Mark as cancelled"""
        self.status = QueueItemStatus.CANCELLED
        self.end_time = datetime.now()
    
    def get_duration(self):
        """Get processing duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'algorithm': self.algorithm,
            'priority': self.priority,
            'status': self.status.value,
            'added_time': self.added_time.isoformat(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'file_size': self.file_size,
            'error_message': self.error_message
        }


class BatchQueue(QObject):
    """Manage batch wipe queue"""
    
    # Signals
    queue_updated = pyqtSignal()
    item_added = pyqtSignal(str)  # item_id
    item_removed = pyqtSignal(str)  # item_id
    item_status_changed = pyqtSignal(str, str)  # item_id, status
    
    def __init__(self):
        super().__init__()
        self.items = []
        self.current_item = None
        self.is_paused = False
    
    def add_item(self, file_path, algorithm="dod", priority=0):
        """Add item to queue"""
        item = QueueItem(file_path, algorithm, priority)
        self.items.append(item)
        
        # Sort by priority (higher first)
        self.items.sort(key=lambda x: x.priority, reverse=True)
        
        self.item_added.emit(item.id)
        self.queue_updated.emit()
        
        return item.id
    
    def add_multiple(self, file_paths, algorithm="dod"):
        """Add multiple files to queue"""
        added_ids = []
        for file_path in file_paths:
            item_id = self.add_item(file_path, algorithm)
            added_ids.append(item_id)
        return added_ids
    
    def remove_item(self, item_id):
        """Remove item from queue"""
        item = self.get_item(item_id)
        if item and item.status == QueueItemStatus.PENDING:
            self.items.remove(item)
            self.item_removed.emit(item_id)
            self.queue_updated.emit()
            return True
        return False
    
    def get_item(self, item_id):
        """Get item by ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def get_next_pending(self):
        """Get next pending item"""
        for item in self.items:
            if item.status == QueueItemStatus.PENDING:
                return item
        return None
    
    def get_pending_count(self):
        """Get count of pending items"""
        return sum(1 for item in self.items if item.status == QueueItemStatus.PENDING)
    
    def get_processing_count(self):
        """Get count of processing items"""
        return sum(1 for item in self.items if item.status == QueueItemStatus.PROCESSING)
    
    def get_completed_count(self):
        """Get count of completed items"""
        return sum(1 for item in self.items if item.status == QueueItemStatus.COMPLETED)
    
    def get_failed_count(self):
        """Get count of failed items"""
        return sum(1 for item in self.items if item.status == QueueItemStatus.FAILED)
    
    def get_statistics(self):
        """Get queue statistics"""
        return {
            'total': len(self.items),
            'pending': self.get_pending_count(),
            'processing': self.get_processing_count(),
            'completed': self.get_completed_count(),
            'failed': self.get_failed_count(),
            'cancelled': sum(1 for item in self.items if item.status == QueueItemStatus.CANCELLED)
        }
    
    def clear_completed(self):
        """Clear completed items"""
        self.items = [item for item in self.items 
                     if item.status not in [QueueItemStatus.COMPLETED, QueueItemStatus.FAILED]]
        self.queue_updated.emit()
    
    def clear_all(self):
        """Clear all items"""
        # Only clear if not processing
        if self.get_processing_count() == 0:
            self.items.clear()
            self.queue_updated.emit()
            return True
        return False
    
    def pause(self):
        """Pause queue processing"""
        self.is_paused = True
    
    def resume(self):
        """Resume queue processing"""
        self.is_paused = False
    
    def get_total_size(self):
        """Get total size of all pending items"""
        return sum(item.file_size for item in self.items 
                  if item.status == QueueItemStatus.PENDING)
    
    def export_queue(self):
        """Export queue to list of dicts"""
        return [item.to_dict() for item in self.items]
    
    def get_items_by_status(self, status):
        """Get all items with specific status"""
        return [item for item in self.items if item.status == status]


class BatchProcessor(QObject):
    """Process batch queue"""
    
    # Signals
    batch_started = pyqtSignal()
    batch_completed = pyqtSignal(dict)  # statistics
    item_started = pyqtSignal(str)  # item_id
    item_completed = pyqtSignal(str, bool)  # item_id, success
    item_progress = pyqtSignal(str, int)  # item_id, percent
    
    def __init__(self, queue, wiper_engine):
        super().__init__()
        self.queue = queue
        self.wiper = wiper_engine
        self.is_processing = False
        self.current_item_id = None
    
    def start_batch(self):
        """Start processing batch queue"""
        if self.is_processing:
            return False
        
        if self.queue.get_pending_count() == 0:
            return False
        
        self.is_processing = True
        self.batch_started.emit()
        
        # Process items
        self._process_next()
        
        return True
    
    def _process_next(self):
        """Process next item in queue"""
        if not self.is_processing or self.queue.is_paused:
            return
        
        # Get next item
        item = self.queue.get_next_pending()
        
        if not item:
            # All done
            self._finish_batch()
            return
        
        # Process item
        self.current_item_id = item.id
        item.start_processing()
        self.queue.item_status_changed.emit(item.id, item.status.value)
        self.item_started.emit(item.id)
        
        # Wipe file
        try:
            self.wiper.set_algorithm(item.algorithm)
            success = self.wiper.wipe_file(item.file_path)
            
            if success:
                item.mark_completed()
            else:
                item.mark_failed("Wipe failed")
            
            self.queue.item_status_changed.emit(item.id, item.status.value)
            self.item_completed.emit(item.id, success)
            
        except Exception as e:
            item.mark_failed(str(e))
            self.queue.item_status_changed.emit(item.id, item.status.value)
            self.item_completed.emit(item.id, False)
        
        # Process next
        self._process_next()
    
    def _finish_batch(self):
        """Finish batch processing"""
        self.is_processing = False
        self.current_item_id = None
        
        stats = self.queue.get_statistics()
        self.batch_completed.emit(stats)
    
    def pause_batch(self):
        """Pause batch processing"""
        self.queue.pause()
    
    def resume_batch(self):
        """Resume batch processing"""
        self.queue.resume()
        if self.is_processing:
            self._process_next()
    
    def stop_batch(self):
        """Stop batch processing"""
        self.is_processing = False
        
        # Mark current item as cancelled
        if self.current_item_id:
            item = self.queue.get_item(self.current_item_id)
            if item:
                item.mark_cancelled()


# Example usage
if __name__ == "__main__":
    # Create queue
    queue = BatchQueue()
    
    # Add items
    queue.add_item("file1.txt", "dod", priority=1)
    queue.add_item("file2.pdf", "nist", priority=2)
    queue.add_item("file3.doc", "dod", priority=0)
    
    # Display queue
    print("Queue Statistics:")
    stats = queue.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\nTotal size: {queue.get_total_size()} bytes")
    print(f"Next item: {queue.get_next_pending().file_name}")
