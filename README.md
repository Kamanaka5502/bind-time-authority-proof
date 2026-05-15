<p align="center">
  <img src="assets/holographic-boundary-banner.svg" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Execution-Bind--Time%20Enforced-00ffcc?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cryptography-Ed25519-7d5fff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Ledger-Merkle%20Sealed-ff00aa?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Corridors-Isolated-00aaff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Boot-Fail--Closed-ff3b3b?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Replay-Deterministic-00ff88?style=for-the-badge" />
</p>

# Bind-Time Authority Fabric

Deterministic execution-boundary enforcement with cryptographic standing validation.

---

## Core Thesis

Execution permission does not persist.
Standing must be proven at the moment consequence would bind.

Drift is continuous.
Binding is discrete.
Authority collapses at commit.

---

## Visual Surfaces

<p align="center">
  <img src="assets/merkle-lattice.svg" width="80%" />
</p>

<p align="center">
  <img src="assets/corridor-isolation.svg" width="80%" />
</p>

<p align="center">
  <img src="assets/key-lineage.svg" width="80%" />
</p>

---

## Hardened Execution Model

✔ Asymmetric Authority Keys (Ed25519)
✔ Epoch Rotation
✔ Commit-Bound Attestation
✔ Merkle Ledger Compression
✔ Multi-Corridor Isolation
✔ Fail-Closed Boot Verification
✔ Deterministic Replay
✔ Fork Detection

---

## Invariants

**I1 — Bind-Time Authority Collapse**  
Authority mismatch at commit forces REFUSE.

**I2 — Deterministic Replay**  
Identical state produces identical decision and ledger root.

**I3 — No Resurrection Without Reissue**  
Authority cannot recover implicitly from geometric correction.

**I4 — Fork Detectability**  
Ledger mutation is provably detectable.

---

## Security Posture

Fail-closed by default.

If authority cannot be proven,
execution does not proceed.

---

<p align="center">
  <img src="https://img.shields.io/badge/Integrity-Commit--Sealed-00ffe0?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Hardened%20Boundary%20Fabric-00ffcc?style=for-the-badge" />
</p>
