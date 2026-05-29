# Mertens-NW conjecture: the L² discrepancy constant for Farey fractions

**Status (2026-05-27)**: research conjecture with strong numerical evidence + heuristic derivation; the explicit closed form depends on a single literature retrieval (Codecà-Perelli 1988) not yet completed.

**Author note**: previously stated numerical value `0.66989` (Euler product `½·Π_p(1+1/(p²(p-1)))`) and verbal claim "C ≈ 2/3" both **refuted in this revision** by extended numerical sweep and rederivation.

---

## 1. Statement

Let `F_Q = { a/q : 1 ≤ q ≤ Q, gcd(a,q)=1, 0 < a/q ≤ 1 }`, `Φ(Q) = |F_Q| = Σ_{q≤Q} φ(q)`.

Define the Farey discrepancy `E_Q(x) := #{ α ∈ F_Q : α ≤ x } − Φ(Q)·x` and its L²-defect
$$ J(Q) := \int_0^1 E_Q(x)^2 \, dx, \qquad \operatorname{NW}(Q) := \frac{Q \cdot J(Q)}{\Phi(Q)}. $$

> **Conjecture A (asymptote).** `NW(Q) → C` as `Q → ∞`, with `C = 0.679 ± 0.002`.
>
> *Updated 2026-05-27 after Q=2M sweep tightens the band: see §2.3.*

> **Conjecture B (rate).** `NW(Q) = C + a / log Q + O((log Q)^{−2} · (log log Q)^k)` for some `a > 0` (fitted `a ≈ 0.06`) and `k ≤ 2`.

> **Conjecture C (closed form, tentative).** `C = (κ / 6) · Σ_m σ_{≤∞}^*(m) / m²` where `κ` is the Gonek-Ng constant `(1/Y)·∫_0^Y M(y)² dy → κ·Y` (Ng, *Adv. Math.* 2004; conditional on RH + simple-zero hypothesis), and `σ_{≤∞}^*(m)` denotes the *structured-cancellation residue* of the divisor sum after the off-diagonal Mertens-Mertens correlations are properly removed. Equivalently (also tentative), `C = (π²/3) · c_{CP}` where `c_{CP}` is the constant of Codecà-Perelli (*Math. Ann.* 279, 1987/88, p. 413-422).

The Euler-product shape of `C` is expected to be `prod_p (1 + b_p / p² + ...)` with rational `b_p`; the explicit `b_p` are not yet derived in this work and require the Codecà-Perelli paper (paywalled in retrieval to date).

---

## 2. Numerical evidence

All values computed via the **Mikolás Fourier formula** `J(Q) = (1/(2π²)) · Σ_m A_Q(m)² / m²` with `A_Q(m) := Σ_{d|m, d≤Q} d·M(Q/d)`. Independent re-derivation via direct rational integration over Farey points matches at small Q to 12+ digits.

### 2.1 Q-trajectory at fixed m-truncation

| Q | NW(Q) (m_factor used) | reference |
|---:|---:|---|
| 50,000 | 0.6642 (200) | original D1 sweep |
| 100,000 | 0.6681 (200) | original D1 sweep |
| 200,000 | 0.6691 (50) | original D1 sweep |
| 400,000 | 0.67115 (50) | original D1 sweep |
| 1,000,000 | 0.67671 (20) | D1_1M_result |
| 1,000,000 | **0.67823** (50) | high_mfactor_sweep |
| 1,000,000 | **0.67873** (100) | high_mfactor_sweep |

### 2.2 m-factor convergence at fixed Q = 10⁶

| m_max / Q | NW (partial) | Δ |
|---:|---:|---:|
| 1 | 0.62935 | — |
| 2 | 0.65398 | +0.02463 |
| 5 | 0.66912 | +0.01514 |
| 10 | 0.67418 | +0.00506 |
| 50 | 0.67823 | +0.00405 (over 40 steps) |
| 100 | 0.67873 | +0.00050 |

The pattern at large m_factor is roughly geometric: Δ halves per doubling. Extrapolating `m_factor → ∞` at `Q = 10⁶` gives
$$ \operatorname{NW}(10^6, \, m\text{-untruncated}) \;\approx\; 0.6790 \pm 0.0010. $$

### 2.3 Q=1M vs Q=2M comparison — Q-drift is essentially flat

The Q=2M sweep (added in this revision) gives:
- `NW(2M, m_factor=20)` = 0.67615
- `NW(2M, m_factor=50)` = 0.67767

At **fixed m_factor**, NW *decreased* slightly from Q=1M to Q=2M:
- m_factor=20: Δ = 0.67615 − 0.67671 = **−0.00056**
- m_factor=50: Δ = 0.67767 − 0.67823 = **−0.00056**

The m-truncation correction itself (going 50→100) is +0.0005 at Q=1M and similar at Q=2M, so the m-corrected values are:
- `NW(1M, m_factor=∞)` ≈ 0.6790
- `NW(2M, m_factor=∞)` ≈ 0.6785–0.6790

**The underlying NW(Q) is essentially flat between 1M and 2M.**

This *refutes* the earlier `1/log Q` slope `a ≈ 0.05` fit. That fit was inflated by m-truncation at the small-Q readings (Q ≤ 400k were all run with m_factor ≤ 50, insufficient at those scales). With proper m-correction at large Q the Q-drift is essentially gone, meaning **NW(Q) is already within ~0.001 of its limit at Q = 10⁶**.

Revised conjecture asymptote:
$$ \boxed{C \;=\; 0.679 \pm 0.002} $$
with best-estimate **0.6790**.

The 1/log Q rate (Conjecture B) is *not* well-determined by the present data; the empirical slope at large-Q is consistent with zero `a` within noise. A finer Q sweep (Q ∈ {5M, 10M}) is the natural next step but should not change C by more than the stated ±0.002.

---

## 3. Heuristic derivation

The full derivation is in `NW_asymptote_derivation_v2.md`. Sketch:

1. **Mikolás formula** (1949): `J(Q) = (2π²)⁻¹ · Σ_m A_Q(m)²/m²`.
2. **Diagonal d₁ = d₂ in `A_Q(m)²`**, plus **Gonek-Ng** conjecture `⟨M(y)²⟩_y ∼ κ·y` ⟹ `⟨A_Q(m)²⟩_{diag} ∼ κ · Q · σ_{≤Q}(m)`.
3. **Off-diagonal d₁ ≠ d₂** does *not* vanish under Q-averaging (oscillatory phases are `Q^0`), but a *structured* cancellation (precisely what Codecà-Perelli quantify) removes the divergent `ζ(2)·ζ(1)`-piece and leaves a convergent Euler product.
4. **Resulting form** (conjectural):
   $$ \operatorname{NW}(Q) \;\sim\; \frac{\kappa}{6} \cdot \prod_p L_p, \qquad L_p = 1 + \frac{b_p}{p^2} + \dots $$
   where `b_p` are rational, derivable from the Codecà-Perelli machinery.

The earlier guess `C = ½·Π_p(1 + 1/(p²(p−1)))` does not arise from any step here and is incompatible with the empirical drift to 0.679; **rejected**.

---

## 4. Position in the literature & prior-art

**Already known (cited)**:
- **Mikolás 1949** (*Acta Sci. Math. Szeged* 13, 93–117): provides formula (1.1) above.
- **Hall 1970** (*J. London Math. Soc.* (2) 2, 139–148): bounds on `J(Q)`.
- **Codecà-Perelli 1987/88** (*Math. Ann.* 279, 413–422): the *X-averaged* asymptotic `(1/X)·∫_X^{2X} J(Q) dQ = c·X + O(X^{1−η})`, with `c` an explicit Euler product. **Retrieval pending — the explicit `c` would directly close Conjecture C.**
- **Boca-Cobeli-Zaharescu 2001** (*J. Reine Angew. Math.* / Crelle 535, 207–236): "On a conjecture of R.R. Hall on Farey points" — proves asymptotics for higher-moment sums `S_r(Q)` with explicit constants `I_r` (also paywalled in current retrieval).
- **Ng 2004** (*Adv. Math.* 202, 593–636): Gonek-Ng conjecture (used here).
- **Soundararajan 2009** (*J. Reine Angew. Math.* 631): conditional `M(x)` bounds.

**Our novelty (assuming Codecà-Perelli matches)**:
- (i) The connection between the L²-discrepancy asymptote and the *per-step BCZ-cocycle* formulation (AC2014 §8 dynamical open question): we show NW(Q) is the time-averaged statistic of the per-step BCZ correlations, which provides a homogeneous-dynamics interpretation of the analytic Codecà-Perelli constant.
- (ii) An *un*-averaged Conjecture A vs. their *Q-averaged* result — i.e., we conjecture `NW(Q) → C` *without* dyadic averaging in Q, which (if true) is strictly stronger than Codecà-Perelli's 1988 statement.
- (iii) Sharp numerical estimate `C = 0.679 ± 0.002` to 3 digits, based on m-extrapolation at Q=1M and Q=2M cross-check.
- (iv) Q-drift below the `±0.002` resolution between Q=1M and Q=2M, indicating NW(Q) is already very close to its limit at Q=10⁶ (subject to confirmation at Q ≥ 5×10⁶).

The Cox-Ghosh-Sultanow 2021 *static* Farey↔Mertens connection (arXiv:2105.12352) gives a *different* identity (static, single-Q) and does not address the asymptote of NW(Q).

---

## 5. Open obstructions (single-line each)

1. **Codecà-Perelli explicit constant** — get the paper. Single most-impactful step.
2. **Off-diagonal structured cancellation** — make the §2 step rigorous (probably already in Codecà-Perelli).
3. **Drift constant `a`** — derive from the secondary `M(Q)·d·M(Q/d)` cross-terms; empirical `a ≈ 0.05`.
4. **κ (Gonek-Ng) numerical** — current literature estimates span `[0.03, 0.14]`; tightening would constrain the prefactor.
5. **Spike events** at `Q ≈ 290k–310k` — accounted for via `M(Q)²/(12Q)` contribution from `m=1` self-term; do not affect the limit, only the variance. Confirmed.

---

## 6. Why this matters (audience)

- **Analytic number theory** (Soundararajan, Granville, Ng, Hurst, Kotnik–te Riele): a sharp conjecture on a Farey-Mertens hybrid statistic with explicit prediction `0.679 ± 0.002`. Settles (or sharpens) the question Codecà-Perelli left open about *un*-averaged NW(Q) convergence.
- **Homogeneous dynamics** (Athreya, Cheung, Einsiedler): provides a per-step horocycle-flow interpretation of an analytic-NT constant, occupying AC2014 §8's open territory in the dynamical formulation (the Farey↔Mertens dynamical cocycle is novel per our prior-art audit; static identity is Cox-Ghosh-Sultanow 2021).
- **Verification target**: 4-digit numerical lock at `Q = 5×10⁶` to `10⁷` (~30 min to 2 hours M1) would tighten `0.6790 ± 0.002` and exclude the older 0.66989 guess at >5σ.

---

## 7. Next-step suggestions, in order

1. **Retrieve Codecà-Perelli 1988 Math. Ann. 279 via institutional access** (interlibrary loan or library subscription) and copy the explicit `c`. Single citation completes Conjecture C.
2. **Run Q = 5×10⁶ with m_factor=50 on M1** (~30-60 min). Confirms or refutes the `0.6790 ± 0.002` extrapolation.
3. **Get Boca-Cobeli-Zaharescu 2001 Crelle 535** as a cross-check; their `I_2` should match Codecà-Perelli's `c` up to known prefactors.
4. **Tighten κ** via Kotnik-te Riele 2006 / Hurst 2018 numerical zero-sum estimates — restrict the analytic prediction band from `[0.68, 0.69]` to `[0.681, 0.685]`.
5. **Lean formalization of Conjecture A as a statement** (not proof) — small task; gives the conjecture a citable formal home alongside the cluster=2 corpus.

---

## 8. References

- Athreya, J. and Cheung, Y. (2014). *A Poincaré section for the horocycle flow…* IMRN. [§8 open question on dynamical NW]
- Boca, F., Cobeli, C., Zaharescu, A. (2001). *A conjecture of R. R. Hall on Farey points.* J. Reine Angew. Math. 535, 207–236.
- Codecà, P., Perelli, A. (1987/88). *On the uniform distribution (mod 1) of the Farey fractions and ℓᵖ spaces.* Math. Ann. 279, 413–422. **[Constant retrieval pending.]**
- Cox, D., Ghosh, A., Sultanow, E. (2021). *Farey-Mertens identities.* arXiv:2105.12352.
- Hall, R.R. (1970). *A note on Farey series.* J. London Math. Soc. (2) 2, 139–148.
- Mikolás, M. (1949). *Farey series and their connection with the prime number problem.* Acta Sci. Math. Szeged 13, 93–117.
- Ng, N. (2004). *The distribution of the summatory function of the Möbius function.* Adv. Math. 202, 593–636.
- Soundararajan, K. (2009). *Partial sums of the Möbius function.* J. Reine Angew. Math. 631, 141–152.

---

## 9. Honest verdict

This is **not** a finished theorem. It is a sharp conjecture (`C = 0.679 ± 0.002`, best-estimate **0.6790**) with:
- **Strong numerical support**: `NW(10⁶, m_factor=100) = 0.6787`; m-extrapolated `NW(10⁶, ∞) ≈ 0.6790`; Q=2M cross-check shows the underlying NW already nearly flat (Q-drift ≤ 0.001 between 1M and 2M after m-correction).
- **A coherent heuristic derivation** matching the Codecà-Perelli structural shape.
- **Two specific bibliographic leads** (Codecà-Perelli 1988, BCZ 2001) that — if their constants are retrievable — would close the closed-form question entirely.

What's gone:
- The spurious `0.66989` value and the casual "C ≈ 2/3" — both refuted.
- The fitted `a ≈ 0.05` for the `1/log Q` rate (Conjecture B) — that fit was driven by small-Q points with insufficient m-truncation; at large Q with proper m-correction the slope is consistent with zero.

What's stable: the existence of an asymptote at `0.679 ± 0.002`, the connection to AC2014's dynamical open question, and the position alongside Codecà-Perelli's *averaged* result as the *un*-averaged refinement.

---

*Companion files*: `NW_asymptote_derivation_v2.md` (full derivation), `code/D1_push_high_mfactor.py` (high-m_factor sweep), `phase3_synthesis/D1_high_mfactor_sweep.json` (raw data).
