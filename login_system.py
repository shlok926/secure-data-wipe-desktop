"""
Login System Module for Secure Wipe
Multi-user authentication with password protection
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path


class LoginSystem:
    """Manage user authentication and sessions"""
    
    def __init__(self):
        self.users_file = "config/users.json"
        self.current_user = None
        self.ensure_config_dir()
        self.load_users()
    
    def ensure_config_dir(self):
        """Create config directory if not exists"""
        os.makedirs("config", exist_ok=True)
    
    def hash_password(self, password):
        """Hash password with SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
            # Create default admin user
            self.create_default_admin()
    
    def save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def create_default_admin(self):
        """Create default admin user"""
        self.users['admin'] = {
            'password': self.hash_password('admin123'),
            'role': 'admin',
            'created': datetime.now().isoformat(),
            'last_login': None
        }
        self.save_users()
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if username not in self.users:
            return False, "User not found"
        
        if self.users[username]['password'] != self.hash_password(password):
            return False, "Incorrect password"
        
        # Update last login
        self.users[username]['last_login'] = datetime.now().isoformat()
        self.save_users()
        
        self.current_user = username
        return True, f"Welcome {username}!"
    
    def create_user(self, username, password, role='user'):
        """Create new user"""
        if username in self.users:
            return False, "User already exists"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        
        self.users[username] = {
            'password': self.hash_password(password),
            'role': role,
            'created': datetime.now().isoformat(),
            'last_login': None
        }
        
        if self.save_users():
            return True, f"User {username} created successfully"
        return False, "Error creating user"
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if username not in self.users:
            return False, "User not found"
        
        if self.users[username]['password'] != self.hash_password(old_password):
            return False, "Incorrect current password"
        
        if len(new_password) < 4:
            return False, "New password must be at least 4 characters"
        
        self.users[username]['password'] = self.hash_password(new_password)
        
        if self.save_users():
            return True, "Password changed successfully"
        return False, "Error changing password"
    
    def delete_user(self, username):
        """Delete user"""
        if username == 'admin':
            return False, "Cannot delete admin user"
        
        if username not in self.users:
            return False, "User not found"
        
        del self.users[username]
        
        if self.save_users():
            return True, f"User {username} deleted"
        return False, "Error deleting user"
    
    def get_all_users(self):
        """Get list of all users"""
        return list(self.users.keys())
    
    def is_admin(self, username=None):
        """Check if user is admin"""
        if username is None:
            username = self.current_user
        
        return self.users.get(username, {}).get('role') == 'admin'
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
