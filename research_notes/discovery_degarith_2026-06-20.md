# Degree-of-Arithmeticity from Resonance Rigidity — discovery scout (2026-06-20)

**Aim 3.** Classical arithmeticity is binary (Takeuchi: Hecke G_q arithmetic iff q∈{3,4,6,∞}).
Our certified even-sector resonance-geometry produces a NUMBER — the standard deviation of
the real parts (Re) of the even resonances. Question: is `Re-std` a genuine *continuous*
"degree-of-arithmeticity" invariant with a sharp law, or does it COLLAPSE to known
trace-field / discriminant data (= a re-encoding, not new)?

## COMPUTED data (certified, python-flint Arb balls, 400 bits)

From `code/out/resonance_geometry.json` and `code/out/resonance_g7.json` (re-checked here):

| surface | arith? | deg Q(2cos π/q) | n resonances | Re-std | Re-range |
|--------|--------|------|----|----------|----------|
| q=3 (PSL₂ℤ) | YES | 1 | 8 | 6.5e-14 | 2.3e-13 |
| G_5 (golden) | no | 2 | 8 | 0.029986 | 0.0855 |
| G_7 | no | 3 | 12 | 0.102922 | 0.3307 |

- q=3 verified: even resonances sit on Re=1/4 to ~1e-14 (they ARE the Riemann zeros:
  det(1−L⁺_s)=0 ⟺ ζ(2s)=0; from prior certified work `zeta_cert_q3.py`).
- G_5/G_7 are genuine off-line scattering poles (Phillips–Sarnak dissolved cusp forms),
  all |det|<1e-14 N-stable.
- Monotone: 0 < 0.030 < 0.103. G_5 vs G_7 differ at ~3.1σ (sampling SE of std with n=8,12).

## SHARP CONJECTURE (candidate)

Define `R(Γ) := std{ Re(s) : s an even-sector scattering resonance of Γ }`
(rigidity defect; R=0 ⟺ all even resonances on a vertical line).

**Conjecture A (separation).** For Hecke G_q, R(G_q)=0 ⟺ q∈{3,4,6} (arithmetic);
R(G_q)>0 otherwise. I.e. the rigidity defect is an arithmeticity DETECTOR.

**Conjecture B (growth law / the sharp, falsifiable part).** Among NON-arithmetic Hecke
groups, R(G_q) is an increasing function of the **trace-field degree**
d(q)=deg Q(2cos π/q)=φ(2q)/2, NOT of q directly. Concretely the data fit
R ≈ c·(d−1) with c≈0.04–0.05 (R: d=2→0.030, d=3→0.103 gives c≈0.036 and a
super-linear hint). Sharp predictions below.

## THE BRUTAL COLLAPSE TEST (does R just re-encode known data?)

This is the make-or-break. With ONLY q∈{3,5,7} the degrees d∈{1,2,3} are in bijection
with q, so R is *trivially* a function of d on this sample — **3 points cannot
distinguish a genuine invariant from a re-encoding of degree.** Honest verdict on the
current evidence: **UNDISCRIMINATED.**

But there IS a decisive, computable discrimination test, because trace-field degree is
*degenerate* across Hecke q (d(q)=φ(2q)/2):

- **d=2:** q=4 (ARITH), q=5 (non-arith), q=6 (ARITH).
- **d=3:** q=7, q=9 (both non-arith).
- **d=4:** q=8, q=10, q=12, q=15 (all non-arith).

Two consequences make R potentially NON-collapsing:

1. **R is provably NOT a function of degree alone IF Conjecture A holds.** q=4, q=5, q=6
   all have d=2, yet A predicts R(q=4)=R(q=6)=0 but R(q=5)=0.030. A degree-2 number
   cannot take both values. So *if* the arithmetic G_4, G_6 give rigid lines, R carries
   information orthogonal to the trace field. (Note degree ALSO fails as a detector:
   d=2 mixes arithmetic and non-arithmetic — so R, if it works, is genuinely finer.)

2. **Within-degree test.** q=7 and q=9 share d=3. If R(q=9)≈R(q=7)≈0.10, R tracks
   degree (supports B, weak novelty — it's the degree in disguise). If R(q=9) differs
   markedly from R(q=7), R sees the **discriminant / regulator**, not just degree —
   strong novelty. min-poly discriminants: q=5→5, q=7→49, and q=9 (a cubic-field q,
   trace field Q(2cos π/9), disc of x³−3x+1 is 81). A disc-driven law would predict
   R(q=9) ≠ R(q=7) despite equal degree.

**Falsifiable predictions (each a single certified run, ~45 min via the existing
Arb engine which already supports q=4,5,6,7,9):**
- P1: R(G_4)=R(G_6)=O(1e-13) (rigid, arithmetic) despite d=2. [tests A, non-collapse]
- P2: R(G_9)∈[0.08,0.12] (≈R(G_7)) if degree-driven; OR R(G_9)≉R(G_7) if disc-driven.
- P3: R(G_8) > R(G_7) (d=4>3).
- A counterexample to A: any arithmetic G_q (q=4,6) with R≫0, or non-arith with R=0.

## NOVELTY — adversarial scan (PARAMOUNT)

- **The phenomenon is OWNED (Phillips–Sarnak).** "Non-arithmetic ⇒ cusp forms dissolve
  into off-line resonances; arithmetic ⇒ resonances stay on the line" is exactly
  Phillips–Sarnak (1985) + the deformation/Fermi-golden-rule program
  (Petridis–Risager arXiv:1003.2820; Wolpert; Sarnak's "rare" Maass-form heuristic).
  The off-line *vs* on-line dichotomy is NOT new.
- **What is NOT in the literature (verified by web scan):** *quantifying* the dissolution
  as a single scalar R = Re-std and proposing it as a **continuous, computable
  degree-of-arithmeticity with a degree/discriminant law**. The Phillips–Sarnak
  literature treats dissolution qualitatively (does a given form dissolve? at what rate
  under a 1-parameter deformation?) — the Fermi-golden-rule "rate" is a *deformation
  derivative*, NOT a static invariant of one fixed surface, and is not tied to the
  trace-field degree. No source found defining R(Γ) or conjecturing R ↑ with d.
- **Owned-detector graveyard (this project's history):** Luo–Sarnak bounded-clustering,
  Geninska–Leuzinger, Takeuchi — all *trace-set/spectral* arithmeticity detectors, and
  all BINARY. R is continuous and in the *resonance-geometry* category, so it is not
  literally any of these. BUT: if R collapses to d(q) (Conjecture B with degree-driven
  P2), it is just φ(2q)/2 re-encoded = OWNED (trace field, Takeuchi-adjacent). The
  novelty survives ONLY if P1 holds (R⊥degree, since d=2 splits arith/non-arith) AND/OR
  the disc-driven branch of P2 holds.

**Honest novelty verdict: PARTLY-OWNED, novelty CONTINGENT on P1.**
- The dichotomy: OWNED (Phillips–Sarnak).
- R as a scalar invariant + the law: genuinely un-stated in the literature, BUT
  un-discriminated from "re-encoding of trace-field degree" on the current 3 points.
- The ONE thing that would make it indisputably new: P1 (arithmetic G_4,G_6 rigid at
  d=2 while non-arith G_5 scatters at d=2) — because then R separates surfaces that
  trace-field degree CANNOT, i.e. R is strictly finer than the degree. This is the
  decisive experiment and it has NOT been run.

## CAVEATS (do not oversell)

1. **q=3 is a different object.** Its "resonances" are literal Riemann zeros (ζ(2s)),
   so R(q=3)=0 is RH-rigidity of an arithmetic L-function, not the same scattering-pole
   object as G_5/G_7. The 3-point "law" interpolates across object types — the rigid
   endpoint is arithmetic-L, the scattered points are genuine resonances. Cleaner to
   anchor the arithmetic end with G_4 or G_6 (true Hecke, still arithmetic) — exactly
   what P1 does.
2. **n=8,12 resonances only**, low windows (Im≲22). std is a small-sample estimator
   (SE≈std/√(2n)); the *value* of R is not yet a converged invariant — need more
   resonances / higher windows for a stable number. The ORDERING (0<0.030<0.103) is
   robust (~3σ); the LAW's functional form is not pinned.
3. **3 data points, degrees in bijection with q** ⇒ cannot fit/falsify B yet. The whole
   discrimination rests on running q=4,6,9 (un-run this session — each ~45 min on the
   Arb engine; the run_resonance_*.py scripts are q-specialized and would need light
   adaptation, the underlying `zeta_cert_rosen.py` already parameterizes q incl. 4,6).
4. **Resonance-set definition is window-/algorithm-dependent** (which poles are "kept",
   N-stability cut). R could be sensitive to the cutoff; needs a canonical definition
   (e.g. all even resonances with Im in a fixed normalized window) before it's a true
   invariant.

## BOTTOM LINE

A sharp, falsifiable conjecture (A: R=0 ⟺ arithmetic; B: R grows with trace-field
degree among non-arith) is on the table, with a concrete decisive experiment (P1: do
arithmetic G_4,G_6 stay rigid at degree 2 while non-arith G_5 scatters?). The underlying
dichotomy is Phillips–Sarnak (OWNED). The scalar invariant R and its degree/discriminant
law are not in the literature, but on present evidence are UNDISCRIMINATED from a
re-encoding of the trace-field degree. **Verdict: promising but novelty-contingent — do
NOT claim a new invariant until P1 is run.** The single most valuable next computation is
G_4 (or G_6) even-resonance geometry.

### Sources (web-verified)
- Phillips–Sarnak dissolving cusp forms / off-line resonances for non-arithmetic
  surfaces — framework confirmed via Petridis–Risager, "Dissolving cusp forms: Higher
  order Fermi's Golden Rules," arXiv:1003.2820 (Mathematika 2013).
- Deformations of Maass forms / cusp-form disappearance — arXiv:math/0302214; Wolpert
  "Disappearance of cusp forms in special families."
- Distribution of resonances near the critical line for hyperbolic surfaces —
  arXiv:1305.4850 (non-arith resonances NOT lined up vs arith lined up — qualitative).
- Takeuchi arithmeticity of Hecke triangle groups (q∈{3,4,6,∞}) — standard; trace field
  Q(2cos π/q), degree φ(2q)/2.
- (UNVERIFIED that any source defines R=Re-std as an invariant or conjectures R↑degree —
  web scan found none.)
