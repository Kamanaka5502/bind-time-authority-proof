import json
import os

class PersistentLedger:
    def __init__(self, path="ledger.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def append(self, receipt):
        with open(self.path, "r") as f:
            data = json.load(f)
        data.append(receipt)
        with open(self.path, "w") as f:
            json.dump(data, f)

    def read_all(self):
        with open(self.path, "r") as f:
            return json.load(f)
