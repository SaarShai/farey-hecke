# Novel achievements — whole project, calibrated (2026-05-16)

Adversarial-honesty posture (project norm; documented #1 failure mode is
novelty/citation inflation). Every item is tagged by **what kind of novelty**
it is and **what it is NOT**. Nothing here claims RH progress or a breakthrough.
Tiers: A = genuinely novel & solid; B = correct framing, classical underneath;
C = external validation; plus honest NEGATIVES that are themselves results.

---

## TIER A — genuinely novel and solid (defensible to experts)

### A1. Verified empirical correction: `N·W(N) → C ≈ 0.66`, BOUNDED
- `W(N)=∫₀¹ E_N² ` = L² second moment of the Farey discrepancy. The working
  belief (incl. Aistleitner, in correspondence) was that `N·W(N)` grows
  (~`log N`). **It does not — it saturates to a constant ≈0.66.**
- Triple cross-verified: fast `O(N log N)` Jordan-totient method = brute
  Mikolás = Parseval; over `N=10³–3·10⁵`.
- Conditionally (RH + Mertens-variance) reduces to the
  Good–Churchhouse / Ng-2004 constant `∝ Σ_ρ |ρζ'(ρ)|⁻²`.
- **Novelty:** a verified empirical fact that *corrects the literature's
  working intuition*. **Not:** a theorem (the limit's existence is conditional).
- **Tier:** clean, citable; Experimental-Mathematics grade.

### A2. Sign Theorem — unconditional, Lean-verified
- At a prime step, primes with Mertens `M(p) ≤ −3` **strictly increase** the
  L² Farey discrepancy (`ΔW(p) > 0`).
- Unconditional; formalized in Lean 4 (0 sorries on the core gadget).
- **Novelty:** the *per-step / prime-indexed differential* framing of Farey
  discrepancy — Aistleitner (a Farey-discrepancy expert) and two independent
  web sweeps confirm this incremental view is unseen.
- **Not:** deep — elementary proof, finite/qualitative, fragile threshold;
  decorates Franel–Landau rather than extending it. No RH/crypto consequence.

### A3. The BCZ horocycle-cocycle dictionary
- The Farey counting discrepancy `E_Q` is **exactly** the Birkhoff sum of an
  explicit BCZ cocycle `g = 1 − Φ·gap`; the founding prime/composite
  dichotomy = lattice-point primitivity/visibility. Verified by exact
  arithmetic.
- **Occupies the explicit open question posed in Athreya–Cheung, IMRN 2014
  no. 10, 2643–2690, §8** ("Questions") — verified by primary-source read:
  they pose the BCZ-error ⇔ RH question and never build the cocycle.
- **Novelty:** of *formulation* — a precise dictionary the canonical
  reference flagged as open and did not build.
- **Not:** a theorem. The associated variance/CLT ("theorem (R)") is
  numerically falsified over ℚ (raw cocycle not uniformly L², α≈½,
  twist-inert). Value = the dictionary + a sharp localization of the barrier.

### A4. Exact function-field results (this session — DERIVED + VERIFIED)
- **Exact F_q[t] Farey–Mertens identity:** `A_D(m)=Σ_{e|m monic} q^{deg e}
  M_A(D−deg e)`. Web-confirmed absent from the literature. (Elementary: a
  2-line Carlitz-Ramanujan corollary.)
- **Exact global trivialization:** for `D>deg m`, `A_D(m)=(1−q)σ_A(m)` — the
  char-0 "RH-depth" *provably vanishes* in `F_q[t]` (because `1/ζ_A` is a
  polynomial). The sharpest possible statement that the RH-depth wall has no
  global function-field analogue.
- **Exact closed form `C_FF(q) = (q+1)²`** for the function-field Mikolás
  second-moment constant. Derived via a clean Euler-product / bilinear
  reduction; verified three independent ways (q=2→9, 3→16, 5→36, 7→64). Also
  *corrected a numerical error* (earlier truncation-biased "≈9.4/17/37").
- **Novelty:** exact, clean, web-confirmed-absent. **Not:** deep — elementary
  (`M_A`-constant collapse); dictionary-tier; no char-0 / RH consequence.

---

## TIER B — correct organizing framing, classical underneath

### B1. The founding per-step differential lens
- `f ↦ e(2πif)` on the circle: a **prime inserts only-new equally-spaced
  points** (every `k/p` reduced), a **composite always re-traces**. This
  overlap structure *is* the Ramanujan sum `c_n(m)`, the geometric origin of
  why Möbius/Mertens governs Farey discrepancy.
- Exact spectral identity `A_N(m)=Σ_{d|m} d·M(⌊N/d⌋)`; prime-step increment
  `ΔA(m)=−1+p·𝟙[p|m]`.
- **Novelty:** the *organizing lens* / per-step differential viewpoint
  (Aistleitner + web confirm unseen as such). **Not:** the underlying facts
  (reduced⇔coprime, roots of unity, Ramanujan 1918) are classical; this is
  the right *picture*, not a new theorem.

---

## TIER C — external validation (real achievement, not a math result)

### C1. Double-verified Koyama replication to ~1.3·10¹³
- Rigorously double-verified replication of the Aoki–Koyama Mertens /
  "Dominance of −1" phenomenon to ~`1.3·10¹³`; a live joint-paper invitation
  from Prof. Shin-ya Koyama (credible analytic number theorist), with the
  user as co-author.
- **The strongest external validation in the project.** A real, collaborative,
  externally-credible track.

---

## Honest NEGATIVES that are themselves contributions

- **Function-field route ⇒ Keating–Rudnick.** The non-trivial twisted object
  is, by an *elementary character-orthogonality duality*, exactly the
  Keating–Rudnick Möbius-in-progressions variance — so there is **no new
  RH-free theorem there**. A cleanly settled negative (saved a multi-week
  rediscovery).
- **Steinerberger greediness-failure hypothesis: refuted and reversed.**
  Steinerberger's energy is logarithmic, not L²; equispaced prime blocks are
  log-energy *optimal* (Fejér/cyclotomic), the opposite of a failure.
- **Internal deflations (retracted overclaims):** Δ-machine "novelty" (it is a
  classical Mellin–Perron contour shift, expository), unconditional off-central
  H1 (needs GRH), B≥0 (disproved), "Annals 2/3π" (self-collapsed). Recording
  these *as retractions* is part of the project's integrity.

---

## What is explicitly NOT claimed

No progress on the Riemann Hypothesis (all results are downstream of the
known Franel–Landau equivalence; RH-glamour = zero). No breakthrough. No
"new mathematics" in the strong sense. No practical/crypto application. Every
Tier-A item is Experimental-Mathematics / specialist-note grade. The genuine
center of gravity remains the **Koyama collaboration**.

---

## One-paragraph external-facing summary (honest)

A program studying the Farey sequence through a **per-step differential
lens** (prime vs. composite fraction insertion). Concrete outputs: a
verified empirical correction to the second-moment asymptotic
(`N·W(N)→C≈0.66`, bounded, not growing); an unconditional, Lean-verified
**Sign Theorem** for prime-step discrepancy increments; an exact
**BCZ-cocycle dictionary** occupying an open question explicitly posed in
Athreya–Cheung (IMRN 2014, §8); and an exact **function-field model**
(`C_FF(q)=(q+1)²`) showing the RH-depth wall has no global function-field
analogue. Plus a double-verified large-scale numerical replication
underpinning a joint paper with S. Koyama. All Experimental-Mathematics /
specialist tier; no RH claims.
