# Bind-Time Authority Substrate

## Problem
Operational continuity does not guarantee standing.

## Enforcement Model
- Manifold admissibility F(x)
- Capacity gating Phi
- Epoch-bound authority
- Sealed HMAC signing
- Quorum extension

## Collapse Rule
Consequence binds iff:
- Authority valid
- Epoch matches
- Signature verifies
- Manifold satisfied
- Capacity positive

## Determinism
Replay under identical state must produce identical chain.

## Resurrection Prevention
Authority recovery requires epoch increment and new signed token.

## Fork Detection
Commit chain mutation produces hash divergence.

## Stress Stability
Monte Carlo invariant validation.

