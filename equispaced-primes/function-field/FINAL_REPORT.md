# D3 Function-Field Farey–Mertens — FINAL REPORT (autonomous run 2026-05-16)

Run: 09:59→ (queue completed ~10:31, ~2.5h before the 13:59 deadline).
Mode: self-paced autonomous loop. Constraints honored: local-only, nothing
sent, nothing pushed, adversarial-honesty, no novelty/citation inflation.

## One-paragraph verdict

The function-field model was the project's best candidate for "new mathematics
without needing RH." It is **not** new mathematics. It is an **exact,
unconditional dictionary / Katz–Sarnak-style predictive model** — real,
honest, specialist, dictionary-tier (same tier as the D1 BCZ-cocycle landing).
The headline hope (a genuinely new RH-free variance theorem) is **correctly
closed**: by an elementary character-orthogonality duality the only
non-elementary object is exactly the Keating–Rudnick Möbius-in-progressions
variance. This was established in one session via cheap exact computations and
self-review — instead of a multi-week theorem push that would have
rediscovered Keating–Rudnick.

## What was established (calibrated, machine-verified)

| Item | Result | Label |
|---|---|---|
| **G0** | Exact FF Farey–Mertens identity `A_D(m)=Σ_{e\|m}q^{deg e}M_A(D−deg e)`; web-confirmed absent from literature | [PROVEN-exact, 477 cases] — but a 2-line Carlitz corollary; elementary |
| **G1** | For `D>deg m`, `A_D(m)=(1−q)σ_A(m)`: the char-0 RH-depth **provably vanishes** globally (`1/ζ_A` is a polynomial) | [PROVEN-exact] |
| **G2(a)** | Twisted `M_A(n,χ)`: unconditional Deligne/Weil-II √-cancellation, Katz–Sarnak-stable variance | [NUMERICAL + Deligne] |
| **Q1** | FF discrepancy = exact Birkhoff sum of `g=1−Φ·gap`; raw cocycle reproduces the char-0 non-`L²` obstruction (`c0` grows with D) — NOT a different statistic | [PROVEN-exact] + [NUMERICAL] |
| **Q1c** | Renormalized `R_D=q^D·W_D^{pf}` converges to an unconditional constant `C_FF(q)` | [PROVEN convergence] |
| **Q6 / C_FF** | **Exact closed form `C_FF(q) = (q+1)²`** (q=2→9, q=3→16, q=5→36, q=7→64). Via the FF Mikolás bilinear form `𝔅(x,y)=(1−xy/q)/((1−x)(1−y)(1−qxy))`, `b(M)=(q+1)q^{M−1}−1/q`, `Φ_D=(q^{2D+1}+1)/(q+1)`. Corrects the earlier truncation-biased "≈9.4/17/37". Elegant but elementary, dictionary-tier, no char-0 consequence. | [DERIVED + VERIFIED] (3 independent checks) |
| **§6 duality** | `Var` over residues mod Q = `Φ_A(Q)^{-1}Σ_{χ≠χ0}|M_A(n,χ)|²` ⇒ twisted variance **is** the Keating–Rudnick object | [PROVEN, inline, citation-free] |

## Self-correction (the anti-inflation norm working)

Q5 adversarial self-review caught a **self-inflicted overclaim**: an earlier
draft conflated the *elementary* untwisted `C_FF` with the *Keating–Rudnick*
twisted variance. Corrected throughout (abstract, §5, §6, bottom line). Q6
further downgraded the over-confident "`C_FF≈9.4/17/37`" to "rational,
unconditional, value open". Verdict unchanged and *strengthened*.

## Deliverables (local, internal — NOT sent/pushed)

- `D3_NOTE_DRAFT.md` — the honest unified specialist note (internally
  consistent, non-inflated, who-cares applied).
- `REVIEW.md` — adversarial self-review.
- `verify_ff_farey_mertens.py` (G0/G1), `verify_ff_g2_variance.py` (G2a),
  `verify_ff_q1_cocycle.py` (Q1a), `verify_ff_q1c_exact_mikolas.py` (Q1c),
  `verify_ff_q6_closedform.py` (Q6) + outputs.
- Memory `project_farey_forward_verdict.md` updated with the resolved verdict.

## BLOCKED-FOR-USER (require your decision / access — not done autonomously)

1. **Lock the Keating–Rudnick citation** (arXiv:1504.03444 / Algebra & Number
   Theory 10(2) 375–420 2016) from the **primary PDF** — exact theorem
   numbers, the `U(N)` `N`, the limiting matrix integral, q→∞/range
   conditions. Web/Project-Euclid access was blocked in the run. The *verdict*
   does not depend on it (the duality is self-proved), but any external use of
   §6 must lock it.
2. **Decision: ship or shelve.** `D3_NOTE_DRAFT.md` is dictionary-tier — a
   short expository note or a subsection of the Koyama-adjacent work, NOT a
   standalone advance. Your call whether to (a) fold it into the Koyama
   collaboration as an exposition section, (b) keep as an internal dictionary,
   or (c) shelve. No email/submission/push without your explicit approval.

## Recommended next steps (for the user)

- Highest value remains, as before: the **Koyama joint paper** (credibility
  anchor) and the **N·W→C / BCZ-dictionary specialist note** (D1) — both
  pre-existing, both more shippable than D3.
- D3's honest role: the *cleanest demonstration* that the RH-depth wall has no
  function-field analogue, plus an exact dictionary. Use it as supporting
  exposition, not a headline.
- Do **not** pursue a Katz-monodromy "new theorem" (G3): it would transcribe
  Keating–Rudnick.

## D4 — Steinerberger greedy-discrepancy lead: CLOSED, honest NEGATIVE

The last untouched forward lead (Aistleitner's volunteered Steinerberger
arXiv:1902.03269 connection). One primary read + classical facts refute it:
Steinerberger's energy is the **logarithmic** pairwise kernel, not the L²
discrepancy of the Sign Theorem; and equispaced points (= a prime's `{k/p}`
block, with `Π2sin(πk/p)=p`) are the **global minimizer** of log-energy
(Fejér). So under Steinerberger's actual functional the prime insertion is
energy-*optimal*, the **opposite** of a "greediness failure" — hypothesis
refuted and reversed. Decisive kill in ~10 min, no strawman probe built.
Detail: `D4_STEINERBERGER_FORMULATION.md`. Net: confirms the project's honest
map — no new bridge here; the per-step lens does not get a Steinerberger home.

## Optional spare research (deliberately NOT auto-pursued — low who-cares, inflation risk)

Exact closed form of `C_FF(q)` via the multi-pole asymptotic of the
head+boundary+`δ_D` sum; sharpen G2(a) to larger q for the `U(N)` fit; ask
whether the FF picture says anything honest about the char-0 D1 theorem-(R)
residual. All low-priority, none load-bearing. Left for an explicit user go.

---
**Bottom line:** the gated plan did its job — a clean, honest *negative on the
headline hope* plus a real exact dictionary, delivered cheaply, with one
self-caught overclaim corrected and one self-caught numerical error fixed
(the truncation bias, now resolved by the exact closed form `C_FF(q)=(q+1)²`).
The function-field Mikolás constant is exactly `(q+1)²` — an elegant,
verified, elementary fact; pleasant, but it does not change the dictionary-tier
verdict or imply anything for char-0. No breakthrough; no inflation; nothing
sent.
