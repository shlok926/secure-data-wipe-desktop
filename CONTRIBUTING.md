# Contributing to SecureWipe Desktop

Thank you for your interest in contributing to SecureWipe Desktop! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Types of Contributions

### 🐛 Bug Reports

Found a bug? Please report it by opening an issue on GitHub.

**Include in your report:**
- Windows version and build number
- Python version (if running from source)
- Application version
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Error messages or screenshots
- Any relevant logs from `logs/wipe_log.txt`

### 💡 Feature Requests

Have an idea for a new feature? Open a discussion or issue with:
- Clear description of the requested feature
- Use cases and benefits
- Potential implementation approach
- Any related features or similar tools

### 📝 Documentation Improvements

Help improve documentation by:
- Pointing out unclear sections
- Suggesting better examples
- Adding missing information
- Fixing typos or formatting

### 🔧 Code Contributions

Want to contribute code? Great! Follow these guidelines:

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Git installed and configured
- Virtual environment support

### Setup Steps

```bash
# 1. Fork the repository on GitHub
# Visit: https://github.com/shlok926/secure-data-wipe-desktop
# Click "Fork" button

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/secure-data-wipe-desktop.git
cd secure-data-wipe-desktop

# 3. Create development virtual environment
python -m venv dev_env
dev_env\Scripts\activate

# 4. Install development dependencies
pip install -r requirements.txt

# 5. Create a feature branch
git checkout -b feature/your-feature-name
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/descriptive-name
# or for bug fixes:
git checkout -b fix/bug-description
# or for documentation:
git checkout -b docs/description
```

### 2. Make Your Changes

- Keep changes focused and limited in scope
- Write clear, descriptive commit messages
- Follow Python PEP 8 style guidelines
- Add comments for complex logic
- Test thoroughly

### 3. Test Your Changes

```bash
# Run the application
python secure_wipe_desktop.py

# Test specific features:
# - Test the feature you modified
# - Test related features to ensure no regression
# - Test on Windows 10 and/or Windows 11 if possible
```

### 4. Update Documentation

If your changes:
- Add new features: Update README.md
- Change behavior: Update relevant documentation
- Fix a significant bug: Add note to version history

### 5. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new secure erase feature

- Implemented new algorithm option
- Added UI controls for feature
- Updated documentation"
```

**Commit Message Format:**
```
type: subject

body (optional)
footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style fixes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `chore`: Build process, dependencies, etc.

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

1. Visit your fork on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template:
   - **Title**: Brief description of change
   - **Description**: Detailed explanation
   - **Testing**: How you tested it
   - **Related Issues**: Issues this addresses

## Code Style Guidelines

### Python Style
- Follow PEP 8 style guide
- Use meaningful variable names
- Add type hints when possible
- Maximum line length: 100 characters
- Use 4 spaces for indentation (not tabs)

### Example:
```python
def secure_wipe_file(file_path: str, algorithm: str = "dod", 
                     progress_callback: Optional[Callable] = None) -> bool:
    """
    Securely wipe a file using the specified algorithm.
    
    Args:
        file_path: Path to file to wipe
        algorithm: Wipe algorithm to use
        progress_callback: Optional callback for progress updates
        
    Returns:
        True if successful, False otherwise
    """
    # Implementation
    pass
```

### Comments
- Use comments to explain "why", not "what"
- Keep comments updated with code changes
- Use docstrings for functions and classes

### Git Commits
- One logical change per commit
- Descriptive commit messages
- Reference issues when relevant: "Fixes #123"

## Testing

### Manual Testing
- Test on multiple Windows versions if possible
- Test with different file types
- Test edge cases and error conditions
- Verify audit logs are created correctly
- Check that no data is recoverable after wipe

### Areas to Test
- Algorithm selection and execution
- Progress tracking accuracy
- Audit logging functionality
- UI responsiveness
- Certificate generation
- Multi-language support

## Pull Request Process

1. **Branch Strategy**: Create PR from your feature branch to master
2. **Description**: Provide clear description of changes
3. **Tests**: Include testing instructions
4. **Documentation**: Update relevant docs
5. **No Conflicts**: Resolve any merge conflicts
6. **Code Review**: Address review comments
7. **Approval**: Wait for maintainer approval
8. **Merge**: Maintainer will merge your PR

## Review Criteria

PRs will be evaluated on:
- ✅ Code quality and style
- ✅ Functionality and correctness
- ✅ Test coverage
- ✅ Documentation updates
- ✅ Performance impact
- ✅ Security implications
- ✅ Compliance with license

## Reporting Security Issues

**DO NOT** open a public issue for security vulnerabilities!

Instead, email: security@securewipe.com

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## License

By contributing, you agree that your contributions will be licensed under the 
same proprietary license as the project.

## Questions?

- 📖 Check the [documentation](README.md)
- 🐛 Search [existing issues](https://github.com/shlok926/secure-data-wipe-desktop/issues)
- 💬 Start a [discussion](https://github.com/shlok926/secure-data-wipe-desktop/discussions)
- 📧 Email: support@securewipe.com

---

**Thank you for contributing to SecureWipe Desktop!** 🙏
