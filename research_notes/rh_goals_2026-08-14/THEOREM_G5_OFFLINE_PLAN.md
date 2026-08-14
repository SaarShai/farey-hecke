# FLAGSHIP — Theorem plan: a proven off-line resonance for G_5
Opened 2026-08-14. Owner: frontier. Priority: TOP (user-directed).

## Target statement

THEOREM (computer-assisted). The even-sector Mayer–Mühlenbruch–Strömberg
transfer-operator determinant for the non-arithmetic Hecke group G_5
(λ = 2cos(π/5) = φ) has a zero s* with Re(s*) ∈ [0.4539 − δ, 0.4539 + δ]
(δ certified, excluding Re = 1/4) — i.e., a scattering resonance OFF the
line that carries every arithmetic member of the family.

Contrast partner (already certified modulo the same heuristic): q = 3, 4, 6
resonances ON Re = 1/4 at ζ(2s) zeros. Together: the rigorous core of the
arithmeticity-signature law.

## The single missing ingredient

Current winding certificates are rigorous EXCEPT the dimension-tail
inflation (geometric-contraction test + ×4 inflation — validated, unproven).
Replace it with a PROVEN truncation bound. Route: the operator is a nuclear
composition-type operator on a disk/Bergman space; branch maps send the
domain strictly inside itself with contraction ratio ρ < 1 ⇒ explicit
singular-value decay s_k ≤ C ρ^k ⇒ explicit Fredholm-determinant tail bound
|det − det_N| ≤ F(C, ρ, N) on the contour. This is the Jenkinson–Pollicott
rigorous-determinant scheme — borrow, do not reinvent (scout dispatched).

## Work items

- T-a (frontier + agent): explicit invariant disk + branch-contraction
  constants for the G_5 even-sector operator (λ=φ, MMS eq.32, sign=+1).
  Interval-verifiable geometric statements.
- T-b (frontier): the explicit tail-bound theorem with all constants;
  adversarial referee pass. Aristotle: the finite algebraic/geometric
  lemmas (branch-map inclusion inequalities; NOT the functional analysis —
  Mathlib support is thin there; the analysis is paper-proved).
- T-c (compute): rerun the G_5 winding boxes with the PROVEN tail radius
  replacing the ×4 heuristic. If boxes still certify → theorem stands.
- T-d (write-up): theorem + proof + certificates + code; the q=3/4/6
  ON-line certificates upgraded with the same bound as corollaries.

## V1 ADVERSARIAL REVIEW AMENDMENTS (2026-08-14 — binding)

Per lane_b/ADVERSARIAL_REVIEW_V1.md, THREE missing ingredients, not one:
1. **K_s divisor gate (was omitted — most dangerous).** MMS: Z_S(s) =
   det(1−L⁺)det(1−L⁻)/det(1−K_s). A det zero is a resonance ONLY IF
   det(1−K_s) ≠ 0 there. New work item T-0: extract MMS secK/Prop 2,
   compute the K_s zero set for q=5, certify det(1−K_s) ≠ 0 inside every
   winding box BEFORE claiming any resonance.
2. **Convention re-derivation.** Independent reimplementation put the pin
   at 0.4332 vs 0.4539 — re-derive the mms+ sector from MMS eq.(32)/(34)
   line-by-line before any decimal is written. Also: rename "even sector"
   → "P-symmetric (mms+) sector" (± is CF-reflection, not Maass parity).
3. Tail bound (T-a/T-b as planned) — V1 found the heuristic's contraction
   premise CONCRETELY violated at a q4 box corner (ratios rising toward
   the cap), confirming the heuristic cannot be presented as conservative.

THEOREM REFRAME (V1 §4.4): target statement is now "first rigorous
localization of a scattering resonance of a non-arithmetic finite-area
hyperbolic surface, with essential-gap content Re(s*) ≤ 1/2 − δ_gap" — not
"Re ≠ 1/4" (near-vacuous) and no pinned decimal until items 1–2 close.

## Honest risks

- The proven tail radius may be larger than the heuristic one → boxes fail
  at current N → increase N (cost grows; q=3 timings suggest tolerable).
- Prior art check running: has anyone proven a resonance location for a
  hyperbolic surface via validated numerics (Borthwick's Schottky-group
  numerics are non-rigorous displays; verify)? If someone has the method,
  we cite and still own the first Hecke/non-arithmetic instance.
- The strategic interpretation ("proof must use arithmetic") is under cold
  adversarial review — the theorem does not depend on it.
