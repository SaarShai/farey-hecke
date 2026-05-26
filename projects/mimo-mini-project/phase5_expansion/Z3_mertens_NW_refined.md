---
model: mimo-v2.5-pro
max_tokens: 14000
---

# Z3 — Refined Mertens-NW formula

## Current state

Empirical:
- Pearson(NW(Q) − C, |M(Q)|) = +0.892
- Simple formula NW(Q) − C ≈ M(Q)²/(6Q) from m=1 Mikolás term matches:
  - Q=300k: predicted 0.027, observed 0.029 (7%)
  - Q=10⁶: predicted 0.0075, observed 0.0094 (25%)
  - Q=50k: predicted 0.00176, observed -0.0057 (formula gives EXCESS, observed is DEFICIT)

Mikolás Fourier formula:
J(Q) = (1/2π²) Σ_{m≥1} |S_Q(m)|² / m²
where S_Q(m) = 1 + Σ_{d|m, d≤Q} d · M(Q/d).

The constant C comes from the average of |S_Q(m)|²/m² over m. The fluctuations NW(Q) − C come from deviations.

## Tasks

### A. Refined formula

Express:
NW(Q) − C = Q/Φ(Q) · (1/2π²) Σ_m [|S_Q(m)|² − ⟨|S_Q(m)|²⟩] / m²
         ≈ (π²/(6Q)) · (1/2π²) Σ_m [|S_Q(m)|² − ⟨|S_Q(m)|²⟩] / m²
         = 1/(12Q) · Σ_m [|S_Q(m)|² − ⟨|S_Q(m)|²⟩] / m²

For m=1: S_Q(1) = 1 + M(Q). |S_Q(1)|² = (1+M(Q))² ≈ M(Q)² for large M.
Average ⟨|S_Q(1)|²⟩ for typical Q ≈ Q (by RH heuristic, since Var(M) ~ Q under RH random model).

So the FLUCTUATION term is M(Q)² - Q, divided by 12Q:
NW(Q) − C ≈ (M(Q)² − Q)/(12Q · 1²) + similar terms for higher m.

Wait — this gives a NEGATIVE contribution when M(Q)² < Q (e.g., at Q=50k where M=23, M²=529, but Q=50000 → M² − Q = -49471, negative). This matches the observed DEFICIT at small Q.

Let me verify:
- Q=50k: (M² − Q)/(12Q) = (529 − 50000)/600000 = -49471/600000 = -0.0824 — too large negative, doesn't match observed -0.0057.

Hmm. The above derivation isn't right. Let me redo with proper normalization.

J(Q) ~ (Q/12) on average (verified at multiple Q in the smooth track ≈ 0.6699 × Φ(Q)/Q ≈ 0.6699 × 3Q/π²). So J(Q) ~ 0.2036 × Q on average. Then NW(Q) = Q · J(Q) / Φ(Q) ~ 0.2036 × Q² / (3Q²/π²) = 0.2036 × π²/3 = 0.670. So C = 0.670 ≈ 0.66989. ✓

For the FLUCTUATION:
NW(Q) − C = Q/Φ(Q) · (J(Q) − ⟨J(Q)⟩)
         ≈ π²/(3Q) · ΔJ(Q)

And ΔJ(Q) comes from the Mikolás formula's m=1 term: |M(Q)|²/(2π²) (subtract the "typical" |M|² which is ~Q under RH).

ΔJ(Q) ≈ (|M(Q)|² − Q)/(2π²)

So NW(Q) − C ≈ π²/(3Q) · (|M(Q)|² − Q)/(2π²) = (|M(Q)|² − Q)/(6Q).

For Q=300k: (220² − 300000)/(6·300000) = (48400 − 300000)/1800000 = -0.140. Observed: +0.029. Doesn't match!

So my derivation is wrong somewhere. Or the typical |S_Q(1)|² isn't Q.

Help me derive the CORRECT refined formula.

### B. Why does the simple M(Q)²/(6Q) work approximately?

Empirically, the formula M(Q)²/(6Q) matches at large Q. Maybe the offset Q is absorbed into C? Let me reconsider:

C is defined as lim NW(Q). If NW(Q) = C + Δ, and Δ depends on Q via M(Q), then:

NW(Q) − C = Δ

The m=1 contribution to J(Q) is |S_Q(1)|²/(2π²) = (1+M(Q))²/(2π²). This contributes (1+M(Q))² Q / (Φ(Q) · 2π²) ≈ (1+M(Q))² / (6Q) to NW(Q).

But this is PART of NW(Q), not part of (NW(Q) − C). The m=1 contribution averages to some baseline value c₁; the fluctuation around c₁ is what correlates with M(Q).

What's ⟨(1+M(Q))²⟩ for "random" Q? If M behaves like √Q · Gaussian (RH heuristic), ⟨M(Q)²⟩ ≈ Q · K for some constant K (related to Selberg's variance).

So the FLUCTUATION:
Δ_{m=1} ≈ [M(Q)² − Q·K] / (6Q) = M(Q)²/(6Q) − K/6

The K/6 is absorbed into C. The fluctuation visible in NW(Q) − C is then M(Q)²/(6Q) MINUS some Q-independent constant.

For Q=300k: M²/(6Q) = 48400/1800000 = 0.0269. Match. ✓
For Q=50k: M²/(6Q) = 529/300000 = 0.00176. But observed is -0.0057.

The deficit at small Q implies that the m=1 contribution is BELOW the typical average, not above. So when M(Q) is unusually small, NW(Q) is below C.

So formula: NW(Q) − C ≈ M(Q)²/(6Q) − (typical_M²)/(6Q) = (M² − typical_M²)/(6Q).

At Q=50k, typical M² might be ~50000 (under RH variance), giving (529 − 50000)/(300000) = -0.165 — too large in magnitude.

Hmm. The empirical correlation is +0.892 with |M(Q)| (not M(Q)² − typical), so this picture is incomplete.

### C. Correct derivation

Carefully derive the closed form for NW(Q) − C as a function of {M(Q/d)}_{d ≥ 1}. Identify which terms contribute.

Predict NW(926265) precisely.

## What I want

Sharp closed-form prediction. Honest about Q-dependent baseline.
