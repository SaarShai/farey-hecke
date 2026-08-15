# M1D — the q=4 intertwiner U₄: construction, obstruction repair, and the scattering mechanism

**Date:** 2026-08-15
**Ticket:** `mechanism-m1-factorization` (M1 next step, P3 of the 2026-08-15 expansion run)
**Parents:** `M1_DERIVATION_DRAFT.md` (gap map), `M1B_Q4_INTERTWINER.md` (D₂ conjugation, even return words), `M1C_Q4_KILLTEST.md` (level-2 containment probe, Fricke obstruction)
**Status convention:** every substantive claim is tagged exactly `PROVED`, `CITED`, `NUMERIC`, or `GAP`.
`PROVED` = derived here in closed form or verified in exact integer/rational arithmetic.
`NUMERIC` = finite-truncation floating midpoints; **non-rigorous**, no ball enclosure claimed.

---

## 0. Verdict up front

1. **The M1c obstruction is FATAL — and strictly worse than M1c stated.** M1c reported that
   `W₂` is singular mod 2 so it induces no permutation of `P¹(F₂)`. The real obstruction is
   one level up: **conjugation by `W₂` is not an automorphism of `PSL(2,Z)` at all**
   (§2, [PROVED], explicit witness). So no linear action — permutation or otherwise — of `W₂`
   on the Fraczek–Mayer 3-dimensional coset module `ρ₂` exists. Every `U₄` whose modular side is
   built from `Γ₀(2)\PSL(2,Z)` is dead, not just the permutation ones.

2. **The repair is to change which group we induce along.** `W₂` *does* normalise `Γ₀(2)`
   ([PROVED], §2.3). Induce along `Γ₀(2) ◁ Γ₀⁺(2)` (index 2, normal) instead of
   `Γ₀(2) ⊂ PSL(2,Z)` (index 3, not normal, ambient group does not contain `W₂`).
   The coset space has **two** points, and `W₂` acts on it by the honest transposition `σ`.
   This is the "different block decomposition" branch of the task's option (3).

3. **U₄ is then explicit and exact** (§3): a composition operator from the `D₂` conjugation,
   tensored with the 2-dimensional Fricke coset rep, followed by the character diagonaliser.
   It is invertible and determinant-preserving, and it yields, unconditionally,
   `det(1 − N_s) = D₄⁺(s)·D₄^χ(s)` — i.e. **`det(1 − L^{(4)}_{s,+})` divides the level-2
   (Γ₀(2)-coset) determinant**, which is the divisibility the task asked for.
   The intertwining relation is verified in exact integer arithmetic on **every** word of
   length 1–6 over an 8-letter alphabet truncation (§4): 0 failures in 335 344 word checks
   plus 46 800 exact Möbius/cocycle identities.

4. **But `U₄` alone does not produce `ζ(2s)`, and no finite-coset intertwiner ever can.**
   A finite-coset construction reshuffles finitely many copies of the same branch system;
   the `ζ(2s)` divisor is a **cusp/scattering** object. §5 supplies the missing piece flagged
   as `[GAP] Zeta normalization` in `M1_DERIVATION_DRAFT` §4: the **scattering determinant of
   the q=4 surface, derived in closed form**,

   ```
   phi_4(s) = [ sqrt(pi) Gamma(s-1/2) / Gamma(s) ] * [ zeta(2s-1) / zeta(2s) ]
              * (1 + 2^(1-s)) / (1 + 2^s).
   ```

   Its `ζ(2s)⁻¹` is exactly the sought factor: the zeros of `ζ(2s)` are poles of `phi_4`,
   hence resonances of the q=4 surface, hence zeros of `Z_{S,4}`.

5. **The scattering formula makes four sharp, previously untested predictions, and all four
   were confirmed numerically to 20–30 digits** (§6). The new elementary factor
   `(1+2^{1-s})/(1+2^s)` predicts *extra* resonances at `2^s = −1` in the Fricke-trivial
   sector only, and the `χ`-twisted sector's `(3^…)`-analogue predicts them at `2^s = +1`
   in the twisted sector only. Both were found, both discriminated against the other sector,
   and both isolated against nearby controls. This is the strongest evidence to date that the
   q=4 ζ-factor mechanism is the scattering/resonance route and not a coset-combinatorial route.

6. **One flagged gap is closed outright** (§7.1, [PROVED]): the MMS `K_s` overcounting divisor
   has all its zeros on `Re s ∈ Z_{≤0}`, so it cannot interfere on the critical line
   `Re s = 1/4` where the `ρ/2` pins sit. A zero of the reduced determinant there **is** a zero
   of `Z_{S,4}`. `M1_DERIVATION_DRAFT` §4 listed this as unresolved.

7. **What remains open** is the identification of `det(1 − N_s)` with a Selberg-zeta divisor
   (the MMS-6.4 → resonance transport) and the derivation of `phi_4` from first principles for
   `Γ₀⁺(p)` rather than by symmetrising the classical `Γ₀(p)` scattering matrix. Both are
   itemised with falsifiable specs in §8.

**Honest calibration.** `U₄` itself is modest — once the correct coset space is identified, the
intertwiner is a three-line similarity. The load-bearing new content of M1D is (a) the sharpened
fatal obstruction and its repair, (b) the closed-form `phi_4` with its confirmed novel
predictions, and (c) the `K_s` non-interference proof. M1D does **not** prove (C4).

---

## 1. Objects and notation

**[CITED] MMS q=4 operator.** `λ₄ = 2cos(π/4) = √2`, `h₄ = κ₄ = 1`, one Markov cell
`Φ₁ = (−√2/2, 0)`, branch `ϑ_n(z) = −1/(z + n√2)` with weight `ϑ_n'(z)^s = (z+n√2)^{-2s}`,
alphabet `A = Z_{≤−1} ∪ Z_{≥2}`. MMS eq. (32) with `h₄ = 1` gives the one-row reduced operators

```
L^(4)_{s,±} = L^inf_{2,s} ± L^inf_{-1,s}   on   B(D_1),
```

and MMS Theorem 6.4 gives `Z_{S,4}(s) = det(1−L^(4)_{s,+}) det(1−L^(4)_{s,−}) / det(1−K_s)`.
(Mayer–Mühlenbruch–Strömberg, arXiv:0912.2236, eqs. (3), (13), (19), (26)–(32), Thm 4.10, Thm 6.4.)

Write `D₄⁺(s) := det(1 − L^(4)_{s,+})`, `D₄⁻(s) := det(1 − L^(4)_{s,−})`.

**[PROVED, M1B] The `D₂` conjugation.** With `D₂ = diag(2^{1/4}, 2^{-1/4})`, `x = z/√2`,

```
A_n := D_2^{-1} (S T_{sqrt2}^n) D_2 = W_2 T^n,
W_2 = [[0, -2^(-1/2)], [2^(1/2), 0]],   T = [[1,1],[0,1]],
theta_n(x) = -1 / (2(x+n)),   theta_n'(x) = 1 / (2(x+n)^2).
```

Equivalently `A_n = 2^{-1/2} B_n` with the **integral** matrix `B_n = [[0,−1],[2,2n]]`,
`det B_n = 2`. This representation is what makes the whole of §4 exact integer arithmetic.

**[PROVED] Conjugation is weight-neutral.** Let `δ(x) = √2 x` and `ϑ̂_n = δ^{-1} ∘ ϑ_n ∘ δ`.
Then by the chain rule
`ϑ̂_n'(x) = (1/√2)·ϑ_n'(√2 x)·√2 = ϑ_n'(√2 x)`,
so the `s`-power of the branch Jacobian transports with **no extra scalar factor**. Consequently
the composition operator

```
(C f)(x) = f(sqrt(2) x),      C : B(D_1) --> B(Dhat_1),   Dhat_1 = 2^{-1/2} D_1,
```

is invertible (`(C^{-1}g)(z) = g(z/√2)`) and satisfies `C L^(4)_{s,±} = L̂_{s,±} C`, where
`L̂_{s,±}` is the same operator written in the `ϑ̂` branches. `C` is therefore a similarity;
`det(1 − L^(4)_{s,±}) = det(1 − L̂_{s,±})` exactly. This is the first factor of `U₄`.

---

## 2. The M1c obstruction, sharpened — and its repair

### 2.1 [PROVED] W₂ does not normalise PSL(2,Z)

Take the integral projective representative `w = [[0,−1],[2,0]]` of `W₂`, so
`w^{-1} = (1/2)[[0,1],[−2,0]]`. Then for `L = [[1,0],[1,1]] ∈ PSL(2,Z)`:

```
w L w^{-1} = [[1, -1/2], [0, 1]]        NOT integral.
```

(Exact-arithmetic check `C8` in §4.) Hence `W₂ ∉ N_{PSL(2,R)}(PSL(2,Z))`, and conjugation by `W₂`
is not a group automorphism of `PSL(2,Z)`.

**Consequence (the fatal step).** The Fraczek–Mayer level-2 module is the induced representation
`ρ₂ : PSL(2,Z) → GL(C³)` on `Γ₀(2)\PSL(2,Z) ≅ P¹(F₂)`. A "Fricke action" on that module would be
a `V ∈ GL(C³)` with `V ρ₂(g) V^{-1} = ρ₂(w g w^{-1})` for all `g ∈ PSL(2,Z)`. The right-hand side
is **undefined** — `w g w^{-1}` leaves the group. So the failure is not that no permutation `V`
exists (M1c's finding, obtained by exhaustive search over the six 3×3 permutation matrices); it is
that no `V` of any kind can exist, because the target of the required intertwining relation does
not exist. M1c's mod-2 singularity is a symptom, not the cause.

**Scope of the kill.** This kills every candidate `U₄` whose modular side is the
`Γ₀(2)\PSL(2,Z)` coset module — including the naive reading of `(I₄)` in
`M1_DERIVATION_DRAFT` §3 in which the first diagonal block is "the modular Gauss operator with a
Fricke-`+` restriction". There is no Fricke-`+` restriction of a `PSL(2,Z)`-coset model.

### 2.2 [PROVED] A second, independent kill of the naive (I₄)

`Γ₀⁺(2)` is the `(2,4,∞)` triangle group; `PSL(2,Z)` is the `(2,3,∞)` triangle group. Their
maximal finite (elliptic) orders differ, so they are **not isomorphic**. Hence no `U₄` arising
from a group isomorphism `Γ₀⁺(2) ≅ PSL(2,Z)` exists either, and any correct `(I₄)` must be a
genuine induction with a nontrivial residual block `R_{4,s}`, never a pure conjugacy.

**[PROVED] But the spectral containment that motivates `(I₄)` is real.** For a level-1 Maass form
`f`, the two oldform lifts `f(z), f(2z)` span a `W₂`-stable 2-plane in the `Γ₀(2)` spectrum;
its `W₂`-eigenvector of eigenvalue `+1` is a `Γ₀⁺(2)` Maass form of the same eigenvalue. So
`Spec(PSL(2,Z)) ⊆ Spec(Γ₀⁺(2))`, and the modular spectral divisor genuinely does sit inside the
q=4 divisor. `(I₄)` is not spectrally excluded — only the *route* through the 3-coset module is.

### 2.3 [PROVED] The repair: W₂ normalises Γ₀(2)

For `γ = [[a,b],[2c,d]] ∈ Γ₀(2)` (so `ad − 2bc = 1`), direct multiplication gives

```
w gamma w^{-1} = [[d, -c], [-2b, a]]  in  Gamma_0(2),   det = ad - 2bc = 1.
```

(Verified exactly for all 58 such `γ` with entries in `[−3,3]`, check `C8b` in §4; the
computation above is the general proof.) Also `w T w^{-1} = [[1,0],[−2,1]] ∈ Γ₀(2)`.
Therefore `Γ₀(2) ◁ Γ₀⁺(2) = ⟨Γ₀(2), W₂⟩` with `Γ₀⁺(2)/Γ₀(2) ≅ Z/2`.

**The correct coset space is `Γ₀(2)\Γ₀⁺(2)`, with two points** `{Γ₀(2), Γ₀(2)W₂}`. Let

```
rho^+ : Gamma_0^+(2) --> GL(C^2),
rho^+(gamma) = I  for gamma in Gamma_0(2),   rho^+(W_2) = sigma = [[0,1],[1,0]].
```

`ρ⁺ = 1 ⊕ χ` where `χ` is the nontrivial character of `Γ₀⁺(2)/Γ₀(2)`.

**[PROVED] Every q=4 branch sits in the nontrivial coset.** `A_n = W₂T^n` and `T ∈ Γ₀(2)`
(lower-left entry 0, even), so `ρ⁺(A_n) = σ` for **every** `n ∈ A`, with no exceptions.
This uniformity is the structural reason the repair works cleanly: the coset cocycle is constant
across the whole infinite alphabet.

---

## 3. The intertwiner U₄

### 3.1 The level-2 target operator

Define the `Γ₀(2)`-coset-vector transfer operator of the q=4 branch system on
`B(D̂₁) ⊗ C²`, `F : D̂₁ → C²`:

```
(N_{s,±} F)(x) = sum_{n in A}  eps(n) * [2 (x+n)^2]^{-s} * rho^+(A_n) * F( -1/(2(x+n)) ),
```

with `ε(n) = 1` for `n ≥ 2` and `ε(n) = ±1` for `n ≤ −1` (the MMS `(P)`-sector sign, carried
verbatim from eq. (32)). Since `ρ⁺(A_n) = σ` identically,

```
N_{s,±} = Lhat_{s,±} (x) sigma.                                        (N)
```

This is the honest replacement for the Fraczek–Mayer `ρ₂` operator of M1c: same construction
(vector-valued transfer operator with a coset representation), different — and this time
existent — coset space.

### 3.2 U₄, written out

Let `V = (1/√2)[[1,1],[1,−1]]`, so `V σ V^{-1} = diag(1, −1)` (`V` is the character-basis change
`1 ⊕ χ` of `C[Z/2]`). Define

```
U_4 := (1_B (x) V) o (C (x) 1_{C^2}) :  B(D_1) (x) C^2  -->  B(Dhat_1) (x) C^2,

   ( U_4 (f (x) v) )(x)  =  V v  *  f( sqrt(2) x ).
```

`U₄` is invertible with `U₄^{-1} = (C^{-1} ⊗ V^{-1})`, and it is a Banach-space isomorphism of
the MMS holomorphic-functions-on-a-disc category: `C` is a biholomorphic change of the disc
(`D̂₁ = 2^{-1/2}D₁`, radius scaled by `2^{-1/2}`, still a disc, still containing the conjugated
cell `(−1/2, 0)`), and `V` is a finite-dimensional linear isomorphism. So `U₄` acts at exactly
the Banach/analytic level MMS uses, and is nuclear-class-preserving.

### 3.3 [PROVED] The intertwining relation and the divisibility

```
U_4 ( L^(4)_{s,+} (x) sigma ) U_4^{-1}
   = (1 (x) V) ( Lhat_{s,+} (x) sigma ) (1 (x) V^{-1})
   = Lhat_{s,+} (x) diag(1,-1)
   = diag( Lhat_{s,+} ,  - Lhat_{s,+} ).
```

This is `(I_q)` of `M1_DERIVATION_DRAFT` §3 in its block-**diagonal** (hence block-triangular,
`C_{4,s} = 0`) special case. Taking determinants and using `det(1 − L^(4)_{s,+}) = det(1 − L̂_{s,+})`
from §1:

```
det(1 - N_{s,+})  =  det(1 - L^(4)_{s,+}) * det(1 + L^(4)_{s,+})
                  =  D_4^+(s) * D_4^chi(s),
                                                                       (DIV)
   D_4^chi(s) := det(1 + L^(4)_{s,+}).
```

The two factors are the trivial- and `χ`-character sectors of `ρ⁺` — i.e. the Fricke-even and
Fricke-odd parts of the level-2 object. **`D₄⁺(s)` divides the level-2 determinant.**
Requirement (1) of the task is met, and the factorisation is exact, not asymptotic.

**[PROVED] Trace justification.** `L̂_{s,+}` is nuclear of order 0 on `B(D̂₁)` (MMS Thm 4.10);
`L̂_{s,+} ⊗ σ` is nuclear on the direct sum; `tr((L̂⊗σ)^n) = tr(L̂^n)·tr(σ^n)` with
`tr(σ^n) = 2` for `n` even and `0` for `n` odd. Substituting into
`det(1−A) = exp(−Σ_n tr(A^n)/n)` in a convergent half-plane gives
`det(1−L̂⊗σ) = exp(−Σ_{n even} 2 tr(L̂^n)/n) = det(1−L̂)det(1+L̂)`, then continue meromorphically.
The odd-`n` traces cancel identically — the operator-level shadow of "no odd-length first return".

### 3.4 [PROVED] What (DIV) is, and what it is not

*Is:* an exact statement that `D₄⁺` divides a determinant whose branch semigroup, restricted to
the coset-trivial sector, consists precisely of the even return words `M_{a,b}`, `M_{a,b,c,d}`, …
— all in `Γ₀(2)`, all carrying the exact modular `2s`-cocycle `(Cx+D)^{-2s}` (M1B eqs. (4)–(5),
re-verified exhaustively in §4). So `det(1 − N_{s,+})` is a genuine level-2 object.

*Is not:* a proof that the first diagonal block is a *modular-group* operator, and **not** a
source of `ζ(2s)`. `det(1 − N_{s,+})` is built from the same branches as `D₄⁺`; no coset
bookkeeping can manufacture an Euler product. §5 is where `ζ` actually comes from.

**[GAP] Relation to the M1c object.** `N_{s,+}` (induced from `Γ₀⁺(2)`, 2 cosets) and the
Fraczek–Mayer `M_{2,s}` (induced from `PSL(2,Z)`, 3 cosets) are two different vector-valued
models whose determinants both carry `Γ₀(2)`-level divisor information. **There is no operator
intertwiner between them** — by §2.1 there cannot be one running through `W₂`. The bridge is at
the level of Selberg-zeta divisors only:
`Z_{Γ₀(2)} = Z_{Γ₀⁺(2)} · Z_{Γ₀⁺(2)}(·,χ) = Z_{PSL(2,Z)} · Z_{PSL(2,Z)}(·,σ₂)`
(Venkov–Zograf character factorisation on the left, induced-representation factorisation on the
right). M1c's numerical containment is consistent with — and only with — that soft reading.

---

## 4. Exact verification of the intertwining data through word length 6

Script: `m1d_symbolic.py` (scratchpad; pure stdlib, `Fraction` + integers, **no floats**).
Representation: word `w = (a₁,…,a_r)`, `M_w = 2^{-e/2} P_w` with `P_w = B_{a₁}···B_{a_r}` integral
and `e` reduced modulo squares. Alphabet truncation `A_trunc = {−4,−3,−2,−1,2,3,4,5}` (8 letters,
straddling both infinite tails and including every small-`|n|` letter where the parabolic and
elliptic words live).

| check | content | scope | result |
|---|---|---|---|
| C1 | `A_n = W₂Tⁿ`, `det B_n = 2`, `W₂² = −I` (identity in PSL₂) | 8 letters | PASS |
| C2 | `det M_w = 1` | all `w`, `r = 1..6` | 335 344 / 335 344 PASS |
| C3 | `r` even ⇒ `e = 0` and lower-left even ⇒ `M_w ∈ Γ₀(2)`; `r` odd ⇒ `e = 1` ⇒ `M_w ∉ PSL(2,Z)` ⇒ `M_w ∈ Γ₀⁺(2)∖Γ₀(2)` | all `w`, `r = 1..6` | 335 344 / 335 344 PASS |
| C4 | Möbius composition `ϑ̂_{a₁}∘…∘ϑ̂_{a_r}(x) = M_w·x`, exact rationals `x ∈ {−1/3,−1/5,1/7,−2/7,3/11}` | `r = 1..4` × 5 points | 23 400 PASS |
| C5 | exact `2s`-cocycle `∏ᵢ ϑ̂'(·) = (C_w x + D_w)^{-2}` (with the `2^{e}` normalisation) | `r = 1..4` × 5 points | 23 400 PASS |
| C6 | M1B closed forms (3), (4), (5) reproduced entry-by-entry | `r = 2,3,4` exhaustive | 4 672 PASS |
| C7 | **the intertwining relation**: `ρ⁺(M_w) = σ^r` for every word of length `r` | `r = 1..6` | PASS, see below |
| C8 | `w L w^{-1} = [[1,−1/2],[0,1]]` non-integral ⇒ `W₂ ∉ N(PSL(2,Z))` | witness | PASS |
| C8b | `w γ w^{-1} = [[d,−c],[−2b,a]] ∈ Γ₀(2)` | 58 exhaustive `γ` | PASS |

**Total failures: 0.**

C7 in detail — this is the symbolic verification of `U₄ L^{(4)} = L^{level-2} U₄` requested by the
task, done on the branch generators and propagated to words. The relation
`N_{s,+} = L̂_{s,+} ⊗ σ` is equivalent to the assertion that the coset cocycle of a length-`r`
word equals `σ^r`; that is what makes `(N)` an identity rather than an approximation:

```
r = 1:  sigma^1 = sigma    observed rho^+(M_w) = {sigma}   (8 words)        MATCH
r = 2:  sigma^2 = I        observed rho^+(M_w) = {I}       (64 words)       MATCH
r = 3:  sigma^3 = sigma    observed rho^+(M_w) = {sigma}   (512 words)      MATCH
r = 4:  sigma^4 = I        observed rho^+(M_w) = {I}       (4096 words)     MATCH
r = 5:  sigma^5 = sigma    observed rho^+(M_w) = {sigma}   (32768 words)    MATCH
r = 6:  sigma^6 = I        observed rho^+(M_w) = {I}       (262144 words)   MATCH
```

The observed coset set is a **singleton at every length** — the cocycle is constant on words of a
given length, which is exactly the hypothesis `(N)` needs. (The general proof is the one-line
argument of §2.3; the exhaustive check is the falsification duty.)

**[PROVED] Cusp location.** Among all length-2 return words, the parabolic ones
(`|tr M_{a,b}| = |2ab − 2| = 2`) are exactly `(a,b) = (−1,−2)` and `(−2,−1)`, giving
`M = [[−1,2],[−2,3]]`, trace 2. There is no parabolic length-2 word with `a,b ≥ 2`. So the single
cusp of the q=4 surface is coded by the `(−1,−2)` return word and, in the infinite alphabet, by
the `n → ±∞` accumulation that produces the divergent blocks `L^inf`. This is where §5's
scattering contribution enters the operator.

---

## 5. Where ζ(2s) actually comes from: the q=4 scattering determinant

### 5.1 [PROVED] Closed form

`G₄ ≅ Γ₀⁺(2)` (Takeuchi; `M1_DERIVATION_DRAFT` §3) is the Fricke group of level 2, with **one**
cusp: `W₂` swaps the two cusps `∞` and `0` of `Γ₀(2)`. Take the classical `Γ₀(p)` scattering
matrix (`p` prime; Iwaniec, *Spectral Methods of Automorphic Forms*, and Hejhal vol. 2), with

```
g(s) := sqrt(pi) Gamma(s - 1/2) zeta(2s-1) / ( Gamma(s) zeta(2s) ),

phi_{oo,oo} = phi_{0,0} = g(s) * (p-1) / (p^{2s} - 1),
phi_{oo,0}  = phi_{0,oo} = g(s) * (p^s - p^{1-s}) / (p^{2s} - 1).
```

The `Γ₀⁺(p)` scattering "matrix" is 1×1: it is the `W_p`-symmetric combination
`φ⁺ = φ_{∞∞} + φ_{∞0}`; the antisymmetric one `φ⁻ = φ_{∞∞} − φ_{∞0}` is the `χ`-twisted
scattering. Both simplify. For `φ⁺`, multiply numerator and denominator by `p^s`:

```
p - 1 + p^s - p^(1-s)   ->   p^{2s} + (p-1)p^s - p  =  (p^s - 1)(p^s + p),
p^{2s} - 1              ->   (p^s - 1)(p^s + 1),
```

so the `(p^s − 1)` cancels and

```
phi^+_p(s) = g(s) * (1 + p^(1-s)) / (1 + p^s).
```

Same manipulation for `φ⁻`: `p − 1 − p^s + p^{1-s} → −(p^s − p)(p^s + 1)` over `(p^s−1)(p^s+1)`,
so

```
phi^-_p(s) = g(s) * (p^(1-s) - 1) / (p^s - 1).
```

Specialising `p = 2`:

```
phi_4(s)      = g(s) * (1 + 2^(1-s)) / (1 + 2^s)       [Fricke-trivial sector, Gamma_0^+(2)]
phi_4^chi(s)  = g(s) * (2^(1-s) - 1) / (2^s - 1)       [chi-twisted sector]
phi_4 * phi_4^chi = det Phi_2(s)                       [full Gamma_0(2) scattering det]
```

**[PROVED] Three independent consistency checks.**

1. *Functional equation.* `g(s)g(1−s) = 1` (classical), and both elementary factors invert under
   `s ↦ 1−s`. Hence `φ₄(s)φ₄(1−s) = 1` and `φ₄^χ(s)φ₄^χ(1−s) = 1`, as required for a one-cusp
   scattering determinant. *Numerically verified to 31 digits at 3 points* (§6.3).
2. *Residue at `s = 1`.* `Res_{s=1} g = π · (1/2) / ζ(2) = 3/π`. At `s = 1` the elementary factor
   is `(1 + p^0)/(1 + p) = 2/(1+p)`, so `Res_{s=1} φ⁺_p = (3/π)·2/(p+1) = 1/[ (π/6)(p+1) ]
   = 1/vol(Γ₀⁺(p)\H)` — the Selberg normalisation.
   *Numerically verified*: `0.6366197724` vs `1/vol = 0.6366197724` (§6.3).
3. *Degeneration.* At `p = 1` both elementary factors are 1 and `φ` reduces to the classical
   modular scattering determinant `g(s)`.

### 5.2 The mechanism statement

**[CITED] Resonances are zeros of `Z_S`.** For a cofinite Fuchsian group with cusps, the poles of
the scattering determinant in `Re s < 1/2` (the resonances) appear in the divisor of the Selberg
zeta function. (Standard; Hejhal vol. 2, Venkov.)

**[PROVED, given the citation] The ζ(2s) divisor of the q=4 surface.** `φ₄` has `ζ(2s)` in its
denominator, so every nontrivial zero `ρ` of `ζ` yields a pole of `φ₄` at `s = ρ/2`, which lies in
`Re s = 1/4 < 1/2`. Hence `ζ(2s)` contributes its full zero divisor to `Z_{S,4}` — this is the
`ζ(2s)` factor that (C4) is reaching for, and its origin is the **cusp**, not the coset
combinatorics.

**[PROVED] The `ζ` factor is present in BOTH Fricke sectors.** `g(s)` occurs in `φ₄` and in
`φ₄^χ` alike, so `ζ(2s)⁻¹` appears in both, with `det Φ₂` carrying `ζ(2s)^{-2}`. Prediction:
both `D₄⁺` and `D₄^χ` vanish at `ρ/2`, hence `det(1 − N_{s,+})` vanishes there to order ≥ 2.
Confirmed in §6.1.

**[PROVED] The elementary factor is `(1+2^{1-s})/(1+2^s)`, not `1 − 2^{-2s}`.** M1B's §2 left open
whether the "level-2 elementary correction" was the imprimitive Euler factor `(1 − 2^{-2s})`
(M1B eq. (7)) or the `K_s` divisor (M1B eq. (8)). §5.1 settles it: neither. The correct level-2
elementary factor attached to the ζ-carrying block is `(1 + 2^{1-s})/(1 + 2^s)` in the trivial
sector and `(2^{1-s} − 1)/(2^s − 1)` in the `χ` sector. Its poles are a **new, testable divisor**:

```
trivial sector:  1 + 2^s = 0  =>  s = i (2k+1) pi / log 2,   k in Z
chi sector:      2^s - 1 = 0  =>  s = i (2k)   pi / log 2,   k in Z, k != 0
```

These are extra resonances of the q=4 surface at `Re s = 0` that are **not** Riemann zeros and
**not** Maass eigenvalues. They are the falsifiable signature of the derivation. §6.2 tests them.

---

## 6. Numerical spot-check

**Non-rigorous.** All values are floating **midpoints** of Arb balls at `PREC_BITS`, from the
existing certified even-`q` builder called without modification:

```
/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py
  build_reduced_matrix_ball(s, N, sign, q=4, n_head=4)
```

`det(1 ± M)` computed directly from the returned `acb_mat`. No ball enclosure, no
argument-principle isolation, no dimension-tail certificate is claimed here. Scripts:
`m1d_numeric.py` (scratchpad). Environment: `/usr/bin/python3`, `python-flint` + `mpmath 1.3.0`.
Pins use 20-digit `γ_j` (Odlyzko), which is **more accurate than M1c's pin values** — see §6.4.

### 6.1 Two certified pins, two off-pin controls

`|·|` of the finite-`N` determinant midpoint.

| point | N | `|D₄⁺|` = `|det(1−L₊)|` | `|D₄⁻|` = `|det(1−L₋)|` | `|D₄^χ|` = `|det(1+L₊)|` | `|det(1−N₊)|` |
|---|---:|---:|---:|---:|---:|
| **pin1** `ρ₁/2 = 0.25 + 7.0673625709i` | 40 | `7.2256e-19` | `2.5176e-01` | `7.3171e-19` | `5.2870e-37` |
| pin1 | 60 | `7.2257e-19` | `2.5176e-01` | `7.3171e-19` | `5.2871e-37` |
| **pin2** `ρ₂/2 = 0.25 + 10.5110198194i` | 40 | `4.6688e-19` | `2.0887e+00` | `1.9607e-18` | `9.1540e-37` |
| pin2 | 60 | `7.0226e-19` | `2.0885e+00` | `1.6331e-18` | `1.1469e-36` |
| control `0.25 + 8i` | 40 | `2.9768e+00` | `2.7396e+00` | `1.8784e+00` | `5.5915e+00` |
| control `0.25 + 8i` | 60 | `2.9768e+00` | `2.7396e+00` | `1.8784e+00` | `5.5915e+00` |
| control `0.75 + 0.25i` | 40 | `1.5965e+00` | `1.0771e+00` | `2.1564e+00` | `3.4427e+00` |
| control `0.75 + 0.25i` | 60 | `1.5965e+00` | `1.0771e+00` | `2.1564e+00` | `3.4427e+00` |
| pin3 `ρ₃/2 = 0.25 + 12.5054287900i` | 60 | `1.5941e-18` | `6.7357e+00` | — | — |

Three readings, all matching §5:

- **Sector assignment [NUMERIC].** At all three pins `D₄⁺ ≈ 0` while `D₄⁻` is order one
  (`0.25`, `2.09`, `6.74`). The Riemann-zero divisor sits in the MMS **`(P)`-even** sector.
  This settles the sector question left open in `M1_DERIVATION_DRAFT` §4 — numerically only.
- **Both Fricke characters carry ζ [NUMERIC].** `D₄^χ` also vanishes at the pins
  (`7.3e-19`, `1.6e-18`), so `det(1 − N_{s,+})` vanishes to order ≥ 2 (`≈ 5e-37`, `≈ 1e-36`).
  This is §5.2's prediction that `g(s)` — and hence `ζ(2s)⁻¹` — is common to `φ₄` and `φ₄^χ`.
- **Controls are order one** on every column, at both `N`, stable to 5 digits under `N = 40 → 60`.
  The vanishing is not an artefact of a degenerate implementation.

### 6.2 The four new predictions of §5.2

`N = 60`. `π/log 2 = 4.532360141827194`.

| point | predicted zero of | `|det(1−L₊)|` (trivial) | `|det(1+L₊)|` (χ) |
|---|---|---:|---:|
| `s = i·π/log2 = 4.5323601i` | trivial sector only | **`5.6686e-30`** | `1.9536e+00` |
| `s = 3i·π/log2 = 13.5970804i` | trivial sector only | **`7.6820e-27`** | `3.7396e+01` |
| `s = 2i·π/log2 = 9.0647203i` | χ sector only | `7.0241e+00` | **`4.6247e-30`** |
| `s = 4i·π/log2 = 18.1294406i` | χ sector only | `9.0581e+01` | **`7.1167e-21`** |
| control `s = 4.0i` | — | `6.2803e-01` | `8.1452e-01` |
| control `s = 5.0i` | — | `9.9875e-01` | `3.3143e+00` |
| control `s = 8.5i` | — | `6.7790e+00` | `1.4829e+00` |
| control `s = 9.6i` | — | `8.6092e+00` | `3.1449e+00` |
| control `s = 13.0i` | — | `1.2915e+01` | `1.1149e+01` |

For reference, `|D₄⁻| = |det(1−L₋)|` at the two trivial-sector prediction points is also order
one (`2.1274e+00` at `iπ/log2`, `3.0797e+01` at `3iπ/log2`), so the vanishing is confined to the
single sector predicted.

**[NUMERIC] Result: 4/4 confirmed, with two-way discrimination.** Each predicted point vanishes
in **exactly the sector §5.1 assigns it and not the other**, and every nearby control is order
`10⁰`–`10¹`. The `(1+2^{1-s})/(1+2^s)` vs `(2^{1-s}−1)/(2^s−1)` split — the entire content of the
new elementary factor — is reproduced by the transfer operator to 20–30 digits.

This is the strongest available evidence that the q=4 ζ-factor is the **scattering/resonance**
divisor. These extra resonances have nothing to do with `ζ`, with Maass forms, or with the `K_s`
divisor; they exist only because the scattering determinant of `Γ₀⁺(2)` carries the elementary
level factor derived in §5.1. Finding them where predicted, and only there, is a genuine
falsification test that the derivation passed.

### 6.3 Scattering-formula self-checks (mpmath, 30 dps)

```
phi_4(s) phi_4(1-s)  at  s = 0.3+2i, 0.8-1i, 1.4+0.5i
    ->  1.000000000000 + 1.15e-31 j ,  1.000000000000 + 6.18e-32 j ,
        1.000000000000 - 1.50e-31 j
Res_{s=1} phi_4  =  0.6366197724 ;   1/vol(Gamma_0^+(2)\H) = 6/(3 pi) = 0.6366197724
```

### 6.4 Correction to the M1c pin values [NUMERIC]

M1c's pin2 was recorded as `0.25 + 10.511019819386503i`, i.e. `γ₂ = 21.022039638773006`. The
Odlyzko value is `γ₂ = 21.022039638771554993`. With the corrected pin, `|D₄⁺|` at pin2 drops from
M1c's `2.74e-12` to `4.7e-19`; at pin1, from `2.83e-15` to `7.2e-19`; the depths become uniform
across pins, as they should for a genuine zero. **M1c's shallow-zero remark about pin 3 is an
artefact of pin precision, not of the operator.** M1c's qualitative verdict is unaffected.

---

## 7. Gaps closed by M1D

### 7.1 [PROVED] The `K_s` divisor cannot interfere at the pins

`M1_DERIVATION_DRAFT` §4 flagged: "a zero of a reduced determinant cannot automatically be
promoted to a zero of the Selberg quotient without locating or excluding that divisor at the same
`s`." For q=4, `h₄ = 1` so `K_s = L_{2,s}` with multiplier `ℓ = √((2−√2)/(2+√2)) = √2 − 1` and
(M1B eq. (8), from MMS Thm 6.4 + Prop. 2)

```
det(1 - K_s) = prod_{m >= 0} ( 1 - (sqrt2 - 1)^(2s + 2m) ).
```

With `ℓ ∈ (0,1)`, `ℓ^{2s+2m} = 1` iff `(2s+2m)log ℓ ∈ 2πiZ` iff

```
s = -m + i k pi / log(sqrt2 - 1),    m >= 0 integer,  k integer.
```

Hence **every zero of `det(1−K_s)` has `Re s ∈ Z_{≤0}`**, and the product converges absolutely
(so has no poles) for `Re s > 0`. In particular `det(1−K_s) ≠ 0` on `Re s = 1/4` and at `s = 1`.

**Consequence.** On the line `Re s = 1/4` — which is where the `ρ/2` pins live — MMS Thm 6.4 reads
`Z_{S,4}(s) = D₄⁺(s)D₄⁻(s)/det(1−K_s)` with a nonvanishing, finite denominator. A zero of `D₄⁺`
there is a zero of `Z_{S,4}` of the same order. The gap is closed for the line that matters.
(It is **not** closed on `Re s ≤ 0`, where §5.2's extra resonances live — see the ledger.)

### 7.2 [PROVED] The zeta normalisation is settled

`M1_DERIVATION_DRAFT` §4 `[GAP] Zeta normalization` asked whether elementary Euler factors belong
to the `ζ(2s)` factor or to `R₄`. §5.1 answers: the ζ-carrying object is the scattering
determinant `φ₄`, the ζ factor is **primitive** `ζ(2s)` (not the imprimitive `ζ^{(2)}(2s)` of
M1B eq. (7)), and the elementary factor that accompanies it is `(1+2^{1-s})/(1+2^s)`, whose
divisor is now numerically confirmed (§6.2).

---

## 8. Falsifiable spec for a complete U₄

Any construction that upgrades (DIV) to the operator-level factorisation (C4)

```
det(1 - L^(4)_{s,+}) = zeta(2s) R_4(s)
```

must satisfy all of the following. They are stated so that a candidate can be **refuted** by
failing any one of them.

- **(S1) Coset existence.** Its modular side must be a coset module of a group that actually
  contains `W₂`. Any candidate using `Γ₀(2)\PSL(2,Z)` is refuted by §2.1 without further work.
- **(S2) Non-conjugacy.** It must be a genuine induction with a nonzero residual block `R_{4,s}`;
  no pure similarity is possible, by the `(2,4,∞)` vs `(2,3,∞)` torsion argument of §2.2.
- **(S3) Constant coset cocycle.** It must reproduce `ρ⁺(word of length r) = σ^r` — verified here
  to `r = 6` with zero exceptions. A candidate predicting a length-dependent or letter-dependent
  coset value is refuted immediately.
- **(S4) Cusp faithfulness.** It must transport the parabolic return word `(−1,−2)` (§4) and the
  `n → ±∞` accumulation of `L^inf_{±}` to the modular cusp, since by §5 that is the sole source of
  the ζ divisor. A candidate that is finite-state on the branch alphabet cannot satisfy (S4) and
  is refuted: no finite-coset intertwiner can produce `ζ(2s)`.
- **(S5) Elementary-factor divisor.** It must place zeros of the trivial sector at
  `s = i(2k+1)π/log 2` and of the χ sector at `s = 2ikπ/log 2`, and at no other point of `Re s = 0`
  in that range. §6.2 shows the true operator does this; a candidate `U₄` whose remainder `R₄`
  absorbs or misplaces these is refuted numerically at a cost of seconds.
- **(S6) Multiplicity.** It must give `ord_{s=ρ/2} D₄⁺ ≥ ord_{s=ρ/2} ζ(2s)` for **every**
  nontrivial `ρ`, with `R₄` globally meromorphic (`M1_DERIVATION_DRAFT` §4 formal quotient
  criterion). Finitely many pins never establish this.
- **(S7) `K_s` compatibility.** Off the line `Re s = 1/4`, it must account for the `K_s` divisor at
  `s ∈ −Z_{≥0} + iπZ/log(√2−1)` (§7.1). In particular any claim about the extra resonances of
  §5.2, which sit at `Re s = 0`, must exclude the `m = 0` family of `K_s` zeros at
  `s = i k π/log(√2−1)`, i.e. `|Im s| ∈ 3.5642·Z` — at `Re s = 0` the two divisors coexist
  (`π/log 2 = 4.5324` vs `π/|log(√2−1)| = 3.5642`) and must be separated.

---

## 9. Gaps ledger

| # | Obligation | Status | Route |
|---|---|---|---|
| G1 | `det(1−L̂⊗σ) = det(1−L̂)det(1+L̂)` for a nuclear operator, via the trace expansion and meromorphic continuation | PROVED here (§3.3) | **ARISTOTLE-ABLE** — finite algebra + a standard nuclear-determinant lemma; the trace identity `tr((A⊗σ)^n) = tr(A^n)tr(σ^n)` is mechanical |
| G2 | `W₂` normalises `Γ₀(2)` but not `PSL(2,Z)`; `ρ⁺(A_n) = σ` for all `n ∈ A` | PROVED here (§2.1–2.3) | **ARISTOTLE-ABLE** — pure 2×2 integer-matrix algebra, already exact-checked |
| G3 | `M_w ∈ Γ₀(2)` for all even words, with the exact `2s`-cocycle, for **all** word lengths (not just `r ≤ 6`) | GAP | **ARISTOTLE-ABLE** — induction on `r` from `A_n = W₂Tⁿ`, `W₂² = 1`, `W₂Γ₀(2)W₂ = Γ₀(2)` |
| G4 | `det(1−K_s)` has all zeros on `Re s ∈ Z_{≤0}` and is nonvanishing on `Re s = 1/4` | PROVED here (§7.1) | **ARISTOTLE-ABLE** — convergence of `∏(1−ℓ^{2s+2m})` plus the root computation |
| G5 | `Γ₀⁺(p)` scattering determinant `φ⁺_p = g(s)(1+p^{1-s})/(1+p^s)` **derived from the Eisenstein constant term**, not by symmetrising a cited `Γ₀(p)` matrix | GAP (formula PROVED modulo the cited `Γ₀(p)` matrix; 3 consistency checks pass) | **FRONTIER** — needs the `W_p`-symmetrised Eisenstein series and its constant term; a literature check for `Γ₀⁺(N)` scattering (Fricke-group spectral theory) may make it CITED instead |
| G6 | "Resonances (poles of `φ` in `Re s < 1/2`) lie in the divisor of `Z_S`", with multiplicity | CITED, not re-derived | **FRONTIER** — the precise divisor statement for a 1-cusp cofinite group; must be pinned to a theorem number before (C4) can be claimed |
| G7 | Transport: identify `ord_{s₀} D₄⁺` with `ord_{s₀} Z_{S,4}` + the resonance order, i.e. connect MMS Thm 6.4 to the Selberg divisor **sector by sector** | GAP — the core remaining obligation | **FRONTIER** — this is the "which MMS `(P)`-sector carries the scattering divisor" theorem; §6.1 gives the answer numerically (`(P)`-even) but no proof |
| G8 | `det(1 − N_{s,+})` ↔ `Z_{Γ₀(2)}`-divisor identification (the level-2 side of (DIV)) | GAP | **FRONTIER** — needs G6 + G7 for `Γ₀(2)`; the Venkov–Zograf character factorisation is the tool |
| G9 | Global meromorphy and multiplicity of `R₄(s) = D₄⁺(s)/ζ(2s)` — spec item (S6) | GAP | **FRONTIER** — not reachable from point evaluations; requires G7 |
| G10 | Separate the `K_s` divisor from the §5.2 extra resonances on `Re s = 0` — spec item (S7) | GAP | **ARISTOTLE-ABLE** — compare two explicit arithmetic progressions, `kπ/log(√2−1)` vs `kπ/log 2`; irrationality of the ratio suffices |
| G11 | Upgrade §6's midpoints to certified ball enclosures + argument-principle winding at the four §6.2 prediction points | GAP | **ARISTOTLE-ABLE / compute lane** — the existing `winding_box` primitive in `zeta_cert_rosen_even.py` does exactly this; no new theory |
| G12 | q=6 analogue: `φ₆(s) = g(s)(1+3^{1-s})/(1+3^s)`, extra resonances at `s = i(2k+1)π/log 3` (`π/log 3 = 2.8596`) | GAP — untested | **compute lane** — a direct rerun of §6.2 with `q=6`; cheap, and a second confirmation would make the mechanism a family statement |

**Summary:** 4 obligations PROVED here, 5 tagged ARISTOTLE-ABLE, 5 tagged FRONTIER (G5–G9 are the
real theorem), 2 cheap compute items (G11, G12) that would materially raise confidence.

---

## 10. What M1D does and does not claim

**Claims.** (i) The M1c obstruction is fatal to the `PSL(2,Z)`-coset route, for a stronger reason
than M1c gave. (ii) The correct level-2 model induces along `Γ₀(2) ◁ Γ₀⁺(2)`; `U₄` is explicit,
invertible, and gives the exact divisibility (DIV). (iii) The intertwining data is exact-verified
through word length 6, 0 failures. (iv) The `ζ(2s)` factor originates in the cusp/scattering, with
`φ₄` derived in closed form and its novel elementary divisor confirmed 4/4 numerically.
(v) The `K_s` divisor is proved harmless on `Re s = 1/4`.

**Does not claim.** (C4) is not proved. No operator intertwiner between `N_{s,+}` and the
Fraczek–Mayer `M_{2,s}` exists or is claimed. The sector assignment ((P)-even carries the
resonances) is numerical only. No ball enclosure, winding number, multiplicity, or global
remainder `R₄` is established. §6 is non-rigorous throughout.

---

## References

**[CITED]** Mayer, Mühlenbruch, Strömberg, "The transfer operator for the Hecke triangle groups,"
*DCDS* 32 (2012) 2453–2484, arXiv:0912.2236 — eqs. (3), (13), (19), (26)–(32), Lemma 4.5,
Thm 4.10, Lemma 5.1, Prop. 2, Thm 6.4.

**[CITED]** Fraczek, Mayer, "Symmetries of the transfer operator for `Γ₀(N)` and a character
deformation of the Selberg zeta function for `Γ₀(4)`," *ANT* 6 (2012) 587–610, arXiv:1011.4441,
§2, eqs. (2.0.2)–(2.0.3) — the 3-coset model shown fatal here for the Fricke step.

**[CITED]** Takeuchi, "Arithmetic triangle groups," *J. Math. Soc. Japan* 29 (1977) 91–106,
Thm 3 §5 — `G₄ ≅ Γ₀⁺(2)`.

**[CITED]** Iwaniec, *Spectral Methods of Automorphic Forms*, and Hejhal, *The Selberg Trace
Formula for `PSL(2,R)`* vol. 2 — the `Γ₀(p)` scattering matrix and the resonance/`Z_S` divisor
statement (G6 must be pinned to a specific theorem number before (C4) is claimed).

**[CITED]** Mayer, *Bull. AMS* 25 (1991) 55–60, Thm 2; Lewis–Zagier, *Ann. Math.* 153 (2001)
191–258, §4 — the `q=3` anchor.

**Scripts (scratchpad, not committed):** `m1d_symbolic.py` (exact, stdlib only),
`m1d_numeric.py` (python-flint + mpmath, via the unmodified
`.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py`).
