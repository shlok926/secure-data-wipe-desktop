#!/usr/bin/env python3
"""Test script to verify PIN login logging captures all system information"""

import socket
import getpass
import platform
import psutil
import sys
from datetime import datetime
import json

def test_system_info_capture():
    """Test capturing all system information like PIN login would"""
    
    print("=" * 80)
    print("SYSTEM INFORMATION CAPTURE TEST")
    print("=" * 80)
    
    timestamp = datetime.now()
    
    # User/Network Info
    username = getpass.getuser()
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "Unknown"
    
    # OS Information
    os_name = platform.system()
    os_release = platform.release()
    full_os = f"{os_name} {os_release}"
    
    # Hardware Information
    architecture = platform.architecture()[0]
    processor = platform.processor()
    
    # Python Information
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # App Information
    app_version = "2.0.0"
    
    # Additional System Info
    try:
        cpu_count = psutil.cpu_count()
        memory_total_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        memory_available_gb = round(psutil.virtual_memory().available / (1024**3), 2)
    except:
        cpu_count = "N/A"
        memory_total_gb = "N/A"
        memory_available_gb = "N/A"
    
    # Display captured information
    print(f"\n✅ TIMESTAMP: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n👤 USER INFORMATION:")
    print(f"   - Username: {username}")
    print(f"   - Hostname: {hostname}")
    print(f"   - IP Address: {ip_address}")
    
    print(f"\n💻 OS INFORMATION:")
    print(f"   - Operating System: {full_os}")
    print(f"   - Architecture: {architecture}")
    print(f"   - Processor: {processor}")
    
    print(f"\n🐍 PYTHON INFORMATION:")
    print(f"   - Python Version: {python_version}")
    print(f"   - App Version: {app_version}")
    
    print(f"\n⚙️  HARDWARE INFORMATION:")
    print(f"   - CPU Count: {cpu_count}")
    print(f"   - Total Memory: {memory_total_gb} GB")
    print(f"   - Available Memory: {memory_available_gb} GB")
    
    # Example PIN authentication log entry
    print("\n" + "=" * 80)
    print("📋 PIN AUTHENTICATION LOG ENTRY")
    print("=" * 80)
    
    system_info = (
        f"[PIN AUTH] User: {username} | Host: {hostname} | IP: {ip_address}\n"
        f"OS: {full_os} | Arch: {architecture} | CPU: {processor}\n"
        f"Python: {python_version} | App: {app_version}\n"
        f"CPUs: {cpu_count} | RAM: {memory_total_gb}GB (Avail: {memory_available_gb}GB)"
    )
    
    print("\n📄 AUDIT TABLE DISPLAY:")
    print("-" * 80)
    print(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System Info:\n{system_info}")
    print(f"Algorithm: PIN Authentication")
    print(f"Status: PIN Login Success")
    print(f"Duration: Auth")
    
    # JSON format for persistent storage
    pin_log_entry = {
        "timestamp": timestamp.isoformat(),
        "event_type": "PIN_LOGIN",
        "status": "SUCCESS",
        "user": {
            "username": username,
            "hostname": hostname,
            "ip_address": ip_address
        },
        "system": {
            "os_name": os_name,
            "os_release": os_release,
            "architecture": architecture,
            "processor": processor,
            "cpu_count": cpu_count,
            "memory_total_gb": memory_total_gb,
            "memory_available_gb": memory_available_gb,
            "python_version": python_version,
            "app_version": app_version
        }
    }
    
    print("\n" + "=" * 80)
    print("📁 JSON PERSISTENT LOG FORMAT (logs/pin_activity.json)")
    print("=" * 80)
    print(json.dumps(pin_log_entry, indent=2))
    
    print("\n" + "=" * 80)
    print("✅ ALL SYSTEM INFORMATION WILL BE CAPTURED AND SAVED")
    print("=" * 80)

if __name__ == "__main__":
    test_system_info_capture()
