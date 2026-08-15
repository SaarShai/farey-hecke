# M1F — first-principles Eisenstein derivation of the Γ₀⁺(p) scattering determinant

**Date:** 2026-08-15
**Ticket:** G5 of `M1D_U4_CONSTRUCTION.md` §9 — "`Γ₀⁺(p)` scattering determinant
`φ⁺_p = g(s)(1+p^{1−s})/(1+p^s)` **derived from the Eisenstein constant term**, not by
symmetrising a cited `Γ₀(p)` matrix" — with a partial attack on G6.
**Parents:** `M1D_U4_CONSTRUCTION.md` §5 (closed form + q=4 numerics),
`M1E_PHI6_FAMILY_PROBE.md` (q=6 family confirmation).
**Status convention:** identical to M1D/M1E. Every substantive claim is tagged exactly
`PROVED`, `CITED`, `NUMERIC`, or `GAP`.
`PROVED` = derived here in closed form, or verified in exact/symbolic arithmetic.
`CITED` = imported from the literature; I state what is imported and how load-bearing it is.
`GAP` = not justified; with a precise statement of what is missing.

**No new numerics.** This is a derivation note. The numerical confirmations already exist
(M1D §6, M1E §4) and are not repeated or relied on as evidence for anything derived here.

---

## 0. Verdict up front

**DERIVED-MODULO-GAPS.** The closed forms of M1D/M1E are **not refuted** — they are confirmed,
and the derivation is now genuinely first-principles rather than a pattern-citation.

What §§1–4 establish, in a chain in which every link is either `PROVED` here or is a
single named textbook theorem:

1. `G_q ≅ Γ₀⁺(p)` for `(q,p) = (4,2), (6,3)`, by an **explicit conjugator** `D = diag(p^{1/4},p^{−1/4})`
   which is simultaneously the cusp scaling matrix — so the scattering function transports with
   **no scalar factor** (§1.4, `PROVED`). Two independent volume cross-checks agree (§1.5).
2. `Γ₀⁺(p)` has **exactly one cusp**, because `W_p` swaps `∞` and `0` (§1.2, `PROVED`), and its
   width-1 stabiliser at `∞` is unchanged from `Γ₀(p)` (§1.3, `PROVED`).
3. The Eisenstein series of `Γ₀⁺(p)` at its single cusp is **exactly** the sum of the two `Γ₀(p)`
   cusp-Eisenstein series, `E^+ = E_∞ + E_0`, by a coset computation with no analytic input
   (§2.2, `PROVED`). The χ-twist gives `E^χ = E_∞ − E_0` (§2.3, `PROVED`).
4. Consequently the one-cusp scattering "matrix" of `Γ₀⁺(p)` is `φ⁺ = φ_{∞∞} + φ_{∞0}` and the
   χ-twisted one is `φ⁻ = φ_{∞∞} − φ_{∞0}` (§2.4, `PROVED`) — i.e. M1D's "symmetrisation" is a
   **theorem, not an ansatz**, and it is exactly the eigenvalue decomposition of the 2×2
   `Φ(s)` on the `W_p`-symmetric / antisymmetric vectors (§3.1).
5. The two entries `φ_{∞∞}, φ_{∞0}` are **derived here from scratch** (§3.2–3.3, `PROVED` modulo
   one `CITED` constant-term formula) by counting allowed moduli and evaluating two Dirichlet
   series against the Euler product of `ζ(2s−1)/ζ(2s)`. They reproduce the entries M1D cited.
6. A **second, independent derivation** that bypasses `Γ₀(p)` entirely: apply the same
   constant-term formula directly to `Γ₀⁺(p)` and count its own allowed moduli (§3.5, `PROVED`).
   The two computations agree term by term.
7. The algebra `φ_{∞∞} ± φ_{∞0} → g(s)(1+p^{1−s})/(1+p^s)`, `g(s)(p^{1−s}−1)/(p^s−1)` is verified
   symbolically (§4, `PROVED`, sympy, exact). **It matches M1D §5.1 and M1E §1 identically.**
8. `g(s) = Λ(2s−1)/Λ(2s)` with `Λ(w) = π^{−w/2}Γ(w/2)ζ(w)`, so `g(s)g(1−s) = 1` is a **one-line
   consequence of `Λ(w) = Λ(1−w)`** rather than a numerical observation (§4.3, `PROVED`).

**What is still `GAP`** (§5.4, §6): the resonance transport. The statement "poles of the
scattering determinant in `Re s < 1/2` are zeros of `Z_S`" is used with a **derivation sketch
that is sound in structure but rests on the Selberg-zeta functional equation of a cofinite
group, which I have not pinned to a verified theorem number**. I give the argument, isolate
exactly the one imported ingredient, and show that the ingredient's *shape* (a ratio of
Γ-functions times an exponential of an entire function) is enough for the conclusion off the
real axis — which is where every point of interest lies. That reduces G6 but does not close it.

**Honest calibration.** The load-bearing new content of M1F is items 3, 4, 5, 6 — the
`E^+ = E_∞ + E_0` coset identity and the two independent moduli counts. These convert M1D §5.1
from "we symmetrised a formula we found in a book" into "we computed the constant term of the
`Γ₀⁺(p)` Eisenstein series". That is precisely what G5 asked for. Item 8 is a small
simplification that removes a numerical check in favour of a proof. Nothing here proves (C4),
and nothing here upgrades any of M1D's `NUMERIC` claims to `PROVED`.

---

## 1. Set-up: the group, its cusp, and the conjugation

Throughout `p` is prime, and all groups are taken in `PSL(2,R)` (i.e. modulo `±I`).

```
T   = [[1,1],[0,1]]
W_p = (1/sqrt(p)) [[0,-1],[p,0]]        (normalised Fricke involution, W_p^2 = -I ~ 1 in PSL_2)
Gamma_0(p)  = { [[a,b],[c,d]] in PSL(2,Z) : c = 0 mod p }
Gamma_0^+(p) = Gamma_0(p)  union  Gamma_0(p) W_p
```

`W_p` acts as `z ↦ −1/(pz)`.

### 1.1 [PROVED] `W_p` normalises `Γ₀(p)`, and the index is 2

For `γ = [[a,b],[pc,d]] ∈ Γ₀(p)` with `ad − pbc = 1`:

```
W_p gamma W_p^{-1}
  = (1/p) [[0,-1],[p,0]] [[a,b],[pc,d]] [[0,1],[-p,0]]
  = (1/p) [[-pc,-d],[pa,pb]] [[0,1],[-p,0]]
  = (1/p) [[pd, -pc],[-p^2 b, pa]]
  = [[d, -c],[-pb, a]].                                            (1.1)
```

This is integral, has lower-left `−pb ≡ 0 (mod p)`, and determinant `ad − pbc = 1`. So
`W_pΓ₀(p)W_p^{-1} = Γ₀(p)` (the reverse inclusion is the same computation, `W_p^{-1} = W_p` in
`PSL₂`). Since `W_p ∉ PSL(2,Z)` (entries `±1/√p, ±√p`), `Γ₀(p) ◁ Γ₀⁺(p)` with quotient `Z/2`.
This is M1D §2.3 for `p = 2`; (1.1) is the general-`p` statement, and it is the only group-theoretic
input §2 needs.

Write `χ` for the nontrivial character of `Γ₀⁺(p)/Γ₀(p) ≅ Z/2`: `χ|_{Γ₀(p)} = 1`, `χ(W_p) = −1`.
`χ` is real, so `χ̄ = χ`.

### 1.2 [PROVED] `Γ₀⁺(p)` has exactly one cusp

`Γ₀(p)` (`p` prime) has exactly two cusp classes, represented by `∞` and `0`.
[`CITED`, standard: the cusp count of `Γ₀(N)` is `Σ_{d|N} φ(gcd(d, N/d))`, which for `N = p` is
`φ(1) + φ(1) = 2`. Also directly: `PSL(2,Z)` acts transitively on `P¹(Q)` and `Γ₀(p)` has index
`p+1`; the two orbits are `{a/c : p | c}` and `{a/c : p ∤ c}`.]

`W_p` maps `∞ ↦ 0` and `0 ↦ ∞`:

```
W_p(z) = -1/(pz),   W_p(oo) = 0,   W_p(0) = oo.                     (1.2)
```

`Γ₀⁺(p)` has the same set of parabolic fixed points as `Γ₀(p)`, namely `P¹(Q)`, so its cusps are
the `Γ₀⁺(p)`-orbits on `P¹(Q)`. Since `Γ₀⁺(p) = Γ₀(p) ⊔ Γ₀(p)W_p`, the `Γ₀⁺(p)`-orbit of `∞` is
`Γ₀(p)·∞ ∪ Γ₀(p)·0` = the union of the two `Γ₀(p)` classes. Hence **one cusp**. ∎

This is the fact M1D §5.1 asserted ("`W₂` swaps the two `Γ₀(2)` cusps `∞` and `0`") without proof.
It is (1.2), one line.

### 1.3 [PROVED] The cusp width does not change

`Γ₀⁺(p)_∞ = Γ₀(p)_∞ = ⟨T⟩`.

*Proof.* `⊇` is clear. For `⊆`: an element of the nontrivial coset is `γW_p` with `γ ∈ Γ₀(p)`, and
`γW_p(∞) = γ(0)`. If this equals `∞` then `γ` carries the cusp `0` to the cusp `∞` inside `Γ₀(p)`,
contradicting §1.2's statement that they are inequivalent. So the stabiliser lies in `Γ₀(p)`, where
it is `⟨T⟩` (the stabiliser of `∞` in `PSL(2,Z)`, which lies in `Γ₀(p)`). ∎

**Consequence.** The scaling matrix of the single cusp of `Γ₀⁺(p)` may be taken to be
`σ_∞ = I`, exactly as for the cusp `∞` of `Γ₀(p)`. This matters: the scattering matrix depends on
the choice of scaling matrices, and a mismatch would introduce a spurious factor `t^{2s−1}`.
Here there is none.

### 1.4 [PROVED] `G_q ≅ Γ₀⁺(p)` via a conjugator that *is* the cusp scaling matrix

Let `G_q = ⟨S, T_{λ_q}⟩`, `S(z) = −1/z`, `T_{λ}(z) = z + λ`, `λ_q = 2cos(π/q)`. For `q = 4`,
`λ = √2 = √p` with `p = 2`; for `q = 6`, `λ = √3 = √p` with `p = 3`. In both cases `λ_q = √p`.

Set `D = diag(p^{1/4}, p^{−1/4})`, i.e. `D(z) = z√p`, so `D^{-1}(z) = z/√p`. Then

```
D^{-1} T_{sqrt p} D  =  T                    (translation by sqrt p  ->  translation by 1)
D^{-1} S D           =  (1/sqrt p)[[0,-1],[p,0]]  =  W_p.           (1.3)
```

*(Second line: `D^{-1}SD = diag(p^{−1/4},p^{1/4})·[[0,−1],[1,0]]·diag(p^{1/4},p^{−1/4})
= [[0, −p^{−1/2}],[p^{1/2}, 0]] = W_p`.)* This is M1B's `A_n = W₂T^n` computation at `p = 2`,
here in its general-`p` form.

So `D^{-1}G_q D = ⟨W_p, T⟩`. And `⟨W_p, T⟩ = Γ₀⁺(p)`:

- `⊆`: both generators lie in `Γ₀⁺(p)`.
- `⊇`: by (1.1), `W_p T W_p^{-1} = [[1,0],[−p,1]]`, so `⟨W_p,T⟩ ⊇ ⟨T, [[1,0],[p,1]]⟩`. For `p = 2,3`
  the latter is all of `Γ₀(p)` [`CITED`, standard generators of `Γ₀(2)`, `Γ₀(3)`; for `p = 2` note
  `[[1,0],[2,1]] = E·T` with the order-2 element `E = [[1,−1],[2,−1]]`, and `Γ₀(2)/± ≅ Z/2 * Z`
  is generated by `T` and `E` — signature `(0; 2; 2 cusps)`]. Adjoining `W_p` gives `Γ₀⁺(p)`.

`[CITED]` Takeuchi, *Arithmetic triangle groups*, J. Math. Soc. Japan **29** (1977) 91–106 —
`G_4 ≅ Γ₀⁺(2)`, `G_6 ≅ Γ₀⁺(3)` (the arithmetic Hecke groups are `q = 3,4,6,∞`). M1D §5.1 and
M1E §1 already cite this; (1.3) makes the conjugator explicit, which is what §1.3 needs.

**[PROVED] No scalar transport factor.** The cusp of `G_q` at `∞` has width `λ_q = √p`, so its
scaling matrix is `σ_∞^{G_q} = diag(p^{1/4}, p^{−1/4}) = D`. Under the isometry `z ↦ D^{-1}z` of
`H`, this is carried to `D^{-1}·D = I`, which by §1.3 is the correct scaling matrix for
`Γ₀⁺(p)`. Scaling matrices correspond; therefore

```
phi_{G_q}(s) = phi_{Gamma_0^+(p)}(s)     exactly, with no factor of lambda^{2s-1}.   (1.4)
```

This is a trap that a careless conjugation argument falls into, and (1.4) closes it.

### 1.5 [PROVED] Two independent volume cross-checks

`vol(Γ₀⁺(p)\H) = vol(Γ₀(p)\H)/2 = (π/3)(p+1)/2 = (π/6)(p+1)`, using
`vol(PSL(2,Z)\H) = π/3` and `[PSL(2,Z) : Γ₀(p)] = p+1`.

Independently, `G_q` is the `(2,q,∞)` triangle group: the hyperbolic triangle with angles
`π/2, π/q, 0` has area `π − π/2 − π/q = π(1/2 − 1/q)`, and the orientation-preserving group is
index 2 in the reflection group, so `vol(G_q\H) = 2π(1/2 − 1/q) = π(1 − 2/q)`.

```
q = 4:  pi(1 - 1/2) = pi/2       vs  (pi/6)(2+1) = pi/2        MATCH
q = 6:  pi(1 - 1/3) = 2pi/3      vs  (pi/6)(3+1) = 2pi/3       MATCH
```

Both agree. This independently corroborates §1.4's identification *and* its normalisation, since
volume is a conjugation invariant that the `λ^{2s−1}` trap would not have disturbed but a wrong
group identification would.

---

## 2. The Eisenstein series of `Γ₀⁺(p)` is the symmetrised `Γ₀(p)` vector

This section is the heart of the note and contains **no analytic input at all** — it is a coset
bijection. Everything converges absolutely for `Re s > 1` where the series are defined; the
identities then persist under meromorphic continuation.

Write `Γ' = Γ₀(p)`, `Γ = Γ₀⁺(p)`. For a cusp `a` of `Γ'` with scaling matrix `σ_a`, the Eisenstein
series is

```
E_a(z,s) = sum_{gamma in Gamma'_a \ Gamma'}  Im( sigma_a^{-1} gamma z )^s ,   Re s > 1.   (2.1)
```

By §1.3 take `σ_∞ = I`.

### 2.1 [PROVED] `W_p` is a valid scaling matrix for the cusp `0` of `Γ₀(p)`

`σ_0 := W_p` satisfies `σ_0(∞) = 0` by (1.2), and

```
W_p^{-1} [[1,0],[p,1]] W_p
  = (1/p) [[0,1],[-p,0]] [[1,0],[p,1]] [[0,-1],[p,0]]
  = (1/p) [[p,1],[-p,0]] [[0,-1],[p,0]]
  = (1/p) [[p, -p],[0, p]]  =  [[1,-1],[0,1]] = T^{-1},           (2.2)
```

and `Γ'_0 = ⟨[[1,0],[p,1]]⟩`. So `σ_0^{-1}Γ'_0σ_0 = ⟨T⟩`, as required. ∎

**This is the structurally important coincidence of the whole construction:** the scaling matrix
of the *second cusp* of `Γ₀(p)` and the *Fricke involution we quotient by* are the **same
element**. That is why the symmetrisation is exact and not merely formal.

### 2.2 [PROVED] `E^+ = E_∞ + E_0`

`Γ` has one cusp `∞` with `Γ_∞ = Γ'_∞` (§1.3) and `σ_∞ = I`, so its Eisenstein series is
`E^+(z,s) = Σ_{γ ∈ Γ_∞\Γ} Im(γz)^s`. Decompose the cosets:

```
Gamma_infty \ Gamma  =  ( Gamma'_infty \ Gamma' )  sqcup  ( Gamma'_infty \ Gamma' W_p ),
```

which is legitimate because `Γ_∞ = Γ'_∞ ⊆ Γ'` and `Γ = Γ' ⊔ Γ'W_p` is a disjoint union of
**left** `Γ'`-cosets, hence of `Γ'_∞`-coset-blocks. Therefore

```
E^+(z,s) = sum_{gamma in Gamma'_infty \ Gamma'} Im(gamma z)^s
         + sum_{gamma in Gamma'_infty \ Gamma'} Im(gamma W_p z)^s
         = E_infty(z,s) + E_infty(W_p z, s).                       (2.3)
```

Now identify the second term. Using `Γ'_0 = W_pΓ'_∞W_p^{-1}` (which is (2.2) read backwards), the
map `γ ↦ W_p^{-1}γ` is a bijection `Γ'_0\Γ' → Γ'_∞\(W_p^{-1}Γ') = Γ'_∞\(Γ'W_p)` (using
`W_p^{-1}Γ' = Γ'W_p^{-1} = Γ'W_p` in `PSL₂`, by §1.1). Hence writing `δ = γW_p`,

```
E_0(z,s) = sum_{gamma in Gamma'_0 \ Gamma'} Im(sigma_0^{-1} gamma z)^s
         = sum_{delta in Gamma'_infty \ Gamma' W_p} Im(delta z)^s
         = E_infty(W_p z, s).                                       (2.4)
```

Combining (2.3) and (2.4):

```
   E^+(z,s)  =  E_infty(z,s) + E_0(z,s).                            (E+)
```
∎

**This replaces M1D §5.1's "the `Γ₀⁺(p)` scattering matrix is the `W_p`-symmetric combination"
with a proof.** M1D asserted the symmetrisation; (E+) derives it from the coset decomposition.

### 2.3 [PROVED] The χ-twisted series

For a character `χ` of `Γ` trivial on `Γ_∞` (which holds: `T ∈ Γ'` and `χ|_{Γ'} = 1`), the twisted
Eisenstein series `E^χ(z,s) = Σ_{Γ_∞\Γ} χ(γ)^{-1} Im(γz)^s` is well defined. The identical coset
split, with `χ = +1` on `Γ'` and `χ = −1` on `Γ'W_p`, gives

```
   E^chi(z,s)  =  E_infty(z,s) - E_0(z,s).                          (Echi)
```
∎

### 2.4 [PROVED, given the constant-term convention] The two scattering functions

Let `Φ(s) = (φ_{ab}(s))_{a,b ∈ {∞,0}}` be the `Γ₀(p)` scattering matrix, defined by the constant
terms

```
E_a(sigma_b z, s) = delta_{ab} y^s + phi_{ab}(s) y^{1-s} + (nonzero Fourier modes).   (2.5)
```

`Φ` is symmetric, `φ_{∞0} = φ_{0∞}` [`CITED`, general theory; for this group it is also immediate
from §1.1 as shown in §3.4]. Taking the constant term of (E+) and (Echi) at the cusp `∞`
(i.e. `b = ∞`, `σ_∞ = I`) and using (2.5):

```
E^+  :  y^s (from E_infty) + 0 (from E_0) + [ phi_{oo,oo} + phi_{0,oo} ] y^{1-s}
E^chi:  y^s                - 0             + [ phi_{oo,oo} - phi_{0,oo} ] y^{1-s}
```

Since `Γ₀⁺(p)` has one cusp, its scattering "matrix" is the `1×1` matrix `φ⁺`, and its determinant
is `φ⁺` itself. Hence

```
   phi^+(s) = phi_{oo,oo}(s) + phi_{oo,0}(s)      [ Gamma_0^+(p),  trivial character ]
   phi^-(s) = phi_{oo,oo}(s) - phi_{oo,0}(s)      [ Gamma_0^+(p),  chi-twisted ]      (2.6)
   phi^+(s) phi^-(s) = phi_{oo,oo}^2 - phi_{oo,0}^2 = det Phi(s)   [ full Gamma_0(p) ]
```
∎

The last line uses `φ_{00} = φ_{∞∞}` (§3.4).

---

## 3. The entries, computed from the constant term

Now — and only now — analysis enters, through one imported formula.

### 3.1 The eigenvalue framing (equivalent packaging of (2.6))

`W_p` permutes the cusps of `Γ₀(p)` by the transposition `∞ ↔ 0`. Conjugation-invariance of `Γ₀(p)`
under `W_p` (§1.1) forces `Φ(s)` to commute with the swap `σ = [[0,1],[1,0]]`, i.e.

```
Phi(s) = [[A, B],[B, A]],    A := phi_{oo,oo} = phi_{0,0},   B := phi_{oo,0} = phi_{0,oo}.
```

`σ` has eigenvectors `(1,1)ᵀ` (eigenvalue `+1`, the `W_p`-symmetric / trivial-character vector) and
`(1,−1)ᵀ` (eigenvalue `−1`, the χ vector), and

```
V Phi V^{-1} = diag(A+B, A-B),   V = (1/sqrt2)[[1,1],[1,-1]].       (3.1)
```

So (2.6) is exactly the eigenvalue decomposition the task asked for, and `V` is **the same
character-basis matrix `V` M1D §3.2 used to diagonalise `ρ⁺ = 1 ⊕ χ`**. The operator-side and
cusp-side `Z/2`-decompositions are the same decomposition. That is a structural consistency check
M1D did not make explicit.

### 3.2 [CITED] The one imported ingredient

**Constant-term / allowed-moduli formula.** For a cofinite Fuchsian group `Γ` with cusps `a, b` and
scaling matrices `σ_a, σ_b`, the scattering entry is

```
   phi_{ab}(s) = sqrt(pi) * Gamma(s - 1/2)/Gamma(s) * sum_{c in C_ab} c^{-2s} * S_{ab}(0,0;c),
                                                                              (3.2)
   C_ab = { c > 0 : [[*,*],[c,*]] in sigma_a^{-1} Gamma sigma_b },
   S_{ab}(0,0;c) = # { d mod c : [[*,*],[c,d]] in sigma_a^{-1} Gamma sigma_b }.
```

This is the `m = n = 0` case of the Fourier expansion of `E_a(σ_b z, s)` in Kloosterman sums,
obtained by Bruhat-decomposing `σ_a^{-1}Γσ_b` and integrating `Im(γz)^s` over one period; the
`√π Γ(s−1/2)/Γ(s)` is `∫_R (x²+1)^{-s}dx`.

`[CITED]` Iwaniec, *Spectral Methods of Automorphic Forms*, 2nd ed. (AMS GSM 53), Chapter 3
(Eisenstein series / their Fourier expansion). Also Hejhal, *The Selberg Trace Formula for
PSL(2,R)* vol. 2 (Springer LNM 1001), Ch. 11.
**`[GAP — citation precision]`** I have **not** verified the theorem/equation numbering against
the physical texts in this session; do not put a number in a paper on my say-so. The *content*
of (3.2) is textbook and I am confident in it; the *label* is unpinned. See §6, obligation N1.

This is the **only** analytic import in §§1–4. Everything downstream of (3.2) is counting and
Euler products.

### 3.3 [PROVED] `φ_{∞∞}` for `Γ₀(p)`

Here `σ_∞ = I`, so `σ_∞^{-1}Γ₀(p)σ_∞ = Γ₀(p)`, and:

- **Allowed moduli.** `c > 0` with `p | c`, i.e. `c = pm`, `m ≥ 1`.
- **Count.** For such `c`, a lower row `(c,d)` completes to `[[a,b],[c,d]] ∈ SL(2,Z)` iff
  `gcd(c,d) = 1`; the congruence `c ≡ 0 (p)` is automatic. So `S_{∞∞}(0,0;c) = φ_E(c)`
  (Euler `φ`; subscript E to avoid collision with the scattering `φ`).

Hence, with `D(s) := Σ_{c≥1} φ_E(c)c^{-2s}`,

```
   Z_{oo,oo}(s) := sum_{p | c} phi_E(c) c^{-2s}.
```

**[PROVED] The Euler-product restriction lemma.** `D(s) = ζ(2s−1)/ζ(2s)`, with local factor at a
prime `ℓ`

```
L_ell = 1 + (1 - 1/ell) * sum_{k>=1} ell^{k(1-2s)}
      = 1 + (1-1/ell) x/(1-x)  |_{x = ell^{1-2s}}
      = (1 - ell^{-2s}) / (1 - ell^{1-2s}) ,
```

and `∏_ℓ L_ℓ = ζ(2s−1)/ζ(2s)` ✓. Restricting to `p | c` removes exactly the `k = 0` term of the
`p`-local factor:

```
Z_{oo,oo}(s) = D(s) * (L_p - 1)/L_p = D(s) * (1 - 1/L_p).
```

With `u := p^{-2s}`, `L_p = (1−u)/(1−pu)`, so `1 − 1/L_p = u(p−1)/(1−u)`
*(verified symbolically, §4.1)*, and multiplying numerator and denominator by `p^{2s}`:

```
1 - 1/L_p = (p-1)/(p^{2s} - 1).
```

Therefore, by (3.2),

```
   phi_{oo,oo}(s) = g(s) * (p-1)/(p^{2s} - 1),
   g(s) := sqrt(pi) Gamma(s-1/2) zeta(2s-1) / ( Gamma(s) zeta(2s) ).        (3.3)
```
∎ **This is exactly the entry M1D §5.1 cited.** It is now derived.

### 3.4 [PROVED] `φ_{∞0}` for `Γ₀(p)`

Here `σ_∞^{-1}Γ₀(p)σ_0 = Γ₀(p)W_p`. For `γ = [[a,b],[pc,d]] ∈ Γ₀(p)`:

```
gamma W_p = (1/sqrt p) [[a,b],[pc,d]] [[0,-1],[p,0]]
          = (1/sqrt p) [[ b p, -a ],[ d p, -p c ]]
          = [[ b sqrt p, -a/sqrt p ],[ d sqrt p, -c sqrt p ]].              (3.4)
```

- **Allowed moduli.** Lower-left entry `C = d√p`. From `ad − pbc = 1` we get `ad ≡ 1 (mod p)`, so
  `p ∤ d`. Taking `C > 0`: `C = n√p` with `n ≥ 1`, `p ∤ n`.
  *(These are disjoint from §3.3's moduli `pm`, since `√p` is irrational — relevant in §3.5.)*
- **Count.** Right multiplication by `T^k` sends the lower row `(C,D) ↦ (C, D + kC)`, so we count
  `D = −c√p` modulo `C = n√p`, i.e. `−c` modulo `n`. Existence of `a,b` with `ad − pbc = 1` for
  given `d = n` and `c` requires and is implied by `gcd(n, pc) = 1`, i.e. (given `p ∤ n`)
  `gcd(n,c) = 1`. So `S_{∞0}(0,0; n√p) = φ_E(n)`.

Hence

```
Z_{oo,0}(s) = sum_{n>=1, p not| n} phi_E(n) (n sqrt p)^{-2s}
            = p^{-s} sum_{p not| n} phi_E(n) n^{-2s}
            = p^{-s} D(s) / L_p
            = p^{-s} D(s) (1 - p^{1-2s})/(1 - p^{-2s})
            = D(s) (p^s - p^{1-s})/(p^{2s} - 1),
```

the last step by multiplying numerator and denominator by `p^{2s}`. Therefore

```
   phi_{oo,0}(s) = g(s) * (p^s - p^{1-s})/(p^{2s} - 1).                     (3.5)
```
∎ **Again exactly the entry M1D §5.1 cited.**

**[PROVED] `φ_{00} = φ_{∞∞}` and `φ_{0∞} = φ_{∞0}`.** `σ_0^{-1}Γ₀(p)σ_0 = W_p^{-1}Γ₀(p)W_p = Γ₀(p)`
by §1.1, which is the same set as in §3.3, so the moduli and counts are identical and
`φ_{00} = φ_{∞∞}`. Likewise `σ_0^{-1}Γ₀(p)σ_∞ = W_p^{-1}Γ₀(p) = Γ₀(p)W_p` (in `PSL₂`, §1.1), the
same set as in §3.4, so `φ_{0∞} = φ_{∞0}`. The symmetry of `Φ` is here a computation, not an
appeal to general theory. ∎

### 3.5 [PROVED] Independent derivation: apply (3.2) directly to `Γ₀⁺(p)`

This bypasses `Γ₀(p)` and its scattering matrix entirely — it is the derivation G5 literally asked
for.

`Γ = Γ₀⁺(p)`, one cusp, `σ_∞ = I`. So `σ_∞^{-1}Γσ_∞ = Γ = Γ₀(p) ⊔ Γ₀(p)W_p`. Its allowed moduli
and counts are the **disjoint union** of the two computations above:

- from `Γ₀(p)`: moduli `pm` (`m ≥ 1`), count `φ_E(pm)` — §3.3;
- from `Γ₀(p)W_p`: moduli `n√p` (`n ≥ 1`, `p ∤ n`), count `φ_E(n)` — §3.4.

The two modulus sets are disjoint (rational vs irrational multiples of `√p`), so no interference
and no recount. Feeding this single set into (3.2):

```
   phi^+(s) = g(s) [ (p-1)/(p^{2s}-1)  +  (p^s - p^{1-s})/(p^{2s}-1) ].     (3.6)
```

which is `φ_{∞∞} + φ_{∞0}`, agreeing with (2.6). ∎

Similarly, weighting the second block by `χ(W_p) = −1` (i.e. applying (3.2) to the χ-twisted
expansion of (Echi)) gives `φ^- = φ_{∞∞} − φ_{∞0}`.

**Reading.** §3.5 and §2.2 are logically independent routes to the same conclusion: §2.2 is a pure
coset-bijection argument at the level of the series, §3.5 is a moduli count at the level of the
Dirichlet series. They agree. Together they retire the "pattern-citation" character of M1D §5.1.

---

## 4. The closed form, and the match with M1D/M1E

### 4.1 [PROVED, symbolic] The algebra

Verified exactly in `sympy` (rational-function identities in `p^s`, no floating point):

```
A := (p-1)/(p^{2s}-1),   B := (p^s - p^{1-s})/(p^{2s}-1)

A + B - (1 + p^{1-s})/(1 + p^s)   ==  0        [sympy: 0]
A - B - (p^{1-s} - 1)/(p^s - 1)   ==  0        [sympy: 0]
1 - 1/L_p  ==  u(p-1)/(1-u),  u = p^{-2s}      [sympy: u*(1-p)/(u-1)]
```

By hand, with `X = p^s` (multiply numerator and denominator by `p^s`):

```
A + B :  numerator   (p-1)X + X^2 - p  =  (X - 1)(X + p)
         denominator X (X^2 - 1)       =  X (X - 1)(X + 1)
         ratio       (X + p) / (X(X+1))  =  (1 + p X^{-1}) / (1 + X)
                                          =  (1 + p^{1-s}) / (1 + p^s)

A - B :  numerator   (p-1)X - X^2 + p  =  -(X - p)(X + 1)
         denominator X (X - 1)(X + 1)
         ratio       -(X - p) / (X(X-1))  =  (p^{1-s} - 1)/(p^s - 1)
```

Hence

```
   phi^+_p(s) = g(s) * (1 + p^{1-s}) / (1 + p^s)          [ Gamma_0^+(p), trivial ]
   phi^-_p(s) = g(s) * (p^{1-s} - 1) / (p^s - 1)          [ chi-twisted ]          (PHI)
   phi^+_p * phi^-_p = det Phi_p(s)                        [ full Gamma_0(p) ]
```

### 4.2 [PROVED] Match with M1D and M1E

`(PHI)` is **character-for-character** the pair in `M1D_U4_CONSTRUCTION.md` §5.1 and
`M1E_PHI6_FAMILY_PROBE.md` §1. Specialising:

```
p = 2 (q=4):  phi_4(s)     = g(s)(1 + 2^{1-s})/(1 + 2^s)      == M1D  §5.1  OK
              phi_4^chi(s) = g(s)(2^{1-s} - 1)/(2^s - 1)       == M1D  §5.1  OK
p = 3 (q=6):  phi_6(s)     = g(s)(1 + 3^{1-s})/(1 + 3^s)      == M1E  §1    OK
              phi_6^chi(s) = g(s)(3^{1-s} - 1)/(3^s - 1)       == M1E  §1    OK
```

**No discrepancy of any kind was found.** The closed forms are correct and their derivation is now
independent of the "pattern-citation of the classical `Γ₀(p)` scattering matrix" that M1D flagged.

### 4.3 [PROVED] The functional equation, upgraded from numerics to a one-liner

Let `Λ(w) := π^{-w/2}Γ(w/2)ζ(w)`, so `Λ(w) = Λ(1−w)` (Riemann), `Λ` is holomorphic except for
simple poles at `w = 0, 1`, and its zeros are exactly the nontrivial zeros of `ζ`. Then

```
Lambda(2s-1)/Lambda(2s) = [ pi^{-(2s-1)/2} Gamma(s - 1/2) zeta(2s-1) ] / [ pi^{-s} Gamma(s) zeta(2s) ]
                        = sqrt(pi) * Gamma(s-1/2) zeta(2s-1) / ( Gamma(s) zeta(2s) )
                        = g(s).                                            (4.1)
```

Hence `g(1−s) = Λ(1−2s)/Λ(2−2s) = Λ(2s)/Λ(2s−1) = 1/g(s)`, i.e. **`g(s)g(1−s) = 1`, proved**.
The elementary factors invert too (verified symbolically: both `f(s)f(1−s) = 1`, §4.1's script),
so `φ^±(s)φ^±(1−s) = 1` — the required one-cusp scattering functional equation. M1D §5.1 check 1
and M1E §2.1–2.2 verified this numerically to `~1e−31`; it is now a proof.

**(4.1) also hands over the full divisor of `g` for free:**

```
zeros of g  : Lambda(2s-1) = 0  =>  s = (1 + rho)/2,   Re s = 3/4    (rho a nontrivial zeta zero)
              plus the pole of Lambda(2s) at s = 0  =>  simple zero of g at s = 0
poles of g  : Lambda(2s) = 0    =>  s = rho/2,         Re s = 1/4
              plus the pole of Lambda(2s-1) at s = 1  =>  simple pole of g at s = 1
              (the poles of Lambda(2s-1) at s=1/2 and of Lambda(2s) at s=1/2 cancel)
```

`Re s = 1/4` for the `s = ρ/2` poles — this is M1D §5.2's `ζ(2s)` divisor, now with the whole
divisor of `g` accounted for rather than only its denominator.

### 4.4 [PROVED] The residue at `s = 1`

`Res_{s=1} Λ(2s−1) = 1/2` (from `ζ(w) ∼ 1/(w−1)`, `w = 2s−1`, and `π^0Γ(0/2+1/2)`… more directly:
`Res_{s=1} g = [√πΓ(1/2)/Γ(1)]·(1/2)/ζ(2) = π·(1/2)/(π²/6) = 3/π`). The elementary factor at
`s = 1` is `(1+p^0)/(1+p) = 2/(1+p)`. Hence

```
Res_{s=1} phi^+_p = (3/pi) * 2/(p+1) = 6/(pi (p+1)) = 1 / vol(Gamma_0^+(p)\H),
```

using §1.5. This is the Selberg normalisation for a **one-cusp** group, and it is a genuine
consistency check on the whole chain: it would fail if §2.2's coset split, §1.5's volume, or
§1.4's no-scalar-transport claim were wrong. M1D §5.1 check 2 and M1E §2.3 verified it
numerically; here it is exact.

---

## 5. The resonance consequence

### 5.1 [CITED] The theorem being invoked, stated honestly

**What I need.** For a cofinite (finite-area, `κ ≥ 1` cusps) Fuchsian group `Γ`, define the
resonances as the poles of the meromorphically continued resolvent `(Δ − s(1−s))^{-1}`;
equivalently, off the discrete spectrum, as the poles of the scattering determinant
`det Φ(s)` in `Re s < 1/2`. The statement invoked is:

> **(R)** The divisor of the Selberg zeta function `Z_Γ(s)` contains, in `Re s < 1/2`, exactly the
> poles of `det Φ(s)` there, with matching multiplicity (in addition to the "trivial" divisor
> supported on the real axis at `s ∈ 1/2 − N` / `s ∈ −N`), and in `Re s ≥ 1/2` the zeros
> `s_j = 1/2 ± i r_j` coming from the discrete spectrum.

`[CITED]` Hejhal, *The Selberg Trace Formula for PSL(2,R)* vol. 2, Springer LNM 1001 (1983) —
the chapter developing `Z_Γ` for cofinite `Γ` with cusps, its functional equation and complete
divisor. Venkov, *Spectral Theory of Automorphic Functions*, Ch. 5–6. Müller,
*Spectral geometry and scattering theory for certain complete surfaces of finite volume*,
Invent. Math. **109** (1992) 265–305, for the resonance-theoretic formulation.

**`[GAP — G6, sharpened]`** I have **not** pinned (R) to a verified theorem number, and I will not
invent one. M1D §9 already flagged this as G6 ("must be pinned to a theorem number before (C4) can
be claimed"). M1F does not close it. What M1F does is reduce it: §5.2 shows that only a *shape*
property of the functional equation is needed for the points we care about.

### 5.2 [PROVED, modulo one structural import] Why (R) gives what we need, off the real axis

The Selberg zeta of a cofinite group satisfies a functional equation of the form

```
   Z(1-s)  =  Z(s) * phi(s) * Psi(s),        phi = det Phi,                (5.1)
```

where `Ψ(s)` is an **elementary factor**: `exp` of an entire function (from the identity
contribution, `exp(−|F|∫_0^{s−1/2} v tan(πv) dv)`) times a finite product of ratios of
`Γ`-functions and powers (from the parabolic and elliptic contributions).
**`[CITED — structural]`** the *shape* of `Ψ` (Hejhal, Venkov, as above). I am importing only the
shape, not any coefficient.

**[PROVED] Consequence off the real axis.** `Γ`-functions are nowhere zero and have poles only at
non-positive integers; `exp(entire)` is nowhere zero and nowhere infinite; powers `a^{cs}` likewise.
Hence, whatever the exact coefficients,

```
   Psi(s) is finite and non-zero for every s with Im s != 0.               (5.2)
```

Also `Z(s)` is holomorphic and non-vanishing in `Re s > 1` (convergent Euler product), and in the
strip `1/2 < Re s ≤ 1` its only zeros are at real `s_j ∈ (1/2, 1]` corresponding to exceptional
eigenvalues `λ_j = s_j(1−s_j) ∈ [0, 1/4)` — in particular **`Z` has no zeros at non-real points of
`Re s > 1/2`**, and its poles all lie in `Re s < 1/2` on the real axis.

Therefore, for `s₀` with `Im s₀ ≠ 0` and `Re s₀ < 1/2`:

```
   Z(1 - s_0) is finite and non-zero   (since Re(1-s_0) > 1/2, Im != 0)
   Psi(s_0)   is finite and non-zero   (5.2)
   =>  by (5.1),  ord_{s_0} Z  =  - ord_{s_0} phi  =  (order of the pole of phi at s_0).   (5.3)
```

**So: a pole of the scattering determinant at a non-real `s₀` with `Re s₀ < 1/2` is a zero of
`Z_Γ` of exactly the same order.** That is (R) restricted to the half-plane and to `Im s ≠ 0` —
and every point M1D/M1E cares about is non-real. `[GAP]` remaining in this sub-argument: the
*existence* of (5.1) in the stated shape. That is a single, standard, citable fact; it is
obligation G6 and I am not asserting a number for it.

### 5.3 [PROVED, given §5.2] The two divisors of `φ^±`

**(a) The `ζ(2s)` / Riemann divisor.** By §4.3, `φ^+` and `φ^-` both contain `g(s)`, whose poles
include `s = ρ/2` for every nontrivial zero `ρ` of `ζ`, at `Re s = 1/4 < 1/2`, with `Im ≠ 0`. The
elementary factors `(1+p^{1−s})/(1+p^s)` and `(p^{1−s}−1)/(p^s−1)` are finite and non-zero on
`Re s = 1/4` (their zeros/poles all lie on `Re s ∈ {0,1}`, see (b)), so they cannot cancel the pole.
By (5.3), **`Z_{Γ₀⁺(p)}` vanishes at `s = ρ/2` to the order of `ρ`, in both the trivial and the χ
sector.** This is M1D §5.2's claim; the "both sectors" prediction M1D confirmed numerically
(M1D §6.1, `det(1−N_{s,+})` vanishing to order ≥ 2) is here a consequence of `g` being a common
factor of `φ^+` and `φ^-`, which §3 derives rather than assumes.

**(b) The new elementary divisor.** Poles of the elementary factors:

```
trivial sector:   1 + p^s = 0   <=>  p^s = -1  <=>  s = i (2k+1) pi / log p,   k in Z
chi sector:       p^s - 1 = 0   <=>  p^s = +1  <=>  s = i (2k)   pi / log p,   k in Z
```

both on `Re s = 0 < 1/2`. **These are genuine poles of `φ^±`, not removable**, and the check is
where §4.3's full divisor of `g` earns its keep:

- *`g` is finite and non-zero on `Re s = 0`, except at `s = 0`.* By (4.1), `g = Λ(2s−1)/Λ(2s)`.
  On `Re s = 0` we have `Re(2s) = 0` and `Re(2s−1) = −1`, both **outside** the open critical strip,
  where `Λ` has no zeros (its zeros are exactly the nontrivial `ζ` zeros, all in `0 < Re w < 1`).
  `Λ`'s only poles are at `w = 0, 1`, i.e. at `s ∈ {0, 1/2}` and `s ∈ {1/2, 1}` — of these only
  `s = 0` lies on `Re s = 0`. So `g` is finite and non-zero on `Re s = 0 ∖ {0}`.
- *Numerators do not vanish.* At `p^s = −1`: `1 + p^{1−s} = 1 + p·p^{−s} = 1 − p ≠ 0` (`p ≥ 2`).
  At `p^s = +1`: `p^{1−s} − 1 = p − 1 ≠ 0`.

Hence:

```
   trivial sector:  simple poles of phi^+ at  s = i(2k+1)pi/log p,  all k in Z.
   chi sector:      simple poles of phi^- at  s = 2 i k pi / log p, all k in Z, k != 0.
```

**[PROVED] The `k = 0` exclusion in the χ sector is forced, not stipulated.** At `s = 0`,
`Λ(2s)` has a simple pole (`Λ(w) ∼ −1/w` near `w = 0`, since `Γ(w/2) ∼ 2/w` and `ζ(0) = −1/2`), so
by (4.1) `g` has a **simple zero** at `s = 0`; and `(p^{1−s}−1)/(p^s−1)` has a simple pole there.
They cancel exactly, and `φ^-` is finite and non-zero at `s = 0`. M1D §5.2 and M1E §1 both wrote
"`k ≠ 0`" without saying why; this is why.

By §5.2/(5.3) these are resonances, hence zeros of the corresponding Selberg zeta — the trivial
sector's in `Z_{Γ₀⁺(p)}`, the χ sector's in `Z_{Γ₀⁺(p)}(·, χ)`, and by the Venkov–Zograf
factorisation `Z_{Γ₀(p)} = Z_{Γ₀⁺(p)} · Z_{Γ₀⁺(p)}(·,χ)` both in `Z_{Γ₀(p)}`
[`CITED`, character factorisation of the Selberg zeta for a normal subgroup of index 2; M1D §3.4
already invokes it].

Specialising: `p = 2` gives `π/log 2 = 4.5323601…`, `p = 3` gives `π/log 3 = 2.8596009…` — the
loci M1D §6.2 and M1E §4.2 confirmed 4/4 each, with two-way sector discrimination. **The
derivation predicts precisely those numbers and precisely that sector split.**

### 5.4 [GAP] What §5 does *not* establish

- **G6 itself**: the exact statement and citation of (5.1)/(R). §5.2 shows the shape suffices;
  it does not supply the reference.
- **The MMS transport (G7)**: nothing here connects `ord_{s₀} Z_{S,q}` to `ord_{s₀} D_q^+`
  *sector by sector*. The identification of which MMS `(P)`-sector carries which Selberg divisor
  remains numerical (M1D §6.1, M1E §4.1). §3.1's observation that the cusp-side `V` and the
  operator-side `V` are the same `Z/2` character basis is **suggestive, not a proof** — the two
  `Z/2`s are the same group acting on different objects, and no intertwiner is claimed.
- **Multiplicity / global meromorphy (G9)**: untouched.
- **Exceptional eigenvalues**: §5.2 used "no non-real zeros of `Z` in `Re s > 1/2`", which is
  standard (exceptional `s_j` are real). It did **not** need a Selberg-`1/4` input, because all
  points of interest are non-real. Recorded so that a later reader does not think a spectral gap
  for `Γ₀(2)`/`Γ₀(3)` is being assumed. It is not.

---

## 6. Obligations ledger

Conservative accounting against `M1D_U4_CONSTRUCTION.md` §9. "Closed" is used only where the
remaining dependency is a single standard textbook fact whose *content* I have stated explicitly.

| # | Obligation (M1D §9) | Status after M1F | Detail |
|---|---|---|---|
| **G5** | `φ⁺_p = g(s)(1+p^{1−s})/(1+p^s)` **derived from the Eisenstein constant term**, not by symmetrising a cited `Γ₀(p)` matrix | **CLOSED, modulo one CITED constant-term formula** | §2.2 proves `E^+ = E_∞+E_0` by coset bijection (no analysis); §3.3–3.4 derive both `Γ₀(p)` entries from the allowed-moduli formula (3.2) + an Euler-product restriction lemma; §3.5 re-derives `φ⁺` **directly for `Γ₀⁺(p)`**, never mentioning `Γ₀(p)`'s scattering matrix; §4.1 closes the algebra symbolically. The single import is (3.2). Its *number* is unpinned (§3.2) — see N1. |
| **G6** | resonances = poles of `φ` in the `Z_S` divisor, with multiplicity | **REDUCED, still open** | §5.2 derives the implication `pole of φ at non-real s₀, Re s₀<1/2 ⇒ zero of Z of the same order` from (5.1) using only the *shape* of `Ψ` (Γ-ratios × exp(entire) ⇒ zero-free and pole-free off the real axis). The remaining need is a pinned citation for (5.1). Multiplicity now comes for free from (5.3) once (5.1) is cited. |
| **G7** | MMS Thm 6.4 → Selberg divisor, **sector by sector** | **UNCHANGED** | §3.1 notes the cusp-side and operator-side `Z/2` bases coincide; explicitly flagged as suggestive only (§5.4). |
| **G8** | `det(1−N_{s,+})` ↔ `Z_{Γ₀(p)}` divisor | **UNCHANGED** | Needs G6 + G7. |
| **G9** | global meromorphy / multiplicity of `R_q(s) = D_q^+(s)/ζ(2s)` | **UNCHANGED** | Untouched. |
| G1, G2, G4 | (PROVED in M1D) | unchanged | — |
| G3, G10, G11 | (ARISTOTLE-ABLE / compute) | unchanged | — |
| G12 | q=6 analogue | closed by M1E | M1F additionally shows the `p`-generic derivation really is `p`-generic — nothing in §§1–4 specialises `p` until §4.2. |

**New obligations opened by M1F:**

| # | Obligation | Route |
|---|---|---|
| **N1** | Pin (3.2) — the allowed-moduli constant-term formula — to a verified theorem/equation number (Iwaniec *Spectral Methods* 2nd ed., ch. 3; or Hejhal LNM 1001 vol. 2 ch. 11). Do not print a number in any paper until a human has opened the book. | **human / library check.** Content is not in doubt; the label is. |
| **N2** | Pin (5.1) — the Selberg-zeta functional equation for cofinite `Γ` with cusps, including the shape of `Ψ` — to a verified theorem number. This *is* G6's residue. | **human / library check**, or Müller Invent. Math. 109 (1992). |
| **N3** | Literature check: is the `Γ₀⁺(N)` (Fricke-group) scattering determinant already published? If yes, `(PHI)` becomes `CITED` and G5 becomes vacuous — and the "new resonances" of §5.3(b) may not be new. | **prior-art scout.** This is a novelty risk, not a correctness risk. **Must be settled before any novelty claim is made about §5.3(b).** Leads below (§6.1) — **all unread**. |
| **N4** | Generators: `⟨T, [[1,0],[p,1]]⟩ = Γ₀(p)` used in §1.4 for `p = 2,3` only. Trivial but stated as CITED. | ARISTOTLE-ABLE / textbook. |

### 6.1 [GAP] Citation-pinning attempt, and its honest outcome

A web scout was run against N1/N2/N3 and the Takeuchi pin during this session. **It resolved
nothing.** Reported outcome, recorded verbatim in substance so a later reader does not repeat it:

- Iwaniec GSM 53 and Hejhal LNM 1001 were confirmed to **exist** with the stated bibliographic
  data; their contents were **not reachable** (PDFs binary/compressed), so no theorem or equation
  number was verified. N1 and N2 stand open exactly as written.
- Takeuchi, JMSJ **29** (1977) 91–106, confirmed as a publication (Project Euclid), but the scan is
  image-only and the theorem number for `G_4 ≅ Γ₀⁺(2)` / `G_6 ≅ Γ₀⁺(3)` was **not** verified.
  §1.4 does not depend on it — §1.4 proves the identification directly from (1.3) — so this is a
  citation-hygiene item, not a load-bearing gap.
- The general shape `Z(1−s) = ψ(s)φ(s)Z(s)` was found asserted in multiple secondary sources, but
  no primary statement of `ψ` was read. This is precisely the structural import §5.2 relies on; it
  remains `CITED`-unpinned.

**Unread leads for N3** (surfaced by the scout, none opened, none of them confirmed to contain
`(PHI)` — listing them so the next pass starts here rather than from a blank search):

```
Huxley, "Scattering matrices for congruence subgroups", in Modular Forms (ed. Rankin, 1984)
arXiv:math/0702030   "Analogues of the Artin factorization formula for the automorphic
                      scattering matrix"   <- most likely to contain the induced/character
                                              decomposition used implicitly in section 2
arXiv:2207.05325     Eisenstein series / Fricke groups
arXiv:2211.15369     Eisenstein series / Fricke groups
```

**Standing instruction.** Until N3 is settled by someone who has actually read
`arXiv:math/0702030` and Huxley 1984, **no novelty claim may be attached to `(PHI)` or to the
extra resonances of §5.3(b)**. The derivation's correctness does not depend on N3; only its
originality does, and the base rate for "the Fricke-group scattering determinant is already in the
literature" is high.

**Aristotle-able from this note** (self-contained, finite or near-finite):

- **A-1** §1.1: `W_pΓ₀(p)W_p^{-1} = Γ₀(p)`, i.e. `[[a,b],[pc,d]] ↦ [[d,−c],[−pb,a]]` is a bijection
  of `Γ₀(p)`. Pure 2×2 integer algebra. *(Generalises M1D's G2, which was `p = 2` only.)*
- **A-2** §1.2–1.3: `W_p(∞)=0`, `W_p(0)=∞`, and `Γ₀⁺(p)_∞ = ⟨T⟩`. Finite.
- **A-3** §2.2: the coset bijection `Γ_∞\Γ = (Γ'_∞\Γ') ⊔ (Γ'_∞\Γ'W_p)` and the re-indexing
  `Γ'_0\Γ' → Γ'_∞\Γ'W_p`. Group theory, formalizable; the analytic content is nil.
- **A-4** §3.3: the Euler-product restriction lemma
  `Σ_{p|c} φ_E(c)c^{-2s} = (ζ(2s−1)/ζ(2s))·(p−1)/(p^{2s}−1)`, stated as a formal identity of
  Euler products / a Dirichlet-series identity in a convergent half-plane. **Highest-value item.**
- **A-5** §4.1: the rational-function identities `A+B = (1+p^{1−s})/(1+p^s)`,
  `A−B = (p^{1−s}−1)/(p^s−1)` in the variable `X = p^s`. Trivially formalizable; already
  sympy-verified.
- **A-6** §4.3: `g(s) = Λ(2s−1)/Λ(2s)` and `g(s)g(1−s) = 1` from `Λ(w) = Λ(1−w)`.
- **A-7** §5.3(b): `g` is finite and non-zero on `Re s = 0 ∖ {0}` and has a simple zero at `s = 0`
  (given: `Λ` entire off `{0,1}`, zeros only in the critical strip, `Λ(w) ∼ −1/w` at `0`).

**Not Aristotle-able:** anything in §5.1–5.2 requiring (5.1); the whole of G7–G9.

---

## 7. What M1F claims and does not claim

**Claims.**
(i) The closed forms `(PHI)` of M1D §5.1 / M1E §1 are correct, and are now derived from the
Eisenstein constant term of `Γ₀⁺(p)` rather than pattern-matched to a cited `Γ₀(p)` matrix — by
two logically independent routes (§2.2 coset identity; §3.5 direct moduli count).
(ii) `Γ₀⁺(p)` has one cusp, and the conjugation `G_q → Γ₀⁺(p)` transports the scattering function
with no scalar factor (§1.4), corroborated by two volume computations (§1.5).
(iii) The `1×1`/χ split is exactly the eigen-decomposition of the 2×2 `Φ(s)` on the `W_p`-symmetric
and antisymmetric vectors, in the same character basis `V` M1D used on the operator side (§3.1).
(iv) The functional equation and the `s=1` residue, previously numerical checks, are now proofs
(§4.3, §4.4), and the full divisor of `g` is exhibited.
(v) The predicted extra resonances at `p^s = ∓1` follow from `(PHI)`, are genuine (non-removable)
poles, and the `k = 0` exclusion in the χ sector is forced by a zero/pole cancellation (§5.3(b)).

**Does not claim.** (C4) is not proved. G6–G9 are not closed. The MMS sector assignment remains
numerical. No theorem number is asserted for (3.2) or (5.1) — both are flagged. No novelty claim is
made for §5.3(b) until N3 is settled. Nothing in this note is a numerical result.

**No refutation was found.** Had `E^+` failed to equal `E_∞ + E_0`, or had the moduli count in §3.5
disagreed with §3.3+§3.4, or had the residue at `s = 1` missed `1/vol`, this note would have said
so and M1D §5 would have been retracted. None of that happened; the three independent consistency
checks (functional equation, residue/volume, two-route agreement) all pass exactly.

---

## References

**[CITED]** Iwaniec, *Spectral Methods of Automorphic Forms*, 2nd ed., AMS GSM 53 — Ch. 3,
Eisenstein series and their Fourier expansion; the source of (3.2). **Equation number unverified
in this session (N1).**

**[CITED]** Hejhal, *The Selberg Trace Formula for `PSL(2,R)`* vol. 2, Springer LNM 1001 (1983) —
Ch. 11 for scattering matrices of congruence groups; the chapter on `Z_Γ` for cofinite `Γ` for
(5.1)/(R). **Theorem numbers unverified (N1, N2).**

**[CITED]** Venkov, *Spectral Theory of Automorphic Functions* — Selberg zeta for cofinite groups;
the Venkov–Zograf character factorisation `Z_{Γ'} = Z_Γ · Z_Γ(·,χ)` for `Γ' ◁ Γ` of index 2.

**[CITED]** Müller, *Spectral geometry and scattering theory for certain complete surfaces of
finite volume*, Invent. Math. **109** (1992) 265–305 — resonance-theoretic formulation of (R).

**[CITED]** Takeuchi, *Arithmetic triangle groups*, J. Math. Soc. Japan **29** (1977) 91–106 —
`G_4 ≅ Γ₀⁺(2)`, `G_6 ≅ Γ₀⁺(3)`. **Theorem number unverified (§6.1).** §1.4 does not rely on it:
the identification is proved there from the explicit conjugator (1.3).

**[UNREAD LEADS — prior-art risk, obligation N3]** Huxley, *Scattering matrices for congruence
subgroups*, in *Modular Forms* (ed. Rankin, 1984); arXiv:math/0702030; arXiv:2207.05325;
arXiv:2211.15369. None opened; see §6.1.

**[CITED]** Mayer, Mühlenbruch, Strömberg, *The transfer operator for the Hecke triangle groups*,
DCDS **32** (2012) 2453–2484, arXiv:0912.2236 — Thm 6.4, the object M1D's `D_q^±` live in.
Not used in the derivation above, only in the ledger's G7.

**Parents in this repo:** `lane_g/M1D_U4_CONSTRUCTION.md` §5, §9;
`lane_g/M1E_PHI6_FAMILY_PROBE.md` §1, §6; `lane_g/M1B_Q4_INTERTWINER.md` (the `D₂` conjugation,
generalised here to `D = diag(p^{1/4},p^{−1/4})` in §1.4).

**Symbolic check (scratchpad, not committed):** `sympy` verification of §4.1's three identities and
of `f^±(s)f^±(1−s) = 1`; all returned exact `0` / `1`. No floating-point arithmetic was used
anywhere in this note.
