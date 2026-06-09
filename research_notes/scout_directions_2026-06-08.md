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
