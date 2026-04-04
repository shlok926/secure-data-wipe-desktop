# Secure Wipe - Administration & Security Notice

## Overview of Security Implementations
The **Secure Wipe** application implements several security measures to protect the user environment from accidental or malicious operations.

### Key Features
1. **Master PIN & Application Lock** 🔐
   - A PIN protects access to wiping functionalities and settings.
   - **Protection:** Brute-force protected with a 30-second lockout after 5 failed attempts.
   - **Tamper Resistance:** Dual-storage mechanism. PIN hashes are stored simultaneously in the Windows Registry (`QSettings`) and an encrypted local file (`config/.auth_state`). Deleting one will not bypass the authentication, as the application will heal the missing state from the other.

2. **Configuration Protection** 🛒
   - All sensitive data stored locally (such as SMTP email passwords or secondary PIN hashes) is protected using a uniquely generated symmetric key via the **Fernet (AES) algorithm**.

3. **Smart Anomalies & Path Validation** 🚨
   - The Wipe engine contains hardened path validation routines that strictly block target paths resolving to core OS configurations:
     - `C:\Windows`
     - `C:\Program Files`
     - Network / UNC paths (`\\server\`)

## ⚠️ Important Considerations for Distribution
While the codebase implements active protection, this software remains a locally executed Python application. If you intend to distribute this software in an Enterprise environment, please be aware of the following:

- **Code Signing:** The built executable (`.exe`) is currently unsigned. A local Administrator could theoretically replace the executable with a tampered version that bypasses Python-side checks. It is highly recommended to obtain an **Authenticode Code Signing Certificate** to sign your binaries.
- **Physical Access:** If an attacker has elevated Administrator or physical access to the device, they can extract the encryption keys stored in the user partition and decipher the settings.

*Secure Wipe is designed to protect from standard user errors and casual meddling. It relies on the Host Operating System (Windows) to enforce memory and disk permissions for absolute security.*
