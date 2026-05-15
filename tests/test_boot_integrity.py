import hashlib
import os

CRITICAL_FILES = [
    "advanced_execution_field.py",
    "ci_replay_check.py"
]


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def test_boot_integrity():
    for f in CRITICAL_FILES:
        assert os.path.exists(f), f"Critical file missing: {f}"
        h = file_hash(f)
        assert isinstance(h, str) and len(h) == 64
