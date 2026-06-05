---
schema_version: 1
title: "Conjecture B+ direct counterexamples — p=237733 and p=243799"
date: 2026-05-10
type: result
tier: working
confidence: 0.98
sources:
  - handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md
  - handoff-2026-05-09-followup/B_geq_0_identity_audit_FINAL.md
  - handoff-2026-05-09-followup/MERTENS_LB_MR_disproof.md
  - handoff-2026-05-09-followup/B_plus_direct_verify.c
  - handoff-2026-05-09-followup/B_plus_direct_verify_237733.out
  - handoff-2026-05-09-followup/B_plus_direct_verify_243799.out
  - experiments/B_VERIFY_243799.md
tags: [farey, b-plus, mertens-restricted, counterexample, cross-term, direct-verification]
---

# Conjecture B+ direct counterexamples

## Bottom line

**Conjecture B+ in the Lean-canonical form is false.**

The statement killed here is:

`B(p) = 2 * Σ_{f ∈ F_{p-1}} D_{p-1}(f) * δ_p(f) > 0`

for every prime `p` with `M(p) <= -3`, where `D_N(f) = fareyRank_N(f) - |F_N| f` and `δ_p(a/b) = a/b - frac(pa/b)`.

Direct streaming verification gives two Mertens-restricted counterexamples:

| p | M(p) | T(p-1) | |F_{p-1}| | B(p) | B/C | verdict |
|---:|---:|---:|---:|---:|---:|---|
| 237,733 | -20 | +6.657511751192 | 17,178,971,883 | -3.018492026640170e10 | -10.543163714952145 | FAIL |
| 243,799 | -3 | -0.834778256610 | 18,066,862,385 | -9.190201299936827e9 | -3.052438040867344 | FAIL |

So the post-May-9 status is stronger than "SP-2's Mertens sufficient condition failed." The actual `B(p)>0` positivity claim fails at explicit primes in the Mertens-restricted domain.

## Verification

Command, run from `primes-equispaced/handoff-2026-05-09-followup/`:

```bash
cc -O3 -march=native -o B_plus_direct_verify B_plus_direct_verify.c -lm
./B_plus_direct_verify 237733 | tee B_plus_direct_verify_237733.out
./B_plus_direct_verify 243799 | tee B_plus_direct_verify_243799.out
```

The verifier first checks the Lean `native_decide` anchors in `B_geq_0_identity_audit_FINAL.md`:

| p | expected B(p) | result |
|---:|---:|---|
| 5 | -2/9 | OK |
| 11 | -55/36 | OK |
| 13 | 271/385 | OK |
| 19 | 2905619/680680 | OK |
| 23 | 14608817/6348888 | OK |

This pins the C implementation to the Lean-canonical `crossTerm`, not to the rejected Bern/Saw displacement.

For `p=243799`, the new verifier reproduces the old March computation in `experiments/B_VERIFY_243799.md`:

`B(p) = -9.190201299936827e9`

The diagnostic `C` differs by `+1` from the March file because the new verifier includes the harmless boundary `f=1`, where `δ=1` but `D=0`; `B(p)` is unchanged.

## Relation to prior May 9 state

May 9 had already shown:

- universal `(MERTENS-LB)` is false;
- Mertens-restricted `(MERTENS-LB-MR)` is false, first flip at `p=237733`;
- the R1 algebraic equivalence `B+ <=> S_ψ(p) < B0(p-1)` remains valid.

This continuation closes the remaining ambiguity: the first MR flip is not merely a failed sufficient condition. At `p=237733`, the canonical cross term itself is negative.

## Consequences

- **Retract:** "Conjecture B+ Mertens-restricted survives" and "confidence 0.80/0.85".
- **Drop:** SP-1a / SP-2 routes as B+ proof programs. They may still be useful as identities, but they no longer prove a true positivity statement.
- **Keep:** R1, SP-1a, and SP-2 exact identities as theorem-grade algebraic artifacts.
- **Reframe:** Paper B can retain these identities and counterexamples as a negative theorem / failure map, not as a positivity conjecture.
- **Next research target:** characterize sign clusters of `B(p)` among Mertens-restricted primes and explain why `T(p-1)` and `B(p)` decouple (`p=243799` has `T(p-1)<0` but `B(p)<0`).

## Confidence

Aggregate confidence: **0.98**.

Evidence:

- Lean anchor values match at 5/5 primes.
- `p=237733` has a very large negative margin: `B/C = -10.54`.
- `p=243799` independently reproduces the prior March counterexample.
- `M(p)` values are computed by integer Mobius sieve in the same verifier.

Residual risk:

- The large-prime computation is floating-point streaming, not exact rational. The negative margins are `1e9` to `1e10`, far beyond plausible double/Kahan summation noise for this loop.
