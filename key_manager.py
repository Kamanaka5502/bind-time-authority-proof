import hashlib
import hmac
import os
import platform

KEY_FILE = "sealed.key"
SALT = b"bind-time-authority-hardware-salt"

def device_fingerprint():
    return platform.node().encode()

def initialize_key():
    if not os.path.exists(KEY_FILE):
        seed = hashlib.sha256(b"bind-time-authority-seed").digest()
        with open(KEY_FILE, "wb") as f:
            f.write(seed)

def load_root():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def derive_device_key():
    root = load_root()
    device = device_fingerprint()
    return hashlib.sha256(root + device + SALT).digest()

def sign(epoch: int):
    key = derive_device_key()
    return hmac.new(key, str(epoch).encode(), hashlib.sha256).hexdigest()

def verify(epoch: int, signature: str):
    expected = sign(epoch)
    return hmac.compare_digest(expected, signature)
