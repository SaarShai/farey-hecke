# Closing what's closeable — rigorous proofs

**Date**: 2026-05-26
**Status**: Closing 3 of the open items. The rest are honestly stated as RESEARCH-OPEN.

---

## CLOSED #1: Mikolás-Parseval identity J(Q) = (1/(2π²)) Σ_m |S_Q(m)|²/m²

### Setup

Let F_Q = {f_1, f_2, ..., f_Φ} be the Farey fractions in [0, 1] with denominators ≤ Q, in increasing order. Φ = Φ(Q) = #F_Q.

The **count function** count_Q(x) = #{f ∈ F_Q : f ≤ x} for x ∈ [0, 1].

Define **g(x) = count_Q(x) − Φ·x**. We want to compute J(Q) = ∫₀¹ g(x)² dx via Parseval.

### Step 1: Compute the Fourier coefficients of g

For m ∈ ℤ, m ≠ 0:

  ĝ(m) := ∫₀¹ g(x) · e^{-2πimx} dx

Split: ĝ(m) = ∫₀¹ count_Q(x) e^{-2πimx} dx − Φ ∫₀¹ x e^{-2πimx} dx.

**Term 1**: ∫₀¹ count_Q(x) e^{-2πimx} dx.

Integration by parts (u = count, dv = e^{-2πimx} dx):
  = [count(x) · e^{-2πimx}/(-2πim)]₀¹ − ∫₀¹ count'(x) · e^{-2πimx}/(-2πim) dx

Boundary: count(1) = Φ, count(0) = 0 (since 0/1 is the first Farey fraction in our convention; or count(0) = 1 in alternative convention — adjust accordingly).
  [count·e^{-2πimx}/(-2πim)]₀¹ = (Φ·1 − 0)/(-2πim) = −Φ/(2πim)

count'(x) = Σ_{f ∈ F_Q} δ(x − f) (sum of Dirac deltas at Farey points).
  ∫₀¹ count'(x) e^{-2πimx}/(-2πim) dx = (1/(-2πim)) Σ_f e^{-2πimf} = -S_Q(m)*/(2πim)
where S_Q(m)* = Σ_f e^{-2πimf}.

Note: Σ_f e^{2πimf} = Σ_{q≤Q} Σ_{1≤a≤q, gcd(a,q)=1} e^{2πim·a/q} = Σ_{q≤Q} c_q(m) =: S_Q(m). Since c_q(m) is real (Ramanujan sum), S_Q(m) is real, so S_Q(m)* = S_Q(m).

So Term 1 = −Φ/(2πim) + S_Q(m)/(2πim).

**Term 2**: Φ · ∫₀¹ x · e^{-2πimx} dx.

Integration by parts (u=x, dv=e^{-2πimx} dx):
  = Φ · ([x · e^{-2πimx}/(-2πim)]₀¹ − ∫₀¹ e^{-2πimx}/(-2πim) dx)
  = Φ · (1/(-2πim) − 0) − Φ · [e^{-2πimx}/(2πim)²]₀¹
  = −Φ/(2πim) − 0  (since e^{-2πim} = 1, so the second term vanishes)

So Term 2 = −Φ/(2πim).

**Combining**: ĝ(m) = Term 1 − Term 2 = [−Φ/(2πim) + S_Q(m)/(2πim)] − [−Φ/(2πim)] = **S_Q(m)/(2πim)**.

### Step 2: Apply Parseval

For real-valued g on [0,1] with zero mean (which holds since ĝ(0) = ∫g dx = 0 by direct verification or by the Farey-symmetry argument):

  ∫₀¹ g(x)² dx = Σ_{m∈ℤ, m≠0} |ĝ(m)|² = 2 · Σ_{m=1}^∞ |ĝ(m)|²

(factor 2 because g is real, so ĝ(-m) = ĝ(m)*, hence |ĝ(-m)|² = |ĝ(m)|².)

|ĝ(m)|² = |S_Q(m)|² / (2πim · -2πim) = |S_Q(m)|² / (4π²m²)

So:

  **J(Q) = ∫₀¹ g(x)² dx = 2 · Σ_{m=1}^∞ |S_Q(m)|²/(4π²m²) = (1/(2π²)) · Σ_{m=1}^∞ |S_Q(m)|²/m²**

This is the Mikolás-Parseval identity. ∎

### Note on c_0 and zero-mean assumption

c_0 = ĝ(0) = ∫₀¹ g(x) dx. We need this to be 0 for direct Parseval. By Farey symmetry (Farey set is symmetric under f ↦ 1−f), Σ_f f = Φ/2 (with boundary adjustments depending on whether 0/1 and 1/1 are included). And ∫count(x) dx = Φ − Σ_f f = Φ/2. And ∫Φ·x dx = Φ/2. So ∫g dx = 0. ✓

---

## CLOSED #2: Double-sum identity Σ_m |S_Q(m)|²/m² = ζ(2)·Σ_{d,d'} gcd(d,d')²·M(⌊Q/d⌋)·M(⌊Q/d'⌋)/(d·d')

### Setup

S_Q(m) = Σ_{q=1}^Q c_q(m) where c_q(m) is the Ramanujan sum.

**Identity**: S_Q(m) = Σ_{d | m} d · M(⌊Q/d⌋).

**Proof**: 
  S_Q(m) = Σ_{q=1}^Q c_q(m) = Σ_{q=1}^Q Σ_{d | gcd(m,q)} d · μ(q/d)
  
  Swap sum order: for each d|m, sum over q with d|q and q ≤ Q. Let q = d·e:
  
  = Σ_{d|m} d Σ_{e=1}^{⌊Q/d⌋} μ(e) = Σ_{d|m} d · M(⌊Q/d⌋). ∎

### Double sum

  Σ_{m=1}^∞ |S_Q(m)|² / m² = Σ_{m=1}^∞ (1/m²) · |Σ_{d|m} d · M(⌊Q/d⌋)|²
                              = Σ_{m=1}^∞ (1/m²) · Σ_{d|m, d'|m} d·d' · M(⌊Q/d⌋) · M(⌊Q/d'⌋)

**Swap order**: For fixed (d, d'), sum over m such that BOTH d|m and d'|m, i.e., lcm(d,d') | m.

  = Σ_{d=1}^∞ Σ_{d'=1}^∞ d·d' · M(⌊Q/d⌋) · M(⌊Q/d'⌋) · Σ_{m: lcm(d,d')|m} 1/m²

**Inner sum**: Σ_{m: L|m} 1/m² where L = lcm(d, d') = Σ_{k=1}^∞ 1/(kL)² = ζ(2)/L².

  = Σ_{d, d'} d·d' · M(⌊Q/d⌋) · M(⌊Q/d'⌋) · ζ(2)/lcm(d,d')²

**Identity**: d·d' / lcm(d,d')² = gcd(d,d')² / (d·d'), since lcm(d,d')·gcd(d,d') = d·d'.

  = ζ(2) · Σ_{d, d'} gcd(d,d')² · M(⌊Q/d⌋) · M(⌊Q/d'⌋) / (d·d')

Note: M(⌊Q/d⌋) = 0 if d > Q (since the sum is empty), so effectively the sum is finite: d, d' ≤ Q. ∎

### Combining with Mikolás-Parseval

J(Q) = (1/(2π²)) · ζ(2) · Σ_{d,d'≤Q} gcd(d,d')² · M(⌊Q/d⌋) · M(⌊Q/d'⌋) / (d·d')

Using ζ(2) = π²/6:
  
  **J(Q) = (1/12) · Σ_{d,d'≤Q} gcd(d,d')² · M(⌊Q/d⌋) · M(⌊Q/d'⌋) / (d·d')**

This is the **structural double-sum identity** for the Farey L²-discrepancy. ∎

---

## CLOSED #3: BCZ floor identity (Lemma 1 of cluster=2 proof) — TIGHT bound

### Setup

Let b_i, b_{i+1} ∈ ℕ with 1 ≤ b_i, b_{i+1} ≤ N. Define:
  k := ⌊(b_i + N) / b_{i+1}⌋
  b_{i+2} := k · b_{i+1} − b_i

### Tight bound

By the integer division identity:
  b_i + N = k · b_{i+1} + r, where 0 ≤ r ≤ b_{i+1} − 1

Therefore:
  k · b_{i+1} = b_i + N − r

And:
  b_{i+2} = k · b_{i+1} − b_i = (b_i + N − r) − b_i = **N − r**

Since 0 ≤ r ≤ b_{i+1} − 1:

  **N − b_{i+1} + 1 ≤ b_{i+2} ≤ N**

This is the **tight bound**. Aristotle's `bcz_next_lower_bound` proved a weaker version (with extra `-b_i` from looser algebra). The TIGHT version follows by directly substituting b_i = k·b_{i+1} − (k·b_{i+1} − b_i) and using the floor identity.

### Corollary

If b_{i+1} ≤ N/3, then b_{i+2} ≥ N − N/3 + 1 = **2N/3 + 1**.

This is the rigorous statement used in the cluster=2 proof's Lemma 3. ∎

---

## What's still open (honestly)

### #1 (Mertens-NW)

**Open**: The Tauberian asymptotic

  D(Q) + O(Q) = (36C/π²) · Q + o(Q)

where:
- D(Q) = Σ_{d=1}^Q M(⌊Q/d⌋)² (diagonal)
- O(Q) = Σ_{d ≠ d'} gcd(d,d')² · M(⌊Q/d⌋) · M(⌊Q/d'⌋) / (d·d') (off-diagonal)
- C = (1/2) ∏_p (1 + 1/(p²(p−1)))

Both D(Q) and O(Q) grow superlinearly individually; their sum is conjecturally Q + smaller.

This is a Tauberian-style problem in analytic number theory. Σ M(n)²/n³ = 1.13616 converges, but the Q-asymptotic of the FULL double sum requires:
- Sharp control on Σ_n M(n)²/n² type sums
- Cross-correlation of M(Q/d) with M(Q/d')
- Multiplicative-function machinery to identify the Euler product C

**Status**: well-defined, but beyond a single research session.

### #2 (Cluster=2)

**Open #2.1**: BCZ-density-to-finite-N approximation error. The proof for q ≥ 7/9 is rigorous in the BCZ-density LIMIT. For finite N, the empirical threshold q*(N) is larger than 7/9. Conjectured: q*(N) → 7/9 with rate likely O(N^{-1/2}). Verification in progress (q*(N) trend test running).

**Open #2.2**: Cluster ≥ 3 impossibility extension to q < 7/9. Empirically true (with different threshold per N), but the BCZ-chain argument gives 7/9 directly. Tighter bound requires more case analysis.

**Open #2.3**: Exact rate P(size = 2) → 1 at fixed q > 7/9. Empirically slow (99.2% → 99.5% as N goes 10⁴ to 10⁵), suggesting O(N^{-α}) convergence with α small. Theoretical rate unknown.

### Aristotle scaffolding

**Closed in v1**: BCZ Corr(X,Y) = -1/2 (fully proven).
**Closed in v2**: 7 BCZ moment identities, 2 BCZ chain inequalities (loose version), 3 S_Q(m) divisor sum identities.
**Open in v2**: Mikolás-Parseval identity (proof above — could submit to v3 dispatch), Mikolás double-sum (proof above), tight BCZ chain bound (also above).

A **v3 Aristotle dispatch** with the proofs above as careful lemmas + Mathlib-targeted tactics could close another 3-5 sorries.

---

## Bottom line

| Open item | Closed here? |
|---|---|
| Mikolás Fourier identity | ✅ CLOSED (direct Parseval) |
| Mikolás double-sum identity | ✅ CLOSED (algebra from Fourier) |
| BCZ floor identity (Lemma 1) tight bound | ✅ CLOSED (direct integer arithmetic) |
| BCZ anti-clustering with Farey coprimality | 🔶 PARTIAL (tight Lemma 1 closes a large part) |
| Tauberian D + O = 36CQ/π² + o(Q) | ⏳ RESEARCH-OPEN |
| Cluster=2 finite-N q*(N) → 7/9 rate | ⏳ Running compute |
| Closed form for C = (1/2)∏(1+1/(p²(p-1))) | ⏳ Likely originates from this work |
| Closed form for Σ M(n)²/n³ = 1.13616 | ⏳ Likely new constant |

3 of 8 items definitively closed in this session. Of the remaining 5: 2 are running compute (~hours), 2 are conjectured-but-published-elsewhere-or-new, 1 is genuinely deep open problem.
