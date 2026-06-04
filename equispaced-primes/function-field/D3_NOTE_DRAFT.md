# The function-field Farey–Mertens object: an exact, unconditional model — and why it is a dictionary, not a new theorem

**Status: DRAFT (autonomous run 2026-05-16). NOT sent, NOT pushed. Internal.**
Adversarial-honesty posture: every claim labelled
[PROVEN] / [PROVEN-exact, machine-verified] / [NUMERICAL] / [CONJECTURAL] /
[CITATION-UNVERIFIED]. No novelty/citation inflation.

---

## Abstract

We transplant the Farey↔Mertens / per-step / BCZ-cocycle program from `ℚ` to
`A = F_q[t]`, the one setting where the analogue of the Riemann Hypothesis is a
theorem (Deligne, Weil II). We obtain: (G0) an exact function-field
Farey–Mertens identity, absent from the literature; (G1) an exact proof that
the global object trivializes — the char-0 "RH-depth" *provably vanishes*
because `1/ζ_A` is a polynomial; (G2) the twisted/family object is non-trivial
and exhibits **unconditional** square-root cancellation; (Q1) the Farey
discrepancy is exactly the Birkhoff sum of an explicit cocycle whose raw form
reproduces the char-0 non-`L²` obstruction, yet whose renormalized second
moment converges to an **exact, unconditional constant** `C_FF(q)`. We then
prove a character-orthogonality duality which separates two objects that must
not be conflated: the **untwisted** constant `C_FF(q)` is *elementary* (an
explicit `σ_A²` Euler-product value — no characters, no depth), while the
**twisted** family variance is — up to normalization — exactly the
Keating–Rudnick / Katz Möbius-in-progressions object. **Net: this is an exact
unconditional dictionary and a Katz–Sarnak-style predictive model, not new
mathematics — "not new" for two different reasons (elementary vs.
Keating–Rudnick). We say so plainly.**

---

## 1. Setup

`A=F_q[t]`, monic polynomials as "positive integers", `|f|=q^{deg f}`. The
"circle" is `K_∞={α∈F_q((1/t)):|α|<1}`, compact, Haar mass 1, with additive
characters `ψ_m(α)=ψ(mα)` indexed by `m∈A` (`ψ` = residue at ∞). Möbius `μ`
over monic polynomials; Mertens `M_A(n)=Σ_{f monic, deg f≤n}μ(f)`. Farey set
`F_D={h/g: g monic, deg g≤D, deg h<deg g, gcd(h,g)=1}∪{0}`, `Φ_D=|F_D|`.
Character sum `A_D(m)=Σ_{f∈F_D}ψ(mf)`.

## 2. G0 — exact function-field Farey–Mertens identity  [PROVEN-exact, machine-verified, 477 cases q=2,3,5]

> `A_D(m) = Σ_{e | m, e monic} q^{deg e} · M_A(D − deg e)`,
> with `M_A(0)=1`, `M_A(n≥1)=1−q`, `M_A(k<0)=0`.

Derivation: `A_D(m)=Σ_{g monic, deg g≤D} c_g(m)` with `c_g` the Carlitz–
Ramanujan sum `=Σ_{e|gcd(g,m)}q^{deg e}μ(g/e)`; reorganize by `e|m`. This is
the exact `F_q[t]` analogue of the classical `A_Q(m)=Σ_{d|m}d·M(⌊Q/d⌋)`.
Verified: the direct character sum over the entire Farey set equals this
divisor–Mertens form, exactly, for all tested `(m,D)`, `q∈{2,3,5}`
(`verify_ff_farey_mertens.py`). Web search (2 independent passes) found **no
function-field Farey–Mertens identity in the literature**; it is new *as a
formula* — but it is a **2-line corollary** of Carlitz's evaluation of the
function-field Ramanujan sum, summed over `deg g≤D` and reorganized by `e|m`.
Its absence from the literature reflects that it is **too elementary to
publish on its own**, not that it is deep. Stated for completeness / as the
dictionary's entry point, not as a contribution.

## 3. G1 — exact global trivialization: the RH-depth provably vanishes  [PROVEN-exact]

`1/ζ_A(s)=1−q·q^{-s}` is a *polynomial* in `q^{-s}`, so `M_A(n)` is exactly
*eventually constant*: `M_A(0)=1`, `M_A(n≥1)=1−q`. Consequently, for
`D>deg m`,

> `A_D(m) = (1−q)·σ_A(m)`,  σ_A(m)=Σ_{e|m monic}q^{deg e},

**independent of `D`**. The char-0 Farey character sums fluctuate with `M(⌊·⌋)`
(that fluctuation *is* RH-depth); here they *stabilize exactly*. This is the
sharpest possible statement that the RH-depth wall has no global function-field
analogue. (Verified `verify_ff_farey_mertens.py` Gate 1.)

## 4. G2(a) — the twisted/family object is non-trivial, with UNCONDITIONAL square-root cancellation  [NUMERICAL + Deligne]

Twist by a Dirichlet character `χ` mod an irreducible `Q`: `M_A(n,χ)=
Σ_{deg f≤n}μ(f)χ(f)`. Generating function `Σμ(f)χ(f)u^{deg f}=1/L(u,χ)`,
with `L(u,χ)` a polynomial of degree `deg Q−1` whose inverse roots are
Frobenius eigenvalues of modulus `√q` — **Deligne / Weil II, unconditional**.
Numerics (q=2,3,5; `verify_ff_g2_variance.py`): `mean_χ|M_A(n,χ)|²∼q^n`,
normalized variance `O(1)`-stable, `max|M_A|/q^{n/2}` bounded — exactly the
unconditional square-root cancellation that, over `ℚ`, is the conjectural
content of RH. The strategic thesis ("RH-depth is real but unconditional in
the FF model") holds.

## 5. Q1 — the Farey cocycle: exact Birkhoff sum; raw obstruction reproduced; renormalized constant EXACT and UNCONDITIONAL

Order `F_D` by the (exact, lexicographic) `t^{-1}`-coefficient sequence — this
**is** the `K_∞` circle order, which **is** the BCZ first-return orbit order
(function-field Athreya–Cheung structure). Define the cocycle
`g_j=1−Φ_D·gap_j`.

- [PROVEN-exact] `S_j:=Σ_{i≤j}g_i = E_D(f_j)` (the Farey discrepancy) for every
  node, every `q,D` tested (`verify_ff_q1_cocycle.py`). The FF discrepancy
  **is** the Birkhoff sum of an explicit cocycle. (Telescoping ⇒ structural.)
- [NUMERICAL] The *raw* cocycle is **not uniformly `L²`**: its variance `c0`
  grows with `D` (q=2: 0.57→1.41; q=3: 0.87→1.64). This is the **same
  obstruction signature as the char-0 D1 BCZ-cocycle** — *not* a
  spectral-gap-stabilized different statistic.
- The *renormalized* normalized second moment `R_D:=q^D·W_D^{pf}`,
  `W_D^{pf}=Φ_D^{-1}(q−1)Σ_{m monic}A_D(m)²q^{-2deg m}` (exact rational
  arithmetic per `D`, `verify_ff_q1c_exact_mikolas.py`), is monotone increasing
  and bounded, hence **converges** to a finite **unconditional** constant
  `C_FF(q)` — the FF analogue of the *conjectural* char-0 `N·W(N)→C`, here
  unconditional because `M_A` is exactly constant (no RH-depth).
  - [PROVEN-by-verification, Q6] `C_FF(q)` is a **rational function of `q`**:
    the `σ_A²` generating function is exactly
    `F(u)=Σ_m σ_A(m)²u^{deg m}=(1−q³u²)/((1−qu)(1−q²u)²(1−q³u))`
    (FF transport of Ramanujan's `Σσ(n)²n^{-s}=ζ(s)ζ(s−1)²ζ(s−2)/ζ(2s−2)`),
    machine-verified vs brute force q=2,3,5 (`verify_ff_q6_closedform.py`);
    nearest singularity `u=1/q³` ⇒ `R_D` tends to a rational limit.
  - [DERIVED + VERIFIED] **Exact closed form: `C_FF(q) = (q+1)²`.**
    Reduce `S_D` to a function-field Mikolás *bilinear form* (swap divisor
    sums): `S_D=(q/(q−1))Σ_{0≤j₁,j₂≤D}B(j₁,j₂)M_A(D−j₁)M_A(D−j₂)`. The Euler
    product over irreducibles gives
    `Σ B(j₁,j₂)xʲ¹yʲ²=(1−xy/q)/((1−x)(1−y)(1−qxy))`, so `B` depends only on
    `M=min(j₁,j₂)` with `b(M)=(q+1)q^{M−1}−1/q`; and `Φ_D=(q^{2D+1}+1)/(q+1)`
    exactly. Carrying the leading `q^D` modes through
    `S_D=(q/(q−1))[(q−1)²U−2q(q−1)V+q²W]` gives `S_D∼[q(q+1)/(q−1)]q^D`, hence
    `C_FF(q)=(q²−1)·[q(q+1)/(q−1)]/q=(q+1)²`. Verified three independent ways
    (`verify_ff_CFF_v2.py`): (i) direct `A_D(m)` enumeration converges *up* to
    the closed `S_D` as the cutoff grows; (ii) exact-Fraction `R_D→(q+1)²` for
    q=2,3,5,7 (D=60: q=2→9 to 1e-15, q=3→16, q=5→36, q=7→64); (iii) exact
    geometric extrapolation →9.000…. **Correction:** the earlier Q1c/Q6
    "`≈9.4/17/37`" were *truncation-biased low* (finite `m`-cutoff); the true
    infinite-sum constant is exactly `(q+1)²` = 9, 16, 36. Still **not
    load-bearing / dictionary-tier**: an elegant *elementary* closed form
    (the `M_A`-is-constant collapse of the Mikolás bilinear form), no
    arithmetic depth, no char-0 consequence — but exact, clean, citable.

## 6. Why the *twisted* object is Keating–Rudnick and the *untwisted* `C_FF` is elementary — neither is a new statistic  [PROVEN duality + abstract-confirmed KR scope]

**Character-orthogonality duality (proved here, no citation needed).** For
monic `Q`, let `(A/Q)^*` be the reduced residues, `Φ_A(Q)=|(A/Q)^*|`. For any
finitely-supported `α(f)` (here `α=μ·1_{deg≤n}`):

> `Σ_{a∈(A/Q)^*} |Σ_{f≡a (Q)} α(f)|²
>   = Φ_A(Q)^{-1} Σ_{χ mod Q} |Σ_{(f,Q)=1} α(f)χ(f)|²`,

immediately from `Σ_{χ}χ(a)χ̄(b)=Φ_A(Q)·1_{a≡b}`. Subtracting the principal
term: the **variance of the Möbius sum over residue classes mod `Q`** equals
`Φ_A(Q)^{-1}Σ_{χ≠χ_0}|M_A(n,χ)|²` — i.e. **the character-ensemble second
moment is, up to normalization, exactly the Möbius-in-arithmetic-progressions
variance.**

The Keating–Rudnick paper "Squarefree polynomials and Möbius values in short
intervals and arithmetic progressions" (Algebra & Number Theory 10(2),
375–420, 2016; arXiv:1504.03444) computes precisely the Möbius-variance in
arithmetic progressions (and short intervals) over `F_q[t]` as a `U(N)`
matrix integral, unconditionally via Katz equidistribution.
**[CITATION-UNVERIFIED — see §9: exact theorem numbers / monodromy `N` /
integral could not be locked from the primary PDF in this run; the
abstract-level scope IS confirmed; lock before external use.]**

**These are two DIFFERENT objects and must not be conflated** (an earlier
draft of this note conflated them — corrected here per the Q5 self-review):

- **C_FF(q) (§5), the untwisted Mikolás/Parseval second moment**, is — by G0
  (`A_D(m)=(1−q)σ_A(m)`) — an **explicit, elementary, convergent `σ_A²`
  Euler-product constant** (rational in `q`). It has **no characters, no
  fluctuation, no arithmetic depth** — it is the FF collapse of the classical
  Mikolás bilinear form to a zeta value because `M_A` is constant. It is *not*
  the Keating–Rudnick object; it is *below* dictionary-tier (elementary).
- **The twisted G2(a) variance** `Φ_A(Q)^{-1}Σ_{χ≠χ_0}|M_A(n,χ)|²` **is** —
  by the duality above — the Möbius-in-arithmetic-progressions variance, i.e.
  the **Keating–Rudnick / `U(N)` / Katz object**.

So "not new" holds for *both* but for *different reasons*: the untwisted
constant is **elementary**; the twisted variance is **Keating–Rudnick**.
**Conclusion: G3 (a Katz-monodromy "new variance theorem") is NOT warranted —
the only non-elementary object is the twisted variance, which is exactly
Keating–Rudnick. Not pursued.**

## 7. The genuinely-new content: a dictionary, honestly bounded

What is new is **of formulation, not of theorem** (mirrors the D1 BCZ-cocycle
landing):

1. The exact FF Farey–Mertens identity (§2) — web-confirmed absent; elementary.
2. The exact statement that RH-depth globally *vanishes* in `F_q[t]` (§3).
3. The Farey-discrepancy ↔ BCZ ↔ Bruhat–Tits-tree-geodesic **dictionary**: the
   FF discrepancy is the exact Birkhoff sum of `g=1−Φ·gap`; the renormalized
   constant is exact/unconditional where char-0 it is RH-conditional and
   theorem-(R)-blocked. This **occupies the function-field analogue of the
   open slot Athreya–Cheung (IMRN 2014) §8 flagged but did not build**, and is
   the unconditional Katz–Sarnak *prediction* mirroring the conjectural char-0
   `C`.

## 8. Who cares (applied honestly)

- **Who:** the Franel–Landau / BCZ / Keating–Rudnick–Sawin function-field
  analytic-NT community (a few dozen).
- **What they get:** a clean exact unconditional *model* of the
  Farey–Mertens second moment, and an explicit dictionary; **not** a new tool,
  **not** a new theorem, **no** consequence for char-0 `ζ`.
- **Counterfactual:** if it vanished, no open problem they care about changes
  (the variance itself is Keating–Rudnick).
- **Verdict:** worthwhile as a short *expository/dictionary* note (Exp. Math. /
  a section of the Koyama-adjacent work), **not** a standalone research
  advance. Same tier as D1.

## 9. Citations & honesty ledger

- Cox–Ghosh–Sultanow, arXiv:2105.12352 (2021): static char-0 Farey↔Mertens —
  the prior art for the *static identity*; G0 is its FF analogue. [VERIFIED in
  project prior-art lock.]
- Athreya–Cheung, IMRN 2014 no.10, 2643–2690 (arXiv:1206.6597), §8: the open
  question the (FF) cocycle dictionary occupies. [VERIFIED in project lock.]
- Karvonen–Zhigljavsky, arXiv:2407.10214: MMD/RKHS Farey–RH; *not*
  Cox–Ghosh–Sultanow (correct the recurring misattribution). [VERIFIED.]
- Keating–Rudnick, Algebra & Number Theory 10(2) 375–420, 2016
  (arXiv:1504.03444): Möbius variance in AP & short intervals = unitary
  matrix integrals via Dirichlet-character/L-function + Katz equidistribution,
  q→∞. **[CITATION-LOCKED 2026-05-16 from ar5iv full text + arXiv abstract —
  see `KR_CITATION_LOCK.md`.]** Locked: Möbius short-interval = **Thm 1.2**
  (`Var~H=q^{h+1}`, monodromy `U(n−h−2)`); Möbius arithmetic-progressions =
  **§8** (`Var_Q=Φ(Q)^{-1}Σ_{(A,Q)=1}|S_{μ,n,Q}(A)|²`, monodromy
  `U(n−deg Q−2)`); μ² AP = Thm 1.5. §1.3 states the AP/short-interval ⇒
  Dirichlet-character ⇒ L-function ⇒ unitary-Katz reduction explicitly — i.e.
  exactly our §6 duality. Soft residual: the AP-Möbius theorem *number*
  (vs Thm 1.2 / 1.5) not verbatim-pinned; confirm vs published PDF before
  final submission. The D3 verdict no longer depends on this citation (the §6
  duality is self-proved) but is now additionally backed by it.

---

### One-line bottom line
The function-field route delivers an *exact, unconditional model* and a clean
dictionary — the cleanest possible demonstration that the char-0 RH-depth wall
has no function-field analogue — but **no new mathematics**: the untwisted
constant `C_FF(q)` is *elementary* (an explicit `σ_A²` value), and the only
non-elementary object, the twisted family variance, is *exactly*
Keating–Rudnick by an elementary character-orthogonality duality. Honest,
shippable as exposition; not a breakthrough. (We do not resolve the
Athreya–Cheung §8 question itself; §7.3 is the function-field-side dictionary
only.)
