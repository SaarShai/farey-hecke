# LAW TAIL SCOPING — attack selection for step 4 of the family-law program

Lane G, 2026-08-15. Scope: **scoping/attack-selection only.** No new
certificate, no commit, no other lane's files touched. Every substantive
claim is labelled `PROVED` / `CITATION` / `HEURISTIC` / `GAP`.
`PROVED` = derived here or already machine-certified in this repo with a
receipt named. `CITATION` = imported, with the import stated. `HEURISTIC` =
float evidence or a plausibility argument, explicitly not a proof.
`GAP` = not justified, with the missing statement written out.

Parent ticket: `plans/wayfinder/rh-goals/tickets/family-law-theorem.md` step 4.
Anchors read: `lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md`,
`lane_g/M1F_EISENSTEIN_DERIVATION.md`, `lane_g/M2_NONFACT_WITNESSES.md`,
`lane_g/NO_VERTICAL_LINE_COROLLARY.md`, `lane_g/FAMILY_PREP_CONSTANTS.md`,
`lane_f/F7_CONSTANTS_MANIFEST.md`, `lane_f/F7_4B_REOPT_REPORT.md`,
`lane_k/harvest/hecke_family_q7_q8_scan.json`,
`.worktrees/aletheia-restore/research_notes/UNCONDITIONAL_REDUCTION_2026-06-20.md`.

---

## 0. Verdict up front

**Ranking: (d) > (a) [merged] > (b) > (c).**

The winner is a **merge of (d) and (a)**, and the merge is what makes either
of them viable. Neither survives on its own:

- (a) as the ticket phrases it rests on a **false premise**: `G_q` does **not**
  degenerate as `q → ∞`. Area is `π(1 − 2/q) → π` (bounded), and the limit
  object is the Hecke group at `λ = 2`, `G_∞ = ⟨S, T_2⟩` — which is
  **arithmetic** (the theta group, index 3 in `PSL(2,Z)`). There is no thin
  limit, no pinching, and therefore no degenerating-surface resonance
  literature to import (§1.1, §2).
- (d) as the ticket phrases it ("make the ABSENCE of factorization
  quantitative") has **no anchor**: for non-arithmetic `q` we have no closed
  form for `φ_q` at all, so there is nothing to measure a distance from.

Merged, they become one route with a genuine anchor: **the `λ → 2` arithmetic
anchor**. At `λ = 2` the scattering determinant *is* known in closed form
(M1F's derivation is `p`-generic and the `λ=2` group is arithmetic), its
resonances at `s = ρ/2` are **unconditionally off the critical line** (de la
Vallée Poussin: `Re ρ < 1` ⇒ `Re(ρ/2) < 1/2`), and `2 − λ_q = π²/q² + O(q⁻⁴)`
is a small, explicit perturbation parameter. The tail lemma becomes a
**Rouché/Hurwitz continuation from an arithmetic anchor**, not an asymptotic
expansion of a pin and not a uniform bound on our certification constants.

(b) is **refuted as a uniform strategy** by data already in the repo: the
contraction margin `1 − ρ*(q)` decays like `q^{-1.4}` (three points; §3.2), and
the mechanism is identified — `λ → 2` is a **parabolic degeneration of the
transfer operator** (the `n = 1` branch generator has trace `λ_q → 2`), even
though the *surface* does not degenerate. Every constant in the gate list is
downstream of `1 − ρ*`. (b) survives only as the finite-base engine.

(c) is a **FALSE-FRIEND**, for a sharper reason than the usual type mismatch:
the onset theorem's `q ≥ 22` step works precisely because its margin is
**monotone with a strictly positive limit** (`δ_inf = 5.77e−5 > 0`). Ours is
the same shape of object — an explicit inequality in `λ_q` — with margin
`→ 0`. The mechanism transplants; the sign of the limit does not. §4.

---

## 1. Facts established before evaluating any attack

### 1.1 [PROVED] The `q → ∞` limit is not a degeneration, and it is arithmetic

`vol(G_q\H) = π(1 − 2/q)` (M1F §1.5, re-derived: the `(2,q,∞)` triangle has
area `π(1/2 − 1/q)`, doubled). So `vol → π`: **bounded, no pinching, no thin
limit, no escape to infinite area.** The limit group is `⟨S, T_λ⟩` at
`λ_∞ = 2`, i.e. the `(2,∞,∞)` triangle group, of area `π` — the cone point of
order `q` opens into a second cusp.

`[CITATION — to be pinned]` `⟨S, T_2⟩` is the **theta group** `Γ_θ`, of index 3
in `PSL(2,Z)`, hence arithmetic (area `3·π/3 = π` ✓, matching the triangle
computation — an independent cross-check of the identification, exactly the
check M1F §1.5 runs for `q = 4, 6`). Pin the standard reference before this
appears in a paper; the area agreement is evidence, not the citation.

**Consequence, and it is the single most important fact in this note:** the
Hecke family's `q → ∞` limit lies in the **arithmetic** class, where the
scattering determinant is a ratio of completed zetas and the resonances are
`ζ`-driven. The family therefore runs *from* a non-arithmetic interior *toward*
an arithmetic boundary point at which everything is computable. That boundary
point is the anchor the tail argument has been missing.

`[GAP]` The literature scout (this session, 3–6 sources, honest report)
found **no** published asymptotic expansion of Hecke-group resonances in `1/q`
or `2 − λ_q`; **no** uniform asymptotic for a lowest off-line resonance along
any degenerating family; and **no** existence theorem for off-line Selberg
zeros for any infinite family of Fuchsian groups. It also independently
confirmed that the standard degenerating-surface machinery
(Guillopé–Zworski, Borthwick, Naud, Dyatlov–Zahl) targets **infinite-area /
thin** limits and does not apply here. So the tail is genuinely unclaimed
territory, and the ticket's stated intuition ("degenerates toward the
parabolic/thin limit") must be retired from all lane text.

### 1.2 [PROVED — this note] `λ → 2` is a *parabolic* degeneration of the operator

The MMS branch maps are `θ_n(z) = −1/(z + nλ)`, with Möbius matrices
`M_n = [[0,−1],[1,nλ]]`, `det = 1`, `tr M_n = nλ`. For `n = 1`:

```
tr M_1 = λ_q,   λ_q < 2 for all finite q  ->  M_1 ELLIPTIC (rotation)
tr M_1 -> 2     as q -> infinity          ->  M_1 PARABOLIC (indifferent)
```

(checked: `λ² − 4 = −1.382, −0.753, −0.586, −0.081` at `q = 5, 7, 8, 22`;
float, illustrative). The `n = 1` branch acquires an **indifferent fixed
point** exactly in the limit. This is a degeneration of the *dynamics*, not of
the *geometry* — and it is precisely why the branch-contraction constant
degrades. It is also why the repo's own disc data show the `+1` head blocks
binding: at `q = 7` the worst block at every enlargement cap is `5→3, +1, head`
(`F7_4B_REOPT_REPORT.md` §2–3), and at `q = 5, 7, 8` the "full Markov branches
at inflation 1" lists (`FAMILY_PREP_CONSTANTS.md`) are dominated by `n = ±1`
heads. `PROVED` for the trace statement; `HEURISTIC` for the attribution of the
worst-block identity to it (the correlation is exact at `q = 5, 7, 8`, which is
three points).

### 1.3 [PROVED] Why no *soft* argument closes the tail

Worth recording so nobody re-attempts it. For a cofinite `Γ` with cusps the
Selberg/Weyl relation is `N(T) + M(T) ~ (|F|/4π)T²` where `M` is the winding of
the scattering determinant `[CITATION: standard Selberg trace formula]`. So at
least one of {discrete spectrum, resonances} is infinite. This does **not**
give the law, for two independent reasons: (i) bounding `N(T)` from above is
exactly the Phillips–Sarnak / Selberg-conjecture wall, open; (ii) even granted
infinitely many resonances, they are poles of `φ` in `Re s < 1/2` that could a
priori all be **real**, and the theorem needs `Im ≠ 0`. Both walls are
unconditional-looking and neither is ours to move. **Any proposed tail argument
must produce a specific non-real point.**

### 1.4 [PROVED, repo receipts] The certified/observed pin data, honestly

| q | κ | blocks | certified ρ\* | B (‖L‖₁) | ρ̂ | N | lowest-Im mms+ pin | δ = ½ − Re |
|--:|--:|--:|--:|--:|--:|--:|---|--:|
| 5 | 3 | 11 | 0.697802 | 17.2912 | 0.94834 | 160 | 0.4538952 + 5.7635372 i | 0.0461038 |
| 7 | 5 | 19 | 0.763212 | 20.1696 | 0.91524 | 256 | 0.4751648 + 4.6687438 i | 0.0248342 |
| 8 | 3 | 8 | (float 0.8208) | — | — | (82) | 0.4252310 + 4.3457608 i | 0.0747690 |

Sources: `THEOREM_G5_OFFLINE_ASSEMBLY.md` constants table; `F7_4B_REOPT_REPORT.md`
§3 + `F7_CONSTANTS_MANIFEST.md`; `FAMILY_PREP_CONSTANTS.md` (q=8 is float prep,
**not** certified); `lane_k/harvest/hecke_family_q7_q8_scan.json` (q=7,8 pins are
400-bit Arb *scan* pins, N-stable, **not** winding-certified).

**Two readings that must not be made:**

1. `δ_q` is **not** monotone: `0.0461 → 0.0248 → 0.0748` at `q = 5, 7, 8`. Any
   "the gap is closing" story is refuted by the `q = 8` row. `PROVED` (from the
   table).
2. "The lowest-Im pin" is **not a canonical family member.** It is selected per
   surface by determinant conditioning, not by any structural label. Fitting an
   asymptotic to it is fitting to an artifact. This is the hidden well-posedness
   defect in attack (a) as written, and §2 is the fix: label pins by the
   `λ = 2` anchor instead.

The full scan sets are wider than the lowest-Im pin suggests: at `q = 7` and
`q = 8` there are `mms+` pins at `Re ≈ 0.1535` and `Re ≈ 0.1214`, i.e.
`δ ≈ 0.35`, far off-line. The `mms−` sector is on-line to scan precision at
both `q` (`F7_CONSTANTS_MANIFEST.md` §5; the `q=8` rows above). `HEURISTIC`
(scan, not certified) but strongly suggestive that the off-line phenomenon is
robust and not a near-miss.

---

## 2. Attack (a)+(d) MERGED — continuation from the arithmetic anchor at λ = 2

### 2.1 The lemma that would close the tail

> **LEMMA T (target).** There exist `Q₀`, an explicit `s`-domain
> `Ω ⊂ {0 < Re s < 1/2, Im s > 1}`, and an explicit function `ε(λ)` with
> `ε(λ) → 0` as `λ → 2⁻`, such that:
>
> **(T1) [anchor]** the scattering determinant `φ_∞` of `G_∞ = ⟨S,T_2⟩` has a
> pole at some `s_∞ ∈ Ω` with `Re s_∞ ≤ 1/2 − 2η` for an explicit `η > 0`;
>
> **(T2) [family]** the map `λ ↦ det(1 − L_{s,λ})` (equivalently `λ ↦ Z_λ(s)`
> in a divisor-equivalent form) extends to a function **jointly holomorphic in
> `(s, λ)` on `Ω × (2 − ε₀, 2]`**, whose restriction to `λ = λ_q` is the object
> the certified chain consumes;
>
> **(T3) [quantitative continuity]** `|Z_{λ}(s) − Z_2(s)| ≤ ε(λ)` uniformly on
> `∂D` for a fixed disc `D ∋ s_∞`, `D ⊂ Ω`, with
> `ε(λ) < min_{∂D}|Z_2|`.
>
> Then by Rouché, for every `q` with `2 − λ_q < ε₀` (i.e. `q ≥ Q₀`), `Z_{λ_q}`
> has a zero in `D`, hence a zero with `Re ≤ 1/2 − η`. Combined with the
> certified base `q ≤ Q₀`, this is the law. ∎ (the Rouché step is one line;
> all content is T1–T3.)

### 2.2 What is already known / provable today

**(T1) is essentially in hand and is the strongest asset in this note.**
`[PROVED, modulo the §1.1 citation pin]` `G_∞` is arithmetic; M1F's derivation
of the scattering determinant is **`p`-generic — nothing in M1F §§1–4
specialises `p` until §4.2** (M1F ledger G12). The `g(s) = Λ(2s−1)/Λ(2s)`
factor (M1F §4.3, `PROVED`) is common to every member and supplies poles at
`s = ρ/2` for every non-trivial `ζ` zero `ρ`. By de la Vallée Poussin's
zero-free region `[CITATION, classical]`, `Re ρ < 1`, hence
**`Re(ρ/2) < 1/2` unconditionally, with `Im(ρ/2) ≠ 0`** — an off-line
resonance of the anchor with **no RH assumption**. Under RH the margin is
`η = 1/8` (`Re = 1/4`); unconditionally `η` is whatever the zero-free region
gives at height `Im ρ₁ = 14.13`, which is a computable positive number, and in
fact `Re ρ₁ = 1/2` is verified for the first zeros `[CITATION: Odlyzko /
verified RH to large height]`, giving `η = 1/8` legitimately for a *named*
zero. `s_∞ = ρ₁/2 ≈ 0.25 + 7.0673626 i`, and the repo has **already evaluated
at exactly this point**: `M2_NONFACT_WITNESSES.md`'s control row is
`G_4` at `0.25 + 7.0673625708673465 i`, verdict PASS-CONSISTENT-WITH-ZERO.

Remaining work on (T1): M1F's `Γ₀⁺(p)` computation covers `q = 4, 6`
(`p = 2, 3`). `G_∞ = Γ_θ` has **two cusps**, so it is a `2×2` scattering matrix,
not the one-cusp case M1F treats. The needed statement is the classical
scattering matrix of `Γ_θ` (or of `Γ₀(4)`, to which `Γ_θ` is conjugate), which
is textbook. `GAP: write it down and pin it.` Small.

**(T2) is the crux and is genuinely open.** Two candidate carriers:

- *Transfer-operator carrier.* The MMS reduced operator has `κ_q` components —
  `κ_q = q − 2` (odd `q`), `κ_q = q/2 − 1` (even `q`) (`FAMILY_PREP_CONSTANTS.md`
  manifest). **`κ_q → ∞`**: the matrix size diverges, so the *reduced* family
  is not a holomorphic family in `λ` in any naive sense. `GAP/likely fatal for
  this carrier as stated.` What may rescue it: the *unreduced* Mayer-type
  operator's branch index set is `{n ∈ Z : |n| ≥ 1}`, **independent of `q`** —
  only the reduction to `κ_q` discs is `q`-dependent. Whether the unreduced
  determinant is holomorphic in `λ` near `2`, and whether it has the same
  divisor, is the open technical question. Note the parabolicity of §1.2 sits
  exactly here: at `λ = 2` the `n = 1` branch is indifferent, so the operator is
  **not** trace-class in the naive space at the anchor and the family is
  singular at its own endpoint. The MMS head/Hurwitz-tail split (`L^∞` blocks,
  infinite `n`-sums, already present in every block list) is the standard
  induced-map device for exactly this pathology, which is grounds for cautious
  optimism, not a proof.
- *Scattering carrier.* Work with `φ_λ(s)` directly. Here the obstruction is
  different and cleaner to state: **`{G_{λ_q}}` is a discrete family.**
  `⟨S, T_λ⟩` is discrete and cofinite only at `λ = λ_q` and `λ ≥ 2`; the
  intermediate `λ ∈ (λ_q, λ_{q+1})` are non-discrete. So there is **no
  continuous deformation inside the family**, and Kato / Phillips–Sarnak
  analytic perturbation theory — which needs a continuous family of groups —
  **does not apply**. `PROVED` (the discreteness classification of Hecke groups
  is classical `[CITATION: Hecke 1936]`). This is why (T2) must be carried by an
  *operator/determinant* that is defined for all `λ`, not by a *group* that is
  not.

**(T3)** is downstream of (T2); with a holomorphic carrier it is a Cauchy
estimate plus an explicit `λ`-derivative bound, i.e. routine but laborious.

### 2.3 The single hardest obstruction

**(T2) with the parabolic endpoint.** The perturbation parameter is small
(`2 − λ_q = π²/q² + O(q⁻⁴)`: `0.0204` at `q = 22`, `0.00099` at `q = 100` —
float, illustrative, matching `2 − λ_q` to 3 digits at `q ≥ 22`), and the
target margin `η = 1/8` is **large**. Numerically this is a very favourable
ratio. The difficulty is entirely structural: the object that must be
holomorphic in `λ` up to and including `λ = 2` is the object whose contraction
constant tends to `1` there.

### 2.4 Feasibility: **MEDIUM** (highest of the four; and the only one that
could produce a *theorem* rather than a computation)

### 2.5 First falsification probe (cheap, decisive, ticket-sized)

**Probe D1 — does a pin migrate to the anchor?** Run the existing `lane_k`
harvest scanner (`mms+`, 400-bit Arb, the protocol that produced
`hecke_family_q7_q8_scan.json`) at `q = 12, 16, 22` over the *narrow* window
`Re ∈ [0.15, 0.45]`, `Im ∈ [6.6, 7.6]` — a box around `s_∞ = ρ₁/2 ≈
0.25 + 7.0674 i`, small enough to be cheap (the q=7 full scan was 7533 s over a
17×141 grid; this box is ~10% of that area).

- **Alive** if a pin appears in the box and its distance to `s_∞` shrinks
  monotonically in `q` — ideally like `q^{-2}`.
- **Dead** if pins in that window drift *away* from `s_∞`, or if the region
  empties. Current data are inconclusive and must be reported as such: at
  `q = 7` the nearest pins are `0.2303 + 6.371 i` and `0.4842 + 7.567 i`; at
  `q = 8`, `0.4376 + 7.279 i` and `0.3038 + 7.959 i`. **`HEURISTIC`,
  inconclusive** — which is exactly why the probe is worth running.

**Probe D2 (proof-side, parallel, ~1 day)** — write down the `Γ_θ` (or `Γ₀(4)`)
`2×2` scattering matrix and confirm `det Φ_θ` carries the `g(s)` factor, i.e.
that `s = ρ₁/2` really is a pole for the anchor. Closes (T1). Small, and it is
required for any version of the route.

---

## 3. Attack (b) — uniform machinery bounds

### 3.1 The lemma that would close the tail

> **LEMMA B (target).** There exist `Q₀`, `ρ_max < 1`, `B_max < ∞`, and
> `q`-independent radius and enlargement rules (e.g. `e_B = min(clearance/4,
> 0.15 R)` and a `d_κ`-style tail-disc rule) such that for every `q ≥ Q₀` the
> resulting certified constants satisfy `ρ*(q) ≤ ρ_max`, `ρ̂(q) < 1`,
> `B(q) ≤ B_max`, and `F_R(N(q)) < 0.1 m₀(q)` with `N(q)` explicit.

Note this is **not yet the law**: Lemma B makes the *machinery* uniform, but
each `q` still needs its own winding computation, and there are infinitely many.
Lemma B closes the tail only if paired with a `q`-uniform *existence* argument
for the pin — i.e. with (a)+(d) anyway. **This is a structural weakness of (b)
that the ticket's phrasing hides.** `PROVED` (by inspection of the 8-link
chain: link 1 is a per-`q` finite computation with no uniform-in-`q` content).

### 3.2 What is known today — and it refutes the lemma

`1 − ρ*` from the repo (`FAMILY_PREP_CONSTANTS.md` float optimum, the only
series computed the same way at three `q`):

```
q = 5:  rho* = 0.659689   1-rho* = 0.340311
q = 7:  rho* = 0.782264   1-rho* = 0.217736
q = 8:  rho* = 0.820778   1-rho* = 0.179222
power-law fits (float, illustrative):  1-rho* ~ q^-1.33 / q^-1.36 / q^-1.46
                                        (pairs 5-7, 5-8, 7-8)
N-needed = log(1e-7)/log(rho*):  39, 66, 82
```

Three points, one fitted exponent — `HEURISTIC`, not a proof. But the *mechanism*
is `PROVED` (§1.2): the binding branch is `n = ±1`, whose generator trace is
`λ_q → 2`, so its contraction is lost in the limit. `1 − ρ* → 0` is therefore
the expected behaviour and the numbers agree. **Lemma B's `ρ_max < 1` is
false as stated.**

Downstream consequences, all `PROVED` given `ρ* → 1`: `N ≳ 1/(1−ρ*) ~ q^{1.4}`;
matrix size `κ_q · N ~ q^{2.4}`; determinant cost superlinear in that. Block
count grows linearly (`4κ−1` odd, `3κ−1` even — checked against the `q=5,7,8`
lists). `B` is the mildest constant (`17.29 → 20.17`, `q=5 → 7`) and is the one
plausibly uniformly bounded, but it is not the binding one.

Genuinely transferable from `q = 7`, and worth banking regardless of which
attack wins: the **relative enlargement cap** `e_B = min(clearance/4, 0.15R)`
(`F7_4B_REOPT_REPORT.md` §2) is `q`-independent *by construction* — it fixes
`η = R/R_enl = 0.8696` for every block at every `q`. That was a real porting
defect fixed by a genuinely scale-free rule, and it is the correct template for
step 2 of the ticket (template hardening). It does not, however, rescue `ρ*`.

### 3.3 Hardest obstruction

`ρ* → 1` is not an artifact of the disc optimizer; it is the parabolicity of
the `λ = 2` endpoint. Beating it requires **inducing** (accelerating) the
`n = ±1` branches — i.e. re-deriving the MMS reduction with the head blocks
also summed into `L^∞`-type families, which is a new operator-theoretic
construction, not a constant re-tune.

### 3.4 Feasibility: **LOW** as a tail argument. **REQUIRED** as the finite base.

Keep (b) alive and funded as the engine for step 3's instance sweep
(`q = 8..Q₀`), where every gate demonstrably passes and the constants are merely
uncomfortable. Do not present it as a route to the law.

### 3.5 First falsification probe

**Probe B1 (hours).** Run the existing float disc optimizer at
`q = 10, 12, 16, 22, 30` and plot `1 − ρ*` vs `q`. Three points do not
establish an exponent. If `1 − ρ*` *plateaus* above ~0.05, (b) is resurrected
and this note's ranking must be revised. If it continues as `q^{-1.4}`, (b) is
closed as a tail route and the finding is banked as a negative. Cheap: the
optimizer is `float64`, `~10³–10⁵` grid points per `q`
(`FAMILY_PREP_CONSTANTS.md` §Disc optimization).

---

## 4. Attack (c) — onset-theorem transplant: **FALSE-FRIEND**

### 4.1 What actually made the onset `q ≥ 22` step work

From `UNCONDITIONAL_REDUCTION_2026-06-20.md` (in the `aletheia-restore`
worktree) and its Lean sources: the `q ≤ 21` cap was purely a **hard-coded
6-step window** (`Fwindow6`). Lifting it parametrized the window as
`L_blk q = ⌈33q/256⌉ + 2` and reduced the whole `q ≥ 22` claim to **two
explicit scalar inequalities**:

```
cos_sq_lt        : cos(33*pi/512)^2  <  24/25
arc_coverage_ineq: 2*arccos(2*sqrt6/5)/pi  <  33/256
```

i.e. the window slope `33/256 = 0.128906` strictly exceeds the arc-fraction
limit `0.128190`. The uniformity is a **three-distance / rotation-arc
pigeonhole**, and its margin is monotone decreasing in `q` **to a strictly
positive limit**: `δ_inf = 3/(25cos²(33π/512)) − 1/8 = 5.7719e−5 > 0`, with
`margin ≈ δ_inf + C₁π/q`. Not compactness, not a limit argument — an explicit
inequality with positive limiting headroom.

### 4.2 Why it does not transplant — three independent reasons

1. **Type.** `X_Ω(q) = inf over Tgen-invariant measures of essSup(P)` — an
   `L^∞` support edge / minimizing-measure extremal quantity, machine-verified
   in that form (`per_q_Xomega_lb_*`). A resonance is the location of a zero of
   an analytic determinant. There is no inf-of-essSup formulation of "`Z_λ` has
   a zero at `s`", and the DO-NOT-RE-CHASE ledger records that
   `λ = 2cos(π/q)` is a serial false friend precisely across this
   `L^∞`/spectral boundary.
2. **Sign of the limiting margin — the decisive one.** The onset argument is
   uniform because its margin tends to `+5.77e−5`. The resonance machinery's
   corresponding margin is `1 − ρ*(q)`, which tends to `0` (§3.2). Even if one
   could manufacture the type match, the mechanism would deliver
   "`margin → 0`", i.e. no `Q₀`.
3. **The residual is a different kind of object.** The onset's one open
   interface is `hpin`, the in-domain residency `D_{N+j} > 1` — a *geometric*
   orbit fact, provably **not** derivable from positivity alone (the Lean
   `hpin_not_unconditional` scaling counterexample: `Qp` scales as `ε²` while
   `Blam²` is fixed, so radius forcing fails for every `μc`). Its resonance
   analogue would have to be "the certified box contains a zero", which is the
   thing to be proved, not an interface.

### 4.3 Feasibility: **FALSE-FRIEND.** Recommend a DO-NOT-RE-CHASE entry.

One thing *is* worth stealing, and it is methodological rather than
mathematical: **the shape of the reduction.** The onset program's win was
identifying that a single hard-coded constant (`Fwindow6`) was the only thing
blocking uniformity, parametrizing it, and reducing to a named scalar
inequality. The resonance chain's analogue of `Fwindow6` is the pair
(`N`, disc radii) — and `F7_4B_REOPT_REPORT.md` already found one such
hard-coded constant (the enlargement rule) and made it scale-free. That
methodology should be applied deliberately across the chain. It is process
transfer, not proof transfer.

### 4.4 First falsification probe

None needed; (c) is closed on argument. If a probe is wanted, it is Probe B1:
if `1 − ρ*` plateaued, reason 2 above would weaken and (c) could be reopened.

---

## 5. Ranked recommendation

| rank | attack | feasibility | one-line reason |
|---:|---|---|---|
| **1** | **(d)+(a) merged: Rouché continuation from the `λ = 2` arithmetic anchor** | **MEDIUM** | the only route with a *provable* off-line anchor (`s = ρ/2`, unconditional via de la Vallée Poussin) and an explicit small parameter (`2 − λ_q ≈ π²/q²`); the whole difficulty is concentrated in one clean statement (T2) |
| 2 | (b) uniform machinery bounds | **LOW** as tail, **REQUIRED** as base | `1 − ρ* ~ q^{-1.4} → 0`, mechanism identified (parabolic `n=1` branch); and even if it held it would not by itself close an infinite tail |
| 3 | (a) standalone pin asymptotics | **LOW** | ill-posed without a canonical pin label; `δ_q` non-monotone (`0.046, 0.025, 0.075`); no literature; false "degeneration" premise |
| 4 | (c) onset transplant | **FALSE-FRIEND** | onset uniformity needs a margin with positive limit; ours tends to zero — plus the `L^∞`/spectral type mismatch |

**Also retired by this note (write into the lane text):** the phrase
"`G_q` degenerates toward the parabolic/thin limit as `q → ∞`". False. The
surface does not degenerate (area `→ π`); the *transfer operator* does
(parabolic `n = 1` branch); the *limit group is arithmetic*. The third clause
is the asset.

---

## 6. Concrete next ticket-sized step for the winner

**Ticket `law-tail-anchor-probe` — two parallel legs, both cheap, both
decisive at their own level.**

- **Leg 1 (proof, ~1 day, no compute).** Write down the scattering matrix of
  `G_∞ = ⟨S, T_2⟩` from first principles by the *same* method as
  `M1F_EISENSTEIN_DERIVATION.md` §3 (allowed-moduli count against the constant
  term), using the two-cusp structure. Deliverable: `φ_∞` in closed form,
  `det Φ_∞` exhibited with its `g(s) = Λ(2s−1)/Λ(2s)` factor, and the
  statement, unconditional: *`G_∞` has a resonance at `s = ρ₁/2 ≈ 0.25 +
  7.0673626 i` with `Re < 1/2`.* Plus the `Γ_θ ≅ Γ₀(4)`-class citation pinned.
  This is (T1) and it is required by every version of the route.
  **Aristotle-able sub-items:** the moduli counts and the Euler-product
  restriction lemma, exactly as M1F's A-4.
- **Leg 2 (numeric, Probe D1, ~1–2 h of Arb per `q`).** The narrow-box scan at
  `q = 12, 16, 22` around `s_∞`, per §2.5. Deliverable: a table of nearest-pin
  distance to `s_∞` vs `q`, with an explicit alive/dead verdict against the
  `q^{-2}` prediction.

**Gate.** If Leg 2 shows migration toward `s_∞`, open the real ticket —
(T2): *is there a determinant, defined for all `λ` in a left-neighbourhood of
`2`, holomorphic in `(s, λ)`, whose `λ = λ_q` divisor is the Selberg divisor of
`G_q` and whose `λ = 2` divisor is that of `G_∞`?* — and route it to a
frontier + Aristotle pairing. If Leg 2 shows no migration, the merged route
loses its anchor and the program should fall back to the ticket's own stated
fallback (finite certified family `q ≤ Q₀` + dichotomy + mechanism), which
`family-law-theorem.md` already judges publishable.

**Run Probe B1 (§3.5) alongside**: hours of float, and it either closes (b) as a
tail route with a banked negative or overturns this note's ranking. Cheap
insurance against a three-point extrapolation.

---

## 7. What this note does not claim

No new certificate. No theorem. The `1 − ρ* ~ q^{-1.4}` law is a three-point
float fit, labelled `HEURISTIC` throughout, and Probe B1 exists to test it. The
`Γ_θ` identification of `G_∞` is corroborated by an area cross-check but its
citation is unpinned. (T2) is stated, not proved, and is honestly the crux —
this note argues only that it is the *right* crux, i.e. a single clean analytic
question with a provable anchor on one side, rather than an open-ended
constants fight. `δ_q` is not claimed to have any asymptotic behaviour; the
data refute monotonicity and nothing more.
