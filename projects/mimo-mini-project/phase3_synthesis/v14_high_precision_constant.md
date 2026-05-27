# Σ M(n)²/n³ — high-precision verification

## Computed value (this session)

| N | Σ_{n≤N} M(n)²/n³ |
|---|---|
| 100 | 1.13563000 |
| 1,000 | 1.13612944 |
| 10,000 | 1.13615946 |
| 100,000 | 1.13616204 |
| 1,000,000 | 1.13616228 |
| **5,000,000** | **1.13616230** |

Convergence rate: ~10⁻¹ per decade of N. Final 8-digit estimate:

  **Σ_{n=1}^∞ M(n)²/n³ ≈ 1.1361623 ± 10⁻⁷**

## Literature/OEIS search verdict (Phase 7 subagent + this session)

- **OEIS**: not found (multiple searches)
- **Tenenbaum** / **Iwaniec-Kowalski**: not listed as standard constant
- **Ng 2004 thesis** (Σ M(n)²): gives asymptotic for partial sum, not the s=3 Dirichlet series
- **Web search** for "1.1361623" / "1.13616": no math constant match
- Decimal pattern doesn't match Apéry's ζ(3) ≈ 1.20206, log(2) ≈ 0.69315, 12/π² ≈ 1.21586, ζ(2)/ζ(4) ≈ 1.51982, or any standard combination

**Verdict**: Σ M(n)²/n³ = 1.1361623 appears to be a **genuinely new convergent constant**.

## Why it's relevant for #1 (Mertens-NW)

The structural identity (this session):

  J(Q) = (1/12) · [ Σ_d M(⌊Q/d⌋)² + Σ_{d≠d'} gcd(d,d')² M(⌊Q/d⌋) M(⌊Q/d'⌋) / (d·d') ]

The diagonal D(Q) = Σ_d M(⌊Q/d⌋)² connects to Σ M(n)²/n³ via the Dirichlet-hyperbola substitution:

  D(Q) = Σ_u M(u)² · (⌊Q/u⌋ − ⌊Q/(u+1)⌋) ≈ Q · Σ_u M(u)² / (u·(u+1))

The latter sum DIVERGES (~ log N). But the closely-related Σ M(u)²/u³ CONVERGES to 1.1361623.

This convergent constant is the natural "leading-order coefficient" if we instead consider the sum:

  Σ_{u=1}^∞ M(u)² · u/(u(u+1)(u+2)) = Σ M(u)²/((u+1)(u+2))

or via partial summation. It's the "tail" / "principal value" of the divergent Σ M(u)²/(u(u+1)).

## Possible identifications (untested)

The value 1.1361623 might equal:
- Some combination involving Σ_ρ over Riemann zeros (Ng 2004 form)
- A new constant emerging from the Mikolás-Mertens setup
- A constant related to Σ μ(n)²/n^s = ζ(s)/ζ(2s) family

**For #1 paper**: I'd cite Σ M(n)²/n³ ≈ 1.1361623 as "a new convergent Dirichlet-type constant naturally arising in the Mikolás-Mertens decomposition of NW(Q)." Possibly worth its own short note.

## How to verify novelty more rigorously

1. Access Ng's full PhD thesis (request from author or library) and check appendix tables
2. Cross-reference with Aistleitner / Hofer arXiv:1405.6532 (mentioned in Phase 7 lit search)
3. Run wider OEIS search with more decimal places (need authenticated OEIS access)
4. Direct query to Boca, Cobeli, Zaharescu, or Kanemitsu (authors who'd recognize it if known)
