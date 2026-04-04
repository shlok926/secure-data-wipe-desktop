"""
Generate comprehensive PDF documentation for Secure Data Wiping Desktop Application
Includes: Backend Architecture, Frontend Architecture, Algorithms, Modules, Solutions
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

def create_documentation_pdf():
    """Generate comprehensive PDF documentation"""
    
    # Create PDF
    pdf_path = "Secure_Data_Wiping_System_Documentation.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00e676'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#00e676'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#00b8e6'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # Build story
    story = []
    
    # Title Page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("SECURE DATA WIPING SYSTEM", title_style))
    story.append(Paragraph("Complete Technical Documentation", heading2_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("TABLE OF CONTENTS", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    contents = [
        "1. Project Overview",
        "2. Build & Run Instructions",
        "3. Backend Architecture",
        "4. Secure Wiping Algorithms",
        "5. Frontend Architecture",
        "6. Module Documentation",
        "7. UI/UX Solutions",
        "8. Threading & Performance",
        "9. Security & Compliance",
        "10. Future Enhancements"
    ]
    for item in contents:
        story.append(Paragraph(item, body_style))
    story.append(PageBreak())
    
    # 1. PROJECT OVERVIEW
    story.append(Paragraph("1. PROJECT OVERVIEW", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    overview_text = """
    <b>Secure Data Wiping Desktop Application</b> is a professional Windows desktop 
    application designed for secure, auditable data destruction using military-grade 
    algorithms. Built with PyQt6 framework and Python 3.10+, it provides compliance 
    with GDPR, HIPAA, PCI-DSS, and DoD standards.
    """
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Key Features:", heading2_style))
    features = [
        "5 Government-Approved Wiping Algorithms (Simple, DoD, NIST, Gutmann, Crypto Erase)",
        "Complete Audit Trail & Compliance Logging",
        "Batch File Processing with Progress Tracking",
        "Free Space Wiping & External Drive Support",
        "Scheduled Wipe Operations",
        "Email-Based Compliance Reports",
        "Modern PyQt6 GUI with 11 Feature Pages",
        "Data Persistence & History Management",
        "Tamper-Proof Logging with Hash Chain",
        "Network Wiping Capabilities"
    ]
    for feature in features:
        story.append(Paragraph(f"• {feature}", body_style))
    story.append(PageBreak())
    
    # 2. BUILD & RUN INSTRUCTIONS
    story.append(Paragraph("2. BUILD & RUN INSTRUCTIONS", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.1 Prerequisites", heading2_style))
    prereqs = "Python 3.10 or higher, pip package manager, Windows operating system"
    story.append(Paragraph(prereqs, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.2 Installation", heading2_style))
    install_steps = [
        "pip install -r requirements.txt",
        "Installs: PyQt6, PyInstaller, cryptography, reportlab, etc."
    ]
    for step in install_steps:
        story.append(Paragraph(f"• {step}", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.3 Development Mode", heading2_style))
    story.append(Paragraph("python secure_wipe_desktop.py", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.4 Build Executable", heading2_style))
    build_cmd = "python build_exe.py  (preferred) OR pyinstaller SecureWipe.spec"
    story.append(Paragraph(build_cmd, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.5 Output", heading2_style))
    story.append(Paragraph("./dist/SecureWipe.exe (Standalone executable)", body_style))
    story.append(PageBreak())
    
    # 3. BACKEND ARCHITECTURE
    story.append(Paragraph("3. BACKEND ARCHITECTURE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("3.1 Core Components", heading2_style))
    
    backend_components = """
    <b>wiper_core.py</b> - Core wiping engine implementing 5 algorithms<br/>
    • WipeAlgorithm enum: SIMPLE, DOD, NIST, GUTMANN, CRYPTO<br/>
    • Supports individual files, directories, and free space<br/>
    • Progress callbacks for UI updates<br/>
    • Chunk-based processing (8192 bytes/chunk)<br/>
    <br/>
    <b>history_manager.py</b> - Maintains wipe history and persistence<br/>
    • JSONified wipe records with timestamps<br/>
    • Performance metrics (speed, duration)<br/>
    • File/directory tracking<br/>
    <br/>
    <b>audit_chain.py</b> - Tamper-proof audit logging<br/>
    • Hash-chain implementation (blockchain-style)<br/>
    • Cryptographic signatures<br/>
    • Immutable audit trail<br/>
    <br/>
    <b>verification_module.py</b> - Post-wipe verification<br/>
    • Confirms successful deletion<br/>
    • Generates verification reports<br/>
    • Hash comparison<br/>
    """
    story.append(Paragraph(backend_components, body_style))
    story.append(PageBreak())
    
    # 4. SECURE WIPING ALGORITHMS
    story.append(Paragraph("4. SECURE WIPING ALGORITHMS", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Algorithm 1: Simple
    story.append(Paragraph("4.1 Simple Wipe (Single Pass Random)", heading2_style))
    simple_text = """
    <b>Speed:</b> ⚡⚡⚡⚡⚡ (Fastest)<br/>
    <b>Security:</b> ⚔️ (Basic)<br/>
    <b>Passes:</b> 1<br/>
    <b>Use Case:</b> Quick deletion of non-sensitive data<br/>
    <br/>
    <b>Process:</b><br/>
    1. Generate random bytes using secrets.token_bytes()<br/>
    2. Overwrite file with random data in 8KB chunks<br/>
    3. Sync to disk using os.fsync()<br/>
    4. Delete file reference<br/>
    <br/>
    <b>Time Complexity:</b> O(n) where n = file size<br/>
    <b>Security Level:</b> No recovery possible with basic tools
    """
    story.append(Paragraph(simple_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Algorithm 2: DoD
    story.append(Paragraph("4.2 DoD 5220.22-M (Military Standard)", heading2_style))
    dod_text = """
    <b>Speed:</b> ⚡⚡⚡ (Moderate)<br/>
    <b>Security:</b> ⚔️⚔️⚔️⚔️ (Military Grade)<br/>
    <b>Passes:</b> 3<br/>
    <b>Use Case:</b> Government/Defense data, classified information<br/>
    <br/>
    <b>Process:</b><br/>
    • Pass 1: Random bytes (secrets.token_bytes)<br/>
    • Pass 2: Zero bytes (0x00) - detects magnetic remanence<br/>
    • Pass 3: One bytes (0xFF) - inverts magnetics<br/>
    • Each pass: 8KB chunks with os.fsync() sync<br/>
    <br/>
    <b>Time Complexity:</b> O(3n) = O(n)<br/>
    <b>Security Level:</b> Exceeds NSA/DoD standards, reverses magnetic imprints
    """
    story.append(Paragraph(dod_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Algorithm 3: NIST
    story.append(Paragraph("4.3 NIST SP 800-88 (SSD Optimized)", heading2_style))
    nist_text = """
    <b>Speed:</b> ⚡⚡⚡⚡ (Fast)<br/>
    <b>Security:</b> ⚔️⚔️⚔️⚔️ (Enterprise Grade)<br/>
    <b>Passes:</b> 1<br/>
    <b>Use Case:</b> Modern SSDs, enterprise environments<br/>
    <br/>
    <b>Process:</b><br/>
    1. Single pass with cryptographically secure random data<br/>
    2. Optimized for NAND flash memory (no multi-pass wear)<br/>
    3. Proper chunk buffering<br/>
    4. File system sync with integrity check<br/>
    <br/>
    <b>Why 1 Pass for SSD:</b> SSD controllers use wear-leveling; cannot<br/>
    reliably overwrite same physical location multiple times<br/>
    <br/>
    <b>Time Complexity:</b> O(n)<br/>
    <b>Security Level:</b> Standards-compliant for SSDs, impossible recovery
    """
    story.append(Paragraph(nist_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Algorithm 4: Gutmann
    story.append(Paragraph("4.4 Gutmann (Maximum Security)", heading2_style))
    gutmann_text = """
    <b>Speed:</b> ⚡ (Slowest)<br/>
    <b>Security:</b> ⚔️⚔️⚔️⚔️⚔️ (Maximum)<br/>
    <b>Passes:</b> 7<br/>
    <b>Use Case:</b> Maximum security requirements, paranoid users<br/>
    <br/>
    <b>Process:</b><br/>
    • Pass 1-4: Specific bit patterns (0x55, 0xAA, 0x92, 0x49)<br/>
    • Pass 5-7: Random data with different seeds<br/>
    • Each pass: Full file overwrite + fsync<br/>
    • Total time = 7x of simple wipe<br/>
    <br/>
    <b>Historical Context:</b> Originally designed to defeat MFM encoding<br/>
    artifacts. Modern HDDs have different encoding, but still provides<br/>
    maximum assurance against theoretical forensic recovery.<br/>
    <br/>
    <b>Time Complexity:</b> O(7n) = O(n)<br/>
    <b>Security Level:</b> Highest theoretical security for magnetic media
    """
    story.append(Paragraph(gutmann_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Algorithm 5: Crypto
    story.append(Paragraph("4.5 Cryptographic Erase (AES-256)", heading2_style))
    crypto_text = """
    <b>Speed:</b> ⚡⚡⚡⚡⚡ (Fastest)<br/>
    <b>Security:</b> ⚔️⚔️⚔️⚔️⚔️ (Maximum)<br/>
    <b>Passes:</b> 1 (XOR encryption)<br/>
    <b>Use Case:</b> SSDs, cloud storage, encrypted partitions<br/>
    <br/>
    <b>Process:</b><br/>
    1. Generate AES-256 encryption key<br/>
    2. XOR file data with encrypted key stream<br/>
    3. Original data mathematically unrecoverable<br/>
    4. Key disposal = data disposal<br/>
    <br/>
    <b>Mathematical Security:</b> If AES-256 is unbroken, data recovery<br/>
    is mathematically IMPOSSIBLE (not just practically difficult).<br/>
    <br/>
    <b>Comparison:</b><br/>
    • Overwrite-based: Data is destroyed, but recovery possible with<br/>
      forensic tools if overwrite incomplete<br/>
    • Crypto Erase: Original data NEVER exposed to unencryption;<br/>
      mathematically proven impossible to recover<br/>
    <br/>
    <b>Time Complexity:</b> O(n) with AES hardware acceleration<br/>
    <b>Security Level:</b> Mathematically impossible recovery
    """
    story.append(Paragraph(crypto_text, body_style))
    story.append(PageBreak())
    
    # 5. FRONTEND ARCHITECTURE
    story.append(Paragraph("5. FRONTEND ARCHITECTURE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("5.1 Main Window Structure", heading2_style))
    frontend_structure = """
    <b>secure_wipe_desktop.py</b> - Main PyQt6 GUI Application<br/>
    <br/>
    <b>Architecture Pattern:</b> QMainWindow + QStackedWidget<br/>
    • Central widget contains horizontal layout<br/>
    • Left sidebar: Navigation menu (QListWidget)<br/>
    • Right side: QStackedWidget with 11 pages<br/>
    • Status bar: Shows current operation status<br/>
    <br/>
    <b>Window Configuration:</b><br/>
    • Size: 1200x800 (resizable)<br/>
    • Theme: Dark (#0d1117 background)<br/>
    • Accent: Green (#00e676)<br/>
    • Font: Segoe UI, 10pt<br/>
    """
    story.append(Paragraph(frontend_structure, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("5.2 Navigation Sidebar (11 Pages)", heading2_style))
    pages = [
        "1. Dashboard - Overview, statistics, quick actions",
        "2. Secure Wipe - Main file wiping interface",
        "3. Free Space Wiper - Wipe unallocated disk space",
        "4. External Drives - USB/SD card wiping",
        "5. Batch Processing - Bulk file/folder wipe",
        "6. Scheduled Wipe - Automated wipe scheduling",
        "7. Audit & History - Complete operation logs",
        "8. Verification Reports - Post-wipe verification",
        "9. Settings - Configuration & preferences",
        "10. Legal & Compliance - Terms, compliance info",
        "11. About - Version, credits, help"
    ]
    for page in pages:
        story.append(Paragraph(f"• {page}", body_style))
    story.append(PageBreak())
    
    story.append(Paragraph("5.3 Key UI Components", heading2_style))
    components = """
    <b>File Selection</b><br/>
    • QListWidget: Multi-select, word-wrap, 280-500px height<br/>
    • Buttons: Add Files, Add Folder, Remove, Clear All<br/>
    • File count displayed dynamically<br/>
    <br/>
    <b>Algorithm Selection</b><br/>
    • QComboBox dropdown with 5 algorithms<br/>
    • Tooltip descriptions for each algorithm<br/>
    • Real-time time estimate calculation<br/>
    <br/>
    <b>Progress Tracking</b><br/>
    • QProgressBar: Overall operation progress<br/>
    • QLabel: Current file being processed<br/>
    • Speed, estimated time remaining<br/>
    <br/>
    <b>Operation Controls</b><br/>
    • Start, Pause, Cancel buttons<br/>
    • Confirmation dialogs before destructive actions<br/>
    • Warning messages for user safety<br/>
    """
    story.append(Paragraph(components, body_style))
    story.append(PageBreak())
    
    # 6. MODULE DOCUMENTATION
    story.append(Paragraph("6. MODULE DOCUMENTATION", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("6.1 Core Modules", heading2_style))
    core_modules = """
    <b>wiper_core.py</b> (300+ lines)<br/>
    Purpose: Five secure wiping algorithms<br/>
    Classes: WipeAlgorithm (enum), FileWiper<br/>
    Key Methods: wipe_file(), wipe_directory(), wipe_free_space()<br/>
    <br/>
    <b>secure_wipe_desktop.py</b> (1500+ lines)<br/>
    Purpose: Main PyQt6 GUI application<br/>
    Classes: SecureWipeApp (QMainWindow)<br/>
    Key Methods: batch_add_files(), start_wipe(), update_progress()<br/>
    <br/>
    <b>history_manager.py</b><br/>
    Purpose: Persistent wipe history storage<br/>
    Data Format: JSON with timestamps, file paths, algorithms<br/>
    Key Methods: add_record(), get_history(), export_report()<br/>
    """
    story.append(Paragraph(core_modules, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("6.2 Security & Compliance Modules", heading2_style))
    security_modules = """
    <b>audit_chain.py</b> - Tamper-proof audit logging<br/>
    Hash-chain implementation preventing log tampering<br/>
    <br/>
    <b>verification_module.py</b> - Post-wipe verification<br/>
    Confirms files are unrecoverable via hash comparison<br/>
    <br/>
    <b>certificate_generator.py</b> - Compliance certificates<br/>
    ReportLab PDF generation for compliance reports<br/>
    <br/>
    <b>crypto_utils.py</b> - Cryptographic utilities<br/>
    AES-256 encryption, SHA256 hashing, key generation<br/>
    """
    story.append(Paragraph(security_modules, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("6.3 Feature Modules", heading2_style))
    feature_modules = """
    <b>batch_processor.py</b> - Batch file processing<br/>
    Queue management, parallel processing coordination<br/>
    <br/>
    <b>scheduled_wipe.py</b> - Scheduled operations<br/>
    Windows Task Scheduler integration<br/>
    <br/>
    <b>free_space_wiper.py</b> - Unallocated space wiping<br/>
    Recovers and wipes deleted file remnants<br/>
    <br/>
    <b>external_drives.py</b> - USB/SD card support<br/>
    External drive detection and wiping<br/>
    <br/>
    <b>network_wipe.py</b> - Network device wiping<br/>
    Remote device discovery and secure wiping<br/>
    """
    story.append(Paragraph(feature_modules, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("6.4 Support & Integration Modules", heading2_style))
    support_modules = """
    <b>email_system.py</b> - Compliance report generation & sending<br/>
    <b>notification_manager.py</b> - User notifications (desktop alerts)<br/>
    <b>sound_manager.py</b> - Audio feedback for operations<br/>
    <b>login_system.py</b> - User authentication<br/>
    <b>auth_manager.py</b> - Role-based access control<br/>
    <b>update_checker.py</b> - Software update notifications<br/>
    <b>system_tray.py</b> - System tray integration<br/>
    <b>translations.py</b> - Multi-language support<br/>
    <b>legal_terms.py</b> - Terms & conditions management<br/>
    <b>monitoring_page.py</b> - Real-time operation monitoring<br/>
    <b>tamper_proof_page.py</b> - Tamper detection UI<br/>
    <b>ai_assistant.py</b> - AI-powered recommendations<br/>
    <b>algorithm_recommender.py</b> - Algorithm suggestions<br/>
    """
    story.append(Paragraph(support_modules, body_style))
    story.append(PageBreak())
    
    # 7. UI/UX SOLUTIONS
    story.append(Paragraph("7. UI/UX SOLUTIONS & FIXES", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("7.1 File List Display Issue", heading2_style))
    file_list_issue = """
    <b>Problem:</b> File names not visible in QListWidget<br/>
    <br/>
    <b>Root Causes:</b><br/>
    1. Missing color property in stylesheet<br/>
    2. Item height too small for text display<br/>
    3. No text wrapping enabled<br/>
    4. Layout stretch factor causing overlap<br/>
    <br/>
    <b>Solutions Applied:</b><br/>
    1. Added explicit color in stylesheet: color: #c9d1d9<br/>
    2. Increased min-height to 48px (from 28px)<br/>
    3. Enabled word wrap: setWordWrap(True)<br/>
    4. Changed layout stretch to 0 (no expansion)<br/>
    5. Set maximum height: setMaximumHeight(500)<br/>
    6. Added visual separator between list and buttons<br/>
    <br/>
    <b>Resulting Styles:</b><br/>
    • Dark background: #0d1117<br/>
    • Light text: #c9d1d9<br/>
    • Hover color: #00e676<br/>
    • Selection: #147EFB background<br/>
    • Item padding: 16px 18px<br/>
    • Line height: 1.5 for readability<br/>
    """
    story.append(Paragraph(file_list_issue, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("7.2 Layout & Spacing Improvements", heading2_style))
    layout_improvements = """
    <b>Changes Made:</b><br/>
    1. Icon sizes standardized to 18x18px<br/>
    2. Minimum button heights set to 36px<br/>
    3. Spacing between elements: 8px<br/>
    4. Dialog box minimum height: 120px<br/>
    5. Main window minimum: 800x600px<br/>
    <br/>
    <b>Visual Hierarchy:</b><br/>
    • Title labels: 14pt, bold, light color<br/>
    • Section labels: 11pt, #888888<br/>
    • Input fields: Dark background with border<br/>
    • Buttons: Padded, with hover effects<br/>
    """
    story.append(Paragraph(layout_improvements, body_style))
    story.append(PageBreak())
    
    # 8. THREADING & PERFORMANCE
    story.append(Paragraph("8. THREADING & PERFORMANCE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("8.1 Threading Model", heading2_style))
    threading_text = """
    <b>Problem Being Solved:</b><br/>
    Wiping large files can take significant time. Without threading,<br/>
    the UI would freeze, making the application unresponsive.<br/>
    <br/>
    <b>Solution: QThread with Signals/Slots</b><br/>
    1. WipeWorker class runs in separate thread<br/>
    2. Emits progress signals to main thread<br/>
    3. Main thread updates UI via signal handlers<br/>
    4. Non-blocking architecture<br/>
    <br/>
    <b>Implementation Pattern:</b><br/>
    • WipeWorker(QObject) with custom signals<br/>
    • progress_updated signal: emits (current, total, speed)<br/>
    • finished signal: emits success/error status<br/>
    • Main thread runs QThread: thread.start()<br/>
    • UI remains responsive during wipe operations<br/>
    """
    story.append(Paragraph(threading_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("8.2 Performance Characteristics", heading2_style))
    performance_text = """
    <b>Chunk-Based Processing</b><br/>
    • 8192 bytes (8KB) chunks read/written at once<br/>
    • Reduces memory usage for large files<br/>
    • Allows progress updates every ~8KB<br/>
    <br/>
    <b>Speed Estimates (Per Algorithm):</b><br/>
    • Simple: ~50-100 MB/sec on modern SSD<br/>
    • DoD: ~15-30 MB/sec (3x passes)<br/>
    • NIST: ~50-100 MB/sec (SSD optimized)<br/>
    • Gutmann: ~7-15 MB/sec (7x passes)<br/>
    • Crypto: ~50-100 MB/sec (AES-NI hardware)<br/>
    <br/>
    <b>Optimization Techniques:</b><br/>
    • Hardware AES acceleration (AES-NI)<br/>
    • Buffer-based I/O (not byte-by-byte)<br/>
    • Proper file system journal flushing<br/>
    • Parallel processing for batch operations<br/>
    """
    story.append(Paragraph(performance_text, body_style))
    story.append(PageBreak())
    
    # 9. SECURITY & COMPLIANCE
    story.append(Paragraph("9. SECURITY & COMPLIANCE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("9.1 Encryption & Cryptography", heading2_style))
    crypto_text = """
    <b>Algorithms Used:</b><br/>
    • AES-256: Industry standard encryption<br/>
    • SHA-256: Hash function for verification<br/>
    • secrets.token_bytes(): Cryptographically secure RNG<br/>
    • PBKDF2: Key derivation for passwords<br/>
    <br/>
    <b>Key Management:</b><br/>
    • Keys generated fresh for each operation<br/>
    • No key persistence (keys destroyed after use)<br/>
    • Hardware random number generator when available<br/>
    <br/>
    <b>Compliance Standards Supported:</b><br/>
    • GDPR: Right to erasure compliance<br/>
    • HIPAA: Protected health information destruction<br/>
    • PCI-DSS: Payment card data elimination<br/>
    • DoD 5220.22-M: Military data disposal standards<br/>
    • NIST SP 800-88: Data sanitization guidelines<br/>
    """
    story.append(Paragraph(crypto_text, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("9.2 Audit & Logging", heading2_style))
    audit_text = """
    <b>Tamper-Proof Audit Chain:</b><br/>
    • Hash-chain implementation (blockchain pattern)<br/>
    • Each log entry includes hash of previous entry<br/>
    • Modification detection: any tampering breaks chain<br/>
    <br/>
    <b>Logged Information:</b><br/>
    • Timestamp (precise to millisecond)<br/>
    • User account (Windows integrated)<br/>
    • Files/folders affected<br/>
    • Algorithm used<br/>
    • Success/failure status<br/>
    • Duration and speed<br/>
    • Device/media information<br/>
    <br/>
    <b>Audit Report Generation:</b><br/>
    • PDF certificates via ReportLab<br/>
    • Email delivery capability<br/>
    • Compliance statement generation<br/>
    • Digital signatures<br/>
    """
    story.append(Paragraph(audit_text, body_style))
    story.append(PageBreak())
    
    # 10. BUILD & DEPLOYMENT
    story.append(Paragraph("10. BUILD & DEPLOYMENT GUIDE", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("10.1 Development Setup", heading2_style))
    dev_setup = """
    <b>Step 1: Clone/Download Project</b><br/>
    • Ensure all project files are in one directory<br/>
    <br/>
    <b>Step 2: Create Virtual Environment (Optional)</b><br/>
    • python -m venv venv<br/>
    • .\\venv\\Scripts\\activate (Windows)<br/>
    <br/>
    <b>Step 3: Install Dependencies</b><br/>
    • pip install -r requirements.txt<br/>
    <br/>
    <b>Step 4: Run in Development</b><br/>
    • python secure_wipe_desktop.py<br/>
    • Opens GUI, ready for testing<br/>
    <br/>
    <b>Step 5: Build Executable</b><br/>
    • python build_exe.py<br/>
    • Generates ./dist/SecureWipe.exe<br/>
    """
    story.append(Paragraph(dev_setup, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("10.2 Build Configuration", heading2_style))
    build_config = """
    <b>build_exe.py Details:</b><br/>
    • Uses PyInstaller under the hood<br/>
    • One-file executable (all dependencies bundled)<br/>
    • Compresses Python bytecode<br/>
    • Strips unneeded symbols<br/>
    • Windows icon and version metadata included<br/>
    <br/>
    <b>Output Structure:</b><br/>
    ./dist/SecureWipe.exe (main executable)<br/>
    ./build/ (temporary build artifacts)<br/>
    """
    story.append(Paragraph(build_config, body_style))
    story.append(PageBreak())
    
    # 11. FUTURE ENHANCEMENTS
    story.append(Paragraph("11. FUTURE ENHANCEMENTS & ROADMAP", heading1_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("11.1 Planned Features", heading2_style))
    future_features = """
    <b>Version 3.0+ Roadmap:</b><br/>
    <br/>
    <b>Data Recovery Prevention</b><br/>
    • Cluster Tip Wiper: Wipe NTFS cluster tips<br/>
    • MFT Analysis: Master File Table sanitization<br/>
    • Slack Space: Wipe partition slack space<br/>
    <br/>
    <b>Advanced Scheduling</b><br/>
    • Recurring schedules (daily, weekly, monthly)<br/>
    • Smart scheduling (during off-peak hours)<br/>
    • Event-triggered wiping (USB insertion, etc.)<br/>
    <br/>
    <b>Cloud Integration</b><br/>
    • OneDrive/SharePoint cloud file destruction<br/>
    • Backup system integration<br/>
    • Version history deletion<br/>
    <br/>
    <b>Management Features</b><br/>
    • Central management console<br/>
    • Multi-device deployment<br/>
    • Remote monitoring dashboard<br/>
    <br/>
    <b>Platform Expansion</b><br/>
    • Linux/Ubuntu support<br/>
    • macOS support<br/>
    • Web-based interface<br/>
    """
    story.append(Paragraph(future_features, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("11.2 Technical Debt & Optimization", heading2_style))
    optimizations = """
    <b>Performance Improvements</b><br/>
    • C++ backend for critical algorithms (via ctypes)<br/>
    • SIMD vectorization for overwrite operations<br/>
    • GPU acceleration for crypto operations<br/>
    <br/>
    <b>Code Quality</b><br/>
    • Full unit test suite (pytest)<br/>
    • Integration tests for all algorithms<br/>
    • Security audit by third party<br/>
    • Code coverage >80%<br/>
    <br/>
    <b>User Experience</b><br/>
    • Dark/light theme toggle<br/>
    • Customizable keyboard shortcuts<br/>
    • Multi-language localization<br/>
    • Accessibility improvements (WCAG 2.1)<br/>
    """
    story.append(Paragraph(optimizations, body_style))
    
    # Final Page - Summary
    story.append(PageBreak())
    story.append(Paragraph("CONCLUSION", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    conclusion = """
    The Secure Data Wiping System represents a comprehensive solution for 
    government-grade data destruction. Built with modern Python technologies 
    (PyQt6, cryptography), it provides:<br/>
    <br/>
    ✓ Military-grade wiping algorithms (DoD, NIST, Gutmann)<br/>
    ✓ Mathematically secure crypto-erase option (AES-256)<br/>
    ✓ Complete audit trail with tamper detection<br/>
    ✓ Compliance with GDPR, HIPAA, PCI-DSS standards<br/>
    ✓ Modern, responsive UI with threading<br/>
    ✓ Enterprise-ready with batch processing<br/>
    ✓ Extensive feature set (scheduling, verification, reporting)<br/>
    <br/>
    All code follows security best practices, with proper error handling,
    logging, and validation throughout. The modular architecture enables
    future expansion and feature additions without compromising security
    or stability.
    """
    story.append(Paragraph(conclusion, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    footer = """
    <i>Document Generated: {}<br/>
    Secure Data Wiping System v2.0<br/>
    © 2024 - Professional Data Destruction</i>
    """.format(datetime.now().strftime('%B %d, %Y %H:%M:%S'))
    story.append(Paragraph(footer, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"✓ PDF Generated: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_documentation_pdf()
