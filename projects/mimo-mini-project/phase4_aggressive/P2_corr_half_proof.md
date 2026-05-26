---
model: mimo-v2.5-pro
max_tokens: 16000
---

# P2 — PROOF attempt: lim Corr(d_i, d_{i+1}) = 1/2 for Farey gaps

## The empirical fact (Discovery #2)

Define the Pearson correlation of consecutive Farey gaps:

  ρ_N = Σ_i (d_i - μ_N)(d_{i+1} - μ_N) / Σ_i (d_i - μ_N)²

where μ_N = mean Farey gap = 1/|F_N|.

Empirically (N=10k-50k): ρ_N = 0.36 → 0.38 → 0.39, extrapolating to 1/2.

## Goal

Prove rigorously that lim_{N→∞} ρ_N = 1/2.

## Tools available

1. **BCZ joint density**: in scaled coords (x_i, x_{i+1}) = (k_i/N, k_{i+1}/N), the joint density of consecutive denominators is f(x, y) = 2 on the triangle {x + y > 1, x, y ∈ (0, 1]}.

2. **BCZ recurrence**: third denominator k_{i+2} = κ k_{i+1} - k_i with κ = ⌊(N + k_i)/k_{i+1}⌋, i.e. z = κy - x in scaled coords.

3. **Gap formula**: d_i = 1/(k_i k_{i+1}) = 1/(N² xy).

## Strategy

The covariance:

  Cov(d_i, d_{i+1}) = E[d_i d_{i+1}] - E[d_i] · E[d_{i+1}]

Variance: Var(d_i) = E[d_i²] - E[d_i]² (with E[d_i²] divergent in the limit but cut off at finite N).

By the joint density:

  E[d_i d_{i+1}] = ∫∫∫ (1/(N² xy)) (1/(N² yz)) · density · dx dy dz
                 = (2/N⁴) ∫∫_{x+y>1} 1/(xy² · (κy-x)) dx dy

where κ = ⌊(1+x)/y⌋ and the integrand is split over κ ∈ {2, 3, 4, ...} branches.

For each κ = n branch, x ∈ (max(1-y, (n-1)y), ny) (with the triangle constraint y > 1 - x).

  E[d_i²] = (2/N⁴) ∫_{x+y>1} 1/(x²y²) dx dy = (2/N⁴) ∫₀¹ 1/(x(1-x)) dx [Cut off at finite N]

Both E[d_i²] and E[d_i d_{i+1}] diverge logarithmically as N → ∞. The RATIO should give 1/2.

## Your task

1. Carry out the κ-branched integral for E[d_i d_{i+1}] explicitly.

2. Identify the leading logarithmic term: E[d_i d_{i+1}] ~ C_xy log(N) / N⁴.

3. Similarly E[d_i²] ~ C_xx log(N) / N⁴.

4. Show: C_xy / C_xx = 1/2 + O(?).

5. The correlation: ρ_N → (Cov / Var) = ((C_xy - 0) / C_xx + O(1/log N)) = 1/2.

The hard part is the κ-branched integral. Use:

  Σ_n ∫_{(n-1)y}^{ny} dx / (x(ny - x)) = Σ_n (1/(ny)) ∫_{(n-1)y}^{ny} (1/x + 1/(ny-x)) dx = Σ_n (1/(ny)) · 2 log(...)

(Partial fractions.) Push through.

## What I want

A rigorous derivation showing ρ_N → 1/2. If the proof is incomplete, identify the missing step.

If you find that ρ_N → some OTHER value, report honestly.
