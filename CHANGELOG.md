# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [2.0.1] - 2026-06-11

### Changed
- 🎨 **UI Refinements**: Professional dark-only theme (removed Light Mode and Auto theme options)
- 🔐 **Authentication Screen Redesign**: Enterprise-grade login dialog with professional branding
  - Added "Secure Wipe" title and lock icon
  - Improved gradient button styling
  - Optimized button sizing (UNLOCK 44px, EXIT 35px) to prevent overlap
  - Better spacing and typography
- 📐 **Layout Optimization**: Reduced padding and increased button spacing for cleaner appearance
- 🎯 **Qt Stylesheet Compatibility**: Removed CSS-only properties (box-shadow, word-wrap) for better Qt compatibility

### Fixed
- ✅ Stylesheet parsing errors (invalid Qt properties)
- ✅ Button overlap issues in authentication dialog
- ✅ UI cluttering on login screen

### Technical
- Built standalone executable: SecureWipe.exe (75 MB)
- Verified clean app launch without stylesheet warnings
- Ready for distribution on Windows 10/11

---

## [2.0.0] - 2024-01-15

### Added
- ✨ Complete rewrite with PyQt6 modern UI
- 🔐 Five military-grade wiping algorithms:
  - DoD 5220.22-M (3-pass)
  - NIST SP 800-88
  - Gutmann Method (7-pass)
  - Single Pass
  - Cryptographic Erase
- 📊 Comprehensive dashboard with statistics
- 📋 Advanced audit logging system
- 🏆 Audit chain with tamper detection
- 📜 PDF certificate generation
- 🌐 Multi-language support (English, Spanish, French)
- 🎨 Dark/Light theme support
- 📁 Batch file processing
- 🔔 System tray integration
- 📧 Email integration for reporting
- 🎯 File and folder targeting
- ⚡ Real-time progress tracking
- 🔒 PIN-based access control
- 📱 Mobile-responsive UI

### Changed
- Migrated from Tkinter to PyQt6
- Completely new architecture
- Improved performance and efficiency

### Fixed
- Multiple stability issues
- Memory management improvements

### Security
- Enhanced cryptographic functions
- Improved permission handling
- Better error handling

---

## [1.0.0] - 2023-06-01

### Added
- Initial release
- Basic secure file wiping
- Simple command-line interface
- Single wiping algorithm
- Basic logging

### Security
- Initial cryptographic implementation
- Basic validation checks

---

## [Previous Versions]

### v0.9.0 (Beta)
- Pre-release version
- Core wiping engine
- Experimental features

---

## Versioning

This project uses [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR** version = Breaking changes
- **MINOR** version = New features (backward compatible)
- **PATCH** version = Bug fixes (backward compatible)

---

## How to Report Changes

To report changes for inclusion in the changelog:

1. Create a Pull Request with your changes
2. Document changes in the "Unreleased" section
3. Follow the format: Added, Changed, Deprecated, Removed, Fixed, Security
4. Update version number when creating releases

---

## Release Schedule

- **Major Releases**: Quarterly (planned new features, breaking changes)
- **Minor Releases**: Monthly (new features, enhancements)
- **Patch Releases**: As needed (bug fixes, security patches)

---

**Note**: Dates in YYYY-MM-DD format follow [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
