"""
ai_assistant.py - AI-Powered Smart Recommendations for Secure Wipe
Provides intelligent algorithm suggestions and anomaly detection
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path


# ─── Algorithm Profiles ──────────────────────────────────────────────────────
ALGORITHMS = {
    "dod":     {"name": "DoD 5220.22-M",     "passes": 7,  "security": "High",    "speed": "Medium",  "hdd_ok": True,  "ssd_ok": False},
    "nist":    {"name": "NIST SP 800-88",     "passes": 1,  "security": "High",    "speed": "Fast",    "hdd_ok": True,  "ssd_ok": True},
    "gutmann": {"name": "Gutmann (35-pass)",  "passes": 35, "security": "Maximum", "speed": "Slow",    "hdd_ok": True,  "ssd_ok": False},
    "crypto":  {"name": "Cryptographic Erase","passes": 1,  "security": "High",    "speed": "Fastest", "hdd_ok": True,  "ssd_ok": True},
    "simple":  {"name": "Single Pass Zero",   "passes": 1,  "security": "Basic",   "speed": "Fastest", "hdd_ok": True,  "ssd_ok": True},
}

# ─── File Sensitivity Rules ───────────────────────────────────────────────────
FILE_CATEGORY = {
    # High-sensitivity: financial, medical, legal
    "high": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv", ".db", ".sqlite",
             ".mdb", ".accdb", ".key", ".pfx", ".p12", ".pem", ".enc"],
    # Medium: media, work files
    "medium": [".mp4", ".mov", ".avi", ".mkv", ".pptx", ".ppt", ".zip", ".rar",
               ".7z", ".tar", ".gz", ".py", ".js", ".java", ".cpp", ".cs"],
    # Low: temp/cache/logs
    "low": [".tmp", ".log", ".bak", ".cache", ".lnk", ".ini", ".cfg", ".txt"],
}


def _categorize_file(file_path: str) -> str:
    """Return 'high', 'medium', or 'low' sensitivity for a file."""
    ext = Path(file_path).suffix.lower()
    for cat, exts in FILE_CATEGORY.items():
        if ext in exts:
            return cat
    return "medium"  # unknown → treat as medium


def _detect_drive_type(file_path: str) -> str:
    """
    Detect if the drive containing file_path is SSD or HDD.
    Returns 'ssd', 'hdd', or 'unknown'.
    """
    try:
        drive = Path(file_path).anchor  # e.g. 'C:\\'
        drive_letter = drive.replace("\\", "").replace("/", "").upper()  # 'C:'

        result = subprocess.run(
            ["powershell", "-Command",
             f"Get-PhysicalDisk | Where-Object {{$_.DeviceId -eq "
             f"(Get-Partition -DriveLetter '{drive_letter[0]}').DiskNumber}} | "
             f"Select-Object MediaType"],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.lower()
        if "ssd" in output:
            return "ssd"
        elif "hdd" in output or "hard" in output:
            return "hdd"
    except Exception:
        pass
    return "unknown"


def _file_size_mb(file_path: str) -> float:
    """Return file size in megabytes."""
    try:
        return os.path.getsize(file_path) / (1024 * 1024)
    except Exception:
        return 0.0


# ─── Core AI Recommender ─────────────────────────────────────────────────────

def recommend_algorithm(file_path: str) -> dict:
    """
    Analyse file_path and return the best wipe algorithm with reasoning.

    Returns:
        {
          "algorithm":  "nist",          # key matching ALGORITHMS dict
          "name":       "NIST SP 800-88",
          "confidence": 92,              # 0-100 %
          "reasons":    ["SSD detected", "..."],
          "warnings":   ["..."],         # optional concerns
          "file_info":  {...},           # diagnostics
        }
    """
    reasons  = []
    warnings = []
    score    = {}   # algo_key → score

    # ── Context analysis ──────────────────────────────────────────
    sensitivity  = _categorize_file(file_path)
    drive_type   = _detect_drive_type(file_path)
    size_mb      = _file_size_mb(file_path)
    ext          = Path(file_path).suffix.lower()

    # ── Scoring rules ─────────────────────────────────────────────

    # SSD: overwrite-based passes ineffective → prefer NIST or Crypto
    if drive_type == "ssd":
        score["nist"]    = score.get("nist",    0) + 40
        score["crypto"]  = score.get("crypto",  0) + 35
        score["simple"]  = score.get("simple",  0) + 10
        score["dod"]     = score.get("dod",     0) - 20
        score["gutmann"] = score.get("gutmann", 0) - 30
        reasons.append("💾 SSD detected — multi-pass algorithms are ineffective on SSDs due to wear-leveling.")
        warnings.append("⚠️ Gutmann & DoD are NOT recommended for SSDs; NIST SP 800-88 is the industry standard.")
    elif drive_type == "hdd":
        score["dod"]     = score.get("dod",     0) + 35
        score["gutmann"] = score.get("gutmann", 0) + 20
        score["nist"]    = score.get("nist",    0) + 25
        reasons.append("🖴 Traditional HDD detected — multi-pass overwriting is effective.")
    else:
        score["nist"]   = score.get("nist",   0) + 20
        score["dod"]    = score.get("dod",    0) + 20
        reasons.append("❓ Drive type unknown — recommending a universal standard.")

    # Sensitivity-based scoring
    if sensitivity == "high":
        score["dod"]     = score.get("dod",     0) + 30
        score["gutmann"] = score.get("gutmann", 0) + 25
        score["nist"]    = score.get("nist",    0) + 20
        score["simple"]  = score.get("simple",  0) - 30
        reasons.append(f"🔴 High-sensitivity file type ({ext}) — strong wiping is recommended.")
    elif sensitivity == "medium":
        score["dod"]    = score.get("dod",    0) + 20
        score["nist"]   = score.get("nist",   0) + 20
        score["simple"] = score.get("simple", 0) + 5
        reasons.append(f"🟡 Medium-sensitivity file ({ext}) — standard military wipe is sufficient.")
    else:  # low
        score["simple"] = score.get("simple", 0) + 40
        score["nist"]   = score.get("nist",   0) + 10
        reasons.append(f"🟢 Low-sensitivity file ({ext}) — a quick single-pass wipe is adequate.")

    # File size scoring
    if size_mb > 1000:         # >1 GB
        score["simple"]  = score.get("simple",  0) + 15
        score["crypto"]  = score.get("crypto",  0) + 15
        score["gutmann"] = score.get("gutmann", 0) - 20
        reasons.append(f"📦 Large file ({size_mb:.0f} MB) — fast algorithms save significant time.")
    elif size_mb < 1:          # <1 MB
        score["gutmann"] = score.get("gutmann", 0) + 10
        reasons.append(f"📄 Small file ({size_mb:.2f} MB) — maximum security is feasible here.")

    # ── Pick winner ───────────────────────────────────────────────
    best_key = max(score, key=score.get)
    best_info = ALGORITHMS[best_key]

    # Normalise confidence (0-100)
    vals = list(score.values())
    min_v, max_v = min(vals), max(vals)
    raw = score[best_key]
    confidence = int(((raw - min_v) / max((max_v - min_v), 1)) * 60 + 40)
    confidence = min(confidence, 99)

    return {
        "algorithm":  best_key,
        "name":       best_info["name"],
        "confidence": confidence,
        "reasons":    reasons,
        "warnings":   warnings,
        "file_info": {
            "path":        file_path,
            "size_mb":     round(size_mb, 2),
            "extension":   ext,
            "sensitivity": sensitivity,
            "drive_type":  drive_type,
        },
    }


# ─── Anomaly Detection ────────────────────────────────────────────────────────

ANOMALY_THRESHOLDS = {
    "batch_file_count":   50,    # More than 50 files at once
    "large_file_mb":    5000,    # Single file > 5 GB
    "total_batch_gb":     20,    # Total batch data > 20 GB
    "system_path_keywords": [
        "windows", "system32", "program files", "program files (x86)",
        "appdata", "boot", "recovery", "drivers",
    ]
}


def detect_anomalies(file_paths: list) -> list:
    """
    Check a list of files about to be wiped for suspicious patterns.

    Returns a list of human-readable warning strings (empty = all clear).
    """
    alerts = []

    # Count anomaly
    if len(file_paths) > ANOMALY_THRESHOLDS["batch_file_count"]:
        alerts.append(
            f"⚠️ LARGE BATCH: {len(file_paths)} files selected at once. "
            f"Verify this is intentional before proceeding."
        )

    total_bytes = 0
    for fp in file_paths:
        try:
            size = os.path.getsize(fp)
            total_bytes += size

            # Individual large file
            if size > ANOMALY_THRESHOLDS["large_file_mb"] * 1024 * 1024:
                alerts.append(
                    f"⚠️ LARGE FILE: '{os.path.basename(fp)}' "
                    f"({size/(1024**3):.1f} GB) — double-check before wiping."
                )

            # System path detection
            fp_lower = fp.lower()
            for kw in ANOMALY_THRESHOLDS["system_path_keywords"]:
                if kw in fp_lower:
                    alerts.append(
                        f"🚨 SYSTEM PATH DETECTED: '{fp}' looks like a system file. "
                        f"Wiping system files may cause OS damage!"
                    )
                    break

        except Exception:
            pass

    # Total data anomaly
    total_gb = total_bytes / (1024 ** 3)
    if total_gb > ANOMALY_THRESHOLDS["total_batch_gb"]:
        alerts.append(
            f"⚠️ HIGH DATA VOLUME: Total batch is {total_gb:.1f} GB. "
            f"Ensure you have backups of anything important."
        )

    return alerts
