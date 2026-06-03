# Closed form / geometric formula for the Hecke ergodic-optimization infimum X(q) (2026-06-02)

**Resolves `/goal #2`.** Object: Hecke group `G_q`, `λ=λ_q=2cos(π/q)`, `θ=π/q`. BCZ-type return map
`T_q(x,y)=(y, ⌊(1+x)/(λy)⌋λy−x)` on `{x>0,y>0,x+λy>1}`, observable `P=xy`,
`X(q)=inf_μ ess-sup_μ P`. Optimizer = parabolic word `(1^{q−3},2)` (period `N=q−2`), q≥4; q=3 special `(1,4)`.

Verification: `code/Xq_closedform_verify.py`. Closed form matches the independent boundary-scan
`Xq_exact_for_word` (in `code/ergodic_hecke_hunt.py`) to **≤8e-56 over all q=4..80** (mpmath, dps=60).

---

## RESULT — three equivalent statements

### (A) Uniform GEOMETRIC / Chebyshev formula (single expression, q≥4)
```
X(q) = maxprod(q) / (4 sin²(2π/q)) ,     maxprod(q) = max_{1≤k≤q−2} sin(kπ/q)·sin((k+1)π/q)
```
Both pieces are explicit:
- `s_lo = 1/(2 sin(2π/q))` is the lower edge of the scale-free family (the **cusp** binds, ∀q≥4).
- `maxprod = sin(k*θ)·sin((k*+1)θ)` with `k* = ⌊(q−1)/2⌋` (the orbit pair straddling π/2), and
  `X(q) = s_lo² · maxprod`.

In Chebyshev `U`: the orbit is `v_n = U_n(λ/2) sinθ = sin((n+1)θ)`, n=0..q−3; `maxprod` is the
largest product of consecutive `U`-values. Uniform, but the `⌊⌋` (= parity of q) is irreducible —
see (C).

### (B) Two PROVEN sub-formulas, split by parity of q
```
q even :  X(q) = cos(π/q) / (4 sin²(2π/q))           = 1/( 8 sin(π/q) sin(2π/q) )
q odd  :  X(q) = cos²(π/2q) / (4 sin²(2π/q))         = (1+cos(π/q)) / ( 32 sin²(π/q) cos²(π/q) )
q = 3  :  X(3) = 2/9                                  (special word (1,4))
```

### (C) Honest verdict on a *single uniform elementary* formula: **NO** (now precisely characterized)
`maxprod = ½(cosθ − min_k cos((2k+1)θ))`. The inner min hits the odd multiple of `θ=π/q` nearest π:
- q odd ⟹ `(2k+1)=q` is reachable ⟹ `cos(π)=−1` ⟹ `maxprod = ½(1+cosθ) = cos²(θ/2)`;
- q even ⟹ nearest odd is `q∓1` ⟹ `cos(π±θ)=−cosθ` ⟹ `maxprod = cosθ`.
So `X(q)` is an explicit algebraic number whose *form switches with q mod 2* (a cyclotomic/parity
effect — which neighbour of π/2 the rotation orbit lands on). There is **no single smooth elementary
formula in λ_q**; the cleanest uniform form is (A) (one expression, with `max`/`⌊⌋`), and the cleanest
elementary form is the parity split (B). This *refines* DISCOVERY Finding 3 from "no uniform formula"
to "uniform geometric form (A) + exactly two elementary branches (B), split = parity".

---

## DERIVATION (this is a proof for the word (1^{q−3},2); word-optimality itself is separate — see Scope)

**1. Eigenvector in closed form.** Index the cyclic orbit `v_0..v_{N−1}`, N=q−2, defect center at 0.
The all-`1` recurrence `v_{m−1}+v_{m+1}=λ v_m` (= rotation by θ, since λ=2cosθ) holds at the q−3
non-defect centers, forcing `v_n = A cos nθ + B sin nθ`. Two closure equations remain:
- center N−1 (rotation, with wrap `v_N≡v_0`): `f(N−2)+f(0)=λ f(N−1) ⟺ f(N)=f(0)`;
- center 0 (defect): `f(N−1)+f(1)=2λ f(0)`.

`f(N)=f(0)` with `Nθ=π−2θ` gives `B/A=(1+cos2θ)/sin2θ=cotθ`, hence
```
v_n = sin((n+1)θ),  n=0..q−3        (= sinθ · U_n(cos θ) = sinθ · U_n(λ/2)).
```
The defect equation is then an identity: `v_{N−1}+v_1 = 2 sin2θ = 2λ sinθ = 2λ v_0` ✓.
Smallest orbit value is the cusp point `v_0=sinθ`; `v_1=v_{N−1}=sin2θ`. (Verified vs the monodromy
nullspace to 1e-60 for q=4..16.)

**2. The lower edge s_lo, and which constraint binds.** Floor-consistency + triangle give, for each n,
two lower bounds on s. Both simplify to the *same shape*:
- triangle_n:  `s > 1/(v_n + λ v_{n+1})`;
- floor-jump_n: `s > 1/(λ v_{n+1}(k_n+1−r_n)) = 1/(v_{n+2} + λ v_{n+1})`   (uses `k_n λ v_{n+1}=v_n+v_{n+2}`).

So `s_lo = 1/D`, `D = min_n min(v_n+λv_{n+1}, v_{n+2}+λv_{n+1})` = min over the orbit of `λv_m+(neighbour)`.
The minimum is at the **cusp**: at center 0, `v_{N−1}+λv_0 = v_1+λv_0 = 2 sin2θ`. The decisive identity
```
(2 sinθ + sin3θ) − 2 sin2θ = sinθ (2cosθ−1)²  ≥ 0     (= 0 only at q=3)
```
shows the cusp sum `2sin2θ` is ≤ its neighbours for all q≥4 (strict for q≥4); interior sums are larger
(larger v's). Hence
```
s_lo = 1/(2 sin 2θ) = 1/(2 sin(2π/q))   for all q≥4.
```
(Confirmed globally: `Xq_exact_for_word` takes the true max over ALL constraints and agrees to 56 digits.)

**3. The max product.** `max_n v_n v_{n+1} = max_k sin(kθ)sin((k+1)θ) = ½(cosθ − min_k cos((2k+1)θ))`,
evaluated in (C): `cosθ` (q even), `cos²(θ/2)` (q odd).

**4. Assemble.** `X(q) = s_lo² · maxprod`, giving (A)/(B). ∎ (for this word)

**Geometric meaning.** As `s→s_lo⁺` the cusp point `(s v_{N−1}, s v_0)` lands exactly on the edge
`x+λy=1` at the **universal limit point `(½, 1/(2λ_q))`** (indep. of q: `½ + λ·1/(2λ)=1`). `X(q)` is the
max gap-product over the rotation-by-π/q one-defect orbit pinned there — an **open** boundary ⇒ inf
not attained ⇒ the no-ground-state structure (matches the q=3,4 Lean proofs).

---

## Explicit small values, from the general formula
| q | formula (A)/(B) | value | matches |
|---|---|---|---|
| 3 | special word (1,4) | 2/9 = 0.2222222… | Lean-proven |
| 4 | 1/(8 sin45° sin90°) = 1/(4√2) | **√2/8** (global min) | Lean-proven |
| 5 | cos²18°/(4 sin²72°) = cos²18°/(4cos²18°) | **1/4** | exact |
| 6 | 1/(8 sin30° sin60°) = 1/(2√3) | **√3/6** | exact |
| 7 | (1+cos π/7)/(32 sin²cos²) | 0.3887395330… | exact |
| 8 | cos(π/8)/(4 sin²(π/4)) | ½cos(π/8) = 0.4619397… | exact |
| 10 | cos(π/10)/(4 sin²(π/5)) | ½cot(π/5) = 0.6881909… | exact |
| 12 | cos(π/12)/(4 sin²(π/6)) | cos(π/12) = 0.9659258… | exact |
| 200 | even branch | 253.0… (→∞) | exact |

`X(q)` strictly increasing for q≥4, `→∞` as q→∞; global min `X(4)=√2/8`. The earlier guessed pattern
`½cot(2π/q)` (fits q=6,10) is a **coincidence** of `4 sinθ cos2θ=1` at those q — the true even branch
is `1/(8 sinθ sin2θ)`.

## Scope (adversarial honesty)
- **PROVEN here (analytic + 56-digit cross-check):** for the parabolic word `(1^{q−3},2)`, the closed
  forms (A)/(B), the eigenvector `sin((n+1)θ)`, `s_lo=1/(2sin2θ)` with the cusp binding, and the
  derivation of X(3),X(4),X(5),X(6).
- **NOT re-litigated here (prior status, unchanged):** that `(1^{q−3},2)` is the *optimal* parabolic
  word (search-verified q=4..10, conjectured ∀q≥4) and that the tabulated X(q) is the *exact* infimum
  (matching lower bound formalized in Lean only for q=3,4). The closed form is conditional on that
  optimality, exactly as the table is.
- **No outbound. Nothing sent.**
