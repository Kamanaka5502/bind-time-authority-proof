class AuthorityState:
    def __init__(self, epoch: int = 1, valid: bool = True):
        self.epoch = epoch
        self.valid = valid

    def revoke(self):
        self.valid = False
        self.epoch += 1

    def reissue(self):
        self.valid = True
        self.epoch += 1

    def snapshot(self):
        return {
            "epoch": self.epoch,
            "valid": self.valid
        }
