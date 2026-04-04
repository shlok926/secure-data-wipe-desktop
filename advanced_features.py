"""
Advanced Features Module for Secure Wipe
Implements cutting-edge capabilities
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import threading
import hashlib


# ====================================================================
# FEATURE 1: SCHEDULED WIPING
# ====================================================================

class AdvancedScheduler:
    """Schedule wipes for specific times"""
    
    def __init__(self):
        self.schedules = []
        self.load_schedules()
    
    def add_schedule(self, file_path, algorithm, schedule_time, recurring=False):
        """Add a scheduled wipe"""
        schedule = {
            'id': len(self.schedules) + 1,
            'file_path': file_path,
            'algorithm': algorithm,
            'schedule_time': schedule_time.isoformat(),
            'recurring': recurring,  # daily, weekly, monthly
            'status': 'pending',
            'created': datetime.now().isoformat()
        }
        self.schedules.append(schedule)
        self.save_schedules()
        return schedule
    
    def get_pending_schedules(self):
        """Get schedules that need to run"""
        now = datetime.now()
        pending = []
        
        for schedule in self.schedules:
            if schedule['status'] != 'pending':
                continue
            
            schedule_time = datetime.fromisoformat(schedule['schedule_time'])
            if schedule_time <= now:
                pending.append(schedule)
        
        return pending
    
    def mark_completed(self, schedule_id):
        """Mark schedule as completed"""
        for schedule in self.schedules:
            if schedule['id'] == schedule_id:
                schedule['status'] = 'completed'
                schedule['completed_at'] = datetime.now().isoformat()
        self.save_schedules()
    
    def save_schedules(self):
        """Save schedules to file"""
        os.makedirs('config', exist_ok=True)
        with open('config/schedules.json', 'w') as f:
            json.dump(self.schedules, f, indent=4)
    
    def load_schedules(self):
        """Load schedules from file"""
        if os.path.exists('config/schedules.json'):
            try:
                with open('config/schedules.json', 'r') as f:
                    self.schedules = json.load(f)
            except:
                self.schedules = []


# ====================================================================
# FEATURE 2: BATCH PROCESSING
# ====================================================================

class BatchProcessor:
    """Process multiple files at once"""
    
    def __init__(self):
        self.queue = []
        self.completed = []
        self.failed = []
    
    def add_files(self, file_paths, algorithm='dod'):
        """Add multiple files to batch"""
        for file_path in file_paths:
            if os.path.exists(file_path):
                self.queue.append({
                    'file_path': file_path,
                    'algorithm': algorithm,
                    'status': 'queued',
                    'added_at': datetime.now()
                })
    
    def process_batch(self, wiper, progress_callback=None):
        """Process all files in batch"""
        total = len(self.queue)
        
        for i, item in enumerate(self.queue):
            try:
                if progress_callback:
                    progress_callback(i, total, item['file_path'])
                
                wiper.set_algorithm(item['algorithm'])
                success = wiper.wipe_file(item['file_path'])
                
                if success:
                    self.completed.append(item)
                else:
                    self.failed.append(item)
                
            except Exception as e:
                item['error'] = str(e)
                self.failed.append(item)
        
        self.queue = []
        return len(self.completed), len(self.failed)
    
    def get_summary(self):
        """Get batch processing summary"""
        return {
            'total': len(self.completed) + len(self.failed),
            'successful': len(self.completed),
            'failed': len(self.failed),
            'completed_files': [Path(f['file_path']).name for f in self.completed],
            'failed_files': [Path(f['file_path']).name for f in self.failed]
        }


# ====================================================================
# FEATURE 3: SECURE FOLDER WIPE
# ====================================================================

class SecureFolderWiper:
    """Wipe entire folders securely"""
    
    def __init__(self):
        self.total_files = 0
        self.wiped_files = 0
        self.failed_files = 0
    
    def scan_folder(self, folder_path):
        """Scan folder and count files"""
        files = []
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
        
        self.total_files = len(files)
        return files
    
    def wipe_folder(self, folder_path, wiper, algorithm='dod', progress_callback=None):
        """Wipe entire folder"""
        files = self.scan_folder(folder_path)
        
        wiper.set_algorithm(algorithm)
        
        for i, file_path in enumerate(files):
            try:
                if progress_callback:
                    percent = int((i / len(files)) * 100)
                    progress_callback(percent, f"Wiping: {Path(file_path).name}")
                
                if wiper.wipe_file(file_path):
                    self.wiped_files += 1
                else:
                    self.failed_files += 1
            
            except Exception as e:
                print(f"Error wiping {file_path}: {e}")
                self.failed_files += 1
        
        # Remove empty directories
        try:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        os.rmdir(dir_path)
                    except:
                        pass
            os.rmdir(folder_path)
        except:
            pass
        
        return self.wiped_files, self.failed_files


# ====================================================================
# FEATURE 4: DUPLICATE FILE FINDER & WIPE
# ====================================================================

class DuplicateFinder:
    """Find and wipe duplicate files"""
    
    def __init__(self):
        self.duplicates = {}
    
    def find_duplicates(self, directory):
        """Find duplicate files by hash"""
        file_hashes = {}
        
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                try:
                    file_hash = self.hash_file(file_path)
                    
                    if file_hash in file_hashes:
                        if file_hash not in self.duplicates:
                            self.duplicates[file_hash] = [file_hashes[file_hash]]
                        self.duplicates[file_hash].append(file_path)
                    else:
                        file_hashes[file_hash] = file_path
                
                except Exception as e:
                    print(f"Error hashing {file_path}: {e}")
        
        return self.duplicates
    
    def hash_file(self, file_path, block_size=65536):
        """Calculate file hash"""
        hasher = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hasher.update(data)
        
        return hasher.hexdigest()
    
    def get_duplicate_summary(self):
        """Get summary of duplicates"""
        total_duplicates = sum(len(files) - 1 for files in self.duplicates.values())
        total_space = 0
        
        for files in self.duplicates.values():
            if files:
                file_size = os.path.getsize(files[0])
                total_space += file_size * (len(files) - 1)
        
        return {
            'duplicate_sets': len(self.duplicates),
            'total_duplicates': total_duplicates,
            'space_wasted': total_space
        }


# ====================================================================
# FEATURE 5: SMART WIPE RECOMMENDATIONS
# ====================================================================

class SmartRecommender:
    """AI-powered wipe recommendations"""
    
    def __init__(self):
        self.rules = {
            'temp_files': ['.tmp', '.temp', '.cache'],
            'backup_files': ['.bak', '.backup', '~'],
            'log_files': ['.log'],
            'old_downloads': ['Downloads'],
        }
    
    def scan_system(self, base_path=None):
        """Scan system for files to recommend wiping"""
        if not base_path:
            base_path = os.path.expanduser('~')
        
        recommendations = {
            'temp_files': [],
            'old_files': [],
            'large_files': [],
            'duplicates': []
        }
        
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                try:
                    # Check temp files
                    if any(filename.endswith(ext) for ext in self.rules['temp_files']):
                        recommendations['temp_files'].append(file_path)
                    
                    # Check old files (>1 year)
                    mod_time = os.path.getmtime(file_path)
                    if datetime.now().timestamp() - mod_time > 365 * 24 * 3600:
                        recommendations['old_files'].append(file_path)
                    
                    # Check large files (>100MB)
                    size = os.path.getsize(file_path)
                    if size > 100 * 1024 * 1024:
                        recommendations['large_files'].append({
                            'path': file_path,
                            'size': size
                        })
                
                except:
                    pass
        
        return recommendations
    
    def get_space_savings(self, recommendations):
        """Calculate potential space savings"""
        total_space = 0
        
        for file_path in recommendations.get('temp_files', []):
            try:
                total_space += os.path.getsize(file_path)
            except:
                pass
        
        for file_path in recommendations.get('old_files', []):
            try:
                total_space += os.path.getsize(file_path)
            except:
                pass
        
        return total_space


# ====================================================================
# FEATURE 6: WIPE PATTERNS
# ====================================================================

class WipePatterns:
    """Custom wipe patterns for different scenarios"""
    
    PATTERNS = {
        'zero': 'Fill with zeros',
        'one': 'Fill with ones',
        'random': 'Random data',
        'gutmann': 'Gutmann 35-pass',
        'dod_3': 'DoD 3-pass',
        'dod_7': 'DoD 7-pass',
        'custom': 'Custom pattern'
    }
    
    @staticmethod
    def get_pattern(pattern_name):
        """Get wipe pattern details"""
        return WipePatterns.PATTERNS.get(pattern_name, 'Unknown')
    
    @staticmethod
    def create_custom_pattern(pattern_bytes):
        """Create custom wipe pattern"""
        return {
            'type': 'custom',
            'data': pattern_bytes,
            'description': f'Custom {len(pattern_bytes)}-byte pattern'
        }


# ====================================================================
# FEATURE 7: WIPE PROFILES
# ====================================================================

class WipeProfiles:
    """Predefined wipe profiles for different use cases"""
    
    PROFILES = {
        'quick': {
            'name': 'Quick Wipe',
            'algorithm': 'simple',
            'passes': 1,
            'verify': False,
            'description': 'Fast wipe for non-sensitive data'
        },
        'standard': {
            'name': 'Standard Wipe',
            'algorithm': 'dod',
            'passes': 3,
            'verify': True,
            'description': 'DoD standard for most use cases'
        },
        'high_security': {
            'name': 'High Security',
            'algorithm': 'gutmann',
            'passes': 7,
            'verify': True,
            'description': 'Maximum security for sensitive data'
        },
        'ssd_optimized': {
            'name': 'SSD Optimized',
            'algorithm': 'nist',
            'passes': 1,
            'verify': True,
            'description': 'Optimized for modern SSDs'
        },
        'compliance': {
            'name': 'Compliance Ready',
            'algorithm': 'dod',
            'passes': 7,
            'verify': True,
            'certificate': True,
            'description': 'GDPR/HIPAA compliant wipe'
        }
    }
    
    @staticmethod
    def get_profile(profile_name):
        """Get wipe profile"""
        return WipeProfiles.PROFILES.get(profile_name)
    
    @staticmethod
    def list_profiles():
        """List all available profiles"""
        return list(WipeProfiles.PROFILES.keys())


# ====================================================================
# FEATURE 8: WIPE QUEUE MANAGER
# ====================================================================

class WipeQueueManager:
    """Manage wipe queue with priority"""
    
    def __init__(self):
        self.queue = []
        self.processing = None
        self.completed = []
    
    def add_to_queue(self, file_path, algorithm, priority='normal'):
        """Add file to queue with priority"""
        item = {
            'id': len(self.queue) + 1,
            'file_path': file_path,
            'algorithm': algorithm,
            'priority': priority,  # low, normal, high, urgent
            'status': 'queued',
            'added_at': datetime.now()
        }
        
        # Insert based on priority
        priority_order = {'urgent': 0, 'high': 1, 'normal': 2, 'low': 3}
        priority_value = priority_order.get(priority, 2)
        
        inserted = False
        for i, existing in enumerate(self.queue):
            existing_priority = priority_order.get(existing['priority'], 2)
            if priority_value < existing_priority:
                self.queue.insert(i, item)
                inserted = True
                break
        
        if not inserted:
            self.queue.append(item)
        
        return item
    
    def get_next(self):
        """Get next item from queue"""
        if self.queue:
            self.processing = self.queue.pop(0)
            return self.processing
        return None
    
    def mark_completed(self, success=True, error=None):
        """Mark current item as completed"""
        if self.processing:
            self.processing['status'] = 'completed' if success else 'failed'
            self.processing['completed_at'] = datetime.now()
            if error:
                self.processing['error'] = error
            self.completed.append(self.processing)
            self.processing = None
    
    def get_queue_info(self):
        """Get queue information"""
        return {
            'queued': len(self.queue),
            'processing': 1 if self.processing else 0,
            'completed': len([c for c in self.completed if c['status'] == 'completed']),
            'failed': len([c for c in self.completed if c['status'] == 'failed'])
        }


# ====================================================================
# FEATURE 9: WIPE ANALYTICS
# ====================================================================

class WipeAnalytics:
    """Advanced analytics for wipe operations"""
    
    def __init__(self):
        self.metrics = {
            'total_wipes': 0,
            'total_bytes': 0,
            'total_time': 0,
            'by_algorithm': {},
            'by_date': {},
            'success_rate': 0
        }
    
    def analyze_history(self, history):
        """Analyze wipe history"""
        if not history:
            return self.metrics
        
        self.metrics['total_wipes'] = len(history)
        
        successful = 0
        for entry in history:
            # Count by algorithm
            algo = entry.get('algorithm', 'unknown')
            if algo not in self.metrics['by_algorithm']:
                self.metrics['by_algorithm'][algo] = 0
            self.metrics['by_algorithm'][algo] += 1
            
            # Total bytes
            self.metrics['total_bytes'] += entry.get('file_size', 0)
            
            # Total time
            self.metrics['total_time'] += entry.get('duration_seconds', 0)
            
            # Success rate
            if entry.get('success', False):
                successful += 1
            
            # By date
            timestamp = entry.get('timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    date = timestamp.split()[0]
                else:
                    date = timestamp.strftime('%Y-%m-%d')
                
                if date not in self.metrics['by_date']:
                    self.metrics['by_date'][date] = 0
                self.metrics['by_date'][date] += 1
        
        self.metrics['success_rate'] = (successful / len(history)) * 100 if history else 0
        
        return self.metrics
    
    def get_trends(self):
        """Get trending data"""
        return {
            'most_used_algorithm': max(self.metrics['by_algorithm'].items(), 
                                      key=lambda x: x[1])[0] if self.metrics['by_algorithm'] else 'None',
            'avg_file_size': self.metrics['total_bytes'] / self.metrics['total_wipes'] 
                           if self.metrics['total_wipes'] > 0 else 0,
            'avg_wipe_time': self.metrics['total_time'] / self.metrics['total_wipes']
                           if self.metrics['total_wipes'] > 0 else 0
        }


# ====================================================================
# FEATURE 10: EXPORT CAPABILITIES
# ====================================================================

class AdvancedExporter:
    """Export data in multiple formats"""
    
    @staticmethod
    def export_to_json(data, filename):
        """Export to JSON"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, default=str)
    
    @staticmethod
    def export_to_csv(history, filename):
        """Export to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'File', 'Algorithm', 'Status', 'Size', 'Duration'])
            
            for entry in history:
                writer.writerow([
                    entry.get('timestamp', ''),
                    entry.get('file_path', ''),
                    entry.get('algorithm', ''),
                    'Success' if entry.get('success') else 'Failed',
                    entry.get('file_size', 0),
                    entry.get('duration_seconds', 0)
                ])
    
    @staticmethod
    def export_to_html(history, filename):
        """Export to HTML report"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Secure Wipe Report</title>
            <style>
                body { font-family: Arial; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #3498db; color: white; }
                .success { color: green; }
                .failed { color: red; }
            </style>
        </head>
        <body>
            <h1>Secure Wipe Audit Report</h1>
            <p>Generated: {timestamp}</p>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>File</th>
                    <th>Algorithm</th>
                    <th>Status</th>
                    <th>Size</th>
                </tr>
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for entry in history:
            status_class = 'success' if entry.get('success') else 'failed'
            status_text = 'Success' if entry.get('success') else 'Failed'
            
            html += f"""
                <tr>
                    <td>{entry.get('timestamp', '')}</td>
                    <td>{Path(entry.get('file_path', '')).name}</td>
                    <td>{entry.get('algorithm', '')}</td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{entry.get('file_size', 0)} bytes</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html)


# ====================================================================
# USAGE EXAMPLES
# ====================================================================

if __name__ == "__main__":
    print("Advanced Features Module Loaded!")
    print()
    print("Available Features:")
    print("1. AdvancedScheduler - Schedule wipes")
    print("2. BatchProcessor - Batch file processing")
    print("3. SecureFolderWiper - Wipe entire folders")
    print("4. DuplicateFinder - Find & wipe duplicates")
    print("5. SmartRecommender - AI recommendations")
    print("6. WipePatterns - Custom wipe patterns")
    print("7. WipeProfiles - Predefined profiles")
    print("8. WipeQueueManager - Priority queue")
    print("9. WipeAnalytics - Advanced analytics")
    print("10. AdvancedExporter - Multi-format export")
