# Track 3 — Does X_Ω(Γ) generalize beyond Hecke? (2n-gon / Bouw–Möller Veech surfaces)

**Date:** 2026-06-14. **Question (from the pipeline follow-on roadmap, Path 1):** is the
support edge X_Ω(Γ) = (cusp-vertex value) a NEW LATTICE INVARIANT beyond Hecke, does the
uniform method PORT to the next Veech families (2n-gon = Δ(n,∞,∞), Bouw–Möller = Δ(m,n,∞)),
and does it detect commensurability / arithmeticity?

## VERDICT: **PARTIAL** — the *mechanism* ports cleanly; X_Ω(Γ) is **NOT a new invariant**.

- The **dynamical mechanism** "support edge of the slope-gap statistic = the value of the
  return-time at the cusp / parabolic-fixed point of the horocycle Poincaré section" **PORTS**
  to the entire triangle-group Veech family (golden L, all 2n-gons; and structurally to
  Bouw–Möller). This is genuine and is the conceptual core of the Hecke result.
- The **scalar value X_Ω(Γ) itself is NOT a new computable invariant.** It is fixed by the
  choice of horocycle-section normalization (= 1 in the canonical "shortest horizontal =
  shortest vertical saddle connection = 1" coordinates of Athreya–Chaika–Lelièvre and
  Berman et al, for *every* lattice surface). Where it varies (the Hecke-specific Taha
  normalization gives 1/λ_q³) it lies entirely in the classical **trace field ℚ(cos π/q)**
  and carries **no commensurability information beyond what the trace field already gives**.
- The **arithmeticity dichotomy does NOT acquire a new local detector** from this family.
  The Takeuchi crystallographic criterion (λ²∈ℤ ⇔ n∈{3,4,6}) is the real mechanism, and it
  is *classical*. The slope-gap *complexity* statistics (# return-time pieces, #
  non-differentiability points) grow monotonically in n for BOTH arithmetic and
  non-arithmetic surfaces (Berman et al Thm 1.3) and **do not jump at n∈{3,4,6}** — so they
  do not detect arithmeticity.

This is the same niche-trap the 2026-06-14 pipeline-target verdict diagnosed: where the edge
is real (the mechanism), it is owned/classical; where a value *could* be a new invariant, it
collapses to a normalization artifact. **Do not pursue X_Ω(Γ) as a standalone new invariant.**

---

## Oracle (validated FIRST, as required)

`code/xomega_generalize_oracle.py` — STEP A. The Hecke/Taha support edge is the **cusp-tip
value of the genuine gap-product observable** P_gen = a(a+λb)/λ on the cusp branch:
at the parabolic-fixed tip (a,b)=(1/λ,0), P_gen = (1/λ)(1/λ)/λ = **1/λ³**, matching the
project threshold X(q)=1/λ³ EXACTLY (to <1e-30) for q=3,4,5,6,7,8,12. So the dictionary
"support edge = value at the cusp/parabolic point" is correct in our own setting — the oracle.

## What the literature actually establishes (prior-art gate)

| Object | Source | Status |
|---|---|---|
| golden L = double pentagon, **Veech group Δ(2,5,∞) = Hecke H₅**, "golden-L BCZ map", return time R, 3 pieces, R≥1, smallest slope gap = 1 | Athreya–Chaika–Lelièvre [arXiv:1308.4203] | exact |
| 2n-gon O_{2n}, **Veech group Δ(n,∞,∞)**, section = 2 triangles, R = b/(x(ax+by)), **n+1 pieces**, no support at 0, # non-diff pts ~ linear in n | Berman–McAdam–Miller-Murthy–Uyanik–Wan [arXiv:2109.04495] | exact |
| general lattice surface: slope-gap distribution piecewise real-analytic, finite # non-analyticity pts, quadratic tail, **never support at 0** (Smillie–Weiss no-small-triangles) | Kumanduri–Sanchez–Wang [arXiv:2102.10069] | exact |
| Bouw–Möller S_{m,n}, **Veech group Δ(m,n,∞)** (Hooper flat model); arithmetic ⇔ specific (m,n) | Bouw–Möller; Davis–Pasquinelli–Ulcigrai | structural |
| effective slope-gap convergence | [arXiv:2409.15660] | exact |

**Prior-art check on the invariant itself:** the literature studies the slope-gap *distribution*
(its shape, non-analyticity count, tail) and the qualitative *no-small-gaps / no-small-triangles*
property. **Nobody defines "X_Ω(Γ) = the smallest-gap VALUE" as a lattice invariant** — precisely
because, as below, it is normalization-fixed to 1 and carries no surface-specific data. So there is
no prior claimant to scoop, but also no invariant there to claim.

---

## Computation 1 — support edge for the families (`xomega_generalize_oracle.py`)

- **2n-gon O_{2n}, n=3..10:** min R = **1.000000** for ALL n, attained at the corner
  (x,y)=(1,1) — the parabolic cusp point where the two length-1 shortest saddle connections
  meet. The value is *constant across the family* ⇒ carries no per-surface information.
- **golden L:** min R = 1 in ACL section coordinates (their R≥1, smallest gap = 1).

## Computation 2 — normalization artifact, proven (`xomega_normalization_proof.py`)

golden L = Hecke H₅ = Δ(2,5,∞) is **one surface** with **two different "support edges"**:
- Taha/Hecke normalization (parabolic = [[1,λ],[0,1]]): X_Ω = **1/λ³ = 0.23607**.
- ACL normalization (parabolic = [[1,1],[0,1]]): min R = **1**.

The two differ by **λ³** — a pure power of the trace. The explicit conjugation
D = diag(√(1/λ), √λ) sends [[1,λ],[0,1]] ↦ [[1,1],[0,1]], scaling slopes by 1/λ and slope-gaps
by 1/λ². Hence the bare value is fixed by the *choice of section normalization*, NOT by Γ.
**⇒ X_Ω(Γ) as a scalar is a normalization artifact.**

## Computation 3 — commensurability / arithmeticity (`xomega_commensurability.py`)

- Invariant trace field of Δ(2,q,∞) and of Δ(q,∞,∞) is **ℚ(cos 2π/q)** — the real
  commensurability invariant (Maclachlan–Reid). X_Ω^Hecke = 1/λ_q³ lives in the trace field
  ℚ(cos π/q) (degree-2 over the invariant trace field) ⇒ it is a *function of the trace*,
  giving **no new commensurability data**.
- Arithmeticity (Takeuchi 1977): Δ(2,q,∞) arithmetic ⇔ q∈{3,4,6} ⇔ λ²∈ℤ;
  Δ(n,∞,∞) arithmetic ⇔ n∈{3,4,6}. There are exactly **9 cusped triangle groups
  commensurable with PSL₂(ℤ)** (Takeuchi class I) — all arithmetic over ℚ. This is the
  *classical* dichotomy mechanism (crystallographic restriction), the same λ²∈ℤ that drives
  the project's cluster-ceiling=2 result. It is NOT new and is NOT refined by the slope-gap.
- Slope-gap **complexity** (# pieces = n+1; # non-diff pts, Berman Thm 1.3
  n/5−11 ≤ # ≤ 2n+⌊n/2⌋+1) grows **monotonically in n** for both arithmetic and
  non-arithmetic surfaces ⇒ **does not detect arithmeticity** (no jump at n∈{3,4,6}).

---

## Honest reconciliation with the project's Hecke result

The Hecke breakthrough's durable content is NOT the scalar 1/λ³ (normalization-dependent) but:
1. the **family-uniform method** (GATE-2 corridor classification → arc-coverage → the support
   edge is forced) — a real first (one-surface-per-paper → uniform), and
2. the **bridge** ergodic-ground-value = cluster onset, machine-verified.

Track 3 asked whether (1) spawns a *new invariant* / *commensurability detector*. Answer:
the *mechanism* generalizes (support edge = cusp/parabolic value, attained at the cusp, for the
whole triangle-group Veech family), so a **uniform support-edge THEOREM for the 2n-gon /
Bouw–Möller families is plausibly reachable by the same method** — but the *output* of such a
theorem is the constant 1 (artifact) or a trace-field scalar, i.e. it would be a *methods*
contribution (family-uniform slope-gap support edge), **not a new invariant and not an
arithmeticity detector**. That matches the standing strategic verdict: the value is
*methodological* (AI-math-engine / family-uniform technique), not a new pure-math object.

## Files
- `code/xomega_generalize_oracle.py` (+ `out/xomega_generalize_oracle.json`) — oracle + family min-R.
- `code/xomega_invariance_test.py` (+ `out/...json`) — normalization conventions + arith signatures.
- `code/xomega_commensurability.py` (+ `out/...json`) — invariant trace field vs X_Ω.
- `code/xomega_normalization_proof.py` (+ `out/...json`) — the λ³ artifact proof + cusp attainment.

## Do-not-rechase
- X_Ω(Γ) as a standalone new lattice invariant: **DROP** (normalization artifact / trace-field-bound).
- Slope-gap statistic as an arithmeticity detector for 2n-gon/BM: **DROP** (complexity is
  monotone in n; arithmeticity is the classical λ²∈ℤ/Takeuchi criterion, not new, not local-refined).
- Reachable & honest residual: a **family-uniform support-edge / smallest-slope-gap=cusp-value
  THEOREM** for the 2n-gon or Bouw–Möller families via the GATE-2 method = a genuine *methods*
  result (collapses the one-surface-per-paper slope-gap industry), with no new-invariant claim.
