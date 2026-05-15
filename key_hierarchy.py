import os
import hashlib
import hmac

class KeyHierarchy:
    def __init__(self, root_key: bytes = None):
        self.root_key = root_key or os.urandom(32)

    def derive_epoch_key(self, epoch: int) -> bytes:
        return hmac.new(self.root_key, str(epoch).encode(), hashlib.sha256).digest()

    def rotate_root(self):
        self.root_key = os.urandom(32)
