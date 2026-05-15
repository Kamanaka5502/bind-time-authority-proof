from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

class Ed25519Authority:
    def __init__(self):
        self._signing_key = SigningKey.generate()
        self.verify_key = self._signing_key.verify_key

    def sign(self, message: bytes) -> bytes:
        return self._signing_key.sign(message)

    def verify(self, signed: bytes) -> bool:
        try:
            VerifyKey(self.verify_key.encode()).verify(signed)
            return True
        except BadSignatureError:
            return False
