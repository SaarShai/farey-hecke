# T1 GAP-12 — prior-art re-scout (Cramér–Rao draft, both angles)

Lane T. Written 2026-08-26. Status: **RE-SCOUT FILED.** Ticket obligation:
`T1_CRAMER_RAO_DRAFT.md` §6 GAP-12 / spec `G1_MODEL_SPEC.md` §5 gate G-c
("re-scout at first-draft time"). Observable under amendment A2: the order-1
Riesz/Cesàro mean `(1/N)Σ_{k<N} M(k)`. **This file is the scout; it does not
close GAP-12 until a referee accepts the verdict.**

Claim under review (draft §0, byte-identical in v1–v3): in model N2,

```
max_j RMSE(γ̂_j)  ≥  √6 · (log(γ_d/2π))^{1/2} / (log X)^{3/2},
X(ε)             ≥  exp( (6 log(γ_d/2π))^{1/3} · ε^{-2/3} ).
```

The signal model is the random-phase almost-periodic sum with tones at the
Riemann-zero ordinates `γ_j` and amplitudes `1/|ρ ζ'(ρ)|`, windowed by
`M_W(s) = 1/(s(s+1))`.

---

## 0. Collision criterion

A source is a **COLLISION** only if it already states a Cramér–Rao / Fisher /
sample-complexity / minimax *lower bound* for estimating Riemann-zero (or
L-function zero) ordinates from arithmetic data (`M`, `μ`, `ψ`, `π`), or
already maps super-resolution lower-bound machinery onto zeta zeros with a
comparable rate. Matching the displayed constants `√6` or `exp(c ε^{-2/3})`
would also be a collision.

**NEAR-MISS:** same objects (Cesàro-Mertens explicit formula; amplitudes
`1/|ρ ζ'(ρ)|`; random-phase almost-periodic model; textbook frequency-estimation
CR) but a different theorem (forward formula, distribution of `M(x)`,
disproof of Mertens, generic sinusoid CR, uniqueness without rates, FFT
*display* of peaks).

**CLEAR:** adjacent topic, no overlap on the claim.

Occupancy of the *forward* map is not a collision on T1. It is prior art T1
must *cite* (that is GAP-16's job). This scout records it as NEAR-MISS so the
widened A2 search is not silently converted into "the formula is classical,
therefore the bound is scooped."

---

## 1. Search surface (honest)

GAP-12 exists because `lane_c/S2_PRIOR_ART.md` (2026-08-14, **NO-COLLISION**)
itself flagged a negative on `"Cramér–Rao Riemann zeros"` as weaker than a
systematic review, and because A2 moved the observable onto a classical
object (Riesz means of `1/ζ`, `ψ_1`, Cesàro `M`) that S2 did not cover.

This re-scout used:

| layer | what | dates |
|---|---|---|
| S2 web scout | Cramér–Rao / Fisher / line-spectral / super-resolution × zeta zeros; Inverse Problems, IEEE SP, Exp. Math. | 2018–2026, run 2026-08-14 |
| Gate 0 (101-agent) | `projects/mimo-mini-project/SPECTROSCOPY_GATE_RESULTS.md`: Q6 = "O(d) / CR for zeros-from-counts" | 2026-06-05 |
| L3 / T2A / D2 | MUSIC/Prony/CFG/Stoica–Nehorai novelty notes (same project, unpublished) | 2026-06 |
| S1 / S3 | Ng 2004, Gonek–Hejhal `J_{-k}`, Kotnik–van de Lune | 2026-08-14 |
| T1_GAP16 | Hardy–Riesz Ch. V, Montgomery–Vaughan §5.1, Titchmarsh §3.7/§9.7/§14 as the *forward* citation list | 2026-08-15 |
| Canonical corpus | Ingham `ψ_1`, Titchmarsh Ch. 12–14, Odlyzko–te Riele 1985, Rife–Boorstyn, Kay, Donoho, Candès–Fernandez-Granda, Moitra | not re-fetched this session |

**This session.** Live arXiv / Scholar / IEEE / `export.arxiv.org` fetches were
blocked (WebSearch, WebFetch, and curl all rejected). No 2025–2026 preprint
sweep was completed here. Residual risk, already named by S2: a paper in an
unexpected venue (ML-for-NT, a physics arXiv, an IEEE workshop) that the
keyword intersection `"Cramér-Rao" ∩ "Riemann zeros"` misses. That risk is
not zero; it is the same risk S2 logged, plus the classical (b) angle S2
omitted, which *is* covered below from the canonical corpus and in-repo
citations.

In-house MIMO notes (MUSIC on prime counts, internal CR drafts) are
**unpublished** and are not prior art. They are listed in §5 so they are not
mistaken for a collision.

---

## 2. Angle (a) — estimation / information-theoretic bounds

Question: has anyone published a CR / Fisher / sample-complexity / minimax
bound for *estimating* `γ_j` from arithmetic sequences?

### A1. S2 scout (2026-08-14) — **NEAR-MISS on method, CLEAR on the bound**

`research_notes/rh_goals_2026-08-14/lane_c/S2_PRIOR_ART.md`. Queries:
Cramér–Rao + zeta zeros, explicit-formula inverse problem, line-spectral
estimation primes, super-resolution Riemann zeros, Fisher information
L-function. Verdict on Program A: **NO COLLISION.** Its own limitation
section is why GAP-12 exists.

### A2. Gate 0, 101-agent scan (2026-06-05) — **CLEAR on Q6**

`SPECTROSCOPY_GATE_RESULTS.md`: "Q6 (O(d) sample-complexity / Cramér–Rao for
zeros-from-counts) entirely unaddressed in literature." Independent of S2,
two months earlier, same negative on the *bound*. (Gate 0 found a near-miss
*display* cluster, recorded as A7–A8.)

### A3. Rife & Boorstyn 1974 — **NEAR-MISS**

D.C. Rife and R.R. Boorstyn, "Single-tone parameter estimation from
discrete-time observations," *IEEE Trans. Inform. Theory* **20** (1974),
591–598.

CR bound for frequency of a real cosine in white noise; discrete form
`Var(ω̂) ≥ 12 σ² / (A² N(N²−1))` (centered window). This is the algebra of
T1 Lemma 2. T1 already cites it for the 12-vs-24 convention (GAP-1). It is
generic sinusoids, not zeta zeros, and not coloured interference from the
zero tail.

### A4. Stoica & Nehorai 1989 — **NEAR-MISS**

P. Stoica and A. Nehorai, "MUSIC, maximum likelihood, and Cramér–Rao bound,"
*IEEE Trans. Acoust. Speech Signal Process.* **37** (1989), 720–741.

Multi-tone CR + MUSIC efficiency in white Gaussian noise. Relabeling `f_k →
γ_k` is textbook; it does not produce T1's amplitude cancellation
`S_ε(γ)/a_γ² = log(γ/2π)` or the sample-complexity `X(ε) ≥ exp(c ε^{-2/3})`.
In-repo adversarial note Z4 claimed T1 "is relabeled Stoica–Nehorai"; that
is true of the *sinusoid block* and false of the *N2 interference model*.

### A5. Kay, *Fundamentals of Statistical Signal Processing*, Vol. I (1993), §7.6 / Ex. 3.14 — **NEAR-MISS**

Canonical real-sinusoid CR, unknown amplitude and phase. Same role as A3–A4.
T1 Lemma 2 already names it as the source of the factor-12 convention.

### A6. van Trees / Ziv–Zakai (generic) — **CLEAR**

Bayesian CR and threshold bounds for nonlinear frequency estimation. T1
GAP-7 flags them as the route around unbiasedness. No zeta/Mertens instance
located.

### A7. Csóka, arXiv:1712.08434 (2017) — **NEAR-MISS**

S2: DFT / Fourier representation of zeta zeros from a modified von Mangoldt
sequence; zeros as superpositions of harmonic waves. Spectral *picture*, no
Fisher information, no sample-complexity bound.

### A8. Lan–Yong, *Physica A* (2006) — **NEAR-MISS**

S2 / Gate 0: power spectrum of `ψ(x) − x`; peaks at `γ_j` visible. Display,
not an estimator, not a lower bound. Gate 0's "spectral-DISPLAY cluster."

### A9. arXiv:2312.00108 (2023) and Ramanujan J. 2025 (DOI 10.1007/s11139-025-01297-y) — **NEAR-MISS**

S2: explicit formulae writing zeros (or weighted zero sums) in terms of
primes, Hermite weights; "zeros can be computed without the zeta function."
An *identity* for the inverse map, not a statistical lower bound from a
finite arithmetic range `X`. Infinite sums over primes are not a
sample-complexity statement. (Authors not re-checked this session; titles
and identifiers as in S2.)

### A10. Harald Cramér, prime-number papers (1920s–1936) *and* Cramér–Rao (1946) — **CLEAR** (bibliographic trap)

The same Cramér proved mean-square theorems for `ψ(x) − x` *and*, later, the
Cramér–Rao inequality (*Mathematical Methods of Statistics*, 1946). The
prime papers are probabilistic models of primes, not CR bounds on zero
ordinates. Do not file a collision by surname.

### A11. Goldston–Montgomery 1987; Montgomery pair correlation — **CLEAR**

Statistical relation between zeros and primes in short intervals. Not
estimation of individual `γ_j` from `M` or `ψ`, not a CR bound.

### A12. L3 / T2A novelty notes (2026-06, unpublished) — **CLEAR** (in-house)

Searches of Odlyzko, Hejhal, Sarnak, Conrey, Keating, Rubinstein, Farmer,
LMFDB algorithms, Candès–Fernandez-Granda applications, IEEE Trans. SP /
ICASSP 1986–2024 for `"MUSIC" + Riemann` / `"ESPRIT" + zeta`: no hit on
subspace recovery of zeros from prime data, and no CR bound for that
inverse problem. Consistent with A1–A2. Not a published source.

**Angle (a) sub-verdict:** no published CR / Fisher / minimax / sample-complexity
lower bound for `γ_j` from arithmetic data. The sinusoid CR algebra is
textbook (A3–A5). Inverse *identities* and FFT *displays* exist (A7–A9) and
do not bound RMSE.

---

## 3. Angle (b) — classical Riesz/Cesàro means of `M`, `ψ_1`, `1/ζ`

Question: is the T1 observable, its explicit formula, or the random-phase
model with amplitudes `1/|ρ ζ'(ρ)|` already treated *quantitatively* — and
does any of that literature invert for `γ_j` with a rate?

### B1. Hardy–Riesz 1915, Ch. V — **NEAR-MISS** (forward machine)

G.H. Hardy and M. Riesz, *The General Theory of Dirichlet's Series*,
Cambridge Tracts 18, 1915, Chapter V.

Riesz typical means of Dirichlet series; the Mellin kernel `1/(s(s+1)⋯(s+k))`
for order `k`. T1's window `W(x)=(1−x)_+`, `M_W(s)=1/(s(s+1))` *is* the
order-1 case. T1_GAP16 cites this as the classical engine. No inverse
estimation, no CR.

### B2. Ingham 1932, Ch. IV, `ψ_1(x)` — **NEAR-MISS**

A.E. Ingham, *The Distribution of Prime Numbers*, Cambridge Tracts 30, 1932,
Chapter IV (explicit formulae).

The order-1 integral `ψ_1(x) = ∫_0^x ψ(t)\,dt` has the explicit formula
`x²/2 − Σ_ρ x^{ρ+1}/(ρ(ρ+1)) − ⋯`. Same Mellin residue `1/(ρ(ρ+1))` as T1,
for Chebyshev rather than Mertens. Used to *characterise* RH (smooth
PNT remainder), not to estimate ordinates from a finite record.

### B3. Titchmarsh, 2nd ed. (Heath-Brown), Ch. 12 and Ch. 14 — **NEAR-MISS**

E.C. Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2nd ed., Oxford
1986.

- §12: explicit formulae for `ψ`, `Π`, and the integrated `ψ_1`.
- §14.25: Mellin representation `1/ζ(s) = s ∫_1^∞ M(x) x^{-s-1}\,dx`.
- §14.27 (and neighbours): `M(x) = Σ_{|γ|<T} x^ρ/(ρ ζ'(ρ)) + remainder`.

The order-1 Riesz mean of `1/ζ` is the contour integral of
`x^s /(s(s+1) ζ(s))`; residue at `ρ` is `x^ρ /(ρ(ρ+1) ζ'(ρ))`. That is T1
§1.1 / GAP-16 Proposition R, including `R_0 = −2` and the pole at `s=−1`
giving `12/N`. Textbook forward formula. Titchmarsh does not estimate `γ`
from the Cesàro mean and does not give a CR bound.

### B4. Montgomery–Vaughan, *Multiplicative Number Theory I*, §5.1 — **NEAR-MISS**

Perron / Mellin inversion, the machine GAP-16 cites for (2.3). No inverse
CR.

### B5. Odlyzko & te Riele 1985 — **NEAR-MISS** (same almost-periodic sum, opposite problem)

A.M. Odlyzko and H.J.J. te Riele, "Disproof of the Mertens conjecture,"
*J. Reine Angew. Math.* **357** (1985), 138–160.

They treat `Σ_j x^{iγ_j}/(ρ_j ζ'(ρ_j))` as an almost-periodic function of
`t = log x` and use lattice reduction (building on Jurkat–Peyerimhoff
Kronecker approximation) to find a *phase* `t` that makes the sum large,
proving `limsup M(x)/√x > 1`. Same amplitudes, same tones, *maximisation
over* `t`, not *estimation of* `γ` from a record in `t`.

### B6. Jurkat & Peyerimhoff 1976 — **NEAR-MISS**

W. Jurkat and A. Peyerimhoff, "A constructive approach to Kronecker
approximations and its application to the Mertens conjecture," *J. Reine
Angew. Math.* **286/287** (1976), 332–348.

Diophantine approximation on the torus of zero ordinates. Input is known
`γ_j`; output is a good `t`. Reverse of T1.

### B7. Ng 2004, *Proc. London Math. Soc.* — **NEAR-MISS** (strongest model collision)

Nathan Ng, "The distribution of the summatory function of the Möbius
function," *Proc. London Math. Soc.* (3) **89** (2004), 361–389.
(arXiv:math/0310381; PDF logged in `lane_c/S1_ZERO_SUM_LIT.md`.)

Under RH + simple zeros + Gonek–Hejhal, `e^{-y/2} M(e^y)` has a limiting
distribution, realised as a random almost-periodic function whose
coefficients are `1/(ρ ζ'(ρ))` and whose phases are random (linear
independence of the `γ`'s). This is T1's signal model (M1)–(M3), used to
study the *law of `M(x)`*, not to bound `RMSE(γ̂)`. The β-constant
`Σ 1/|ρ ζ'(ρ)|²` is the mean-square of that model (S1/S3; in-repo
`mertens_square_sum_closed_form_attack.md`). No Fisher information, no
`X(ε)`.

### B8. Gonek–Hejhal `J_{-k}`; Hughes–Keating–O'Connell; Milinovich–Ng — **NEAR-MISS** (amplitudes)

Negative moments `J_{-k}(T) = Σ_{γ≤T} 1/|ζ'(ρ)|^k`. T1 uses the *first*
moment (`J_{-1} = O(T)`) for absolute convergence of the zero sum (GAP-16)
and cancels amplitudes in the leading CR constant (draft §7.2). These papers
supply the amplitude law. They do not estimate ordinates from `M`.

### B9. Pintz; Soundararajan 2009; Kotnik–van de Lune 2004; Kotnik–te Riele 2006; Hurst 2018 — **CLEAR** / weak **NEAR-MISS**

Ω-results and computation of `M(x)` (how large `|M|/√x` gets; tables).
They consume zeros to bound or compute `M`, or compute `M` directly. They
do not invert for `γ` and do not state a CR bound.

- J. Pintz, oscillatory properties / effective disproof of Mertens
  (Acta Arith. / Astérisque 1987).
- K. Soundararajan, "Partial sums of the Möbius function," *J. Reine Angew.
  Math.* **631** (2009), 159–184.
- T. Kotnik and J. van de Lune, "On the order of the Mertens function,"
  *Experiment. Math.* **13** (2004), 473–481 (S3).
- T. Kotnik and H. te Riele, "The Mertens conjecture revisited," ANTS-VII,
  LNCS 4076 (2006).
- G. Hurst, *Math. Comp.* **87** (2018), improved Mertens bounds.

### B10. Humphries — **CLEAR** on the T1 claim; no Cesàro-inverse paper located

No Humphries paper is in the local corpus. The published Humphries work that
touches Mertens-type objects is function-field Mertens/Pólya and
distributional / zero-density estimates, not a CR bound and not an inverse
estimator of `γ_j` from the Cesàro mean of `M` over `ℤ`. If a Humphries
paper treats the order-1 Riesz explicit formula *quantitatively as a forward
remainder*, it is in the same bin as B3 (NEAR-MISS on the formula, CLEAR on
the bound). **Not re-fetched this session;** this row is a named gap in the
live sweep, not a claimed empty set.

### B11. Weil 1952 / Guinand explicit formulae — **NEAR-MISS**

Fourier duality between primes and zeros. Uniqueness: the zeros determine
the primes and conversely (in the sense of the explicit formula). No finite-`X`
RMSE bound.

### B12. Iwaniec–Kowalski, *Analytic Number Theory*, explicit-formula chapters — **NEAR-MISS**

Standard modern reference for the same forward formulae. GAP-16 / the
smoothed-Dwf import already classify the Gaussian-window analogue as
"essentially classical (Landau, Ingham, Titchmarsh, Iwaniec–Kowalski)."

### B13. Wintner; Good–Churchhouse 1968 — **NEAR-MISS** (older random models of `μ`/`M`)

Almost-periodic / pseudorandom models of Möbius. Ancestors of Ng's
random-phase model. Not estimation of zeros.

### B14. T1_GAP16 Proposition R (2026-08-15, this repo) — **not prior art**

The order-1 Riesz explicit formula with `R_0=−2`, `R_{-1}=12/N`, amplitudes
`1/(|½+iγ||3/2+iγ||ζ'(ρ)|)` is derived there as a *citation* of B1–B4, not
as a discovery. Confirms that angle (b) is import, not novelty.

**Angle (b) sub-verdict:** the observable, the explicit formula, the
amplitudes, and the random-phase almost-periodic model are classical. The
*inverse* CR bound is not. Closest occupants: Ng (model) and Odlyzko–te Riele
(same sum, maximise `t` rather than estimate `γ`).

---

## 4. Angle (c) — super-resolution / line-spectral lower bounds

Question: nearest engineering analogue, and has anyone mapped it to zeta zeros?

Regime fact (load-bearing): T1 assumes (M5), `T · min_{j≠k}|γ_j−γ_k| ≥ 2πK`
with `K≥4`. That is *Rayleigh-separated*. The `T^{-3/2}` CR is Rife–Boorstyn
(A3), not Moitra's sub-Rayleigh exponential barrier. Super-resolution would
become relevant only if (M5) were dropped toward the true gap `2π/log(γ/2π)`
— that is T1 GAP-13, a *different* resource bound `X ≥ (γ_d/2π)^K`, not
T1-c.

### C1. Donoho 1992 — **NEAR-MISS** analogue, **CLEAR** on zeta

D.L. Donoho, "Superresolution via sparsity constraints," *SIAM J. Math.
Anal.* **23** (1992), 1309–1331.

Sparse atomic measures can be uniquely recovered from bandlimited data if
spikes are sufficiently separated. No zeta/Mertens instance. S2/L3: not
applied to L-zeros.

### C2. Candès–Fernandez-Granda 2013/2014 — **NEAR-MISS** analogue, **CLEAR** on zeta

E.J. Candès and C. Fernandez-Granda, "Towards a mathematical theory of
super-resolution," *Comm. Pure Appl. Math.* **67** (2014), 906–956
(arXiv:1203.5871); "Super-resolution from noisy data," *J. Fourier Anal.
Appl.* **19** (2013), 1229–1254.

TV / atomic-norm recovery of spikes from low-pass samples, minimum
separation ~ two Rayleigh lengths. Deterministic exact recovery, not a CR
for well-separated tones in coloured noise. L3: "no record of it being
applied to L-function zeros or prime-count data." In-repo Gate 3 /
close-pair probe *tested* sub-Rayleigh recovery on real L-zeros and killed
it; that is this project's experiment, not a published mapping.

### C3. Moitra 2015 — **NEAR-MISS** analogue, **CLEAR** on zeta

A. Moitra, "Super-resolution, extremal functions and the condition number of
Vandermonde matrices," STOC 2015 (arXiv:1408.1683).

Worst-case SNR to resolve `s` spikes with min separation `Δ` is exponential
in `1/Δ` below Rayleigh. Nearest *lower-bound* analogue in engineering. Not
T1's regime (T1 is above Rayleigh). No paper located that writes a Moitra
bound with `Δ = min|γ_j−γ_k|` and arithmetic data as the samples.

### C4. Tang–Bhaskar–Shah–Recht 2013 — **CLEAR** on zeta

"Compressed sensing off the grid," *IEEE Trans. Inform. Theory*. Atomic-norm
line spectral estimation. S2 lists this cluster; no prime/zeta hit.

### C5. Schmidt 1986 MUSIC; Roy–Kailath 1989 ESPRIT — **NEAR-MISS** (estimators, not lower bounds)

Subspace estimators. This project applied MUSIC to prime-count bias
(unpublished; Gate 2: ties a Hann periodogram). No published CR for that
application (A12). Estimators are not T1.

### C6. Fernandez-Granda lecture notes / "Superfast LSE" arXiv:1705.06073; ESPRIT super-resolution limit arXiv:1905.03782 — **CLEAR** on zeta

S2's line-spectral cluster. Generic multisinusoidal signals. S2: "No search
result connects this machinery to prime-counting functions or Riemann zeros."

**Angle (c) sub-verdict:** the engineering lower-bound literature is real and
is the right analogue to *cite*. Nobody has mapped it onto zeta zeros.
T1's headline rate is the Rayleigh-separated Rife–Boorstyn rate, not
Moitra.

---

## 5. In-house unpublished (do not file as prior art)

| artifact | what it is | why it is not a collision |
|---|---|---|
| MIMO Gate 0–3, SPECTROSCOPY_GATE_RESULTS | MUSIC / periodogram recovery of L-zeros from prime bias; Q6 named as unaddressed | unpublished; and it is an *estimator*, not a CR paper |
| D2 / Z4 / X2 CR notes | internal fight over Stoica–Nehorai relabeling | unpublished; settled as: sinusoid block textbook, N2 model not |
| T1 draft v1–v3 | the claim under review | not prior art for itself |
| T1_GAP16 Prop. R | forward formula under A2 | citation of B1–B4 |

---

## 6. Summary table

| # | source | angle | verdict |
|---|---|---|---|
| A1 | S2 scout 2026-08-14 | a | CLEAR on the bound (NO-COLLISION, weak negative) |
| A2 | Gate 0, 101-agent, 2026-06-05 | a | CLEAR on Q6 |
| A3 | Rife–Boorstyn 1974 | a/c | NEAR-MISS (CR algebra) |
| A4 | Stoica–Nehorai 1989 | a | NEAR-MISS (multi-tone CR in white noise) |
| A5 | Kay FSSP I | a | NEAR-MISS (convention 12) |
| A6 | van Trees / Ziv–Zakai | a | CLEAR |
| A7 | Csóka 2017 | a | NEAR-MISS (DFT display) |
| A8 | Lan–Yong 2006 | a | NEAR-MISS (power-spectrum display) |
| A9 | arXiv:2312.00108; Ramanujan J. 2025 | a | NEAR-MISS (inverse identity, no rate) |
| A10 | Cramér primes vs Cramér–Rao | a | CLEAR (surname trap) |
| A11 | Goldston–Montgomery | a | CLEAR |
| B1 | Hardy–Riesz 1915 Ch. V | b | NEAR-MISS (window / Riesz means) |
| B2 | Ingham `ψ_1` | b | NEAR-MISS (same residue, Chebyshev) |
| B3 | Titchmarsh §§12, 14 | b | NEAR-MISS (Cesàro-Mertens explicit formula) |
| B4 | Montgomery–Vaughan §5.1 | b | NEAR-MISS (Perron) |
| B5 | Odlyzko–te Riele 1985 | b | NEAR-MISS (same sum, max `t`) |
| B6 | Jurkat–Peyerimhoff 1976 | b | NEAR-MISS (Kronecker on `γ`) |
| B7 | Ng 2004 PLMS | b | NEAR-MISS (random-phase model) |
| B8 | Gonek–Hejhal / HKO / Milinovich–Ng | b | NEAR-MISS (amplitudes) |
| B9 | Pintz, Soundararajan, Kotnik, Hurst | b | CLEAR / weak NEAR-MISS (`M(x)` size) |
| B10 | Humphries | b | CLEAR on the claim (live-fetch gap) |
| B11 | Weil–Guinand | b | NEAR-MISS (Fourier duality) |
| C1 | Donoho 1992 | c | NEAR-MISS analogue; CLEAR on zeta |
| C2 | Candès–Fernandez-Granda | c | NEAR-MISS analogue; CLEAR on zeta |
| C3 | Moitra 2015 | c | NEAR-MISS analogue; CLEAR on zeta |
| C4–C6 | off-grid CS, MUSIC/ESPRIT, LSE limits | c | CLEAR on zeta (estimators / generic LSE) |

**Zero COLLISION rows.**

What *would* have been a collision, and was not found:

- `Var(γ̂) ≥ c S_ε(γ) / (a_γ² (log X)^3)` or any equivalent Fisher bound
  for zeros from `M`, `μ`, `ψ`, or `π`.
- Sample complexity `X(ε) ≫ exp(c ε^{-2/3})` (or any exponential-in-`ε^{-α}`
  arithmetic-range bound) for estimating zero ordinates.
- A Moitra / Candès–Fernandez-Granda / Donoho theorem with Riemann zeros as
  the spike train and Möbius/Mertens as the time series.

---

## 7. What T1 may claim, and what it must cite

**May claim (on present evidence):** a CR lower bound *in model N2* for
band-limited estimators of the Cesàro-Mertens line spectrum, with amplitude
cancellation and the displayed `√6` / `exp(c ε^{-2/3})` constants, is not in
the published literature.

**Must cite as occupied ingredients, not as discovery:**

- order-1 Riesz / Cesàro explicit formula for `M` and `ψ_1` (B1–B4, B12);
- random-phase almost-periodic model with coefficients `1/(ρ ζ'(ρ))` (B7, B5);
- real-cosine frequency CR, factor 12 vs 24 (A3–A5);
- super-resolution lower bounds as the *other* engineering regime (C1–C3),
  with the (M5) vs sub-Rayleigh distinction stated.

That citation list is exactly GAP-16 (forward formula) plus GAP-1 (CR
convention) plus this scout. It is not a scoop of T1-c / T1-d.

**G-c reading.** S2's NO-COLLISION on the *bound* survives the widened
search. It does *not* survive as "the observable is new": A2 landed on a
classical object. The honest gate status is: **bound unoccupied, setup
occupied.**

---

## 8. Residual risk

1. Live 2025–2026 arXiv sweep not run this session (network blocked). S2
   covered 2018–2026 as of 2026-08-14; twelve days of new preprints are
   unchecked.
2. Humphries row is a named incomplete fetch, not a proof of absence.
3. Venue silo (S2): ML-for-NT or a physics arXiv paper that never says
   "Cramér–Rao" but proves an equivalent minimax bound under a different
   name. Gate 0's 101-agent scan (2026-06-05) and L3's named-author sweep
   make this unlikely for the exact claim, not impossible.
4. Function-field exact Prony recovery of L-polynomials from point counts
   is classical (Weil); S2 Program B already called that a collision on the
   *theorem* and no collision on the *name*. It is a different inverse
   problem (finite Euler product, exact, `O(d)` counts) and does not bound
   RMSE for ζ-zeros from `M(x)`.

---

OVERALL: PARTIAL-COLLISION
