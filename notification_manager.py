"""
Notification Manager Module for Secure Wipe
Manages in-app notifications with bell icon system
"""

from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal


class NotificationManager(QObject):
    """Manage app notifications with history"""
    
    # Signal emitted when notification count changes
    notification_added = pyqtSignal(dict)  # notification dict
    
    def __init__(self):
        super().__init__()
        self.notifications = []
        self.max_notifications = 50
    
    def add(self, title, message, icon='info', timestamp=None):
        """
        Add a notification
        
        Args:
            title: Notification title
            message: Notification message
            icon: Icon type ('success', 'error', 'info', 'warning')
            timestamp: Optional timestamp (uses now if None)
        
        Returns:
            The created notification dict
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        notification = {
            'id': len(self.notifications) + 1,
            'title': title,
            'message': message,
            'icon': icon,
            'timestamp': timestamp,
            'read': False
        }
        
        # Add to beginning (most recent first)
        self.notifications.insert(0, notification)
        
        # Keep only last N notifications
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[:self.max_notifications]
        
        # Emit signal
        self.notification_added.emit(notification)
        
        return notification
    
    def mark_all_read(self):
        """Mark all notifications as read"""
        for notif in self.notifications:
            notif['read'] = False
        
        # All are now "read" conceptually
        return True
    
    def get_unread_count(self):
        """Get count of unread notifications"""
        return sum(1 for n in self.notifications if not n.get('read', False))
    
    def get_recent(self, count=10):
        """Get recent notifications"""
        return self.notifications[:count]
    
    def get_all(self):
        """Get all notifications"""
        return self.notifications
    
    def clear_all(self):
        """Clear all notifications"""
        self.notifications = []
    
    def clear_old(self, days=30):
        """Clear notifications older than N days"""
        cutoff = datetime.now() - timedelta(days=days)
        self.notifications = [
            n for n in self.notifications 
            if n['timestamp'] > cutoff
        ]


def format_time_ago(timestamp):
    """
    Format timestamp to human-readable 'X ago' format
    
    Args:
        timestamp: datetime object
    
    Returns:
        String like "2 min ago", "3 hours ago", etc.
    """
    now = datetime.now()
    delta = now - timestamp
    
    seconds = delta.total_seconds()
    
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:  # Less than 1 hour
        mins = int(seconds / 60)
        return f"{mins} min ago" if mins > 1 else "1 min ago"
    elif seconds < 86400:  # Less than 1 day
        hours = int(seconds / 3600)
        return f"{hours} hour ago" if hours > 1 else "1 hour ago"
    elif seconds < 604800:  # Less than 1 week
        days = delta.days
        return f"{days} day ago" if days > 1 else "1 day ago"
    else:
        weeks = delta.days // 7
        return f"{weeks} week ago" if weeks > 1 else "1 week ago"


# Example usage
if __name__ == "__main__":
    manager = NotificationManager()
    
    # Add some notifications
    manager.add("Wipe Complete", "Successfully wiped document.pdf", "success")
    manager.add("Error", "Failed to wipe image.jpg", "error")
    manager.add("Info", "Update available: v2.1", "info")
    
    print(f"Total notifications: {len(manager.get_all())}")
    print(f"Unread: {manager.get_unread_count()}")
    
    print("\nRecent notifications:")
    for notif in manager.get_recent(5):
        time_ago = format_time_ago(notif['timestamp'])
        print(f"  {notif['icon']}: {notif['title']} - {time_ago}")