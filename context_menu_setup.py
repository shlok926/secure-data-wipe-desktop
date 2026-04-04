"""
context_menu_setup.py - Utility to add Secure Wipe to the Windows Right-Click Context Menu.
Must be run as Administrator!
"""
import os
import sys
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_context_menu(remove=False):
    """Adds or removes the 'Secure Wipe' option to the Windows context menu."""
    if not is_admin():
        print("[-] Please run this script as Administrator to modify the registry.")
        return False

    # Path to the current Python executable and the secure_wipe_desktop script
    # In a compiled .exe, sys.executable is the .exe itself.
    if getattr(sys, 'frozen', False):
        python_exe = sys.executable
        app_path = ""
    else:
        python_exe = sys.executable
        app_path = f'"{os.path.abspath("secure_wipe_desktop.py")}"'

    menu_name = "Secure Wipe"
    command_string = f'"{python_exe}" {app_path} "%1"' if app_path else f'"{python_exe}" "%1"'
    
    # We target both * (files) and Directory (folders)
    targets = [
        (winreg.HKEY_CLASSES_ROOT, r"*\shell\SecureWipe"),
        (winreg.HKEY_CLASSES_ROOT, r"Directory\shell\SecureWipe"),
    ]

    try:
        for root_key, sub_key in targets:
            if remove:
                try:
                    winreg.DeleteKey(root_key, sub_key + r"\command")
                    winreg.DeleteKey(root_key, sub_key)
                    print(f"[+] Removed Context Menu from: {sub_key}")
                except FileNotFoundError:
                    pass
            else:
                # Create main key
                key = winreg.CreateKey(root_key, sub_key)
                winreg.SetValue(key, "", winreg.REG_SZ, menu_name)
                # Set Icon
                icon_path = os.path.abspath("icon.ico")
                if os.path.exists(icon_path):
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
                
                # Create command key
                cmd_key = winreg.CreateKey(key, "command")
                winreg.SetValue(cmd_key, "", winreg.REG_SZ, command_string)
                
                winreg.CloseKey(cmd_key)
                winreg.CloseKey(key)
                print(f"[+] Added Context Menu to: {sub_key}")
        
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Secure Wipe Context Menu Installer")
    parser.add_argument("--remove", action="store_true", help="Remove the context menu entry")
    args = parser.parse_args()
    
    if setup_context_menu(args.remove):
        action = "removed" if args.remove else "installed"
        print(f"\n✅ Context menu successfully {action}!")
        print("You can now right-click any file in Windows Explorer to wipe it.")
    else:
        print("\n❌ Failed to modify context menu. Did you run as Administrator?")
