# −1 Dominance — LEDGER (honest, cited, scoped)

_Local-only synthesis. Adversarial honesty: PROVEN (and under WHICH hypotheses) /
EMPIRICAL / FORMALIZED are kept strictly separate. No conditional result is ever
upgraded to unconditional. Every citation checked against the primary text in this
directory. Status as of 2026-06-02; the two items marked **[PENDING]** are updated
when the M1 sweep and the M2 sieve finish._

---

## 0. The claim under test
"**−1 dominates the non-residue hierarchy**" in the Chebyshev / Shanks–Rényi prime
race mod `N`. VERDICT: **FALSE, and backwards.**

---

## 1. PROVEN — conditional on GRH + LI (Rubinstein–Sarnak framework)

These are theorems of Rubinstein–Sarnak and Fiorilli–Martin. **Every one is conditional
on GRH and the Linear Independence hypothesis (LI)** of the imaginary parts of the
nontrivial zeros (the variance closed form, FM Thm 1.4, needs only GRH). **None is
unconditional over ℚ.**

- **`a = −1` is the LEAST-biased non-residue, not the most.** For the logarithmic
  Rubinstein–Sarnak sign-density `δ(q;a,1) = dens{x : π(x;q,a) > π(x;q,1)}`,
  `δ(q;−1,1)` is the *minimum* over non-residues `a`. Equivalently its limiting
  variance `V(q;−1,1)` is the *maximum*. This is **Fiorilli–Martin, J. reine angew.
  Math. (Crelle) 676 (2013), 121–212, Theorem 1.10** (assume GRH and LI):
  > "For any integer `a ≠ −1`, we have `δ(q;−1,1) < δ(q;a,1)` for all but finitely many
  > integers `q` with `(q,a)=1` such that both `−1` and `a` are nonsquares (mod q)."
  (FM_text.txt:324–326; verified verbatim.)
  **Scope note (important):** Thm 1.10 is a statement about a *fixed* `a` as `q → ∞`
  ("all but finitely many `q`"), for ANY modulus `q` where `−1` and `a` are both
  nonsquares — it is **not** restricted to "primes `q ≡ 3 (mod 4)`". The per-`q`
  statement "for this `q`, `−1` is the extremal non-residue" is the closely related
  fact our sweep (§2) tests directly.

- **Non-residue vs non-residue is vacuous.** For two *distinct* non-residues `a, b`,
  `δ(q;a,b) = 1/2` exactly: the RS limiting law is symmetric, so neither sign-dominates.
  **Granville–Martin, Amer. Math. Monthly 113 (2006)** (PNR_text.txt:1104–1149,
  "both nonsquares … exactly half the time … the distribution is symmetric"; GRH+LI).
  Reduction `δ(q;a,b)=δ(q;ab⁻¹,1)` for square `b`: Feuerverger–Martin (FM_text.txt:318).

- **Mechanism = parity (three identities, independently re-derived and verified):**
  1. Leading RS mean `= −1 + #{x : x² = a} = −1` for **every** non-residue ⇒ all
     non-residues tie at leading order; `−1` is not a leading-mean effect.
  2. `Σ_{χ≠χ₀} |χ(a)−1|² = 2φ(q)` for every `a ≠ 1` ⇒ total spectral weight is the
     same for all classes; the discriminant must be finer than the raw weight.
  3. The even-character weight of `|χ(a)−1|²` is `0` **iff** `a = −1`. So `−1` alone
     puts ALL its weight on ODD characters, which carry the larger
     `c_χ = b(χ) = Σ_{γ} 1/(¼+γ²)` (FM Def 1.3, FM_text.txt:162) — the
     `ψ(1) − ψ(½) = 2 log 2` archimedean gap. Hence `V(q;−1,1)` is **maximal** ⇒
     `δ(q;−1,1)` **minimal** (`δ` strictly decreasing in `V`).
  Skew `= 0` (symmetric law); the Aoki–Koyama DRH "magnitude" is degenerate among
  non-residues (`m(a)=0` generically) so it is not the discriminant either.

- **The only sense in which `−1` "leads": amplitude.** `V(q;−1,1)` = MAX means `−1`
  has the largest typical `|π(x;q,−1) − π(x;q,1)|` excursions. That is the *same*
  parity fact that makes it the least biased in *sign* — "leading in amplitude" and
  "losing the sign race" are one fact, not two.

Variance closed form actually used (FM Thm 1.4, GRH; specialized to prime `q` where
every non-principal `χ` is primitive):
`V(q;a,1) = Σ_{χ≠χ₀} c_χ |χ(a)−1|²`, `c_χ = log(q/π) + ψ((1+a_χ)/2) + 2 Re L′/L(1,χ)`,
`a_χ = (1−χ(−1))/2`. (FM_text.txt:179–184.)

---

## 2. EMPIRICAL — the analytic variance-ordering sweep (Option 3)  **✅ COMPLETE**

NUMERICAL, conditional on GRH+LI (it evaluates the FM/RS closed form, not a proof).

**Question.** For each prime `q ≡ 3 (mod 4)` (so `−1` is a non-residue), is `a = −1` the
variance-MAXIMAL non-residue (⇔ least-biased)? Report every `q` where it is NOT.

**Method.** `sweep_variance.py` (this dir; run on M1). Computes `V(q;a,1)` for all
non-residues `a` via the FM closed form, with `L′/L(1,χ)` obtained fast and exactly
from the shared Hurwitz-zeta Laurent expansion
(`L′/L(1,χ) = −log q − A₁/A₀`, `A_j = Σ_r χ(r) γ_j(r/q)`, `γ₀=−ψ`, `γ₁` by central
difference), all characters handled by one FFT per modulus → `O(q log q)`.
- **Validation:** matches `compute_delta.py`'s independent slow `mp.diff(log L)` route
  to ~1e-14, and a startup self-test reproduces the established ranks
  `δ`-rank(−1)=1 (V-rank 1) for `q ∈ {7,11,19,23}` exactly (1/3, 1/5, 1/9, 1/11);
  refuses to run otherwise.

**Result (COMPLETE, M1, `sweep_results.tsv`, 20871 s / 8 procs):** swept **all 4808 primes
`q ≡ 3 (mod 4)` in `[3, 99991]`** (the full range `< 10⁵`; not truncated). For **every one**,
`a = −1` is the **unique** variance-max non-residue ⇒ the least-biased: **0 exceptions.**
The margin `V(−1) − max_{a≠−1} V(a)` is positive throughout and grows ~linearly in `q`
(smallest at the smallest prime: `q=7` margin `0.727`, `q=11` `1.506`, `q=19` `6.474`,
`q=23` `10.39`; up to `≈6.5×10⁴` at `q≈10⁵`) — the `2φ(q) log 2` parity gap dominates the
`O(√q · loglog q)` `L′/L` fluctuation, so the bias only widens. Plot: `sweep_plot.png`
(`V(q;−1,1)` and the margin vs `q`; no exception markers).
**Scope/interpretation (honest):** this is the **per-`q`** statement "for this prime `q≡3 mod4`,
`−1` is the extremal non-residue", which has **no exception below `10⁵`** and is *stronger*
than what FM Thm 1.10 asserts (the theorem is per-*fixed*-`a` as `q→∞`, allowing finitely
many `q`-exceptions for each `a`). The sweep does not, and cannot by finite computation,
rule out exceptions above `10⁵`; FM Thm 1.10 covers the asymptotics conditionally (GRH+LI).
Restricted to primes `q≡3 mod4` (the canonical "−1 is a nonsquare" prime case); composite
moduli out of scope.

---

## 3. FORMALIZED — Lean 4 / Mathlib v4.28.0  **✅ CERTIFIED (local, EXIT=0, axioms clean)**

`Minus1Core.lean` (this dir + `primes-equispaced/formal-conjectures/` +
`aristotle_dispatch_minus1/`) certifies the **unconditional finite-combinatorial core**
under the leading-mean computation — no GRH/LI is invoked; these are the plain
combinatorial facts beneath the conditional analytic statements:
- `sqrtCount_eq_zero_of_not_isSquare`: a non-square has no square roots in `ZMod N`;
- `leadingMean_eq_neg_one_of_not_isSquare`: every non-residue's leading mean is `−1`;
- `leadingMean_tie`: any two non-residues have equal leading mean (the tie);
- `minus_one_not_singled_out`: `−1` (when a non-residue) is not singled out.

**Build status — DONE.** The in-repo `primes-equispaced` Mathlib checkout is gutted
(~1409 of ~6000 source files git-deleted; both `import Mathlib` and granular ZMod/Finset
imports unavailable there) so it cannot compile in-tree. Certified instead via a clean
throwaway full-Mathlib v4.28.0 build off the synced drive (`/tmp/lean-minus1`,
`lake exe cache get` → 7655 oleans):
`lake env lean Minus1Core.lean` → **EXIT=0, 0 errors, 0 warnings**. `#print axioms` on all
four declarations → **`[propext, Quot.sound]` only — no `sorryAx`, no `Classical.choice`.**
A self-contained Aristotle dispatch package is also staged at `aristotle_dispatch_minus1/`
(redundant now that local compilation succeeded; kept as portable archive).

---

## 4. EMPIRICAL — the prime-counting curve / sieve  **[DONE 2026-06-03]**

The asymptotic `δ`/`V` ordering above has an **onset scale**: at the largest previously
verified `x = 1.3×10¹³`, the sign bias is not yet visible — `−1` is mid-pack for
`N = 7,11,19,23` (RECONCILE_COMPUTE.md), and `V(−1)=max` is empirically corroborated
only for `N = 7, 11` there, not yet for `N = 8, 19, 23` (onset `~ e^{33.4} ~ 3×10¹⁴`).

**Pre-onset baseline (VALIDATED control, `minus1_curve_analysis.py` Part B on the existing
`out2.tsv`, `x ≤ 1.3×10¹³`):** the RS-normalized empirical variance
`Var_grid[(log x/√x)(π(x;N,a)−π(x;N,1))]` ranks `a=−1` as **NOT** the max for any N —
rank `2/3` (N=7), `4/5` (N=11), `6/9` (N=19), `9/11` (N=23); argmax classes
`a=3,8,14,10` respectively. This is exactly what the theory expects *below* onset
(the finite-`x` signed-`D` is amplitude + low-zero noise, not yet the limiting law), and
matches REPORT.md's "−1 mid-pack at 1.3×10¹³". It also confirms the Part-B code runs clean.

**RESULTS — `curve_3e14.tsv` (M2 `mr1_par`, Xmax=3×10¹⁴, 438-pt grid, completed 2026-06-03 in
98498 s; `minus1_curve_analysis.py curve_3e14.tsv`):**

**Part A — integer cross-check vs `out2.tsv` (x ≤ 1.3×10¹³): EXACT MATCH (PASS), 567/567, 0
mismatches** across N=7,8,11,19,23 at all 9 shared checkpoints. ⇒ the 3×10¹⁴ sieve is
integer-validated against the prior double-verified baseline; no logic/overflow drift to the
frontier. (Independent M1-hardware replication `curve_m1_3e14.tsv` still running, 146/224, for a
second integer cross-check via `compare_curves.py` — not on the critical path; A already passes.)

**Part B — does the onset move `a=−1` to variance-MAX? PARTIAL / TRANSIENT (honest).** RS-normalized
`Var_grid[(log x/√x)(π(x;N,a)−π(x;N,1))]`:
- **N=7: `a=−1` IS variance-MAX at every window incl. top-decade x≥3e13.** ✓ theory-consistent.
- **N=19: `a=−1` BECOMES variance-MAX in the top-decade x≥3e13** (rank 2/9 below that). ✓ onset emerging.
- N=11: `a=−1` rank 2/5 (full) → 3–4/5 (upper); argmax a=6. NOT max.
- N=23: `a=−1` rank 5/11 (full) → 10–11/11 (upper). NOT max.

**Raw table metric (Koyama's Tables 3–7 form): `π(3e14;N,a)−π(3e14;N,1)` ranked among non-residues:**
**`−1` LEADS strictly for N=7 and N=23**; rank 3/3 (coprime NR {3,5,7}) for N=8, rank 3/5 for N=11
(a=7 leads), rank 6/9 for N=19 (−1 value is NEGATIVE, −16802). So the raw-lead and variance-MAX
signals are BOTH modulus-dependent and do NOT coincide — e.g. N=19 is variance-MAX yet value-NEGATIVE
(the Fiorilli–Martin signature: `−1` = noisiest/largest-amplitude, NOT largest value in the unweighted
race). The picture also SHIFTED vs 1.3×10¹³ (where N=8 led and N=7,23 did not) — i.e. non-monotone,
transient, exactly as the low-lying-zero caveat (Koyama nontriv.pdf p.19; our §1) predicts.

**Honest verdict:** at `3×10¹⁴` we are only *at* the onset (`e^{33.4}≈3.2×10¹⁴`), not deep in the
asymptotic regime, so the finite-`x` ranking is **suggestive, not decisive**. The data are
**consistent with** the GRH+LI prediction that `a=−1` is the limiting variance-MAX (cleanly for N=7,
emerging for N=19) and with the transient-reversal caveat for the slow moduli (N=11, 23) — but they do
**not** by themselves establish the ordering. The actual proof of the ordering is the analytic
Fiorilli–Martin result in §1 (GRH+LI), not this curve. DoD met: curve computed + integer-validated +
onset analysis reported honestly.

---

## 5. One-line verdict
"`−1` dominates among non-residues" is **false**. Under GRH+LI, `−1` is the
**least**-biased non-residue (RS sign-density minimum) because its limiting variance is
the **maximum**; non-residue-vs-non-residue races are 50–50. The single true reading is
amplitude (largest `|D|`), which is the very fact that costs it the sign race. **Nothing
here is unconditional over ℚ.**

## Citations (all primary-source verified in this directory)
- Fiorilli–Martin, *J. reine angew. Math. (Crelle)* **676** (2013), 121–212 — Thm 1.10
  (FM_text.txt:324), Thm 1.4 variance (179), Def 1.3 `b(χ)` (162). DOI 10.1515/crelle.2012.004.
- Rubinstein–Sarnak, *Experimental Mathematics* **3** (1994), 173–197 — RS framework,
  sanity densities `δ(4;3,1)=0.99590`, `δ(3;2,1)=0.99906` (reproduced).
- Granville–Martin, *Amer. Math. Monthly* **113** (2006) — two-nonsquare symmetry
  (PNR_text.txt:1104–1149).
- Aoki–Koyama, *J. Number Theory* **245** (2023), arXiv:2203.12266 — DRH magnitude /
  deflection (AK_text.txt:8–19); ruled out as the non-residue discriminant.
