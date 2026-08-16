# LAW anchor (T1) — the scattering matrix of the theta group Γ_θ = ⟨S, T₂⟩

**Date:** 2026-08-15
**Ticket:** `plans/wayfinder/rh-goals/tickets/law-tail-anchor-probe.md`, Leg 1.
**Parents:** `lane_g/LAW_TAIL_SCOPING.md` §2.2 (the anchor claim), `lane_g/M1F_EISENSTEIN_DERIVATION.md`
(the allowed-moduli constant-term method reproduced here for a **two-cusp** group).
**Status convention:** identical to M1F. Every substantive claim is tagged exactly
`PROVED` / `CITATION` / `HEURISTIC` / `GAP`.
`PROVED` = derived here in closed form, or verified in exact/symbolic/brute-force arithmetic.
`CITATION` = imported, with the import named. `HEURISTIC` = float evidence. `GAP` = not justified.

---

## 0. Verdict up front

**(T1) HOLDS, with one honest downgrade of its strategic value.**

- The two-cusp scattering matrix of `Γ_θ` is derived here **from scratch by the M1F
  moduli-count method, directly in `Γ_θ`** (no conjugation needed in the end):

```
   Phi_theta(s) = [[ A(s), B(s) ],
                   [ B(s), A(s) ]]        rows/cols ordered (cusp oo, cusp 1)

   A(s) = phi_{oo,oo} = phi_{1,1} = g(s) / (4^s - 1)
   B(s) = phi_{oo,1}  = phi_{1,oo} = g(s) (2^s - 2^{1-s}) / (4^s - 1)

   g(s) = sqrt(pi) Gamma(s-1/2) zeta(2s-1) / ( Gamma(s) zeta(2s) )  =  Lambda(2s-1)/Lambda(2s)

   det Phi_theta(s) = A^2 - B^2 = g(s)^2 * (4 - 4^s) / ( 4^s (4^s - 1) )          (DET)
```

- **The `s = ρ/2` poles are real and cannot cancel.** `PROVED`, §4: the elementary factor
  `E(s) = (4 − 4^s)/(4^s(4^s − 1))` has **all** its zeros on `Re s = 1` and **all** its poles on
  `Re s = 0`; on `Re s = 1/4` it is finite and non-zero. `g(s)²` has a **double** pole at every
  `s = ρ/2`. Nothing in `(DET)` can kill it. **The anchor's load-bearing point survives an
  adversarial reading.**
- Unconditionally (de la Vallée Poussin, `Re ρ < 1`) every such pole has `Re < 1/2` and `Im ≠ 0`;
  for the named first zero `ρ₁` (`Re ρ₁ = 1/2`, verified) `s_∞ = ρ₁/2 = 0.25 + 7.0673625708…i`,
  margin `η = 1/8`. **`Γ_θ` has an off-line resonance, no RH assumed.**
- Numeric confirmation (§5, `HEURISTIC` by label, but it confirms an exact algebraic statement):
  `Φ_θ(s)Φ_θ(1−s) = I` to `< 5e−40`; `Res_{s=1}` of every entry `= 1/π = 1/vol` to 9 digits;
  `|det Φ_θ|` grows exactly like `r^{−2}` on circles of radius `r` about `s_∞`, with
  `(s − s_∞)² det → −0.14943 − 0.39398 i` (finite, non-zero) — a clean order-2 pole,
  absent at three control points.

**The downgrade, reported loudly (§6).** `Γ_θ = ⟨S, T₂⟩` is `SL(2,Z)`-conjugate to `Γ₀(2)`, so
`det Φ_θ = φ⁺_2 · φ⁻_2`, i.e. **exactly the object M1F already derived for `G_4 = Γ₀⁺(2)`**. The
`ρ/2` resonances therefore are *not* a feature of the `λ = 2` endpoint: the same `g(s)` factor,
with the same `Re = 1/4` poles, is present at `λ = √2 (q=4)` and `λ = √3 (q=6)` as well. The
anchor is **valid** but it is **not a discriminator** — it certifies that the endpoint has an
off-line resonance, and nothing more. Combined with the repo's own scan data (`q = 7, 8` pins at
`Re ≈ 0.43–0.48`, nothing near `Re = 0.25` at `Im ≈ 7.07`), this sharpens rather than weakens the
case for running Probe D1: (T1) is now settled, so D1 tests the *only* remaining question.

---

## 1. Cusp inventory

### 1.1 [PROVED] `Γ_θ = ⟨S, T₂⟩` and its congruence description

`S = [[0,−1],[1,0]]`, `T₂ = T² = [[1,2],[0,1]]`, all in `PSL(2,R)`.

`[CITATION, classical]` The **theta group** is
`Γ_θ = { γ ∈ SL(2,Z) : γ ≡ I or [[0,1],[1,0]] (mod 2) }`, i.e. (`b, c` even) or (`a, d` even),
and `Γ_θ = ⟨S, T²⟩`. (Standard; the name is from the invariance group of `θ(z) = Σ e^{πin²z}`.)

**Independent cross-check performed here, so the identification is not citation-only.**
`PROVED`:
- `S ≡ [[0,1],[1,0]]`, `T² ≡ I (mod 2)`, so `⟨S,T²⟩ ⊆ Γ_θ`.
- Reduction mod 2 gives `PSL(2,Z) ↠ SL(2,Z/2) ≅ S₃` (order 6). `Γ_θ` is the full preimage of the
  order-2 subgroup `{I, [[0,1],[1,0]]}`, hence **index 3** in `PSL(2,Z)`.
- `vol(Γ_θ\H) = 3 · π/3 = π`. Independently, `⟨S, T_2⟩` is the `(2,∞,∞)` triangle group
  (`λ = 2 = λ_∞` in the Hecke family), whose area is `2·(π − π/2 − 0 − 0) = π` — the M1F §1.5
  formula `π(1 − 2/q)` at `q = ∞`. **MATCH**, and it also confirms `⟨S,T²⟩` is all of `Γ_θ`
  (a proper subgroup would have area a positive integer multiple of `π`).

This closes the `LAW_TAIL_SCOPING.md` §1.1 `[CITATION — to be pinned]` at the level of *content*
(the identification is now proved from the mod-2 index count plus the area match). `GAP` remains
only for the bibliographic label: see N1 in §7.

### 1.2 [PROVED] Two cusps: `∞` (width 2) and `1` (width 1)

The ticket asked for this to be verified first. It is verified, and the widths are as stated.

- **Cusp count.** `Γ_θ` has index 3 and the cusps are its orbits on `P¹(Q)`. Coset
  representatives of `Γ_θ\PSL(2,Z)` may be taken as `{I, T, T S}`-type; concretely the three
  `Γ_θ`-orbits of `PSL(2,Z)/Γ_θ` collapse to **two** cusp orbits because the total width equals
  the index. Directly: `0 = S(∞)` with `S ∈ Γ_θ`, so `0 ∼ ∞`. And `1 ≁ ∞`: if `γ(∞) = 1` for
  `γ = [[a,b],[c,d]] ∈ Γ_θ` then `a/c = 1`, so `a = c` (coprime ⇒ `a = c = ±1`), which is odd–odd
  — impossible, since `Γ_θ` forces `a, c` of **opposite** parity (either `a` odd & `c` even, or
  `a` even & `c` odd). So `{∞, 1}` are inequivalent. **Exactly two cusps** then follows from the
  width sum below. ∎
- **Width at `∞`.** `Γ_{θ,∞} = { ±[[1,n],[0,1]] } ∩ Γ_θ`. `[[1,n],[0,1]]` has `a = d = 1` odd, so
  the mod-2 condition forces `b = n` **even**. Hence `Γ_{θ,∞} = ⟨T²⟩`: **width 2**.
  Scaling matrix `σ_∞ = diag(√2, 1/√2)` (`σ_∞^{-1}T²σ_∞ = T` ✓).
- **Width at `1`.** Put `V = [[1,0],[1,1]] ∈ SL(2,Z)`, `V(∞) = 1`. Then
  `V T V^{-1} = [[0,1],[−1,2]]`, which is `≡ [[0,1],[1,0]] (mod 2)`, hence **in `Γ_θ`**, and is
  parabolic (`tr = 2`) fixing `1`. So `Γ_{θ,1} ⊇ ⟨VTV^{-1}⟩`, **width 1**, and
  `σ_1 = V` is a valid scaling matrix (`σ_1^{-1}Γ_{θ,1}σ_1 = ⟨T⟩`).
- **Consistency.** `Σ widths = 2 + 1 = 3 = [PSL(2,Z) : Γ_θ]` ✓ — which simultaneously proves
  the widths are exactly 2 and 1 (no larger stabiliser) **and** that there are no further cusps.
  ∎ `PROVED`.

### 1.3 [PROVED] The conjugation to `Γ₀(2)` — stated, then *not used*

The ticket allows a conjugation shortcut if the normalisations are transported carefully. The
correct target is **`Γ₀(2)`, not `Γ₀(4)`**:

```
   Gamma_theta = V Gamma_0(2) V^{-1},     V = [[1,0],[1,1]] in SL(2,Z).           (1.3)
```

*Proof.* Mod 2, `Γ₀(2)` is the preimage of `{I, [[1,1],[0,1]]}` and `Γ_θ` of
`{I, [[0,1],[1,0]]}` — two order-2 subgroups of `S₃`, hence conjugate. Explicitly
`V [[1,1],[0,1]] V^{-1} = [[0,1],[−1,2]] ≡ [[0,1],[1,0]] (mod 2)`. ∎

Cusp transport: `Γ₀(2)` has cusps `∞` (width 1) and `0` (width 2); `V(∞) = 1`, `V(0) = 0 ∼ ∞`.
So `∞_θ ↔ 0_{Γ₀(2)}` (width 2 ↔ width 2 ✓) and `1_θ ↔ ∞_{Γ₀(2)}` (width 1 ↔ width 1 ✓).

**`GAP` retired from the scoping note.** `LAW_TAIL_SCOPING.md` §2.2 wrote "`Γ_θ` … (or of
`Γ₀(4)`, to which `Γ_θ` is conjugate)". **That is false as stated**: `[PSL(2,Z) : Γ₀(4)] = 6 ≠ 3`,
so `Γ_θ` is *not* conjugate to `Γ₀(4)` in `PSL(2,R)` by any conjugation preserving the index.
(The folklore statement people misremember is that `Γ_θ` is conjugate **in `PSL(2,R)`, by
`diag(√2, 1/√2)`, to a group commensurable with `Γ₀(4)`**, or the `θ`-vs-`Γ₀(4)` modular-forms
isomorphism; neither is a `PSL(2,Z)`-conjugacy of `Γ_θ` with `Γ₀(4)`.) **Correct the lane text.**

**How (1.3) is used.** §3 runs the moduli count **directly in `Γ_θ`** with `σ_∞`, `σ_1` above —
exactly as M1F §3.5 ran its second derivation directly in `Γ₀⁺(p)` — and verifies the resulting
moduli sets and counts exhaustively (§5.3). For the *proof* of those counts I transport via (1.3)
to M1F §3.3–3.4, rather than re-proving the parity bookkeeping synthetically; the direct
enumeration is then an independent confirmation that the transport was done with the right cusp
pairing and scaling matrices — which is precisely the place a two-cusp transport can silently go
wrong. Both roles are labelled at each use.

---

## 2. The imported ingredient (the only one)

`[CITATION]` M1F (3.2), verbatim — for a cofinite `Γ` with cusps `a, b` and scaling matrices
`σ_a, σ_b`:

```
   phi_{ab}(s) = sqrt(pi) * Gamma(s-1/2)/Gamma(s) * sum_{c in C_ab} c^{-2s} * S_{ab}(0,0;c)
   C_ab = { c > 0 : [[*,*],[c,*]] in sigma_a^{-1} Gamma sigma_b }
   S_{ab}(0,0;c) = # { d mod c : [[*,*],[c,d]] in sigma_a^{-1} Gamma sigma_b }.
```

Iwaniec, *Spectral Methods of Automorphic Forms* 2nd ed. (AMS GSM 53) ch. 3; Hejhal LNM 1001
vol. 2 ch. 11. **Theorem/equation number unverified in this session** — this is M1F's obligation
**N1**, inherited unchanged. The *content* is textbook; the *label* is unpinned.

Also inherited: `D(s) := Σ_{c≥1} φ_E(c) c^{-2s} = ζ(2s−1)/ζ(2s)`, with local factor
`L_ℓ = (1 − ℓ^{-2s})/(1 − ℓ^{1−2s})` (M1F §3.3, `PROVED`).

Everything below is counting.

---

## 3. Derivation of the entries

### 3.1 [PROVED] `φ_{∞∞}` — the width-2 cusp

`σ_∞ = diag(√2, 1/√2)`, so `σ_∞^{-1} γ σ_∞ = [[a, b/2],[2c, d]]` for `γ = [[a,b],[c,d]] ∈ Γ_θ`.

- **Allowed moduli.** `C = 2c > 0`. Both parity branches of `Γ_θ` occur (`c` even gives
  `C ≡ 0 mod 4`, `c` odd gives `C ≡ 2 mod 4`), so `C` ranges over **all even positive integers**.
- **Count.** `S_{∞∞}(0,0; 2c) = φ_E(2c)`.
  *Proof route, stated honestly.* The clean proof is by transport, not by a direct parity
  argument: `σ_∞` scales the cusp `∞_θ`, which corresponds under (1.3) to the cusp `0` of
  `Γ₀(2)` (§1.3; widths 2 ↔ 2), and M1F §3.4's last paragraph proves `φ_{00} = φ_{∞∞}` for
  `Γ₀(p)`, whose moduli are `2m` with count `φ_E(2m)` (M1F §3.3, `PROVED`). So (3.1) is
  **`PROVED` via §3.2 + §3.4.** The direct count in `Γ_θ` below is **corroboration**; I do not
  claim a synthetic parity proof of it here — writing one out is Aristotle-able item **T-4(a)**
  (§7.2).
- **Verified by exhaustive enumeration** (§5.3): over all `γ ∈ Γ_θ` with entries `≤ 90`, the
  observed pairs are `C = 2, 4, 6, 8, 10, 12, 14, 16, 18, 20` with counts
  `1, 2, 2, 4, 4, 4, 6, 8, 6, 8` `= φ_E(C)` for every `C` — and the truncated Dirichlet series
  agrees with `Σ_{2|C} φ_E(C) C^{-2s}` to **all 12 printed digits**.

Hence, by M1F's Euler-product restriction lemma with `p = 2`,

```
   Z_{oo,oo}(s) = sum_{2|C} phi_E(C) C^{-2s} = D(s) (1 - 1/L_2) = D(s)/(4^s - 1),

   phi_{oo,oo}(s) = g(s) / (4^s - 1).                                            (3.1)
```

### 3.2 [PROVED] `φ_{11}` — the width-1 cusp

`σ_1 = V`, so `σ_1^{-1}Γ_θσ_1 = V^{-1}Γ_θ V = Γ₀(2)` by (1.3). Its moduli are `c ≡ 0 (mod 2)`
with count `φ_E(c)` — **the identical set and counts as §3.1**. Brute force (§5.3) confirms the
two lists are byte-identical. Hence

```
   phi_{1,1}(s) = phi_{oo,oo}(s) = g(s)/(4^s - 1).                               (3.2)
```

(The equality of the two diagonal entries is *not* automatic for a two-cusp group with unequal
widths; here it happens, and the width factors are absorbed into the scaling matrices.)

### 3.3 [PROVED] `φ_{∞1} = φ_{1∞}` — the off-diagonal entry

`σ_1^{-1}γσ_∞ = V^{-1}γ · diag(√2, 1/√2)`, whose lower row is `√2·(c', d')` where `(c', d')` is
the lower row of `V^{-1}γ`. The common `√2` scales `c` and `d` together, so residue counts are
computed on `(c', d')` and the modulus entering (3.2)-style sums is `c'√2`.

- **Allowed moduli.** `c'` runs over the **odd** positive integers.
- **Count.** `S(0,0; c'√2) = φ_E(c')`.
- **`PROVED` by brute-force enumeration** (§5.3): observed `(c', count)` =
  `(1,1) (3,2) (5,4) (7,6) (9,6) (11,10) (13,12) (15,8) (17,16) (19,18)` `= (n, φ_E(n))`,
  `n` odd; and the truncated series matches `Σ_{n odd} φ_E(n) n^{-2s}` to **all 12 printed
  digits**. The mirror block `σ_∞^{-1}γσ_1` gives the identical list, so `Φ_θ` is symmetric —
  a computation here, not an appeal to general theory.

Therefore

```
   Z_{oo,1}(s) = sum_{n odd} phi_E(n) (n sqrt2)^{-2s} = 2^{-s} D(s)/L_2
               = D(s) (2^s - 2^{1-s})/(4^s - 1),

   phi_{oo,1}(s) = g(s) (2^s - 2^{1-s})/(4^s - 1).                               (3.3)
```

### 3.4 [PROVED] Cross-check against M1F via (1.3)

By (1.3) `Φ_θ` is the `Γ₀(2)` scattering matrix with the two cusps relabelled. M1F §3.3–3.4 at
`p = 2` give `φ_{∞∞} = g/(4^s−1)`, `φ_{∞0} = g(2^s − 2^{1−s})/(4^s−1)`. **Identical to
(3.1)–(3.3).** Two logically independent routes (direct moduli count in `Γ_θ`; conjugation to
`Γ₀(2)` + M1F) agree entry for entry.

### 3.5 [PROVED, symbolic] The determinant

With `X = 2^s` (`4^s = X²`, `2^{1−s} = 2/X`), `sympy`, exact:

```
   det Phi_theta = A^2 - B^2 = -(X-2)(X+2) / ( X^2 (X-1)(X+1) )
                 = g(s)^2 * (4 - 4^s) / ( 4^s (4^s - 1) ).                       (DET)
```

Two exact identities returned `0` / `1` by sympy:

```
   det - g^2 (4-4^s)/(4^s(4^s-1))        == 0
   phi^+_2(s) * phi^-_2(s) - det          == 0     (M1F (PHI) at p=2: the Fricke/chi split)
   E(s) E(1-s)                            == 1     (E := the elementary factor of (DET))
```

The middle identity is a real structural check: `det Φ_{Γ₀(2)} = φ⁺·φ⁻` is M1F (2.6), and it is
recovered here from a derivation that never mentioned `W_2`, `Γ₀⁺(2)`, or the character `χ`.

---

## 4. The resonance consequence — treated adversarially

### 4.1 [PROVED] The complete divisor of the elementary factor

`E(s) := (4 − 4^s)/(4^s(4^s − 1))`. In `X = 2^s`, `E = −(X−2)(X+2)/(X²(X−1)(X+1))`.

```
   zeros of E :  4^s = 4   <=>  s = 1 + i k pi / log 2,   k in Z     -> Re s = 1
   poles of E :  4^s = 1   <=>  s = i k pi / log 2,       k in Z     -> Re s = 0
   ( X^{-2} = 4^{-s} is entire and nowhere zero )
```

`PROVED`. **In particular `E` is finite and non-zero on the whole line `Re s = 1/4`.**

### 4.2 [PROVED] Which factor produces the `s = ρ/2` poles, and why nothing cancels them

By M1F (4.1), `g(s) = Λ(2s−1)/Λ(2s)` with `Λ(w) = π^{−w/2}Γ(w/2)ζ(w)`. The **denominator
`Λ(2s)`** is the factor in question:

```
   Lambda(2s) = 0  <=>  2s = rho (a nontrivial zeta zero)  <=>  s = rho/2,   0 < Re s < 1/2.
```

`det Φ_θ = g² E` carries `g` **squared**, so each such point is a pole of `det Φ_θ` of order
`2·m(ρ)` (`m(ρ)` = multiplicity of `ρ`).

**Adversarial check — could it cancel? Four candidate cancellations, all excluded (`PROVED`):**

1. *Against `E`.* Excluded by §4.1: the zeros of `E` lie on `Re s = 1`, the `ρ/2` poles on
   `0 < Re s < 1/2`. Disjoint. (Even without the zero-free region: `Re(ρ/2) ∈ (0, 1/2)` always,
   and `E`'s zeros have `Re = 1` exactly.)
2. *Against the numerator `Λ(2s−1)`.* Its zeros are `s = (1+ρ')/2`, `Re = 1/2·(1 + Re ρ') > 1/2`
   for any `ρ'` in the strip; its poles are `s = 1` and `s = 1/2`. None has `Re < 1/2` with
   `Im ≠ 0`. So `g` has no zero, and no pole of its own numerator, at any `ρ/2`.
3. *Against the `Γ`-factors.* `Γ(s − 1/2)/Γ(s)` is finite and non-zero off the real axis
   (`Γ` is nowhere zero; its poles are at non-positive integers, all real). `Im(ρ/2) ≠ 0`.
4. *Coincidence `ρ/2 = ρ'/2` from a different zero.* Irrelevant — that only raises the order.

There is **no fifth channel**: `(DET)` is a complete factorisation into `Λ(2s−1)²`,
`Λ(2s)^{−2}`, and the rational-in-`2^s` factor `E`, and each factor's divisor is exhibited.
**The anchor's load-bearing point holds.**

### 4.3 [PROVED, given §4.2 + CITATION] The unconditional off-line statement

`[CITATION, classical]` de la Vallée Poussin / Hadamard: every nontrivial zero of `ζ` has
`Re ρ < 1`. Hence `Re(ρ/2) < 1/2`, and `Im(ρ/2) = Im(ρ)/2 ≠ 0`.

> **(T1) ANCHOR.** `det Φ_θ(s)` has a pole at `s = ρ/2` for every nontrivial zero `ρ` of `ζ`.
> Every such pole satisfies `Re s < 1/2` and `Im s ≠ 0`. **Unconditional.**
> For the first zero `ρ₁` (`Re ρ₁ = 1/2`, verified numerically to great height
> `[CITATION: Odlyzko; van de Lune–te Riele–Winter]`):
> `s_∞ = ρ₁/2 = 0.25 + 7.0673625708673468952…i`, margin `η = 1/8` from the critical line.

Passing to Selberg zeros needs M1F §5.2's transport `(5.3)` — a pole of `det Φ` at non-real `s₀`
with `Re s₀ < 1/2` is a zero of `Z_Γ` of the same order — which rests on the shape of the Selberg
functional equation, M1F obligation **N2/G6**, still **`GAP`**. The scattering-side statement
above needs none of that and is what the Rouché argument (T3) would actually consume.

### 4.4 [PROVED] The other resonances of the anchor

From §4.1, `det Φ_θ` also has poles at `s = ikπ/log 2`, `k ∈ Z`, on `Re s = 0`
(`π/log 2 = 4.5323601…`), of order 2 in `E` — these are the `Γ_θ`/`Γ₀(2)` analogue of M1F
§5.3(b)'s extra resonances, now appearing in the *unsymmetrised* group where the trivial and `χ`
sectors are not separated. At `k = 0` the double pole of `E` meets the double zero of `g²` at
`s = 0` (M1F §5.3(b): `g` has a simple zero at `s = 0`), so `det Φ_θ` is finite and non-zero at
`s = 0` — the same forced cancellation, squared. `PROVED`.

---

## 5. Numeric confirmation — `NON-RIGOROUS` (mpmath, 40 dps)

Script: `scratchpad/t1.py`, `t3.py`, `t4.py` (not committed, per ticket).
All of §5 confirms statements that are proved above; none of it is load-bearing.

### 5.1 Functional equation `Φ_θ(s)Φ_θ(1−s) = I`

| `s` | `max abs(Φ(s)Φ(1−s) − I)` |
|---|---|
| `0.3 + 2.7i` | `2.9e−41` |
| `0.8 + 1.1i` | `4.65e−41` |
| `0.25 + 7.0673626i` | `4.98e−40` |
| `−0.4 + 3.3i` | `2.83e−41` |
| `1.7 + 0.9i` | `2.82e−41` |

Better than the requested `~1e−30`. (This is the full **2×2 matrix** equation, off-diagonal
entries included, not just the determinant.)

### 5.2 Residue at `s = 1` vs `1/vol`

`vol(Γ_θ\H) = π` (§1.1), so the Selberg normalisation demands `Res_{s=1} φ_{ab} = 1/π` for
**every** pair `(a,b)`:

```
eps = 1e-8 :  eps*A(1+eps) = 0.318309883191
              eps*B(1+eps) = 0.318309889810
              1/pi         = 0.318309886184
```

Both entries → `1/π` (9 digits, the residual being the `O(ε)` of the finite-difference probe).
`PROVED` version: `Res_{s=1} g = 3/π` (M1F §4.4); `1/(4^s−1)|_{s=1} = 1/3` and
`(2^s − 2^{1−s})/(4^s − 1)|_{s=1} = (2−1)/3 = 1/3`; both residues `= (3/π)(1/3) = 1/π` ✓.
Consequently `det Φ_θ` has a **simple** (not double) pole at `s = 1`: `A + B` has a double-weight
simple pole and `A − B` is regular there, matching the rank-1 residue matrix of the general
theory.

### 5.3 Independent brute-force moduli enumeration

All `γ ∈ Γ_θ` with `|entries| ≤ 90` (26 318 elements). Moduli and `d`-counts collected per §3:

| block | first `(c, S(0,0;c))` | matches |
|---|---|---|
| `∞∞` | `(2,1)(4,2)(6,2)(8,4)(10,4)(12,4)(14,6)(16,8)(18,6)(20,8)` | `φ_E(c)`, `c` even ✓ |
| `11` | identical list | ✓ |
| `∞1` | `(1,1)(3,2)(5,4)(7,6)(9,6)(11,10)(13,12)(15,8)(17,16)(19,18)` | `φ_E(n)`, `n` odd ✓ |
| `1∞` | identical list | ✓ (symmetry) |

Truncated Dirichlet series at `s = 3`, `c ≤ 40`: diagonal `0.0161785671165` vs
`Σ_{2|c}φ_E(c)c^{-2s} = 0.0161785671165` (all digits); off-diagonal `1.00307219928` vs
`Σ_{n odd}φ_E(n)n^{-2s} = 1.00307219928` (all digits), and the closed form `D/L₂ =
1.00307224039` (differing only in the truncation tail). This is the **strongest** check in the
note: it validates the moduli sets and the counts, which is where a two-cusp derivation is most
likely to go wrong.

### 5.4 Pole signature at `s_∞ = ρ₁/2 = 0.25 + 7.0673625708673468952i`

Mean `|det Φ_θ|` on a circle of radius `r` about `s_∞` (8 sample points):

| `r` | mean `abs(det)` | ratio to previous |
|---|---|---|
| `1e−2` | `4.21762e3` | — |
| `1e−3` | `4.21376e5` | `×99.9` |
| `1e−4` | `4.21372e7` | `×100.0` |
| `1e−5` | `4.21372e9` | `×100.0` |

Exact `r^{−2}` growth ⇒ **order-2 pole**, as §4.2 predicts (`g²`, `ρ₁` simple). Confirmed by the
limit:

```
(s - s_inf)^2 * det Phi_theta   at   s = s_inf + r
  r=1e-3 : -0.1485463958 - 0.3915888507 i
  r=1e-4 : -0.1493453040 - 0.3937447263 i
  r=1e-5 : -0.1494253733 - 0.3939608240 i
  r=1e-6 : -0.1494333821 - 0.3939824389 i     -> finite, non-zero.
```

Single entry: `(s − s_∞)·A(s) → 0.12822 − 0.17480 i`, a **simple** pole of `φ_{∞∞}` ✓
(the entry carries one `g`, the determinant two).

**Controls (no pole expected, none found):**

| `s` | `abs(det Φ_θ)` |
|---|---|
| `0.25 + 5.0i` | `2.6717` |
| `0.25 + 9.0i` | `5.3837` |
| `0.30 + 7.0673626i` | `123.03` |

The third control is the informative one: moving `0.05` off the critical `Re = 1/4` line at the
**same height** drops `|det|` from `4.2e7` (at `r = 1e−4`) to `1.2e2`. The pole is localised at
`Re = 1/4`, exactly on the `Λ(2s) = 0` locus.

---

## 6. Strategic reading — the honest downgrade

**(T1) is closed. Its value to the LAW tail is smaller than `LAW_TAIL_SCOPING.md` §2.2 implies,
and this must be written into the lane text.**

1. **The anchor's resonances are not specific to `λ = 2`.** `det Φ_θ = φ⁺_2 φ⁻_2` (§3.5) — the
   *same* object M1F derived for `G_4 = Γ₀⁺(2)`. The `g(s)` factor, hence the `Re = 1/4` pole
   family, is common to **every** arithmetic member (`q = 4, 6, ∞`) and is `p`-generic in M1F.
   The `λ → 2` endpoint therefore supplies an off-line resonance, but supplies **no mechanism
   that distinguishes the endpoint** from the arithmetic interior points. `PROVED`.
2. **Consequence for (T2)/(T3).** A Rouché continuation anchored at `s_∞` would prove
   "`Z_{λ_q}` has a zero near `ρ₁/2`" — i.e. it predicts non-arithmetic `G_q` resonances
   accumulating at `Re ≈ 1/4`. The repo's scan data do **not** currently show that: the
   lowest-`Im` certified/scanned pins sit at `Re ≈ 0.425–0.475` (`q = 5, 7, 8`;
   `LAW_TAIL_SCOPING.md` §1.4), and the nearest `q = 7, 8` pins to `s_∞` are at
   `0.2303 + 6.371i`, `0.4842 + 7.567i`, `0.4376 + 7.279i`, `0.3038 + 7.959i` — inconclusive.
   `HEURISTIC`. **This is not a refutation of (T1)** — (T1) is about `Γ_θ` alone and is proved —
   **but it means Probe D1 now carries the entire discriminating load** of the merged route.
   With (T1) settled, D1 is the only open empirical question at this level, which strengthens
   the case for running it and reporting its verdict without softening.
3. **What (T1) *does* buy, and it is real.** The Rouché argument needs an anchor whose pole
   location, order, and residue are all exactly known and provably non-cancelling. All three are
   now in hand in closed form, with the order verified two ways (algebra + `r^{−2}` numerics).
   Any (T3) Cauchy estimate can be written against `(DET)` directly.

**Retire from lane text:** "`Γ_θ` is conjugate to `Γ₀(4)`" (§1.3 — false; the correct statement
is `Γ_θ = VΓ₀(2)V^{-1}`, `V = [[1,0],[1,1]]`).

**Index-3 relation to `PSL(2,Z)` (requested self-check): partially usable, `HEURISTIC`.**
`Γ_θ` is **not normal** in `PSL(2,Z)` (its mod-2 image is a non-normal order-2 subgroup of `S₃`),
so the Venkov–Zograf character factorisation M1F §5.3 used does **not** apply. The available
statement is the Artin-type factorisation along
`Ind_{Γ_θ}^{PSL(2,Z)} 1 = 1 ⊕ (2-dim irrep of S₃)`, which predicts
`det Φ_θ = φ_{PSL(2,Z)} · (\text{2-dim-rep factor}) = g(s)·[g(s)E(s)]`. `(DET)` has exactly this
shape, with the `PSL(2,Z)` scattering function `g(s)` splitting off cleanly. **Shape-consistent,
but I have not verified the Artin/induction formula for automorphic scattering matrices** — that
is exactly the unread lead `arXiv:math/0702030` flagged as M1F N3. `GAP`, non-load-bearing.

---

## 7. Ledger — `PROVED` / `CITATION` / `HEURISTIC` / `GAP`, and the Aristotle-able list

### 7.1 Status table

| # | Claim | Status |
|---|---|---|
| C1 | `Γ_θ = ⟨S,T²⟩`, index 3, `vol = π`, area cross-check vs `(2,∞,∞)` triangle | **PROVED** (+ CITATION for the classical name) |
| C2 | Two cusps `∞` (width 2), `1` (width 1); widths sum to index | **PROVED** (§1.2) |
| C3 | `Γ_θ = VΓ₀(2)V^{-1}`, `V = [[1,0],[1,1]]`; `Γ_θ ≇ Γ₀(4)` | **PROVED** (§1.3) |
| C4 | Constant-term / allowed-moduli formula | **CITATION**, number unpinned (N1, inherited) |
| C5 | `φ_{∞∞} = φ_{11} = g/(4^s−1)` | **PROVED** (moduli count + brute force) |
| C6 | `φ_{∞1} = φ_{1∞} = g(2^s−2^{1−s})/(4^s−1)`; `Φ_θ` symmetric | **PROVED** (same) |
| C7 | `det Φ_θ = g² (4−4^s)/(4^s(4^s−1))`; `= φ⁺_2φ⁻_2` | **PROVED** (sympy, exact) |
| C8 | `Φ_θ(s)Φ_θ(1−s) = I` | **PROVED** (`g g(1−s)=1` + `E(s)E(1−s)=1`, sympy) + numeric `<5e−40` |
| C9 | `Res_{s=1}φ_{ab} = 1/π = 1/vol` for all `a,b` | **PROVED** (§5.2) + numeric |
| C10 | `E` has zeros only on `Re s = 1`, poles only on `Re s = 0` | **PROVED** (§4.1) |
| C11 | `s = ρ/2` are poles of `det Φ_θ` of order `2m(ρ)`; **no cancellation** | **PROVED** (§4.2, four channels excluded) |
| C12 | `Re(ρ/2) < 1/2`, `Im ≠ 0` unconditionally | **PROVED** given **CITATION** (de la Vallée Poussin) |
| C13 | `s_∞ = ρ₁/2 = 0.25 + 7.06736257…i` is an order-2 pole | **PROVED** + numeric `r^{−2}` (§5.4) |
| C14 | poles ⇒ zeros of `Z_{Γ_θ}` (resonance transport) | **GAP** — M1F N2/G6, unchanged |
| C15 | anchor is not `λ=2`-specific; same `g` at `q = 4, 6` | **PROVED** (§6.1) |
| C16 | no `q=7,8` scanned pin converging to `s_∞` yet | **HEURISTIC**, inconclusive (§6.2) |
| C17 | Artin/induction shape check against `PSL(2,Z)` | **GAP**, non-load-bearing (§6) |

### 7.2 Aristotle-able sub-lemmas (finite / algebraic — for a v23 dispatch)

Mirrors M1F's A-1…A-7 numbering style; **T-4 and T-5 are the highest-value items.**

- **T-1** (§1.1) `⟨S, T²⟩ ⊆ Γ_θ` and `[PSL(2,Z) : Γ_θ] = 3`. Finite: reduction
  `SL(2,Z) → SL(2,Z/2) ≅ S₃`, plus `|{I, [[0,1],[1,0]]}| = 2`. Pure finite group theory.
- **T-2** (§1.2) **Cusp inventory.** (i) `Γ_{θ,∞} = ⟨T²⟩`; (ii) `VTV^{-1} = [[0,1],[−1,2]] ∈ Γ_θ`
  is parabolic fixing `1`; (iii) `∞ ≁ 1` under `Γ_θ` — the parity argument
  "`γ(∞) = 1 ⇒ a = c = ±1`, both odd, contradicting the `Γ_θ` mod-2 condition"; (iv) widths
  `2 + 1 = 3 =` index. All finite 2×2 integer algebra. **Formalizable as stated.**
- **T-3** (§1.3) `V [[1,1],[0,1]] V^{-1} = [[0,1],[−1,2]]` and `V Γ₀(2) V^{-1} = Γ_θ` as sets,
  via the mod-2 characterisation. Finite matrix algebra + a set equality over the congruence
  description. Also: `[PSL(2,Z):Γ₀(4)] = 6 ≠ 3`, so no `PSL(2,Z)`-conjugacy `Γ_θ ~ Γ₀(4)`.
- **T-4** (§3.1, §3.3) **The two moduli-count lemmas.** *(highest value; the analogue of M1F A-4
  for a two-cusp group, and the only place a two-cusp derivation can silently go wrong)*
  - (a) `{ c > 0 : [[*,*],[c,*]] ∈ σ_∞^{-1}Γ_θσ_∞ } = 2Z_{>0}`, with
    `#{d mod 2c : [[*,*],[2c,d]] ∈ σ_∞^{-1}Γ_θσ_∞} = φ_E(2c)`.
  - (b) `{ c : [[*,*],[c,*]] ∈ σ_1^{-1}Γ_θσ_∞ } = √2·(2Z_{≥0}+1)`, with count `φ_E(n)` at
    `c = n√2`, `n` odd.
  Both are statements about integer lower rows and coprimality; no analysis.
  **Brute-force-verified here to entry bound 90** (§5.3) — a v23 dispatch should prove them
  for all `c`.
- **T-5** (§3.1) **Euler-product restriction, `p = 2`** — verbatim M1F A-4 at `p = 2`:
  `Σ_{2|c} φ_E(c) c^{-2s} = (ζ(2s−1)/ζ(2s))/(4^s − 1)`, and
  `Σ_{n odd} φ_E(n) n^{-2s} = (ζ(2s−1)/ζ(2s))(1 − 2^{1−2s})/(1 − 2^{-2s})`. Formal Dirichlet-
  series / Euler-product identity in `Re s > 1`. **Reuse M1F A-4 if already dispatched.**
- **T-6** (§3.5) **Rational-function identities in `X = 2^s`:**
  `A² − B² = −(X−2)(X+2)/(X²(X−1)(X+1))`, `A²−B² = φ⁺₂φ⁻₂`, and `E(s)E(1−s) = 1`
  (i.e. `E(X)·E(2/X) = 1`). Trivially formalizable; already sympy-verified exactly.
- **T-7** (§4.1) **Divisor of `E`:** `4^s = 4 ⟺ s = 1 + ikπ/log2`; `4^s = 1 ⟺ s = ikπ/log2`;
  hence `E` finite and non-zero on `Re s = 1/4`. Elementary complex exponential.
- **T-8** (§4.2) **Non-cancellation:** given `g = Λ(2s−1)/Λ(2s)`, `Λ` holomorphic off `{0,1}`
  with zeros exactly the nontrivial `ζ` zeros, and T-7 — the order of `det Φ_θ` at `s = ρ/2` is
  `−2m(ρ)`. This is bookkeeping over divisors once T-7 and the `Λ` divisor are given.
  *(Reuse M1F A-6, A-7 for the `Λ`/`g` facts.)*
- **T-9** (§5.2) **Residue:** `Res_{s=1} φ_{ab} = 1/π` for all four `(a,b)`, given
  `Res_{s=1} g = 3/π` (M1F §4.4). Two one-line evaluations.

**Not Aristotle-able:** C14 (the Selberg-zeta transport, M1F N2/G6); C17 (the Artin/induction
formula for scattering matrices); anything in §6.2 (numerics).

### 7.3 Obligations opened

| # | Obligation | Route |
|---|---|---|
| **TN1** | Pin the classical reference for `Γ_θ = ⟨S,T²⟩`, index 3, cusps `{∞, 1}` with widths `{2,1}`. §1.1–1.2 prove all of it, so this is citation hygiene, not a load-bearing gap. | human / library |
| **TN2** | Inherited M1F **N1** (the constant-term formula's number) and **N2** (Selberg functional equation) — unchanged, both still open. | human / library |
| **TN3** | Prior-art: is the `Γ_θ` / `Γ₀(2)` two-cusp scattering matrix published? Almost certainly **yes** — `Γ₀(2)` is the standard worked example in every treatment of congruence scattering matrices. **Make no novelty claim for `(DET)`.** (M1F N3 already governs the `Γ₀⁺` case; this one is more clearly owned, not less.) | prior-art scout |
| **TN4** | Correct `LAW_TAIL_SCOPING.md` §2.2's "`Γ₀(4)`, to which `Γ_θ` is conjugate" → `Γ₀(2)`, `V = [[1,0],[1,1]]`. | lane-text edit (not made here; ticket scopes this note only) |

---

## 8. What this note claims and does not claim

**Claims.** (i) The cusp inventory of `Γ_θ` — two cusps, widths 2 and 1 — is proved, with the
width-sum/index consistency check. (ii) `Φ_θ(s)` is derived in closed form by the M1F
allowed-moduli constant-term method run **directly in `Γ_θ`**, and independently confirmed by
conjugation to `Γ₀(2)` and by brute-force enumeration of the moduli sets. (iii) `det Φ_θ` is
exhibited in closed form and equals `φ⁺₂φ⁻₂`. (iv) Three self-checks pass — functional equation
(exact + `<5e−40`), residue `= 1/vol` (exact + 9 digits), two-route agreement. (v) The `s = ρ/2`
poles are produced by the `Λ(2s)` denominator of `g(s)²` and **cannot** be cancelled; four
candidate cancellation channels are excluded. (vi) The anchor statement of
`LAW_TAIL_SCOPING.md` §2.2 is therefore **correct**, unconditionally.

**Does not claim.** No novelty for `(DET)` (TN3 — the `Γ₀(2)` scattering matrix is textbook).
No Selberg-zero statement: the transport from scattering poles to `Z_Γ` zeros remains M1F's
open G6/N2. No statement about any non-arithmetic `G_q`. (T2) and (T3) are untouched. Nothing
here supports or refutes the Rouché continuation itself — §6 argues only that (T1) is a weaker
lever than the scoping note implied, and that Probe D1 now carries the discriminating load.

**No refutation was found** of the anchor. Had `E` had a zero on `Re s = 1/4`, or had the
residue missed `1/vol`, or had the brute-force moduli disagreed with the closed form, this note
would have said so and the merged (a)+(d) route would have lost its anchor. None of that
happened; the failure modes were checked explicitly and all three self-checks pass.

## Erratum (2026-08-16, from LAW_U3_TRANSPORT.md)
§4.4 correction: the poles of det Φ_θ at s = ikπ/log 2 are SIMPLE, not
"order 2 in E" (r·E → 3/(2 log 2) = 2.164042, r²·E → 0). Hence Z_{Γ_θ}
has simple zeros there. Non-load-bearing for the anchor (which sits at
s_∞ = ρ₁/2, an order-2·m(ρ₁) point via the Λ(2s)² factor).
