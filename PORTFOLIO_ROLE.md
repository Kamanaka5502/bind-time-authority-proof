# Portfolio Role — Bind-Time Authority Proof

## Control Dimension: Authority at the Consequence Boundary

This repository is a supporting proof surface within the **Elyria Systems Pre-Execution Governance** portfolio.

It establishes one non-negotiable condition beneath the flagship runtime:

> **Authority must still be valid at the exact moment protected consequence would bind.**

A request may have been authorized earlier and still be inadmissible at commit time. When standing cannot be proven at that boundary, the outcome must refuse.

## How to Navigate the Portfolio

1. **Start with the flagship runnable proof surface:** [Elyria Admission Runtime](https://github.com/Kamanaka5502/elyria-admission-runtime)
2. **Review the full portfolio hierarchy:** [Elyria Systems — Portfolio Start Here](https://github.com/Kamanaka5502/Samantha-Revita-Elyria-Systems/blob/main/PORTFOLIO_START_HERE.md)
3. **Then return here** to inspect bind-time authority, stale-standing refusal, mutation detectability, and deterministic replay posture.

## Relationship to the Flagship Runtime

```text
Elyria Admission Runtime
    → checks authority and standing before movement binds

Bind-Time Authority Proof
    → isolates why that check must happen at the consequence boundary,
      rather than being assumed from earlier approval
```

## Public / Protected Boundary

This repository is a bounded proof surface. It does not expose production authority evaluators, key management, private signing infrastructure, customer-specific policy, or protected runtime law.

> **Pre-Execution Governance category:** No valid standing at bind time, no admitted consequence.
