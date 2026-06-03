# Function-field (𝔽_q[t]) −1/variance exploration — findings (2026-06-02)

Goal: test whether the Fiorilli–Martin "−1 is the least-biased non-residue" phenomenon has an
**unconditional** analogue over 𝔽_q[t] (where RH is Weil's theorem, not a conjecture).

## What was computed
- `ff_variance_poc.py`: brute-force prime-polynomial race, mean-square amplitude (unconditional,
  hypothesis-free) to degree N=12 over 𝔽_3.
- `ff_exact.py`: EXACT per-character L-polynomial computation for **irreducible (prime)** moduli —
  V(M;a,1)=Σ_{χ≠χ₀}|χ(a)−1|²·N_χ, N_χ = deg L(u,χ) = #Frobenius zeros (all |·|=√q, Weil-checked).

## Finding (UNCONDITIONAL, Weil; verified on 3 moduli)
For a **prime (irreducible) modulus** M of degree d over 𝔽_q, **every** non-principal character χ
has the same L-degree N_χ = d−1 (verified: 𝔽_3 deg-3 → all N_χ=2, V≡104 over all 13 NR; 𝔽_7 deg-3
→ all N_χ=2, V≡1368 over 171 NR; 𝔽_3 deg-5 → all N_χ=4, V≡1936 over 121 NR; |Frob|=√q exactly).
Hence **V(M;a,1) = (d−1)·Σ_χ|χ(a)−1|² = 2(d−1)φ(M) is CONSTANT across all non-residues.**

⇒ **The FM "−1 is uniquely least-biased mod a prime" effect does NOT transfer to function-field
prime moduli — the variance is degenerate (all non-residues tie).** Conceptually: the entire −1
phenomenon over ℚ is an **archimedean** effect (the Γ-factor 2log2 gap + height-weighting
1/(¼+γ²) of zeros); over 𝔽_q[t] all finite zeros have equal weight (Weil) and there is no
archimedean factor at the finite primes, so the distinction collapses.

## Honest scope / caveats (do NOT overclaim)
1. **PoC pitfall, corrected:** the N=12 brute force spuriously showed "−1 rank 1" (e.g. V=354 vs
   ~130); that was **finite-N noise** in the cross-character oscillations. The exact character
   computation (degenerate) is the truth. (Adversarial-honesty catch.)
2. **Infinite place NOT modelled:** `ff_exact.py` uses only the finite-prime L-polynomial zeros.
   The full Cha RS variance may carry an **infinite-place / parity** term (the genuine analogue of
   ℚ's archimedean 2log2) that could restore a −1 effect. **Unresolved** — needs Cha's exact
   variance formula (Compositio 2008); the automated PDF extraction was too fuzzy to trust.
3. **Composite moduli:** there N_χ varies by conductor and V is non-degenerate, but that régime is
   largely covered by **Sedrati (Mathematika 2022, arXiv:2110.06669)** — *conditional on LI*. Whether
   the specific −1-max-variance ordering there is open / unconditional needs the full-text read.

## Verdict on "significant contribution" from this thread
The splashy "unconditional FM-analogue over 𝔽_q[t]" is **not cleanly panning out**: the prime case
is degenerate (no −1 effect to make unconditional — and likely an expert-known corollary of the
uniform L-degree), and the substantive composite case is largely Sedrati 2022. A genuine result
survives **only if** (a) the infinite-place term restores a −1 effect (open, needs Cha's formula),
or (b) the composite −1-ordering is open and can be made RH-only/unconditional. Both require the
primary-text read before any novelty claim. Current honest status: a clarifying observation
(−1/variance is degenerate at function-field prime moduli; the ℚ effect is archimedean), not yet a
significant theorem.

## RESOLUTION (2026-06-02, gate (a) settled — NEGATIVE) — from Cha 2008 full text
Read Cha (Compositio 144 (2008) 1351–1374) in full (pdftotext). Decisive:
- **Correct variance weight is γ/(γ−1) per inverse zero, NOT uniform** (Cha eq. (36); the b_j
  vectors b_j = −χ̄_j(a)·γ_j/(γ_j−1), p.1359). So `ff_exact.py`'s uniform-weight "degeneracy"
  was an ARTIFACT (wrong weight); and the brute-force PoC "−1 max" was finite-N noise. Neither
  of my computations was the right object.
- **GSH/LI is PROVABLY VIOLATED for many moduli** (Cha §5). His Example 5.1 is EXACTLY our Case B:
  p=3, m=T³+2T+1, L(u)=3u²−3u+1, inverse zeros √3·e^{±iπ/6} — rational angle ⇒ GSH violated ⇒ the
  race is PERIODIC (mod 12), not equidistributed. Cha §5 shows the bias can be toward squares,
  nonsquares, OR nonexistent, depending on m — "this contrasts with the number field case."
- Consequence: **there is NO unconditional, universal "−1 is least-biased" over 𝔽_q[t].** Weil gives
  RH (zeros on |·|=√q) but the BIAS needs GSH (LI of the zero angles), which fails over function
  fields. The hoped-for unconditional FM-analogue does not exist; the framework + the GSH-violation
  phenomenon are already in Cha 2008, and the density rates under LI are in Sedrati 2022.

**Verdict:** function-field −1/variance thread is CLOSED as a source of a significant new result.
Value delivered: prevented a wrong "unconditional −1 over 𝔽_q[t]" claim (prior-art + primary-text
discipline). The ℚ result (LEDGER §1) stands as the real content; its conditionality on GRH+LI is
genuine and not escapable via function fields.
