"""
Time Estimation Module for Secure Wipe
Calculates estimated wipe time based on file size and algorithm
"""


class WipeTimeEstimator:
    """Calculate estimated wipe times"""
    
    def __init__(self, base_speed_mbs=80):
        """
        Initialize estimator
        
        Args:
            base_speed_mbs: Average write speed in MB/s (default: 80)
                           - HDD: ~80 MB/s
                           - SSD: ~300 MB/s
                           - Conservative: 80 MB/s
        """
        self.base_speed_mbs = base_speed_mbs
        
        # Algorithm pass counts
        self.algorithm_passes = {
            'simple': 1,
            'dod': 3,
            'nist': 1,
            'gutmann': 7,
            'crypto': 1
        }
    
    def calculate_time(self, file_size_mb, algorithm='dod'):
        """
        Calculate estimated wipe time in seconds
        
        Args:
            file_size_mb: File size in megabytes
            algorithm: Algorithm key (simple, dod, nist, gutmann, crypto)
            
        Returns:
            float: Estimated time in seconds
        """
        # Get pass count for algorithm
        passes = self.algorithm_passes.get(algorithm, 3)
        
        # Calculate base time: (size * passes) / speed
        base_time = (file_size_mb * passes) / self.base_speed_mbs
        
        # Add overhead for file operations (2 seconds minimum)
        overhead = 2.0
        
        # Total time
        total_time = base_time + overhead
        
        # Minimum 1 second
        return max(1.0, total_time)
    
    def format_time(self, seconds):
        """
        Format seconds into human-readable time string
        
        Args:
            seconds: Time in seconds
            
        Returns:
            str: Formatted time string (e.g., "~2 min 30 sec")
        """
        if seconds < 1:
            return "~1 sec"
        
        if seconds < 60:
            return f"~{int(seconds)} sec"
        
        if seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            if secs > 0:
                return f"~{minutes} min {secs} sec"
            else:
                return f"~{minutes} min"
        
        # Hours
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        if minutes > 0:
            return f"~{hours} hr {minutes} min"
        else:
            return f"~{hours} hr"
    
    def get_time_estimate_details(self, file_size_mb, algorithm='dod'):
        """
        Get detailed time estimate with breakdown
        
        Args:
            file_size_mb: File size in megabytes
            algorithm: Algorithm key
            
        Returns:
            dict: Detailed estimate information
        """
        seconds = self.calculate_time(file_size_mb, algorithm)
        passes = self.algorithm_passes.get(algorithm, 3)
        
        return {
            'total_seconds': seconds,
            'formatted_time': self.format_time(seconds),
            'passes': passes,
            'speed_mbs': self.base_speed_mbs,
            'file_size_mb': file_size_mb,
            'algorithm': algorithm
        }
    
    def get_time_for_all_algorithms(self, file_size_mb):
        """
        Get time estimates for all algorithms
        
        Args:
            file_size_mb: File size in megabytes
            
        Returns:
            dict: Time estimates for each algorithm
        """
        estimates = {}
        
        for algo in self.algorithm_passes.keys():
            seconds = self.calculate_time(file_size_mb, algo)
            estimates[algo] = {
                'seconds': seconds,
                'formatted': self.format_time(seconds),
                'passes': self.algorithm_passes[algo]
            }
        
        return estimates


# Convenience functions for quick use
def estimate_wipe_time(file_size_mb, algorithm='dod'):
    """
    Quick function to estimate wipe time
    
    Args:
        file_size_mb: File size in MB
        algorithm: Algorithm key
        
    Returns:
        str: Formatted time string
    """
    estimator = WipeTimeEstimator()
    seconds = estimator.calculate_time(file_size_mb, algorithm)
    return estimator.format_time(seconds)


def get_time_details(file_size_mb, algorithm='dod'):
    """
    Get detailed time estimate
    
    Args:
        file_size_mb: File size in MB
        algorithm: Algorithm key
        
    Returns:
        dict: Detailed estimate
    """
    estimator = WipeTimeEstimator()
    return estimator.get_time_estimate_details(file_size_mb, algorithm)


# Example usage
if __name__ == "__main__":
    estimator = WipeTimeEstimator()
    
    # Test different file sizes
    test_cases = [
        (10, 'dod'),
        (100, 'dod'),
        (1024, 'dod'),      # 1 GB
        (10240, 'gutmann'), # 10 GB
        (50, 'simple'),
    ]
    
    print("Time Estimation Examples:")
    print("=" * 60)
    
    for size_mb, algo in test_cases:
        details = estimator.get_time_estimate_details(size_mb, algo)
        print(f"File: {size_mb} MB | Algorithm: {algo}")
        print(f"  Passes: {details['passes']}")
        print(f"  Estimated Time: {details['formatted_time']}")
        print()
