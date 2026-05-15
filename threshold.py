from key_manager import sign, verify

class ThresholdAuthority:
    def __init__(self, epochs, threshold):
        self.epochs = epochs
        self.threshold = threshold

    def sign_all(self):
        return [(e, sign(e)) for e in self.epochs]

    def verify_threshold(self, signatures):
        valid = sum(
            verify(epoch, sig)
            for epoch, sig in signatures
        )
        return valid >= self.threshold
