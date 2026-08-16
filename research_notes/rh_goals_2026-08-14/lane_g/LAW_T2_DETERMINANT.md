# LAW (T2) — the two-variable determinant: construction, obstruction, replacement

**Date:** 2026-08-15. **Lane G.** Ticket: `plans/wayfinder/rh-goals/tickets/family-law-theorem.md` step 4.
**Parents read in full:** `lane_g/LAW_TAIL_SCOPING.md` (the (T2) statement and its two named
blockers B-I, B-II), `lane_g/LAW_ANCHOR_T1_THETA.md` ((T1) closed: `det Φ_θ` has an order-2 pole
at `s_∞ = ρ₁/2`), `lane_g/LAW_PROBES_D1_B1.md` (D1 MIGRATION-CONSISTENT at `~q⁻²`),
`lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md` (the q=5 determinant identification),
`lane_g/TA_DERIVATION.md`, `lane_g/TB_R1_HILBERT_RESTATEMENT.md`.

**Status convention (identical to M1F / T1):** `PROVED` = derived here in closed form, or verified
in exact/symbolic arithmetic. `CITATION` = imported, import named. `HEURISTIC` = float evidence or
a plausibility argument, explicitly not a proof. `GAP` = not justified, missing statement written out.

**No certificate is produced here. Nothing is committed. No other lane's files are touched.**

---

## 0. Verdict up front

> ### (T2) **as literally stated is STRUCTURALLY-BLOCKED.**
> ### Inducing does **not** rescue it — inducing makes it strictly worse.
> ### But (T2) **is not needed.** A strictly weaker replacement **(T2′)** carries the same
> ### Rouché conclusion and is **CONSTRUCTIBLE**, at the price of two named analytic obligations.
>
> **Headline: STRUCTURALLY-BLOCKED as posed / CONSTRUCTIBLE after reformulation.**

Three things are settled here, and one is new and load-bearing:

1. **B-I's named rescue candidate is dead, provably.** The unreduced Rosen operator on a *fixed
   disc* does not exist as a nuclear (or even bounded-with-invariant-disc) operator for **any**
   `λ ∈ (λ₀, 2]` — not merely at the `λ = 2` endpoint. The `n = ±1` branch `ψ_{±1}` is **elliptic**
   for `λ < 2` and **parabolic** at `λ = 2`; in both cases its multiplier has modulus 1, so by the
   Denjoy–Wolff/Schwarz argument **no** disc satisfies `ψ_1(cl D) ⊂ D`. §2.2, `PROVED`.
2. **Inducing (accelerating the `n=±1` branch) is exactly the wrong move for a λ-family.**
   `ψ_1(λ)` is elliptic of **order `q`** at `λ = λ_q` (rotation angle `π/q` — this *is* the source
   of `κ_q`'s linear growth in `q`), and parabolic of infinite order at `λ = 2`. So the induced
   branch alphabet
   `{ψ_1^k ∘ ψ_n}` is **finite with `k < q` at every `λ_q`** and **infinite at `λ = 2`**. The
   alphabet's cardinality is a function of the *rotation number* `arccos(λ/2)/π`, which is
   `1/q` exactly at `λ_q` and irrational for generic `λ`. No λ-analytic object has that structure.
   §2.3, `PROVED` (for the order statement) + `HEURISTIC` (for the "no λ-analytic object" step).
3. **The obstruction is not an artefact of the operator; it is group-theoretic.** Any carrier that
   is λ-analytic must be indexed by a **λ-independent** set (branches, or words in `⟨S⟩ * ⟨T⟩`).
   At `λ = λ_q` the relation `R^q = 1` (`R = S T_λ`) makes the index→geodesic map infinite-to-one.
   §2.4, `PROVED`. This is B-I and B-II seen as one obstruction rather than two.
4. **NEW — the replacement.** The Rouché step never needed joint holomorphy. `{λ_q}` is a
   *sequence*, so **Vitali + Hurwitz** replaces **Rouché**, and the tail argument then runs entirely
   on **Selberg zeta functions**, with the transfer operator dropped from the tail argument
   altogether. §3. This dissolves B-II completely, dissolves the `κ_q → ∞` half of B-I, and
   converts the crux into two clean, standard-shaped analytic obligations (§5, U1/U2).

**And the reformulation is strongly corroborated numerically** (§4, `NON-RIGOROUS`): the truncated
Selberg Euler product `Z_{G_q}(s)` converges to `Z_{Γ_θ}(s)` at **rate `q^{-2}`** (fitted exponents
`−2.10, −2.15, −2.18` at three `s`, stable under doubling the geodesic cutoff), and the systole
gap closes at **exactly `q^{-2}`** with the exact closed form `sys = 2 arccosh λ_q` (`PROVED`).
`q^{-2}` is the same exponent Probe D1 measured for pin migration — the whole family is a
**smooth deformation in `ε = 2 − λ_q = π²/q² + O(q⁻⁴)`**, and every measured quantity scales in it.

---

## 1. What (T2) asks for, restated exactly

From `LAW_TAIL_SCOPING.md` §2.1, the target:

> **(T2)** a determinant `D(s, λ)`, jointly holomorphic on a neighbourhood of
> `{Re s ∈ (0, 1/2+ε)} × (λ₀, 2]`, with
> (i) at `λ = λ_q`, the `s`-divisor of `D(·, λ_q)` contains the Selberg-zeta divisor of `G_q`
>     (or a certified sub-divisor including our pins);
> (ii) at `λ = 2`, the divisor contains `s_∞ = ρ₁/2`.

The two named blockers:

- **(B-I)** `κ_q = ⌈(q−3)/2⌉ → ∞` kills the REDUCED MMS operator as a λ-family. Named rescue: the
  UNREDUCED operator, whose branch index set `{z ↦ −1/(z + nλ)}_{|n| ≥ 1}` is `q`-independent.
- **(B-II)** `{G_λ}` is discrete in `λ` — only `λ_q` and `λ ≥ 2` give groups — so `D`'s divisor at
  non-group `λ` has no Selberg meaning.

§2 disposes of B-I's rescue. §3 shows B-II was never a blocker for the *conclusion*, only for the
*method*, and supplies the method that does not need it.

### 1.1 [PROVED] The objects, fixed once

`S = [[0,−1],[1,0]]`, `T_λ = [[1,λ],[0,1]]`, `G_λ := ⟨S, T_λ⟩`, `λ_q = 2cos(π/q)`.
`R := S T_λ = [[0,−1],[1,λ]]`, `tr R = λ`.

```
   lam < 2   ->  R ELLIPTIC, eigenvalues e^{+-i theta}, 2 cos theta = lam,  theta = arccos(lam/2)
   lam = lam_q  ->  theta = pi/q,  R^q = -I,  R has ORDER q in PSL(2,R)
   lam = 2   ->  R = [[0,-1],[1,2]] PARABOLIC,  R^k = [[1-k, -k],[k, 1+k]],  INFINITE order
```

`PROVED` (two-line eigenvalue computation; `R^k` verified by induction and numerically).
`G_q ≅ Z/2 * Z/q` (the `(2,q,∞)` triangle group) and `Γ_θ = G_2 ≅ Z/2 * Z`
(`LAW_ANCHOR_T1_THETA.md` §1.1). **The elliptic generator of `G_q` becomes the parabolic generator
of `Γ_θ`'s second cusp.** That single sentence is the whole mechanism of the `q → ∞` limit, and it
is what makes the cusp count jump `1 → 2`.

The Rosen/MMS inverse branches are `ψ_n(z) = −1/(z + nλ)`, `n ∈ Z \ {0}`, on `I_λ = [−λ/2, λ/2]`.

> **`ψ_1 = R` exactly.** `ψ_1(z) = −1/(z+λ)` is the Möbius action of `[[0,−1],[1,λ]] = S T_λ = R`.
> `PROVED`. **The troublesome branch and the elliptic generator are literally the same element.**

This upgrades `LAW_TAIL_SCOPING.md` §1.2 (which recorded only `tr M_1 = λ_q → 2`): the branch whose
contraction degrades is not merely *trace-2-adjacent*, it **is** the group's elliptic generator, the
one that becomes `Γ_θ`'s second cusp. Every symptom the repo has measured — `1 − ρ* ~ q^{-1.27}`
with the worst block `(3→2, n=1 head)` at almost every `q` (`LAW_PROBES_D1_B1.md` Probe B1),
`κ_q ≍ q`, the `(3→1, +1)` full-Markov branch that no uniform inflation can nest
(`TA_DERIVATION.md`) — is one fact about `R`.

---

## 2. The candidate construction, and why it fails

### 2.1 The construction one would write down

> **Candidate C1 (unreduced, fixed disc).** Fix a disc `D = D(c, R) ⊃ I_λ`. Let
> `B(D)` = disc algebra (or `H²(D)`), and
> ```
>    (L_{s,lam} f)(z) = sum_{|n|>=1} ((z + n lam)^2)^{-s} f( -1/(z + n lam) ),
>    D(s, lam) := det( 1 - L_{s,lam} ).
> ```
> Branch index set `{|n| ≥ 1}` is `q`-independent; `λ` enters only as a real parameter.
> This is exactly the rescue candidate `LAW_TAIL_SCOPING.md` §2.2 names.

For `C1` to define a nuclear/trace-class operator one needs the standard hypothesis
(`CITATION`: Mayer, *The thermodynamic formalism approach to Selberg's zeta function for
PSL(2,Z)*, Bull. AMS 25 (1991); MMS §4; Ruelle, Invent. Math. 34 (1976)):

```
   (H)   psi_n( cl D ) subset D   for every branch n,  with the weights holomorphic on cl D.
```

Under (H), each `ψ_n` is a strict contraction in the hyperbolic metric of `D`, the composition
operators are nuclear of order 0, and the determinant is entire in `s`.

### 2.2 [PROVED] (H) fails for **every** `λ ∈ (0, 2]`, not only at `λ = 2`

> **Lemma T2-A.** Let `λ ∈ (0, 2]` and let `D ⊂ C` be any open disc (or any simply connected
> domain `≠ C`) with `ψ_1(cl D) ⊂ D`. Then no such `D` exists.
>
> *Proof.* `ψ_1` is the Möbius map of the matrix `[[0,−1],[1,λ]]`, `det = 1`, `tr = λ ≤ 2`.
> Suppose `ψ_1(cl D) ⊂ D`. Then `ψ_1 : D → D` is a holomorphic self-map with
> `ψ_1(cl D)` compactly contained in `D`, so the Denjoy–Wolff point of `ψ_1` lies **inside** `D`
> and is an **attracting** fixed point: `⋂_k ψ_1^k(cl D)` is a nonempty compact `ψ_1`-invariant set,
> and by the Schwarz–Pick lemma on `D` the iterates converge to a single interior fixed point `p`
> with `|ψ_1'(p)| < 1`.
> But the fixed points of `ψ_1` solve `z² + λz + 1 = 0`, i.e. `z_± = (−λ ± √(λ²−4))/2`, and their
> multipliers are `ψ_1'(z_±) = 1/(z_± + λ)² = z_±²` (using `z_±(z_± + λ) = −1`), of modulus
> `|z_±|² = 1` for **every** `λ ≤ 2` (the roots of `z²+λz+1` have product 1 and are complex
> conjugate for `λ < 2`, so `|z_±| = 1`; for `λ = 2`, `z = −1` doubly, multiplier 1).
> No fixed point of `ψ_1` is attracting. Contradiction. ∎ `PROVED`.

Concretely, the two regimes:

| regime | `ψ_1` type | fixed points | multiplier | consequence |
|---|---|---|---|---|
| `λ < 2` | **elliptic**, rotation angle `2 arccos(λ/2)` | `−λ/2 ± i√(4−λ²)/2` (off `R`) | `e^{∓2i arccos(λ/2)}`, modulus 1 | preserves `R ∪ {∞}` and every hyperbolic circle about `z_+`; at `λ = λ_q` every real orbit is a `q`-cycle on `R ∪ {∞}`, and the endpoint's orbit hits `∞` outright for even `q` (Cor. T2-A′) |
| `λ = 2` | **parabolic** | `−1 = −λ/2` (double), **on the interval endpoint** | 1 | classical failure of nuclearity |

Numeric illustration (§4, P1): `|ψ_1'(−λ/2)| = 1.5279, 1.2346, 1.1080, 1.0519, 1.0101, 1.0000` at
`λ = φ, 1.8, 1.9, 1.95, 1.99, 2` — **always `> 1`**, decreasing to exactly 1.

And at the group values the failure is not just asymptotic, it is **total**:

> **Corollary T2-A′ `[PROVED, exact — §4/P1b]`.** For every **even** `q`,
> `ψ_1^{q/2}(−λ_q/2) = ∞`. The forward `ψ_1`-orbit of the interval's own endpoint is
> **unbounded**, so no bounded set — a fortiori no disc — is `ψ_1`-invariant.
> (Verified exactly at `q = 8, 10, 12, 14, 20, 22, 30, 50`: pole hit at `k = q/2` in every case.
> For odd `q` the orbit misses `∞` by half a step and its maximum modulus is exactly `λ_q + 1`.)

> **Consequence.** `C1` is not merely singular at its endpoint `λ = 2` (as
> `LAW_TAIL_SCOPING.md` §2.2 anticipated); it **does not exist at any `λ`**. The scoping note's
> phrase "the operator is not trace-class in the naive space **at the anchor**" understates the
> problem by a full regime. **B-I's named rescue candidate is dead.** `PROVED`.

**Why the *reduced* MMS operator escapes this.** Because it does not use the full `n = 1` branch.
The full-branch threshold is

```
   psi_n( I_lam ) subset I_lam   <=>   n >= 1/2 + 2/lam^2 .              (2.1)  PROVED
```

(`ψ_n(I) ⊂ I` iff `|1/(y+nλ)| ≤ λ/2` for all `y ∈ I`, i.e. `nλ − λ/2 ≥ 2/λ`.) For
`λ ∈ (√2, 2)` — i.e. **all `q ≥ 5`** — the threshold sits in `(1, 3/2)`, so branches `|n| ≥ 2` are
full and **only `n = ±1` is partial**. The Markov reduction exists precisely to carve the partial
`n = ±1` branch into `κ_q` pieces on which it *is* full; and `TA_DERIVATION.md` records exactly
this ("the positive n=1 branch IS in the transition set — as block (3→1), and it is a FULL Markov
branch … fatal for single-safety schemes"). The `κ_q` components are not bookkeeping — they are
the *only* thing making the operator nuclear at all.

### 2.3 [PROVED + HEURISTIC] Inducing makes it worse, not better

The classical remedy for a parabolic branch is inducing/acceleration (`CITATION`: Isola,
*On the spectrum of Farey and Gauss maps*, Nonlinearity 15 (2002) 1521–1539, arXiv:math/0308017 —
constructs spaces on which the Farey (parabolic) and induced Gauss operators are simultaneously
treatable; Prellberg–Slawny; Prellberg, *Towards a complete determination of the spectrum of a
transfer operator associated with intermittency*). Applied here, one accelerates through runs of the
digit `±1`, giving the induced alphabet

```
   A(lam) = { psi_1^k o psi_n : k >= 0, |n| >= 2 }  u  { psi_{-1}^k o psi_n : ... } .
```

> **Lemma T2-B.** `|{ψ_1^k : k ≥ 0}| = q` at `λ = λ_q` (since `ψ_1 = R` has order `q` in
> `PSL(2,R)`), and `= ∞` at `λ = 2`. `PROVED` (§1.1).

So the induced alphabet is **finite of size `≍ q·(alphabet in n)` at `λ_q`** and **infinite at
`λ = 2`**. Its cardinality is a function of the **rotation number**

```
   nu(lam) := arccos(lam/2) / pi ,     nu(lam_q) = 1/q ,   nu(2) = 0 ,
```

being rational: `|{ψ_1^k}| = ` denominator of `ν(λ)` when `ν(λ) ∈ Q`, `= ∞` otherwise. `PROVED`.

The `k`-sum in the accelerated weight behaves oppositely in the two regimes, and this is the
quantitative heart of the matter:

```
   lam = 2 :   |(psi_1^k)'| ~ k^{-2}  on compacts   ->  sum_k k^{-2s}  converges for Re s > 1/2,
                                                        continues meromorphically (Hurwitz),
                                                        poles at the real lattice s = (1-k)/2
   lam = lam_q : psi_1^k is a ROTATION, |(psi_1^k)'| = O(1), and there are exactly q terms
                                                    ->  finite sum of size ~ sum_{k<=q} k^{-2 sigma}
                                                        ~ q^{1-2 sigma}  ->  q^{1/2}  at sigma = 1/4
```

`PROVED` for the `λ = 2` derivative decay (from `R^k = [[1−k,−k],[k,1+k]]`, derivative
`(kz+1+k)^{-2}`); `HEURISTIC` for the `q^{1-2σ}` estimate (the elliptic iterates track the parabolic
ones for `k ≪ q` and wrap for `k ~ q`; float-level reasoning, no uniform bound proved).

> **This is the sharpest single statement in the note.** At the anchor height `σ = Re s = 1/4`, the
> `λ = 2` object exists **only by analytic continuation in `s`**, while the `λ_q` objects are honest
> finite sums that **grow like `q^{1/2}`**. Analytic continuation in `s` and the limit `q → ∞` do
> not commute for the accelerated representation. Any construction that tries to be λ-analytic
> *through* the accelerated `k`-sum is asking a divergent finite sum to equal a continued value.

**Corollary (the `ζ(2s)` match the brief asked about — and it is real).** The parabolic `k`-sum
`Σ_k k^{−2s}` *is* `ζ(2s)`, up to the Hurwitz shift. The `λ = 2` scattering determinant is
`det Φ_θ = g(s)² E(s)` with `g = Λ(2s−1)/Λ(2s)` (`LAW_ANCHOR_T1_THETA.md` (DET), `PROVED`), and the
poles at `s = ρ/2` are **exactly the zeros of the `ζ(2s)` in the denominator**. So the theta-side
parabolic factor and the anchor's `Λ(2s)` structure **do** match, as hoped — and the match carries a
prediction that the repo's own data already confirm:

> at `λ = λ_q` the parabolic `k`-sum is **truncated at `k ≍ q`**, so no exact `ζ(2s)` factor and
> hence **no exact pole at `s = ρ/2`**; the `λ_q` divisor can only *approach* `s_∞` as `q → ∞`.

That is precisely `LAW_ANCHOR_T1_THETA.md` §6.2's puzzle ("no `q=7,8` scanned pin at `Re = 0.25`")
and `LAW_PROBES_D1_B1.md`'s finding (pins near `s_∞`, migrating at `q^{-2}`, never *at* `s_∞`).
`HEURISTIC`, but it is the first mechanism offered for either observation, and it explains both.

### 2.4 [PROVED] The obstruction is group-theoretic, so no cleverer operator escapes it

Strip away the analysis. Any λ-analytic carrier must be an expression indexed by a set that does
not move with `λ` — a branch alphabet, or (equivalently, on the zeta side) the set of primitive
cyclic words in the free product `⟨S⟩ * ⟨T⟩ ≅ Z/2 * Z`. The natural λ-analytic candidate is

```
   D_word(s, lam) := prod_{[w] prim. cyclic word, |tr w(lam)| > 2}  prod_{k>=0} ( 1 - e^{-(s+k) l_w(lam)} ),
   l_w(lam) = 2 arccosh( |tr w(lam)| / 2 ),      tr w(lam) in Z[lam]  (a POLYNOMIAL in lam).
```

Each factor is genuinely analytic in `λ`. But:

> **Lemma T2-C.** At `λ = λ_q` the map {cyclic words in `Z/2 * Z`} → {conjugacy classes of `G_q`}
> has infinite fibres: `R^a` and `R^{a+q}` are the *same* group element. Hence `D_word(s, λ_q)`
> repeats every factor infinitely often and diverges identically; its divisor is not the Selberg
> divisor of `G_q` for any `q`. `PROVED`.

Conversely, the correct index set — cyclic words in `Z/2 * Z/q` — **is** the one that moves with
`λ`. So:

> **B-I and B-II are one obstruction, not two.** The group `G_λ` fails to exist off `{λ_q}` (B-II)
> *for the same reason* the operator's alphabet fails to be λ-stable (B-I): the relation `R^q = 1`,
> i.e. the rationality of the rotation number `ν(λ) = arccos(λ/2)/π`. Every λ-analytic construction
> is blind to `R^q = 1`; every construction that sees `R^q = 1` is a function of `ν(λ)`'s
> denominator and therefore not λ-analytic.

### 2.5 [HEURISTIC] A rigidity consequence, recorded but not load-bearing

If `D(s, ·)` were holomorphic on a complex neighbourhood of `λ = 2`, then — since
`λ_q → 2`, an **accumulation point** — the values `{D(s, λ_q)}_{q ≥ Q₀}` would determine `D(s, ·)`
entirely, hence determine `D(s, λ_q)` for **all** `q ≥ 3`. Under (T2)(i) with equality of divisors
this would make the Selberg zeta of `G_5` a consequence of those of `G_q`, `q ≥ 100`, by analytic
continuation in `λ`. That is not a contradiction — (T2)(i) only demands *containment* of divisors,
so `D = Z_{G_q} · (junk_q)` is permitted and the rigidity dissolves into the junk — but it is a
loud "too strong to be true" flag on the literal formulation. `HEURISTIC`, non-load-bearing;
recorded so nobody mistakes it for a proof.

### 2.6 Literature status (scouted this session, honest)

`CITATION`/`GAP` mixed. Sources actually retrieved and what they do **not** give:

- Ruelle, *Zeta-functions for expanding maps and Anosov flows*, Invent. Math. **34** (1976) 231–242
  — `det(1−L) = ζ` for real-analytic expanding maps. **Does not** treat a parameter family whose
  branch/Markov structure changes.
- Fried, *The zeta functions of Ruelle and Selberg I*, Ann. Sci. ENS **19** (1986) 491–517 —
  `det(1−L_s) = Z_Γ(s)`, the `s` variable only. **No second variable.**
- Isola, Nonlinearity **15** (2002) 1521 — parabolic Farey vs induced Gauss on common spaces.
  **Does not** give an explicit determinant ratio ("parabolic factor") relating the two.
- Wolpert, *Spectral limits for hyperbolic surfaces I, II*, Invent. Math. **108** (1992) 67–129 —
  spectral degeneration under **pinching**. **Not** our regime (no pinching; §4 confirms this).
- **`GAP`, and this is the honest headline of the scout:** **no** published theorem on
  (a) jointly-`(s,λ)`-holomorphic Fredholm determinants across a Markov-structure change;
  (b) spectral/zeta behaviour under **cone-angle → 0** at bounded area;
  (c) `lim_{q→∞}` of the Hecke-group spectrum, resonances, or Selberg zeta.
  This re-confirms `LAW_TAIL_SCOPING.md` §1.1's finding: the tail is unclaimed territory. It also
  means **no import will do this for us.**

---

## 3. The replacement: (T2′), Vitali + Hurwitz instead of Rouché

### 3.1 The observation that unlocks it

Rouché requires a *continuous deformation*. Hurwitz requires only a **sequence** of holomorphic
functions converging locally uniformly. `{λ_q}_{q ≥ Q₀}` **is** a sequence. Nothing in the
conclusion of `LEMMA T` ("for all `q ≥ Q₀`, `G_q` has a zero within `O(q⁻²)` of `s_∞`") needs a
value of the determinant at a non-group `λ`. **(T2)'s joint holomorphy was a convenience of method,
not a requirement of the theorem.** Dropping it dissolves B-II outright.

Furthermore, once the argument is phrased on the sequence, the natural objects are the **Selberg
zeta functions themselves**, not transfer-operator determinants. The transfer operator then plays
**no role in the tail argument at all** — it is needed only for the certified finite base
`q ≤ Q₀`, where the repo already has it (R5 at `q=5`, lane_f at `q=7`). This is a large
simplification and it retires the entire `κ_q → ∞` worry from the tail.

### 3.2 (T2′) stated

> **(T2′) — replacement for (T2).** There exist `Q₁` and an open connected `Ω̃ ⊂ C` containing
> both `s_∞ = ρ₁/2` and the half-plane `{Re s > 1}`, such that:
>
> **(T2′-a) [uniform normal family]** there are `A, B < ∞` independent of `q` with
> `|Z_{G_q}(s)| ≤ A · exp( B (1+|s|)² )` for all `s ∈ Ω̃` and all `q ≥ Q₁`;
>
> **(T2′-b) [convergence on a set with accumulation]** `Z_{G_q}(s) → Z_{Γ_θ}(s)` pointwise on
> `{Re s > 1}`.
>
> **Then** by **Vitali–Montel** (`CITATION`, classical: a locally uniformly bounded family of
> holomorphic functions on a domain, convergent on a set with an accumulation point, converges
> locally uniformly on the whole domain) `Z_{G_q} → Z_{Γ_θ}` locally uniformly on `Ω̃`.
>
> **And then** by **Hurwitz** (`CITATION`, classical): `Z_{Γ_θ}` has a zero of order `2` at `s_∞`
> (from `(T1)` + the scattering→Selberg transport, obligation U3) and `Z_{Γ_θ} ≢ 0`; so for every
> `r ∈ (0, 1/8)` with `Z_{Γ_θ} ≠ 0` on `∂D(s_∞, r)` there is `Q₀(r)` such that for all `q ≥ Q₀`,
> `Z_{G_q}` has **exactly 2 zeros in `D(s_∞, r)`**, counted with multiplicity.
>
> Each such zero has `Re s ≤ 1/4 + r < 1/2 − (1/8 − r)`: **off the critical line, margin
> `η = 1/8 − r > 0`.** ∎

The Rouché one-liner of `LEMMA T` is replaced by a Hurwitz one-liner; **all** content is in
(T2′-a) and (T2′-b), which are §5's U1 and U2.

### 3.3 Why the two hypotheses are the *right* pair (and are plausible)

- **(T2′-a)** is a growth bound, and the Selberg/Weyl relation makes it uniform *for free at the
  level of the divisor*: `N_q(T) + M_q(T) ~ (|F_q|/4π) T²` with
  `|F_q| = vol(G_q\H) = π(1 − 2/q) ≤ π` for **every** `q` (`PROVED`, `M1F` §1.5). The area is
  **uniformly bounded**, so the zero-counting of `Z_{G_q}` in a box of height `T` is uniformly
  `≤ (π/4π)T²·(1+o(1))`, and a Hadamard factorization of order 2 with `q`-independent counting
  gives exactly the shape of bound (T2′-a) demands. This is the payoff of
  `LAW_TAIL_SCOPING.md` §1.1's central fact — **the family does not degenerate** — used for the
  first time as an *analytic* asset rather than a caution.
- **(T2′-b)** lives in `Re s > 1`, where `Z` is an absolutely convergent Euler product over closed
  geodesics. It needs only (i) convergence of each geodesic length (`PROVED` below), and (ii) a
  `q`-uniform tail bound on the geodesic counting. §4 tests it directly and it passes at rate
  `q^{-2}`.

### 3.4 [PROVED] Length-spectrum convergence, word by word — the exact statement

Fix a cyclically reduced word `w = S R^{a_1} S R^{a_2} … S R^{a_m}` with `a_i ∈ Z\{0}`. Substituting
`R = R(λ) = [[0,−1],[1,λ]]` makes `w(λ)` a matrix of **polynomials in `λ` with integer
coefficients**, and `tr w(λ) ∈ Z[λ]` — **one** polynomial, evaluated at `λ_q` to give an element of
`G_q` and at `λ = 2` to give an element of `Γ_θ`. (The `a_i` are read mod `q` only when asking
*which* element of `G_q` it is; the polynomial itself does not depend on `q`.) Hence for **fixed**
`w` with all `|a_i| < q/2`,

```
   tr_w(lam_q) -> tr_w(2),      l_w(lam_q) -> l_w(2)      as q -> infinity,
```

with error `O(2 − λ_q) = O(q^{-2})`, since `2 − λ_q = π²/q² + O(q⁻⁴)` (`PROVED`; checked:
`q=22`: `2.0357e−2` vs `π²/q² = 2.0392e−2`; `q=80`: `1.54193e−3` vs `1.54213e−3`).

**Worked exact instance — the systole.** The class `[S R²]` has
`S R² = [[−λ, 1−λ²],[−1, −λ]]`, `tr = −2λ`, so

```
   l( [S R^2] ) = 2 arccosh( lam )     EXACTLY, for every lam in (1, 2].         (3.1)  PROVED
```

`§4/P2` finds `[S R²]` (and its inverse `[R^{-2} S]`) to be the **systole-realising class for every
`q` tested and for `Γ_θ`**, giving

```
   sys(Gamma_theta) - sys(G_q) = 2( arccosh 2 - arccosh lam_q )
                               = (2/sqrt 3)(2 - lam_q) + O((2-lam_q)^2)
                               = 1.15470 * (2 - lam_q) + O(q^{-4})               (3.2)
```

Measured ratio `gap/(2−λ_q)`: `1.33877, 1.23954, 1.19434, 1.17450, 1.16430, 1.15894, 1.15622,
1.15529` at `q = 5,7,10,14,20,30,50,80` → **`2/√3 = 1.154701`.** `PROVED` for (3.1)–(3.2);
`HEURISTIC` for "`[S R²]` is the systole" (enumeration to a finite radius, §4).

**Consequence, and it matters for U1/U2:** `sys(G_q)` is **increasing** in `q` to
`2 arccosh 2 = 2.633916`, with `sys(G_5) = 2.12255` the smallest. **No pinching, no short
geodesics, uniformly in `q`** — exactly what a `q`-uniform Euler-product bound needs. (An
independent area argument points the same way: a simple closed geodesic of length `ℓ` carries an
embedded collar of area `2ℓ/sinh(ℓ/2) → 4` as `ℓ → 0`, which exceeds `|F_q| < π` once
`ℓ < 2.4656`. `CITATION`-shaped — Buser's collar lemma — but the **orbifold** version with cone
points needs pinning before it can be quoted, and `sys(G_5) = 2.1226 < 2.4656` shows the naive
form is not directly applicable. Label: `GAP`, see U2b. The measured monotonicity is the honest
evidence.)

### 3.5 What (T2′) does **not** fix

It does **not** produce a rate, and therefore does **not** by itself produce `Q₀`. Vitali+Hurwitz is
qualitative. An explicit `Q₀` needs a quantitative version of (T2′-b) — a rate for
`|Z_{G_q} − Z_{Γ_θ}|` on `∂D(s_∞, r)` beaten against `min_{∂D}|Z_{Γ_θ}|`, which is the original
(T3) with `ε(λ)` replaced by `ε(q)`. §4 measures `ε(q) ≍ C q^{-2}` at three test points in
`Re s > 1`; propagating that to `Re s = 1/4` needs the same uniform bound U1. See U5.

---

## 4. Numeric sanity probe — **NON-RIGOROUS**

Script `lane_g/law_probes/probe_t2_shape.py`; receipts `t2_shape.json` (L=5.0, BFS radius 7.0) and
`t2_shape_L6.json` (L=6.0, radius 9.0). float64, no interval arithmetic, no certificate. Everything
in this section is `HEURISTIC` by construction and is a **shape check, not a certification.**

**Deviation from the brief, flagged loudly.** The brief asked for `det(1 − L_{s,λ})` on the
unreduced/induced operator at `λ = 1.8, 1.9, 1.95, 2.0` near `s_∞`. **That probe is not
well-posed**: §2.2 proves no fixed disc carries the unreduced operator at any of those `λ`, so
there is no matrix to build and no determinant to evaluate. Rather than produce a number from an
operator that does not exist, this section (P1) **demonstrates the non-existence quantitatively at
exactly the requested `λ` grid**, and then (P2, P3) runs the probe that *is* well-posed and that
tests the construction actually being proposed. Note the requested `λ` grid corresponds to
`q ≈ 6.97, 9.89, 14.02, ∞` — so `q = 7, 10, 14, ∞` are included in P2/P3 and the grid is honoured.

### P1 — fixed-disc invariance fails on the requested λ grid

| `λ` | equivalent `q` | `ψ_1` type | `|ψ_1'(−λ/2)|` | `max` of 40-step `ψ_1`-orbit of `−λ/2` | full-branch threshold (2.1) |
|---|---|---|---|---|---|
| 1.618034 | 5.00 | elliptic 36.000° | **1.527864** | 2.618 | `n ≥ 1.2639` |
| 1.800000 | 6.97 | elliptic 25.842° | **1.234568** | 4.00 | `n ≥ 1.1173` |
| 1.900000 | 9.89 | elliptic 18.195° | **1.108033** | **17.41** | `n ≥ 1.0540` |
| 1.950000 | 14.02 | elliptic 12.839° | **1.051940** | **98.89** | `n ≥ 1.0260` |
| 1.990000 | 31.40 | elliptic 5.732° | **1.010076** | 2.42 | `n ≥ 1.0050` |
| 2.000000 | ∞ | **parabolic** at `−1 = −λ/2` | **1.000000** | 1.00 | `n ≥ 1.0000` |

`|ψ_1'| > 1` at the interval endpoint for every `λ < 2` and `= 1` at `λ = 2`: the `n=1` branch is
**expanding-or-neutral** there, never contracting.

The orbit column is the same fact seen dynamically, and at the *group* values `λ = λ_q` it sharpens
to an exact statement. In the coordinate `w = (z − z₊)/(z − z̄₊)` (with `z₊` the upper fixed point)
`ψ_1` is the rotation `w ↦ e^{−2iθ}w`, `θ = π/q`; the real line is `|w| = 1`; the starting point
`−λ/2` sits at `w = −1`, exactly **antipodal to `∞`** (which is `w = 1`). So the orbit reaches `∞`
iff `k·π/q ≡ π/2`, i.e. iff `k = q/2`:

> **[PROVED, exact, verified]** For every **even** `q`, `ψ_1^{q/2}(−λ_q/2) = ∞`.
> Verified exactly at `q = 8, 10, 12, 14, 20`: the pole is hit at `k = 4, 5, 6, 7, 10 = q/2`.
> For **odd** `q` the orbit misses `∞` by half a step and its maximum modulus is exactly `λ_q + 1`
> (`2.61803` at `q=5`, `2.80194` at `q=7` — matching `λ+1`).

So for every even `q` the `ψ_1`-orbit of the interval endpoint is **unbounded** — no bounded set,
let alone a disc, contains it. (Non-integer `q_equiv` rows, e.g. `λ = 1.99` with `q_equiv = 31.40`,
show only a moderate maximum because the rotation grid misses the phase of `∞` by up to half a step;
the reachable modulus is `≈ √(4−λ²)/(phase gap)`. That is a phase-alignment artefact, not evidence
of an invariant disc — Lemma T2-A settles the question for **all** `λ` independently of any orbit.)
**Confirms §2.2. `PROVED` for the even-`q` statement; `HEURISTIC` for the rest of the table.**

### P2 — length-spectrum convergence `G_q → Γ_θ`

Method: BFS the group ball `{g : ‖g‖_F² ≤ 2 cosh(r_max)}` in `G_q = ⟨S⟩ * ⟨R⟩`, tracking the
free-product normal form; cyclically reduce; canonicalise up to cyclic rotation; drop imprimitive
classes; keep translation lengths `ℓ ≤ L`. Same for `Γ_θ` (`R` of infinite order).

| `q` | `λ_q` | #classes `ℓ ≤ 5` | systole | `sys(Γ_θ) − sys(G_q)` | Hausdorff dist. of spectra to `Γ_θ` |
|--:|---|--:|---|---|---|
| 5 | 1.618034 | 28 | 2.122550 | 5.1137e−1 | 0.5114 |
| 7 | 1.801938 | 27 | 2.388409 | 2.4551e−1 | 0.2871 |
| 10 | 1.902113 | 26 | 2.517006 | 1.1691e−1 | 0.2917 |
| 14 | 1.949856 | 26 | 2.575021 | 5.8894e−2 | 0.2691 |
| 20 | 1.975377 | 29 | 2.605247 | 2.8669e−2 | 0.2064 |
| 30 | 1.989044 | 25 | 2.621218 | 1.2698e−2 | 0.1317 |
| 50 | 1.996053 | 25 | 2.629353 | 4.5631e−3 | 0.0470 |
| 80 | 1.998458 | 25 | 2.632134 | 1.7814e−3 | 0.0183 |
| **`Γ_θ`** | 2 | **25** | **2.633916** | — | — |

- **Systole-gap exponent (log-log LS, `q ≥ 14`): `−2.0066`.** Identical (to 4 decimals) at the
  larger cutoff `L = 6, r_max = 9`. This is (3.2), and it is `PROVED` there — the probe is a
  consistency check on the enumerator, and it passes.
- **Class count converges** to `Γ_θ`'s (25 at `L=5`; `67` at `L=6` with `q=50,80` also `67`),
  i.e. the geodesic *combinatorics* stabilise. No spurious extra geodesics appear.
- Hausdorff distance decays but noisily (fitted exponent `−1.58` for `q ≥ 14`) — expected, since a
  max over a discrete matching is sensitive to individual near-misses. Reported unsmoothed.
- **No pinching**: `sys` is monotone **increasing** in `q`. The scoping note's "the surface does not
  degenerate" is now checked at the level of the length spectrum, not only the area.

### P3 — truncated Selberg Euler product `Z_{G_q}(s) → Z_{Γ_θ}(s)`

`Z(s) = Π_{[γ] prim, ℓ ≤ L} Π_{k=0}^{12} (1 − e^{−(s+k)ℓ})`, same enumeration as P2.

| `q` | `|Z_q−Z_θ|` at `s=1.5+7.0674i` | at `s=2.0` | at `s=1.2+7.0674i` |
|--:|---|---|---|
| 5 | 1.8077e−1 | 2.7477e−2 | 3.9169e−1 |
| 7 | 1.1895e−1 | 1.4897e−2 | 2.9681e−1 |
| 10 | 6.0455e−2 | 7.3349e−3 | 1.3701e−1 |
| 14 | 3.6296e−2 | 3.6997e−3 | 8.7539e−2 |
| 20 | 1.5514e−2 | 1.7775e−3 | 3.5585e−2 |
| 30 | 6.3294e−3 | 6.6251e−4 | 1.3554e−2 |
| 50 | 2.2762e−3 | 2.3311e−4 | 4.8786e−3 |
| 80 | 8.9106e−4 | 9.0366e−5 | 1.9158e−3 |
| **fitted exponent (`q ≥ 14`)** | **−2.115** | **−2.145** | **−2.180** |
| same at `L=6, r_max=9` | **−2.126** | **−2.100** | **−2.226** |

**Stability**: doubling the geodesic count (25 → 67 classes for `Γ_θ`) moves every exponent by
`< 0.05` and every `q=80` value by `< 6%`. The signal is not an artefact of the truncation.

### 4.1 What the probe does and does not establish

**Establishes (at float level):** `Z_{G_q} → Z_{Γ_θ}` in `Re s > 1` — i.e. **(T2′-b) is true
numerically** — at rate `≍ q^{-2}`, i.e. `≍ (2 − λ_q)`, i.e. **linear in the natural deformation
parameter `ε = 2 − λ`**. Three independent quantities (systole gap, `|Z_q − Z_θ|` at three `s`,
and — from `LAW_PROBES_D1_B1.md` — pin migration distance) all scale as `q^{-2}`. That coherence
across independently computed objects is the strongest single piece of evidence in this note.

**Does not establish:** anything at `Re s = 1/4`. The Euler product does not converge there; the
probe cannot see `s_∞`. Bridging `Re s > 1` to `Re s = 1/4` is **exactly** obligation U1, and no
amount of Euler-product numerics will do it. Also does not establish that the finite-radius
enumeration is complete (BFS radius `r_max` truncates; the counts stabilising across two radii is
evidence, not proof).

---

## 5. Theorem shape and the full obligation ledger

### 5.1 The theorem the route would deliver

> **THEOREM (LAW, tail half) — target.** There is an effective `Q₀` such that for every
> `q ≥ Q₀`, the Selberg zeta function `Z_{G_q}` has a zero `s_q` with
> `|s_q − ρ₁/2| < r` and hence `Re s_q < 1/2 − (1/8 − r)`, for any fixed `r ∈ (0,1/8)`.
> Combined with the certified base `q = 5, 7, …, Q₀` (`lane_g` flagship + `lane_f` + step-3 sweep)
> and the arithmetic exclusion `q ∈ {3,4,6}`: **every non-arithmetic Hecke group `G_q` has a
> Selberg zero off the critical line.**

### 5.2 Obligation ledger

| # | Obligation | Status | Route / note |
|---|---|---|---|
| **U1** | `q`-uniform bound `|Z_{G_q}(s)| ≤ A e^{B(1+|s|)²}` on a domain joining `Re s > 1` to `s_∞`. **THE crux.** | `GAP` | Hadamard factorization of order 2 using the uniform Weyl counting `N_q(T)+M_q(T) ~ (|F_q|/4π)T²`, `|F_q| = π(1−2/q) ≤ π` (`PROVED`); uniform bound in `Re s ≥ 2` from the Euler product (needs U2b); reflect via the Selberg functional equation. Standard-shaped, laborious. Aristotle-able in pieces. |
| **U2a** | `Z_{G_q}(s) → Z_{Γ_θ}(s)` pointwise on `Re s > 1`, word-level part. | `PROVED` (this note, §3.4) | `tr_w(λ) ∈ Z[λ]` is the same polynomial on both sides; `2−λ_q = π²/q²+O(q⁻⁴)`. |
| **U2b** | `q`-uniform tail: `#{prim. classes with ℓ ≤ L} ≤ C e^L` and `sys(G_q) ≥ ℓ₀ > 0`, both uniform in `q`, so the limit passes through the infinite product. | `GAP` | `sys(G_q) = 2 arccosh λ_q ≥ 2 arccosh λ_5 = 2.1226` **if** `[S R²]` is the systole class (§3.4, `HEURISTIC`; proving it is a finite check per `q` plus a uniform argument). Counting: uniform prime-geodesic upper bound at bounded area. Orbifold collar lemma needs pinning. |
| **U3** | Scattering pole of `det Φ_θ` at `s_∞` ⇒ **zero of `Z_{Γ_θ}`** of order 2. | `GAP` — **inherited unchanged** | M1F obligation **N2/G6**, explicitly still open in `LAW_ANCHOR_T1_THETA.md` §4.3 and C14. Blocks *every* version of the route, `(T2)` and `(T2′)` alike. Should be attacked first — it is the cheapest open item and it is textbook-shaped (Selberg functional equation `Z(1−s) = Z(s)·Ψ(s)·φ(s)`). |
| **U4** | `det(1 − L_{s,λ_q}) ↔ Z_{G_q}(s)` for general `q` (the repo's R5 is `q=5`-specific, bound to a named wrapper sha). | `GAP` — **but DEMOTED** | **Under (T2′) the tail argument never touches the transfer operator.** U4 is needed only to consume the certified finite base `q ≤ Q₀`, i.e. once per certified instance, which is how `lane_f` already works. This is (T2′)'s biggest structural saving over (T2). |
| **U5** | Effective `Q₀`: quantitative (T2′-b) on `∂D(s_∞,r)` beaten against `min_{∂D}|Z_{Γ_θ}|`. | `GAP` | Needs U1's constants. §4 gives `ε(q) ≍ C q⁻²` for `Re s > 1` only. `min_{∂D}|Z_{Γ_θ}|` is computable in closed form from `(DET)` + U3 — `LAW_ANCHOR_T1_THETA.md` already supplies the residue `(s−s_∞)²det Φ_θ → −0.14943 − 0.39398i`. |
| **U6** | `Z_{Γ_θ} ≢ 0` and `Z_{Γ_θ} ≠ 0` on some `∂D(s_∞,r)`, `r < 1/8`. | `CITATION` + finite check | Zeros of `Z_{Γ_θ}` are discrete (`Z` entire, not identically zero); pick `r` avoiding them. Cheap. |
| **U7** | Retire from lane text: "(T2) is the crux, and inducing may rescue it." | this note | §2 replaces it: inducing is *anti*-rescue; the crux moves to U1. |

### 5.3 What is retired and what is opened

**Retired (write into the lane text):**
- `LAW_TAIL_SCOPING.md` §2.2's "*What may rescue it: the unreduced Mayer-type operator's branch
  index set … is independent of `q`*" — **the index set is `q`-independent but the operator does
  not exist on any fixed disc, at any `λ`.** Lemma T2-A. Delete the cautious optimism.
- The framing of B-I and B-II as two blockers. They are one: rationality of `ν(λ) = arccos(λ/2)/π`.
- "(T3) is downstream of (T2) and is a routine Cauchy estimate." Under (T2′) the routine part is
  gone; U1 is a genuine growth theorem, not a Cauchy estimate.

**Opened:**
- **U1 is the new crux** and it is a *different kind* of object from (T2): a uniform-in-`q` growth
  bound for a family of entire functions of order 2 whose divisors are uniformly counted. That is
  standard analytic-number-theory machinery, not new operator theory. This is a real change of
  difficulty class, and it is the note's main deliverable.
- **U3 should be run first** (cheapest, blocks everything, textbook-shaped).

---

## 6. Feasibility verdict

> ## **(T2) as posed: STRUCTURALLY-BLOCKED.**
> Not "hard", not "needs inducing" — **blocked**, with three independent `PROVED` obstructions
> (Lemma T2-A: no invariant disc at any `λ`; Lemma T2-B: the induced alphabet's cardinality is the
> denominator of the rotation number; Lemma T2-C: any λ-independent index set has infinite fibres
> at every `λ_q`). Inducing is the named remedy and it **worsens** the situation: it converts a
> `κ_q ≍ q` finite structure into an infinite one exactly at the endpoint, and at `Re s = 1/4` the
> two sides are separated by an analytic continuation that does not commute with `q → ∞`.
>
> ## **The LAW tail: CONSTRUCTIBLE, via (T2′).**
> Vitali + Hurwitz on the sequence `{Z_{G_q}}` needs no interpolation, no non-group `λ`, and no
> transfer operator. The remaining crux (U1) is a `q`-uniform order-2 growth bound, which the
> bounded area `|F_q| ≤ π` makes structurally available. (T2′-b) is `PROVED` at word level and
> confirmed numerically at rate `q⁻²`. The one item that blocks **both** formulations equally is
> **U3**, inherited from M1F and still open.
>
> **Recommended next ticket, in order:** (1) **U3** — the scattering-pole → Selberg-zero transport
> for `Γ_θ` (small, textbook, blocks everything, Aristotle-able); (2) **U1** — the `q`-uniform
> Hadamard bound (the real work; frontier + Aristotle); (3) **U2b** — uniform systole and geodesic
> counting (finite-flavoured, agent-able). **Do not** fund further work on a two-variable
> determinant.

---

## 7. What this note claims and does not claim

**Claims.** (i) Lemma T2-A (`PROVED`): no disc is invariant under `ψ_1` for any `λ ∈ (0,2]`, so the
unreduced fixed-disc determinant does not exist — B-I's named rescue is dead; and Corollary T2-A′
(`PROVED`, exact): for every even `q`, `ψ_1^{q/2}(−λ_q/2) = ∞`. (ii) Lemma T2-B
(`PROVED`): the induced alphabet has cardinality `q` at `λ_q`, `∞` at `λ = 2`, governed by the
rotation number. (iii) Lemma T2-C (`PROVED`): a λ-independent index set has infinite fibres at every
`λ_q`, so B-I and B-II are one group-theoretic obstruction. (iv) (3.1)–(3.2) (`PROVED`): the class
`[S R²]` has length exactly `2 arccosh λ`, giving `sys(Γ_θ) − sys(G_q) = (2/√3)(2−λ_q) + O(ε²)`,
verified numerically to `1.15529` vs `2/√3 = 1.154701` at `q=80`. (v) §3.4 (`PROVED`): word-level
length convergence, since `tr_w(λ) ∈ Z[λ]`. (vi) The (T2′) reformulation, and the observation that
under it the transfer operator leaves the tail argument entirely.

**Does not claim.** No proof that *every conceivable* `D(s,λ)` is impossible — §2.4 rules out the
two natural carrier classes (fixed branch alphabet; word-indexed product) and §2.5 is explicitly
`HEURISTIC`. No proof of U1, U2b, U3, U5 — all are `GAP` with the missing statement written out.
No claim about `Re s = 1/4`: §4's numerics live entirely in `Re s > 1` and cannot see `s_∞`.
No certificate: every number in §4 is float64, no interval arithmetic, no winding computation.
No claim that `[S R²]` is *provably* the systole (finite-radius enumeration only).
No novelty claim for anything in §1.1 or §3.4 — the trace polynomials and the `(2,q,∞)` structure
are classical; the literature scout found no prior work on the `q → ∞` limit, but absence of a
retrieved source is not a prior-art clearance (`GAP`, prior-art scout owed before any paper).

**A refutation was actively sought and one was found** — of the brief's own premise. The brief asked
whether `det(1 − L_{s,λ})` on a fixed disc "works, needs an induced/regularized determinant, or
fails structurally." It fails structurally, and the induced version fails worse. That is reported as
the headline rather than softened, and the numeric probe was redirected to test the construction
that *does* survive rather than to produce a number from an operator that does not exist.
