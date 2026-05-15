from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import hashlib
import time
import threading
import os

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

LATENCY_CEILING_MS = 200
ALLOWED_CORRIDORS = {"clinical_signoff"}
LEDGER_FILE = "receipt_ledger.json"

LOCK = threading.Lock()

# --------------------------------------------------
# GLOBAL STATE
# --------------------------------------------------

RECEIPT_LOG = []
CHAIN_TIP = None
RECEIPT_INDEX = 0

# --------------------------------------------------
# PERSISTENCE
# --------------------------------------------------

def load_ledger():
    global RECEIPT_LOG, CHAIN_TIP, RECEIPT_INDEX
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            RECEIPT_LOG = json.load(f)
        if RECEIPT_LOG:
            CHAIN_TIP = RECEIPT_LOG[-1]["chain_tip_full"]
            RECEIPT_INDEX = RECEIPT_LOG[-1]["receipt_index"]

def persist_ledger():
    with open(LEDGER_FILE, "w") as f:
        json.dump(RECEIPT_LOG, f, indent=2)

# --------------------------------------------------
# DETERMINISTIC CORE
# --------------------------------------------------

def simulate(steps=5):
    state = 0
    history = []
    for i in range(steps):
        state = (state * 31 + i + 7) % 1000003
        history.append(state)
    return history

def compute_phi(history):
    return -1 + (len(history) * 0.2)

def admissibility_distance(phi):
    return max(0, -phi)

def compute_commitment(history, prior_tip):
    payload = json.dumps(history, sort_keys=True) + str(prior_tip)
    return hashlib.sha256(payload.encode()).hexdigest()

def compute_receipt_hash(receipt):
    canonical = json.dumps(receipt, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()

# --------------------------------------------------
# BOUNDARY EVALUATION
# --------------------------------------------------

class DeterministicBoundary:

    @staticmethod
    def evaluate(prior_tip):
        history = simulate(steps=5)
        phi = compute_phi(history)
        distance = admissibility_distance(phi)

        commitment = compute_commitment(history, prior_tip)

        authority_valid = phi >= 0
        decision = "EXECUTE" if authority_valid else "REFUSE"

        return {
            "history": history,
            "phi": phi,
            "distance": distance,
            "authority_valid": authority_valid,
            "decision": decision,
            "commitment": commitment
        }

# --------------------------------------------------
# REPLAY VALIDATION
# --------------------------------------------------

def replay_from_genesis():
    prior_tip = None
    for receipt in RECEIPT_LOG:
        result = DeterministicBoundary.evaluate(prior_tip)
        expected_tip = result["commitment"]

        if expected_tip != receipt["chain_tip_full"]:
            return False

        prior_tip = expected_tip
    return True

# --------------------------------------------------
# HTTP HANDLER
# --------------------------------------------------

class Handler(BaseHTTPRequestHandler):

    def respond(self, payload, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        if self.path == "/health":
            self.respond({"status": "ok"})

        elif self.path == "/receipts":
            with LOCK:
                self.respond(RECEIPT_LOG)

        elif self.path == "/replay_full":
            with LOCK:
                valid = replay_from_genesis()
            self.respond({
                "deterministic_replay_valid": valid,
                "verified_at": int(time.time())
            })

        else:
            self.respond({"error": "not found"}, 404)

    def do_POST(self):
        global CHAIN_TIP, RECEIPT_INDEX

        if self.path == "/commit":

            corridor = self.headers.get("X-Corridor")
            if corridor not in ALLOWED_CORRIDORS:
                self.respond({"error": "invalid corridor"}, 403)
                return

            client_parent = self.headers.get("X-Parent-Tip")

            with LOCK:

                # Mandatory parent enforcement
                if RECEIPT_LOG and not client_parent:
                    self.respond({"error": "parent tip required"}, 400)
                    return

                if CHAIN_TIP:
                    if client_parent != CHAIN_TIP[:16]:
                        self.respond({
                            "error": "fork detected",
                            "expected_parent": CHAIN_TIP[:16],
                            "provided_parent": client_parent
                        }, 409)
                        return

                start = time.perf_counter()
                prior_tip = CHAIN_TIP
                result = DeterministicBoundary.evaluate(prior_tip)
                elapsed_ms = (time.perf_counter() - start) * 1000

                if elapsed_ms > LATENCY_CEILING_MS:
                    result["decision"] = "ESCALATE"

                # REFUSE does not advance chain
                if result["decision"] != "EXECUTE":
                    self.respond({
                        "decision": result["decision"],
                        "reason": "admissibility failure",
                        "latency_ms": round(elapsed_ms, 3)
                    }, 403)
                    return

                RECEIPT_INDEX += 1
                CHAIN_TIP = result["commitment"]

                receipt = {
                    "receipt_index": RECEIPT_INDEX,
                    "parent_tip": prior_tip[:16] if prior_tip else None,
                    "chain_tip": CHAIN_TIP[:16],
                    "chain_tip_full": CHAIN_TIP,
                    "corridor": corridor,
                    "decision": result["decision"],
                    "authority_valid": result["authority_valid"],
                    "phi": result["phi"],
                    "admissibility_distance": result["distance"],
                    "latency_ms": round(elapsed_ms, 3),
                    "issued_at": int(time.time())
                }

                receipt["receipt_hash"] = compute_receipt_hash(receipt)

                RECEIPT_LOG.append(receipt)
                persist_ledger()

            self.respond(receipt)

        else:
            self.respond({"error": "not found"}, 404)

# --------------------------------------------------
# BOOT
# --------------------------------------------------

if __name__ == "__main__":
    load_ledger()
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Deterministic execution boundary running on port 8000")
    server.serve_forever()
