"""
Tamper-Proof Audit Chain
SHA-256 hash chain — modifying any log entry breaks all subsequent hashes,
making tampering immediately detectable.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple

CHAIN_FILE = "data/audit_chain.json"
GENESIS_HASH = "0" * 64  # Starting hash for the first entry


def _entry_fingerprint(entry: dict, prev_hash: str) -> str:
    """Build a deterministic, ordered string for hashing."""
    fields = [
        'id', 'timestamp', 'file_path', 'file_name', 'file_size',
        'algorithm', 'success', 'operator', 'machine'
    ]
    parts = [f"prev={prev_hash}"]
    for k in fields:
        v = entry.get(k, '')
        if isinstance(v, datetime):
            v = v.isoformat()
        parts.append(f"{k}={v}")
    return "|".join(str(p) for p in parts)


def compute_entry_hash(entry: dict, prev_hash: str) -> str:
    """Return SHA-256 hex digest for one entry chained to prev_hash."""
    data = _entry_fingerprint(entry, prev_hash).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


class AuditChain:
    """Manages a tamper-evident SHA-256 hash chain over wipe history."""

    def __init__(self, chain_file: str = CHAIN_FILE):
        self.chain_file = chain_file
        self._chain: List[Dict] = []   # list of {id, prev_hash, hash}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.chain_file):
                with open(self.chain_file, 'r', encoding='utf-8') as f:
                    self._chain = json.load(f)
        except Exception:
            self._chain = []

    def _save(self):
        try:
            dirpath = os.path.dirname(self.chain_file)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            with open(self.chain_file, 'w', encoding='utf-8') as f:
                json.dump(self._chain, f, indent=2)
        except Exception as e:
            print(f"AuditChain save error: {e}")

    @property
    def last_hash(self) -> str:
        return self._chain[-1]['hash'] if self._chain else GENESIS_HASH

    def add_entry(self, entry: dict) -> str:
        """Hash and append a new wipe entry to the chain. Returns its hash."""
        prev = self.last_hash
        h = compute_entry_hash(entry, prev)
        self._chain.append({
            'id': entry.get('id', ''),
            'prev_hash': prev,
            'hash': h
        })
        self._save()
        return h

    def verify(self, history: List[Dict]) -> Tuple[bool, List[str]]:
        """
        Re-compute every hash and compare with stored chain.
        Returns (all_valid: bool, tampered_entry_ids: List[str]).
        Entries present in history but not in the chain are skipped (legacy).
        """
        chain_map = {c['id']: c for c in self._chain}
        tampered = []
        prev = GENESIS_HASH

        for entry in history:
            eid = entry.get('id', '')
            if eid not in chain_map:
                continue  # legacy entry without a chain record — skip
            c = chain_map[eid]
            if c['prev_hash'] != prev:
                tampered.append(eid)
                # Still advance using stored hash so subsequent entries can be checked
                prev = c['hash']
                continue
            expected = compute_entry_hash(entry, c['prev_hash'])
            if expected != c['hash']:
                tampered.append(eid)
            prev = c['hash']

        return len(tampered) == 0, tampered

    def rebuild_from_history(self, history: List[Dict]):
        """Rebuild entire chain from scratch (initial migration or reset)."""
        self._chain = []
        prev = GENESIS_HASH
        for entry in history:
            h = compute_entry_hash(entry, prev)
            self._chain.append({
                'id': entry.get('id', ''),
                'prev_hash': prev,
                'hash': h
            })
            prev = h
        self._save()

    def get_hash_for(self, entry_id: str) -> str:
        """Return stored hash for a given entry ID, or empty string if not found."""
        for c in self._chain:
            if c['id'] == entry_id:
                return c['hash']
        return ''

    def __len__(self) -> int:
        return len(self._chain)


_singleton: AuditChain = None


def get_audit_chain(chain_file: str = CHAIN_FILE) -> AuditChain:
    """Get singleton AuditChain instance."""
    global _singleton
    if _singleton is None:
        _singleton = AuditChain(chain_file)
    return _singleton
