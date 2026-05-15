import hashlib
import hmac

SECRET_KEY = b"bind-time-root-key"


def sign_root(root_hash: str) -> str:
    return hmac.new(SECRET_KEY, root_hash.encode(), hashlib.sha256).hexdigest()


def verify_root(root_hash: str, signature: str) -> bool:
    expected = sign_root(root_hash)
    return hmac.compare_digest(expected, signature)
