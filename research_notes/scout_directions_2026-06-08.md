# Scout tests of the three expansion directions (2026-06-08)

Goal: explore D1/D2/D3; drop on falsification, keep on significant confirmation;
end with 2–3 verified strong directions. Adversarial stance throughout.

Code: `code/scout_d2_cluster_universality.py`, `code/scout_d2b_lock.py`.

## Outcome summary

| Dir | Verdict | Status |
|---|---|---|
| **D2** bounded-cluster-size universality diagnostic | **STRONG CONFIRMATION** (triple-validated) | **KEEP — lead direction** |
| **D3** bounded-type Rosen-CF survivor-set dimension spectrum | **CLEARED** (prior-art distinct) | **KEEP — viable** |
| **D1** "Hecke–Farey spin chain, one engine" | **REFINED; naive form falsified** | demoted to connective frame + open sub-question |

## D2 — CONFIRMED. A real, sharp, computable universality diagnostic.

Operational test (fair across processes): "extreme gap" = normalized spacing above
the q-quantile; "cluster" = maximal run of consecutive extreme gaps. (For BCZ this is
exactly the cluster-member notion: gap ∝ 1/(2ζ(2)xy), so large gap = small product.)

At q=0.99: **Farey 94.9% size-2 clusters, max-run 2, ZERO size-≥3**; **GUE/GOE 0.0%,
isolated (max-run 1)**; Poisson ~0.7% (≈ independent baseline). A clean ~95%-vs-0%
separation, and the *opposite direction* from RMT (Farey's size-2 fraction grows
toward the tail; RMT's vanishes).

Two adversarial locks (`scout_d2b_lock.py`), both pass:
1. **Sharp transition, not a tautology.** Farey size-≥3 fraction: 0.444 (q=0.30) →
   0.035 (q=0.70) → **0.000 at q≈0.85** → max-run pinned at 2 above. The onset sits
   right at the BCZ constant **q\*≈0.86181**. A genuine threshold phenomenon.
2. **Not a Farey-sorting artifact.** The real BCZ-map orbit (2×10⁶ steps) reproduces
   it (q=0.99 → max-run 2, f(size2)=0.952), and the product-threshold P<2/9 framing
   gives max-run 2, f(≥3)=0 — matching the proven `cluster_size_le_two` theorem.

Significance: a single-statistic classifier that places a point process in the
"BCZ/horocycle class" (extreme gaps come in bounded pairs) vs the RMT/Poisson class
(extreme gaps isolated, unbounded runs). Useful to others (Katz–Sarnak-adjacent).
This is the verified core that earlier scepticism demanded — and it held.

Open follow-ups (not blockers): test on actual ζ-zeros at height (email claimed ~3%,
consistent with GUE-low); a clean proof that the q* onset is the same constant.

## D3 — CLEARED. Object distinct from the nearest prior art.

Soares, *Hecke triangle groups, transfer operators and Hausdorff dimension*,
arXiv:2005.11808 (AHP 2021): dimension δ(w) of the **limit set of infinite-area
(w>2) Hecke groups** — a Fuchsian limit-set / Selberg-zeta-resonance object. The
project's target — the **bounded-type Rosen-CF survivor-set** dimension for the
**cofinite** G_q (q≥3, cusped), with X(q) as the spectral/escape edge — is a
different set in a different regime. NOT pre-empted. The Mayer-transfer-operator
machinery (Mayer–Mühlenbruch–Strömberg, arXiv:0912.2236) is borrowable for the
construction. D3-stretch (spectral-gap ↔ horocycle-rate ↔ RH-adjacent) stays a
flagged moonshot.

## D1 — REFINED. Naive identity falsified; framework intact; role = connective lens.

Confirmed real & borrowable: the Farey Fraction Spin Chain (Knauf 1993;
Fiala–Kleban–Özlük, math-ph/0203048; second-order transition, transfer-operator
free energy) and Hecke transfer operators (Mayer).

Falsified (the strong claim): (a) the BCZ gap-product `P=xy` is a **two-site /
horocycle** observable, NOT the standard single-site Farey-chain energy (log of a
single matrix-product entry) — so "it IS the Knauf chain" is wrong; it is at best a
*sibling* (a horocycle/BCZ chain with a product interaction). (b) The cluster
distribution was obtained as a 2-D **invariant-measure integral**, not visibly as a
value of the same 1-D transfer-operator **pressure** that gives the dimension — so
"one free-energy function reads off all three" is looser than pitched.

Kept role: D1 is the shared **thermodynamic-formalism lens** under which D2 (a
phase-transition signature — extreme-gap pairing) and D3 (dimension = pressure-zero)
both sit. Genuine open sub-question worth one targeted attempt later: does the
pressure of the BCZ-product chain have a non-analyticity encoding the `2/9` / `q*`
threshold? If yes, D1 re-promotes to a unifying theorem; if the cluster threshold is
provably an invariant-measure object unrelated to the pressure, D1 stays a lens only.

## Net (scout round)
Two verified strong directions — **D2 (confirmed)** and **D3 (cleared)** — plus
**D1 as their connective frame** with one crisp open question. Matches the goal:
2–3 verified, significant, strong directions.

---

## WEEK-1 ROUND (workflow wf_cb941c29-9c4, 2026-06-08; 6 agents, research→adversarial-verify; all verdicts "holds:true, high confidence")

Deliverables: `code/d2_diagnostic_suite.py`, `code/d3_hecke_dimension.py`,
`code/d1_pressure.py` (+ `code/out/*.json/png`) and notes
`research_notes/d{2,3,1}_*_2026-06.md`.

### D2 — REACHED & verified. **Lead direction; hardened.**
8 processes tabulated (Farey, real BCZ orbit, Poisson, GUE/GOE/GSE, Semi-Poisson,
**real Odlyzko ζ-zeros** — first 100k, fetched, not a surrogate). At q=0.99:
Farey/BCZ f(size2)≈94–95%, max-run 2, zero size-≥3; RMT + ζ-zeros f(size2)≤~0.1%,
isolated. ~1000× separation, opposite direction. **Exact identity verified:**
`1 − q*_BCZ = (8 ln(3/2)−2)/9 = Pr(xy<2/9)` (diff 2.78e-17). Mechanism via the
`cluster_size_le_two_clean` Lean theorem.
Honest caveats (verifier): "pinned *exactly* at q*" is a Q→∞ limit (F_2000 onset
0.8605 vs 0.8618, converging from below); "≤0.1% all RMT" is borderline for GOE;
ζ-zeros at this height are only approximately GUE (variance 0.16 vs 0.18); BCZ-orbit
shows max-run≤2 even at q≥0.5 (stronger than the theorem — unexplained, interesting).
Open milestone: prove onset = q* (Lean target `bczOnsetEqualsQStar`).

### D3 — REACHED & verified, BUT the X(q)-edge sub-conjecture **FALSIFIED**.
λ_q-Gauss transfer operator built & validated: q=3 recovers dim E_{1,2}=
0.531280506277206 (residual 1.22e-15). `D_q(B)` computed q=3..6, B=1..12 (strictly
↓ in q for B≥2, →1 as B→∞). **`X(q)=1/λ³` is NOT the spectral edge** — `D_q(2)>1/λ³`
for q=4,5,6; no transition there. ⇒ DROP the "X(q)=dimension-edge" claim.
Prior-art (Soares 2005.11808 = infinite-area limit-set δ(w)) confirmed distinct.
Scope caveat: this is the **positive-digit λ_q-Gauss analogue, not the full Rosen
map** (both-sign digits) — labeled. Reframed live question: does `D_q(B) ~ 1 − C_q/B`
(Hensley) with `C_q = 6/(π²λ_q)`? That is the new D3 sub-goal.

### D1 — REACHED. Open question **RESOLVED (negative): INVARIANT-MEASURE-ONLY.**
Farey-map pressure control passes (P(1)=0, P'(1)=−π²/(6 ln2), transition at β=1).
The BCZ moment generating function `E[(xy)^β] = (2/(β+1))[1/(β+1) − B(β+1,β+2)]`
is **exactly analytic for β>−1** (no non-analyticity); so `2/9` / `q*` are level-sets
of the BCZ invariant measure, **not** pressure zeros / phase-transition points. ⇒ D1
does **not** re-promote to a unifying theorem; it stays a connective lens, now with a
definitive verdict. No single free energy reads off both D3 dimensions (pressure
zeros) and the D2 threshold (invariant-measure integral).

## Converged state
- **KEEP: D2** — verified, significant, the publishable lead (cheap universality classifier; ζ-zeros included).
- **KEEP: D3** — transfer-operator + `D_q(B)` invariant verified; X(q)-edge dropped; next = the `C_q(λ_q)` Hensley law + the true Rosen map.
- **CLOSED: D1** — settled negative (invariant-measure-only); remains the lens, not a third direction.
Two strong promising directions remain; D1 resolved. Goal satisfied.

---

## WEEK-2 ROUND (workflow wf_a2b66e0b-8c3, 2026-06-08; fleet-wired: Aristotle + Kaggle live)

### D2-Lean — onset=q* **PROVED in Lean by Aristotle**. ✅
Dispatched `projects/aristotle_dispatch_v10/BCZOnsetQStar.lean` (toolchain v4.28.0, mathlib
v4.28.0) via `aristotle submit`. Aristotle returned **COMPLETE, 0 errors / 0 sorries**:
`theorem bczOnsetEqualsQStar` proved, incl. the hard real-analysis lemmas it generated
(`log(3/2)>1/4` via `exp(1/4)⁴=exp 1<3≤(3/2)⁴`; `log(3/2)<1`). Rests on exactly two axiom
stubs — `bczProb_eq_value` (v5) and `cluster_size_le_two_clean` (v8), both proved in prior
dispatches — plus standard Lean axioms. Solved project saved under
`projects/aristotle_dispatch_v10/solved/`. (Aristotle project id 6f498ae0-…; ~21 min.)
Honest note: the agent correctly REMOVED a wrong lemma mid-build (`1−bczOnset ≠ 2/9` — the
quantile and product thresholds are different objects), keeping the clean statement.

### D2-ζ — bound tightened, **CONFIRMED** (verifier high-confidence). ✅
Real **2,001,052 Odlyzko zeros** (zeros6 table, authenticity re-verified), unfolded. At q=0.99:
19,611 clusters, **0 size-2** (max-run 1) → Clopper–Pearson one-sided 3σ upper bound
**f(size2) < 0.0337%**, i.e. **>2794× below** Farey/BCZ's ~94%. ζ sits firmly in the RMT/GUE
class. `code/d2_zeta_bigsample.py`, §8 of `d2_diagnostic_2026-06.md`.

### D3-Rosen — **UNRESOLVED; research agent's "C_q refuted" FALSIFIED by the verifier (bug caught).** ⚠
The compute agent reported `C_q=6/(π²λ_q)` REFUTED — but the adversarial verifier found its
`D_q^Rosen(B)` was **mislabeled**: it bisected leading-eigenvalue = 0.5 via a bogus
"factor-2 symmetry" (the both-sign branches have *unequal* weights `(aλ∓x)^{-2}` and different
images). Recomputing with the **correct** full operator (bisect eigenvalue = 1, summing both
branches with individual weights) gives q=5: B=1→0, B=2→0.696, B=4→0.881, B=8→0.949, and
`B·(1−D)` decreasing monotonically (0.997→0.407 at B=8) **toward** `C_conj=0.376` — i.e.
*consistent with Hensley convergence from above*, NOT refuted. **Verdict at B≤8: INDETERMINATE.**
Solid sub-results that DO hold: (a) q=3 positive-only Hensley confirmed to ~9% (Richardson
C_3=0.660 vs 6/π²=0.608); (b) positive-only `D_q^{pos}(∞)<1` for q≥4 (IFS doesn't cover domain).
⇒ needs a round-3 with the corrected operator pushed to large B. (Local-feasible — operator is
N×N regardless of B.) `code/d3_rosen_full.py` (buggy bisect; to be superseded).

## Week-2 net
- **D2 = strongly verified on two fronts** (machine-proved onset=q*; ζ 3σ bound 2794× below). Lead, near write-up-ready.
- **D3 = still open** (C_q law indeterminate; the "refuted" was a bug — verification saved it). Round-3 with the correct operator at large B will settle it.

### D3 round-3 (wf_85c9325a-7b7) — operator FIXED & validated; C_q verdict = MODIFIED-FORM (not universal)
The corrected full-Rosen operator (`code/d3_rosen_round3.py`) bisects leading-eigenvalue=1 (no
0.5 relapse) with per-branch restricted-domain indicators. **Both guardrail anchors pass**: q=3
Gauss dim{1,2}=0.531280506277204 (residual 1e-15); q=5 full Rosen B=2/4/8 = 0.696/0.881/0.949.
Independent verifier re-implemented the operator and confirmed anchors + ev→1.

**Verified verdict (reliable range B≤24):** `C_q = 6/(π²λ_q)` is **CONFIRMED** for q=3 (ratio 1.06),
q=4 (0.98), q=7 (0.93); **BORDERLINE** q=5 (0.82), q=6 (0.88), q=8 (0.85); **REFUTED** q=9 (0.75),
q=10 (0.79), q=11 (0.68), q=12 (0.76). For q=3,4 `B·(1−D)→C_conj` from above (convergent); for
q≥9 it sits 20–35% below C_conj at B=24 with no reversal → the conjectured coefficient is NOT the
universal Hensley constant; it deviates (downward) as q grows.
**Precision caveat (the open edge):** large-B (≥32, q≥5) eigenvalues are unresolved at N=80
collocation (leading ev too close to 1); the compute agent's harsher refutations came from that
corrupted data and were discarded by the verifier. A DEFINITIVE large-q verdict needs a
higher-accuracy method — the **Jenkinson–Pollicott periodic-orbit / Fredholm-determinant** scheme
(super-exponential accuracy, the right tool for dims near 1) or extended precision (mpmath), and/or
larger N on M1/M2.

## Standing state (post week-2 + D3r3)
- **D2** — verified (Lean onset=q* + ζ 3σ). Lead; write-up-ready.
- **D3** — Hecke/Rosen dimension spectrum operator validated; finding = **Hensley `6/(π²λ_q)` is q-dependent, holds small-q, breaks large-q** (precision-limited at large q). Real result; next = high-precision JP-determinant pass for a definitive large-q verdict.
- **D1** — closed (invariant-measure-only).

## D3 round-4 (JP Fredholm-determinant) — IN PROGRESS / verdict pending (wf_470d79aa-b54)
Built `code/d3_jp_dimension.py`; M2 ran the large-q high-precision sweep (q=12–20, dps=50,
`/tmp/d3_jp_largeB_m2.json`). **Preliminary, NOT converged:** at large q with B≤8 / cycle-length 4,
JP gives `B·(1−D)≈0.6`, `ratio≈2×C_conj` and *rising* — the OPPOSITE sign of round-3's collocation
(which read *below*). Two methods disagreeing ⇒ neither has reached the B→∞ limit ⇒ **large-q `C_q`
is numerically delicate; still not definitively pinned.** Final synthesis/verify finishing; conclusion
+ the d3_jp code/note to be committed when the workflow lands. Honest current read: the `C_q(λ_q)`
law is harder to nail at large q than hoped; the *small-q* confirmation (q=3,4 ≈ `6/(π²λ_q)`) stands.

## Applications (separate scouts) — NEGATIVE, documented
`research_notes/applications_scout_2026-06-08.md`: D2 has no transferable industrial edge — loses to
spectral (TRNG), Ferro–Segers (extremal clustering), Hurst (network), Sobol (QMC). Value is mathematical.

## Breakthrough goals — `research_notes/breakthroughs_2026-06-08.md`
Goal 1 (q=4 cluster≤2, spawned session) · Goal 2 (fully-formal X(3)=2/9) · Goal 1.5 (uniform all-q).
