# Copilot Workspace Instructions for Secure Data Wiping Desktop Application

## Overview
This project is a professional Windows desktop application for secure data wiping, featuring a modern PyQt6 UI and multiple military-grade algorithms. The codebase emphasizes security, auditability, and compliance.

## Build & Run Conventions
- **Install dependencies:**
  - `pip install -r requirements.txt`
- **Run the app (dev mode):**
  - `python secure_wipe_desktop.py`
- **Build executable:**
  - `python build_exe.py` (preferred)
  - or `pyinstaller SecureWipe.spec`
- **Main entry point:**
  - `secure_wipe_desktop.py`
- **Core logic:**
  - `wiper_core.py`

## Project Structure
- `secure_wipe_desktop.py`: Main PyQt6 GUI
- `wiper_core.py`: Secure wiping algorithms
- `build_exe.py`: Build script for PyInstaller
- `requirements.txt`: Python dependencies
- `logs/`, `data/`, `config/`: App data, logs, and configuration

## Key Conventions
- **Security:** Use cryptographically secure random generation for all wipe operations.
- **Audit:** All destructive actions must be logged with timestamps and user context.
- **Compliance:** Algorithms and logging must meet GDPR, HIPAA, PCI-DSS, and DoD standards.
- **UI:** All user-facing actions should provide clear warnings before destructive operations.
- **Testing:** Manual testing is required for all new wipe algorithms and UI flows.

## Common Pitfalls
- PyQt6 import errors: `pip install PyQt6 PyQt6-Charts`
- Build issues: Ensure all dependencies are installed and Python 3.10+ is used.
- File permission errors: Run as Administrator if needed.

## Example Prompts
- "Add a new secure wipe algorithm following project conventions."
- "Update the audit logging to include user role and device ID."
- "Refactor the UI to add a confirmation dialog before every wipe."
- "Integrate a new compliance standard into the logging system."

## Next Steps
- Consider creating agent customizations for:
  - Automated compliance checks
  - UI/UX consistency enforcement
  - Secure algorithm template generation

---
For more details, see [README.md](README.md).
