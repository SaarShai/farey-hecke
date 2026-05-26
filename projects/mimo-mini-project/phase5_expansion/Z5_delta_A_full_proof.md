---
model: mimo-v2.5-pro
max_tokens: 16000
---

# Z5 — Complete the Δ(A) Abel summation proof

## Status

Empirical: Δ(A) = -2 Re[χ̄(A) log L(q^{-1/2}, χ)] verified across 5 (q, M) cases in F_q[T].

P6 outlined a derivation via Weil RH + explicit formula. AV2 found a gap: the character sum Σ_P χ(P) q^{-deg P/2} doesn't converge absolutely; needs Abel summation.

X8 made progress but didn't complete.

## Task: COMPLETE the proof

### Setup (function fields)

For F_q[T] with modulus M of degree m. Let χ be a primitive character mod M with character order m_ρ. The L-function:
  L(u, χ) = Π_{P prime in F_q[T]} (1 - χ(P) u^{deg P})^{-1}

By Weil RH (a theorem): L(u, χ) is a polynomial of degree d_χ = m - 1 with zeros on |u| = q^{-1/2}:
  L(u, χ) = Π_{j=1}^{d_χ} (1 - α_j u) where |α_j| = q^{1/2}

So log L(u, χ) = -Σ_j log(1 - α_j u) for |u| · q^{1/2} < 1, i.e., |u| < q^{-1/2}.

### The character sum

For ψ(N; χ) := Σ_{deg(P^k) = N} χ(P)^k · deg(P) (function-field analog of ψ(x)):

ψ(N; χ) = -Σ_j α_j^N (Weil explicit formula)

For N ≥ 1.

### The "bias" question

We want Δ(A) for class A ∈ (F_q[T]/M)^×, defined as the "bias toward A vs identity" in the prime count.

Counting primes in class A:
π(N; A, M) = (1/φ(M)) Σ_χ χ̄(A) · ψ̂(N; χ)

where ψ̂(N; χ) is the character-twisted count. For the trivial character: ψ̂(N; χ_0) ≈ q^N/N (prime number theorem).

The "bias" is the deviation from the identity (= χ_0) count. Carefully define:

Δ(A; N) = (1/φ(M)) Σ_{χ ≠ χ_0} (χ̄(A) − 1) · ψ(N; χ)
        = (1/φ(M)) Σ_{χ ≠ χ_0} (χ̄(A) − 1) · (-Σ_j α_j(χ)^N)

For finite N, Δ(A; N) is well-defined. But the "asymptotic Δ(A)" as a single number requires averaging or limiting.

### Abel summation framework

Define the Abel-summable Δ(A) via:
  Δ(A) := lim_{t → q^{-1/2−}} (1 - tq^{1/2}) Σ_{N=1}^∞ Δ(A; N) · (tq^{1/2})^N

(or some other regularization that gives a finite limit)

Then:
Σ_{N=1}^∞ ψ(N; χ) · (tq^{1/2})^N = -Σ_j Σ_N α_j^N (tq^{1/2})^N
                                = -Σ_j α_j tq^{1/2} / (1 - α_j tq^{1/2})

Setting t → q^{-1/2−} (so tq^{1/2} → 1−):
- For α_j = q^{1/2} e^{iθ_j} (on the critical circle):
  α_j tq^{1/2} → e^{iθ_j} on |·| = 1
  1 - α_j tq^{1/2} → 1 - e^{iθ_j}

The limit α_j (limit_t→1) / (1 - α_j (limit)) = α_j(1) / (1 - α_j(1)) = ... divergent at θ_j = 0 (no L-zero at u = q^{-1/2}, so safe).

For generic χ, the values 1 - e^{iθ_j} are bounded away from 0 (since L doesn't vanish at u = q^{-1/2} for non-trivial χ... need to verify).

### Compute the Abel limit

Σ_{N=1}^∞ ψ(N; χ) · t^N = -Σ_j α_j t / (1 - α_j t)

Note: log L(t, χ) = -Σ_j log(1 - α_j t), so d/dt log L = -Σ_j (-α_j)/(1 - α_j t) = Σ_j α_j/(1 - α_j t).

Therefore Σ_N ψ(N; χ) t^N = -t · d/dt log L(t, χ).

Specifically, this is the generating function for ψ.

### Putting it together

Δ(A) = lim_{t → q^{-1/2}} regularization × (1/φ(M)) Σ_{χ ≠ χ_0} (χ̄(A) - 1) × [-t · d/dt log L(t, χ)]

Now: log L(q^{-1/2}, χ) is well-defined (L(q^{-1/2}, χ) is a specific nonzero number by Weil RH).

The regularization should give:
Δ(A) = (1/φ(M)) Σ_{χ ≠ χ_0} (χ̄(A) - 1) · [-q^{-1/2} · (d/dt log L)(q^{-1/2}, χ)]

OR maybe it gives:
Δ(A) = (1/φ(M)) Σ_{χ ≠ χ_0} (χ̄(A) - 1) · log L(q^{-1/2}, χ) · (some factor)

Identify the EXACT formula. Show:
- The factor of -2
- Re[χ̄(A) · log L(...)]
- How the -1 cancels

The factor of 2 should come from conjugate pairs: if χ and χ̄ are both included, Σ over them gives twice the real part.

For REAL characters (χ = χ̄), the -2 Re becomes -2 χ(A) log|L|.

For COMPLEX characters (χ ≠ χ̄), pair χ with χ̄: sum gives 2 Re[χ̄(A) log L].

So the formula -2 Re[χ̄(A) log L(q^{-1/2}, χ)] is the contribution per (χ, χ̄)-pair (for complex χ) or just one χ (for real χ).

## What I want

Complete, rigorous proof of:

**Theorem**: Under Weil RH (a theorem for F_q[T] characters), the function-field Chebyshev bias Δ(A) (defined via Abel summation) equals
  Δ(A) = -2 Re[χ̄(A) · log L(q^{-1/2}, χ)]
for each non-trivial character χ, summed over (χ, χ̄)-pairs in the bias decomposition.

State all hypotheses clearly. Identify any remaining gaps.

This is Discovery #4 going from CONJECTURE to THEOREM.
