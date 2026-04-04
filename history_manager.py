"""
Wipe History Management System
Persistent storage and management of all wipe operations
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


class WipeHistoryManager:
    """Manage complete history of all wipe operations"""
    
    def __init__(self, history_file=None):
        if history_file is None:
            import sys
            if getattr(sys, 'frozen', False):
                BASE_DIR = os.path.dirname(sys.executable)
            else:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            history_file = os.path.join(BASE_DIR, "data", "wipe_history.json")
        self.history_file = history_file
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Load wipe history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert string timestamps back to datetime
                    for entry in data:
                        if 'timestamp' in entry and isinstance(entry['timestamp'], str):
                            entry['timestamp'] = datetime.fromisoformat(entry['timestamp'])
                    self.history = data
            else:
                self.history = []
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []
    
    def save_history(self):
        """Save wipe history to file"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            # Convert datetime to string for JSON
            json_data = []
            for entry in self.history:
                entry_copy = entry.copy()
                if 'timestamp' in entry_copy and isinstance(entry_copy['timestamp'], datetime):
                    entry_copy['timestamp'] = entry_copy['timestamp'].isoformat()
                json_data.append(entry_copy)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_wipe_entry(
        self,
        file_path: str,
        file_size: int,
        algorithm: str,
        success: bool,
        duration: float = 0.0,
        certificate_path: str = None,
        error_message: str = None
    ) -> str:
        """
        Add new wipe operation to history
        
        Returns:
            str: Entry ID
        """
        
        entry_id = self._generate_entry_id()
        
        entry = {
            'id': entry_id,
            'timestamp': datetime.now(),
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'file_size': file_size,
            'algorithm': algorithm,
            'success': success,
            'duration_seconds': duration,
            'certificate_path': certificate_path,
            'error_message': error_message,
            'operator': os.getenv('USERNAME', 'Unknown'),
            'machine': os.getenv('COMPUTERNAME', 'Unknown')
        }
        
        self.history.append(entry)
        self.save_history()

        # Tamper-proof audit chain: hash and chain this entry
        try:
            from audit_chain import get_audit_chain
            get_audit_chain().add_entry(entry)
        except Exception as _chain_err:
            print(f"Audit chain warning: {_chain_err}")
        
        return entry_id
    
    def get_all_history(self) -> List[Dict]:
        """Get complete wipe history"""
        return self.history
    
    def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """Get recent wipe operations"""
        return sorted(
            self.history,
            key=lambda x: x.get('timestamp', datetime.min),
            reverse=True
        )[:limit]
    
    def get_history_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get history within date range"""
        return [
            entry for entry in self.history
            if start_date <= entry.get('timestamp', datetime.min) <= end_date
        ]
    
    def get_monthly_history(self, year: int = None, month: int = None) -> List[Dict]:
        """Get history for specific month"""
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        
        return [
            entry for entry in self.history
            if (entry.get('timestamp', datetime.min).year == year and
                entry.get('timestamp', datetime.min).month == month)
        ]
    
    def get_statistics(self) -> Dict:
        """Calculate comprehensive statistics"""
        
        if not self.history:
            return {
                'total_wipes': 0,
                'successful_wipes': 0,
                'failed_wipes': 0,
                'total_data_destroyed_bytes': 0,
                'total_data_destroyed_gb': 0.0,
                'most_used_algorithm': 'None',
                'average_file_size_mb': 0.0,
                'success_rate': 0.0
            }
        
        total = len(self.history)
        successful = sum(1 for entry in self.history if entry.get('success', False))
        failed = total - successful
        
        total_bytes = sum(entry.get('file_size', 0) for entry in self.history)
        
        # Algorithm usage
        algo_count = {}
        for entry in self.history:
            algo = entry.get('algorithm', 'Unknown')
            algo_count[algo] = algo_count.get(algo, 0) + 1
        
        most_used_algo = max(algo_count.items(), key=lambda x: x[1])[0] if algo_count else 'None'
        
        return {
            'total_wipes': total,
            'successful_wipes': successful,
            'failed_wipes': failed,
            'total_data_destroyed_bytes': total_bytes,
            'total_data_destroyed_gb': total_bytes / (1024**3),
            'total_data_destroyed_mb': total_bytes / (1024**2),
            'most_used_algorithm': most_used_algo,
            'average_file_size_mb': (total_bytes / total / (1024**2)) if total > 0 else 0.0,
            'success_rate': (successful / total * 100) if total > 0 else 0.0,
            'algorithm_usage': algo_count
        }
    
    def export_to_csv(self, output_path: str) -> bool:
        """Export history to CSV file"""
        try:
            import csv
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if not self.history:
                    return False
                
                fieldnames = [
                    'ID', 'Timestamp', 'File Name', 'File Path', 
                    'Size (MB)', 'Algorithm', 'Status', 'Duration (s)',
                    'Certificate', 'Operator', 'Machine'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in self.history:
                    timestamp = entry.get('timestamp', datetime.min)
                    if isinstance(timestamp, datetime):
                        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        timestamp_str = str(timestamp)
                    
                    writer.writerow({
                        'ID': entry.get('id', ''),
                        'Timestamp': timestamp_str,
                        'File Name': entry.get('file_name', ''),
                        'File Path': entry.get('file_path', ''),
                        'Size (MB)': f"{entry.get('file_size', 0) / (1024**2):.2f}",
                        'Algorithm': entry.get('algorithm', ''),
                        'Status': 'Success' if entry.get('success', False) else 'Failed',
                        'Duration (s)': f"{entry.get('duration_seconds', 0):.2f}",
                        'Certificate': entry.get('certificate_path', ''),
                        'Operator': entry.get('operator', ''),
                        'Machine': entry.get('machine', '')
                    })
            
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def clear_old_entries(self, days: int = 90):
        """Remove entries older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        self.history = [
            entry for entry in self.history
            if entry.get('timestamp', datetime.min) > cutoff_date
        ]
        
        self.save_history()
    
    def _generate_entry_id(self) -> str:
        """Generate unique entry ID"""
        import hashlib
        data = f"{datetime.now().isoformat()}{len(self.history)}".encode()
        return hashlib.md5(data).hexdigest()[:12].upper()
    
    def search_history(self, query: str) -> List[Dict]:
        """Search history by filename or path"""
        query_lower = query.lower()
        return [
            entry for entry in self.history
            if (query_lower in entry.get('file_name', '').lower() or
                query_lower in entry.get('file_path', '').lower())
        ]


# Global history manager instance
_history_manager = None

def get_history_manager() -> WipeHistoryManager:
    """Get global history manager instance"""
    global _history_manager
    if _history_manager is None:
        _history_manager = WipeHistoryManager()
    return _history_manager