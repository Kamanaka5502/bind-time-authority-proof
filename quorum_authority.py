from key_manager import sign, verify

class QuorumAuthority:
    def __init__(self, epochs):
        self.epochs = epochs  # list of authority epochs

    def sign_all(self):
        return [sign(e) for e in self.epochs]

    def verify_all(self, signatures):
        return all(
            verify(epoch, sig)
            for epoch, sig in zip(self.epochs, signatures)
        )
