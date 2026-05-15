import hashlib


def compute_system_fingerprint(files: dict) -> str:
    combined = "".join(sorted(files.values()))
    return hashlib.sha256(combined.encode()).hexdigest()


def verify_boot(expected_fingerprint: str, files: dict) -> bool:
    current = compute_system_fingerprint(files)
    return current == expected_fingerprint
