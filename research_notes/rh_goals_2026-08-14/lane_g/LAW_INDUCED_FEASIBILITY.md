# LAW INDUCED — is there a FIXED-DIMENSION transfer operator for the Hecke family? Literature verdict

**Date:** 2026-08-16. **Lane G, reading + feasibility scout. No proofs, no probes, no code run.**
**Parents:** `LAW_U1EFF_ENTRYWISE.md` (the kill: `κ(q) = q−2` grows, no fixed-dimension `θ`-limit
matrix, `λ = 2` partition countably infinite with an indifferent fixed point at `−1`; entry-wise
`q^{−2}` CONFIRMED = Lemma E); `LAW_B5J_JENSEN.md` §6 item 2 ("induce / accelerate … whether the
induced system's determinant relates to `det(1 − L_s)` cleanly is the question to settle first, and
it is a literature question"); `LAW_T2_DETERMINANT.md` §2.2–2.6 (Lemma T2-A/B/C).

**Status labels:** `PROVED-cited` (in a retrieved source, quoted) / `PROVED-repo` (already proved in
a parent note) / `MEASURED` / `INFERRED` (my inference from two cited facts, flagged as such) /
`GAP`.

**No git was run. No existing file was modified.**

---

## 0. Verdict up front

> ### **The question is ANSWERED, and the answer is NO for our branch of the family — but the answer is sharp, it is proved rather than merely unfound, and it comes with two genuinely new facts that the lane did not have.**
>
> **(V1) A fixed-dimension, parameter-analytic transfer-operator representation of the Hecke
> triangle family EXISTS, is published, and is exactly the object the brief describes — but it lives
> on `w > 2`, the *infinite-volume* branch, not on our `λ_q = 2cos(π/q) < 2` branch.**
> `PROVED-cited` (Fedosova, arXiv:2509.17936, Thm 1.1 + eqs (5)–(9), retrieved and read).
> Her matrix is `N × N` with `N` a **pure truncation parameter, independent of `w`**, in a
> `w`-independent orthonormal Bergman basis `ψ_j = √((j+1)/π) z^j` on the **fixed** unit disc
> `D = {|z| < 1}`, and the entries are elementary in `w`:
> ```
>   l_ij(s) = 2 sqrt((j+1)/(i+1)) * zeta(2s+i+j) * binom(2s+i+j-1, i) / w^(2s+i+j)   (i+j even)
>   l_ij(s) = 0                                                                      (i+j odd)
> ```
> with `Z_{Γ_w}(s) = det(1 − L_s)` **exactly** and an explicit error `|Z − F_N| ≤ P_N e^{P_N+Q+1}`,
> `P_N = O(N^{1/2}(w/2)^{−N})`. **This is precisely "fixed dimension + entry-wise parameter decay
> becomes a determinant comparison"** — and in that representation the `(m,j)`-envelope that
> `LAW_U1EFF_ENTRYWISE` §4 measured as FAILING is *manifest*: the whole `w`-dependence is the single
> factor `w^{−(2s+i+j)}`, geometric in `i+j`. The route the brief wanted works. On the wrong side.
>
> **(V2) It cannot be transplanted to `λ < 2`, and the obstruction is an exact inequality, not a
> difficulty.** Fedosova's branches are `ψ_n(z) = −z/(z + nw)`, `n ∈ Z\{0}`. `ψ_n(D) ⊂ D` holds iff
> `z` is nearer `0` than `−nw` for all `|z| < 1`, i.e. iff **`|n| w ≥ 2`**; the binding case is
> `n = ±1`, so the single-disc operator exists **iff `w ≥ 2`, tangentially at `w = 2`**.
> `PROVED-here` (one line, from the perpendicular-bisector criterion; and it is the same statement as
> `LAW_T2_DETERMINANT` Lemma T2-A, "no invariant disc at any `λ`", now with the threshold made
> explicit and two-sided). **`w = 2` is not a technical edge of her method; it is the exact phase
> boundary of the representation, and our family sits strictly on the far side of it.**
>
> **(V3) The brief's device — "induce over the parabolic, pay with Hurwitz-zeta-like sums over
> excursion lengths" — is NOT an unexploited move. It has already been performed, and the repo is
> already computing its output.** Pohl–Wabnitz (arXiv:2209.05927, Memoirs AMS 1616 — already cited in
> `lane_p/FLAGSHIP_PAPER_DRAFT.tex`) organise the literature into a **slow/fast dichotomy**: slow
> operators encode cusp windings step by step, are **non-nuclear, and do NOT satisfy the determinant
> identity**; the **cuspidal acceleration** collapses all successive windings into a single step,
> and the resulting *fast* operators "are indeed nuclear and satisfy (2) and (4)", i.e. `Z = det(1−L)`.
> They state this acceleration "was developed" for "the family of Hecke triangle orbisurfaces of
> finite as well as of infinite area" `[15,43,56,58]`, and list MMS `[41]` among the transfer
> operators arising from strict transfer operator approaches. Since the repo's MMS operator **is**
> nuclear and **does** satisfy `Z_S = det(1 − L_{s,±})` (`LAW_B5J_JENSEN` J1, `PROVED-cited`
> arXiv:0912.2236), it is on the *fast* side of that dichotomy — `INFERRED`, but from two cited
> facts and a stated dichotomy. **The Hurwitz-zeta entries `ζ(2s+m+j, a₀)` that Lemma H bounds are
> the summed-excursion weights the brief hoped to produce.** There is no second acceleration to
> apply.
>
> **(V4) And inducing could not fix `λ < 2` even if it had not been spent, because on our branch the
> obstructing element is ELLIPTIC, not parabolic.** `LAW_T2_DETERMINANT` Lemma T2-B (`PROVED-repo`):
> `ψ_1 = R = S T_λ` is elliptic of **order exactly `q`** at `λ = λ_q` (rotation by `π/q`), parabolic
> only at `λ = 2`. Inducing/jumping is a device for a **transient** neighbourhood of a neutral fixed
> point: it is well defined because almost every orbit *leaves* in finite time, and the price is a
> convergent sum over excursion lengths. A rotation of finite order `q` is not transient — the
> orbit is periodic, `ψ_1^q = id`, every neighbourhood of the elliptic point is essentially
> invariant, and the "excursion-length sum" is a **finite sum of `q` terms** rather than a Hurwitz
> zeta. `LAW_T2_DETERMINANT` §2.3 already measured the consequence: the induced alphabet has
> cardinality `≍ q` at `λ_q` and `∞` at `λ = 2`, its size is the denominator of the rotation number
> `ν(λ) = arccos(λ/2)/π`, and at `σ = ¼` the finite sum **grows like `q^{1/2}`** while the `λ = 2`
> object exists only by continuation in `s`. **`κ(q) = q − 2` is not a defect of the MMS bookkeeping
> that inducing could remove; it is the elliptic order `q` itself, and it is the same fact as
> `θ → 1`.**
>
> **(V5) Therefore: Route A revival through a fixed-dimension transfer operator is NOT FEASIBLE, and
> the correct reading is not "we failed to find the construction" but "the construction exists and
> the family is on the other side of its boundary".** The determinant-identity question the parent
> flagged as the thing to settle first (`B5-J` §6 item 2) is now **settled, and settled favourably**
> — inducing costs **no** regularization factor (§3) — which is precisely why it buys us nothing: the
> identity was never the obstruction.

**What is newly banked (three items, all cheap and all reusable).**
1. **The exact threshold `|n|w ≥ 2`** — the two-sided, quantitative form of Lemma T2-A, which
   identifies `λ = 2` as the phase boundary of the single-disc representation rather than as an
   endpoint where estimates happen to degrade.
2. **The determinant identity survives inducing with no correction factor** (Pohl–Wabnitz Thm A /
   eq. (5)), and the *regularized* determinants of the Rugh/Isola/Prellberg line are the price of
   **not** inducing, not of inducing (§3). This closes `B5-J` §6 item 2 as a literature question.
3. **A fully explicit, `w`-analytic, fixed-dimension `Z_{Γ_w}` evaluator with a certified error
   bound** (Fedosova eqs (5)–(9)) — three lines of code, no new theory. Useless for `q → ∞`, but
   see §5 for the one thing it might legitimately be used for.

---

## 1. Sources verified — what each actually contains

Every item below was **retrieved and text-extracted**, not cited from memory. Where I only have the
abstract I say so.

| source | verified identity | what it actually contains | bearing |
|---|---|---|---|
| **arXiv:2509.17936** — K. Fedosova, *Spectral and dynamical invariants of Hecke triangle groups via transfer operators*, 22 Sep 2025 | **title/author CONFIRMED**; full text extracted | Hecke triangle groups `Γ_w` for **`w > 2`** only — `Γ_w\H` is an **infinite-volume** orbifold with one cusp and one conical singularity. Transfer operator (22) on the **Bergman space `H²(D)` of the fixed unit disc**, `L_s f(z) = Σ_{n∈Z\{0}} (|n|w)^{−2s} e^{−2s log(1+z/(nw))} f(−z/(z+nw))`, nuclear, `Z_{Γ_w}(s) = det(1 − L_s)` for `Re s > ½` (her (23), citing `[23]`). Thm 1.1: `Z_{Γ_w}` continues to `C \ ½(1−2N₀)` and `|Z_{Γ_w}(s) − F_N(s)| ≤ P_N(s)e^{P_N(s)+Q(s)+1}` with `F_N = det(1 − L(s))` an `N × N` determinant and entries as quoted in §0. Applications: `δ_w` to ≥50 digits, Ruelle zeta at `0`, trivial-zero orders. | **the fixed-dimension object exists** — on `w > 2` |
| **arXiv:2209.05927** — A. Pohl & P. Wabnitz, *Selberg zeta functions, cuspidal accelerations, and existence of strict transfer operator approaches*, 13 Sep 2022 (= Memoirs AMS 1616, 2026; already in `lane_p/FLAGSHIP_PAPER_DRAFT.tex`) | **title/authors CONFIRMED**; full text extracted (12.8k lines) | Thm A: every geometrically finite Fuchsian group with a hyperbolic element admitting a *set of branches* admits a **strict transfer operator approach**, i.e. eq. (5) `Z_{X,χ}(s) = det(1 − L^{X,fast}_{s,χ})` — Fredholm determinant **identically** the Selberg zeta. Construction is algorithmic: "reduction, extension, translation, **induction** and **acceleration**", turning a non-uniformly expanding cross-section into a uniformly expanding one; result nuclear of order zero. Explicitly names the **slow/fast dichotomy**: slow operators "are typically non-nuclear and hence **do not satisfy** the identities (2) or (4)"; the **cuspidal acceleration** encodes "all successive windings in the cusp … in a single step" and the fast operators "are indeed nuclear and satisfy (2) and (4)". States this was already done for "the family of Hecke triangle orbisurfaces of finite as well as of infinite area" `[15,43,56,58]`; lists MMS `[41]` among strict approaches. | **the determinant identity SURVIVES inducing, with no correction factor** — and the Hecke acceleration is already done |
| **arXiv:chao-dyn/9610011** — H. H. Rugh, *Intermittency and Regularized Fredholm Determinants*, 7 Oct 1996 | **title/author CONFIRMED** (the brief's "Isola/Prellberg" line; Rugh is the paper that states the determinant question cleanly, and cites Prellberg `[7]`, Isola `[3]`, Mayer `[4]` for the induced-map technique) | Real-analytic interval maps expanding except at a **neutral fixed point at 0**. There `r_ess = r`, so the classical annulus "becomes void". Thm 1.1: `sp(M) = σ_c ∪ σ_p` with `σ_c = [0,1]` **continuous** spectrum; the **regularized** determinant `d_β(λ) = det(1 − M₁R(λ,M₀))` (his (2.35), `M = M₀+M₁`, `R` the resolvent) is holomorphic on `C̄ − σ_c`, its zeros = eigenvalues of `M`, and it continues across `σ_c − {0,1}` **onto different Riemann sheets**. He notes (2.34) "corresponds to the Fredholm determinant associated with the so-called **induced** family of contractions". `d_m` (his (1.6)) is the periodic-orbit sum with the neutral fixed point **excluded**. | **the regularization is the price of NOT inducing** — see §3 |
| **arXiv:0902.3953** — D. Mayer & T. Mühlenbruch, *Nearest `λ_q`-multiple fractions*, v4 2010 | **title/authors CONFIRMED**; full text extracted | The nearest-`λ_q`-multiple CFs for `λ_q = 2cos(π/q)` and their duals, generated by interval maps `f_q`, `f_q*` "conjugate to subshifts over **infinite alphabets**"; natural extension = Poincaré map for the geodesic flow on `G_q\H`; §5.2 constructs the transfer operator. Explicitly warns: `Z_{G_q}` "**cannot be expressed in terms of the transfer operator for the map `f_q` alone**" — the recurrence time must be folded in via Ruelle's lemma 5.2.1 `Z_{G_q}(β) = ∏_k exp(−Σ_n Z_n(β+k)/n)`. `q = 3` is Hurwitz's nearest-integer CF; even `q` is Nakada. | the `λ_q` side is intrinsically an **infinite-alphabet** slow system; the accelerated/reduced form is what MMS supplies |
| **arXiv:0912.2236** — Mayer–Mühlenbruch–Strömberg, *The transfer operator for the Hecke triangle groups* | identity confirmed via search index; **not re-extracted this session** (already `PROVED-cited` in `LAW_B5J_JENSEN` J1 and used by the repo's builder) | the repo's operator; nuclear, `Z_S` = product of the two sector determinants | the object the lane already computes |

**Two things the brief conjectured that the sources do NOT support.**
- *"Fedosova is the reference to read before inducing."* It is the right reference, but for the
  opposite reason to the one expected: it does not induce anything, and it does not treat `w < 2`,
  `w = 2`, cofinite Hecke groups, cusps-as-obstruction, or the `w → 2` limit. Grep of the extracted
  text: **zero** occurrences of "induce/induced/jump/first return/accelerat", and "cusp" appears
  only in the phrase describing `Γ_w\H` as having one cusp, plus one bibliography title.
- *"Inducing changes the determinant by an explicit regularization factor — find the statement."*
  **There is no such factor**, and the search for one is what §3 resolves.

---

## 2. In-repo findings — the induced formulation is not missing, it is the thing already running

Grep over `research_notes/rh_goals_2026-08-14`, `law_probes`, `.worktrees` for
`induced|jump transform|first.?return|accelerat`:

| file | what is there | status |
|---|---|---|
| `lane_g/LAW_T2_DETERMINANT.md` §2.3 | **the induced construction is already written down and already analysed**, with `Lemma T2-B` (`PROVED`): the induced alphabet `A(λ) = {ψ_{±1}^k ∘ ψ_n : k ≥ 0, |n| ≥ 2}` has `|{ψ_1^k}| = q` at `λ_q` and `∞` at `λ = 2`, cardinality = denominator of `ν(λ) = arccos(λ/2)/π`. Verdict at §0: "**Inducing does not rescue it — inducing makes it strictly worse.**" `|(ψ_1^k)'| ~ k^{−2}` at `λ = 2` (so `Σ_k k^{−2s}` = the Hurwitz/`ζ(2s)` sum, poles at `s = (1−k)/2`), versus `O(1)` derivative and `q` terms at `λ_q`, giving `~ q^{1−2σ} → q^{1/2}` at `σ = ¼`. | the brief's step-3(a) **already exists in the repo**, one lane over |
| `lane_g/LAW_T2_DETERMINANT.md` §2.2, §2.4 | Lemma T2-A: no invariant disc for **any** `λ ∈ (λ₀, 2]`, by Denjoy–Wolff (multiplier of modulus 1). Lemma T2-C + §2.4: the obstruction is **group-theoretic** — `R^q = 1` makes any `λ`-independent index set infinite-to-one, so "every `λ`-analytic construction is blind to `R^q = 1`; every construction that sees `R^q = 1` is a function of `ν(λ)`'s denominator and therefore not `λ`-analytic". | `V2`/`V4` above are corroborations, not discoveries |
| `lane_g/LAW_TAIL_SCOPING.md` §~229, §~335 | already names the induced-map device for "exactly this pathology" and "cautious" optimism; already says beating the `λ = 2` endpoint "requires **inducing** (accelerating)". | the open item this note closes |
| `lane_g/M1B_Q4_INTERTWINER.md` §1 | a **concrete candidate first-return regrouping** at `q = 4`: "the induced boundary branch is …", "the first-return section …", "There are no first returns of fast-symbol length 1 or 3 to this section", and §322: what it would take to construct "(i) a genuine `q=4` slow map whose first-return coding …". Notes the literature states the intertwiner "only in the modular `q=3` case" and "does not state a `q=4` first-return" version. | **the only place in the repo with a worked induced/first-return object** — `q = 4` only, single `q`, explicitly incomplete |
| `lane_g/LAW_T2_DETERMINANT.md` §2.6 | honest literature `GAP`: no published theorem on jointly-`(s,λ)`-holomorphic determinants across a Markov-structure change, on cone-angle `→ 0` at bounded area, or on `lim_{q→∞}` of the Hecke spectrum. | **unchanged by this session's reading.** Fedosova is `w > 2`; Pohl–Wabnitz is one group at a time, uniform *in the construction*, not in the group |
| `.worktrees/aletheia-restore/code/` | `zeta_cert_rosen{,_even,_q5}`, `zeta_cert_q3`, `zeta_mayer{,_rosen}` | **no** `Γ_θ` (`λ = 2`) transfer-operator evaluator, confirming `LAW_U1EFF_ENTRYWISE` G4 |

**The `Γ_θ` side of the brief's question 2, answered.** `λ = 2` gives `T_2 = [[1,2],[0,1]]`, so
`G_∞ = ⟨S, T_2⟩` **is** the theta group `Γ_θ` — cofinite, finite volume, genuinely parabolic. Its
CF is the *even/nearest-even-integer* algorithm, the `q → ∞` member of the Mayer–Mühlenbruch family
(**not** the `q = 3` nearest-integer CF of Hurwitz, which is `λ = 1`). Chang–Mayer treat the
nearest-integer CF and general **modular** groups `Γ_0(N)`, not `Γ_θ` at `λ = 2`; the search
surfaced no paper giving a *fixed-dimension* Mayer-type operator with `det = Z_{Γ_θ}`. By
Pohl–Wabnitz Thm A one **exists** (`Γ_θ` is geometrically finite with hyperbolic elements and a
known set of branches), but I found **no explicit matrix for it in the literature and none in the
repo**. `GAP`, and it is the only literature gap on this topic that a bounded amount of work could
close — see §5.

---

## 3. Does the determinant identity survive inducing? **YES, with no correction factor** `[the settled question]`

This is `LAW_B5J_JENSEN` §6 item 2's "question to settle first", and the answer is the opposite of
what the brief anticipated.

**The statement.** Pohl–Wabnitz Thm A + eq. (5): if `Γ` admits a set of branches, the construction —
whose steps *are* "reduction, extension, translation, **induction** and **acceleration**" — outputs a
family `L^{X,fast}_{s,χ}`, nuclear of order zero, with
```
    Z_{X,chi}(s) = det( 1 - L^{X,fast}_{s,chi} )        exactly, no factor, no regularization
```
`PROVED-cited`. The acceleration is *how* the identity is obtained, not something the identity has to
be repaired after. Their slow/fast dichotomy makes the direction of the trade explicit: the **slow**
(un-induced, step-by-step-winding) operator is the one that is **non-nuclear and fails** the
determinant identity.

**Why the "regularization factor" intuition points the wrong way.** Rugh's regularized `d_β(λ)` is
constructed for the operator that **still has** the neutral fixed point in it: there `σ_c = [0,1]`
is genuine continuous spectrum, the ordinary Fredholm determinant does not exist, and the repair is
a **relative/perturbation** determinant `det(1 − M₁R(λ,M₀))` living on `C̄ − σ_c` with continuation
onto **different Riemann sheets** — a branch cut, not a multiplicative factor. His periodic-orbit
sum `d_m` differs from `ζ_m` exactly by **excluding the neutral fixed point** (his (1.5)–(1.6)),
which is the same excision inducing performs. So:

> ### Inducing does not cost a determinant correction. **Not** inducing costs you the determinant.
> The regularized-determinant literature (Rugh; Prellberg; Isola) is what you need if you insist on
> keeping the parabolic branch un-accelerated; the cost is then a branch cut along `σ_c = [0,1]` and
> a two-sheeted continuation, not a clean factor. `PROVED-cited` (Rugh Thm 1.1(a),(c),(d), (2.34)–(2.35)).

**Consequence for the lane.** The identity was never the obstruction, so settling it favourably does
not move Route A. The obstruction is, and remains, `dim = κ(q)N` with `κ(q) = q − 2` — and §§0/2
show that number is the elliptic order `q`, which no inducing step addresses. **`B5-J` §6 item 2
should be marked CLOSED-negative: the literature question resolved in our favour, and the resolution
is not usable.**

---

## 4. The formal induced operator for `G_q`, and why writing it out is the end of the road

For completeness, and because the brief asked for the definition explicitly. Notation of
`LAW_T2_DETERMINANT` §2: `λ ∈ (√2, 2)`, `I_λ = [−λ/2, λ/2]`, branches `ψ_n(x) = −1/(x + nλ)`,
`n ∈ Z\{0}`; `ψ_n(I_λ) ⊂ I_λ` iff `n ≥ ½ + 2/λ²` (T2 (2.1), `PROVED`), so for all `q ≥ 5`
**only `n = ±1` is partial**, and `ψ_{±1} = R^{∓1}` with `R = S T_λ` elliptic of order `q`.

**Definition (induced / jump operator over the `n = ±1` excursion).** Let `Y ⊂ I_λ` be the union of
the full branches' domains (the complement of the `n = ±1` cell). For `x ∈ Y` let
`τ(x) = min{ k ≥ 0 : f^k(x) ∈ Y ... }` be the first-return time counted in `ψ_{±1}`-steps, and set
the induced branch alphabet
```
    A(lam) = { psi_{+1}^k o psi_n : k >= 0, |n| >= 2 }  u  { psi_{-1}^k o psi_n : k >= 0, |n| >= 2 }
    (L^ind_s h)(x) = sum_{|n|>=2} sum_{k>=0} | (psi_{sigma}^k o psi_n)'(x) |^s  h( psi_{sigma}^k(psi_n(x)) )
```
i.e. the return map `F = f^{τ}|_Y`, transfer operator weighted by `|F'|^s`, whose branch set is
`A(λ)`. The `k`-sum is the "sum over excursion lengths" the brief expected.

**Which entries are `λ`-analytic with a `λ = 2` limit — the exact answer.**
- The **`n`-sum** is `λ`-analytic with a clean `λ = 2` limit: each `ψ_n`, `|n| ≥ 2`, is a full
  branch at every `λ ∈ (√2, 2]`, its weight is a rational function of `λ` and `x`, and the sum over
  `|n| ≥ 2` converges to a Hurwitz-zeta value uniformly on compacts. This half is fine, and it is
  the half Lemma H already controls.
- The **`k`-sum is not**, and this is the whole content. `LAW_T2_DETERMINANT` §2.3 (`PROVED` for the
  order statement): `|{ψ_1^k : k ≥ 0}| = q` at `λ_q`, `= ∞` at `λ = 2`, and the cardinality is the
  denominator of `ν(λ) = arccos(λ/2)/π` — `1/q` at `λ_q`, **irrational for generic `λ`**. A function
  of the denominator of a rotation number is nowhere `λ`-analytic. Quantitatively: at `λ = 2`,
  `R^k = [[1−k,−k],[k,1+k]]` gives `|(ψ_1^k)'| ~ k^{−2}`, so `Σ_k k^{−2s}` is `ζ(2s)` up to the
  Hurwitz shift — convergent for `Re s > ½`, continued past it; at `λ_q` the same sum is a **finite**
  sum of `q` rotation terms of size `O(1)`, `~ Σ_{k≤q} k^{−2σ} ~ q^{1−2σ}`, i.e. `q^{1/2}` at the
  anchor `σ = ¼`. **At the anchor height the `λ = 2` object exists only by continuation in `s` while
  the `λ_q` objects are honest finite sums that diverge in `q`. Continuation in `s` and `q → ∞` do
  not commute in this representation.** (`PROVED` for the derivative decay; `HEURISTIC` for the
  `q^{1−2σ}` rate, per T2.)

**So the induced operator is not a fixed-dimension object.** Its alphabet has size `≍ q` — the same
`Θ(q)` that `κ(q) = q − 2` already has. Inducing **relabels** the `κ(q)` Markov cells as `k`-indexed
excursions; it does not reduce their number, because their number *is* the elliptic order. That is
`V4`, and it is why §0 records the induced route as closed rather than untried.

**Work estimate to build an evaluator (asked for, answered — and the answer is "don't").**
- *Induced `G_q` operator, `λ < 2`:* **2–4 weeks** to a certified evaluator (new branch enumeration
  over `(n,k)`, new Taylor/disc geometry per composite branch, Arb ball propagation, cross-check
  against the existing `det(1 − L_{s,±})` at `q = 5,7,9`). **Recommended against**: by §4 the output
  has `Θ(q)` branches and by §3 its determinant equals the same `Z_S` the repo already computes, so
  the deliverable is a slower re-derivation of a known number with no dimension gain. Confidence
  that it fails to fix the dimension: **high** (Lemma T2-B is `PROVED`).
- *Fedosova `w > 2` evaluator:* **half a day.** Entries (6)–(7) are three lines (`ζ`, a binomial with
  complex argument, `w^{−(2s+i+j)}`), the error bound (8)–(9) is two more (`Li_{−1/2}`, `Li_{−2}`),
  and `python-flint`/Arb already has everything. This is the only cheap build in sight, and §5 says
  what it is and is not good for.
- *Explicit fixed-dimension `Γ_θ` (`λ = 2`) operator:* **1–3 weeks**, existence guaranteed by
  Pohl–Wabnitz Thm A but the matrix must be derived by hand (their construction is algorithmic, not
  a formula). Only worth it if a consumer exists — see §5.

---

## 5. Feasibility verdict, and the one legitimate use of what was found

**(a) Does a fixed-dimension representation of the Hecke family exist or can it be built?**
**Exists: YES, for `w > 2`** (Fedosova; fixed disc, fixed Bergman basis, `N` a truncation parameter
only, entries elementary and analytic in `w`, geometric envelope `w^{−(i+j)}` manifest, strict
determinant identity, explicit exponential error bound). **For our `λ_q < 2`: NO, and provably so** —
the single-disc condition is the exact inequality `|n|w ≥ 2` (`V2`), and the group-theoretic form of
the same obstruction (`R^q = 1`, `LAW_T2_DETERMINANT` Lemma T2-C, `PROVED`) rules out **any**
`λ`-analytic carrier, not just this one. **Can it be built by inducing? NO** — inducing is already
spent (`V3`) and could not have helped (`V4`: elliptic of finite order, not parabolic; no
transience, so no excursion-length series, only a finite sum of `q` terms).

**(b) Does the determinant identity survive inducing?** **YES, exactly, with no correction factor**
(Pohl–Wabnitz Thm A / eq. (5)). The regularized determinants of Rugh/Isola/Prellberg are the cost of
**not** inducing, and take the form of a branch cut along `σ_c = [0,1]` with two-sheeted
continuation, not a multiplicative factor (§3). **This closes the parent's named open question, in
our favour and to no benefit.**

**(c) The single biggest risk.**

> ### **The risk is a false-positive transplant: Fedosova's construction looks like exactly what the lane needs, and a future agent — or a referee reading our draft, which already cites Pohl–Wabnitz — will be tempted to "just use it at `λ_q`", or to take a `w → 2⁺` limit and call it the `q → ∞` limit.**
> Both are wrong, and the second is the dangerous one because it produces numbers.
> **The `w → 2⁺` limit is not the `q → ∞` limit.** `w > 2` is the **infinite-volume, free** group
> (`Γ_w\H` has infinite area, limit set a Cantor set of dimension `δ_w < 1`, and `Z_{Γ_w}` has
> exactly **one** zero in `Re s > ½`, at `δ_w`); `λ_q < 2` is **cofinite, finite area**, with
> `R^q = 1` and a genuine `L²` spectrum. They are different phases meeting at `w = 2 = Γ_θ`, and
> nothing in either source connects the one-sided limits. Moreover Fedosova's own error bound
> **degenerates precisely at the boundary**: `P_N = O(N^{1/2}(w/2)^{−N})`, so the convergence rate
> `(2/w)^N → 1` as `w → 2⁺`, and `P_N` contains `Li_{−1/2}(2/w)` which **diverges at `w = 2`**. Her
> `N`-uniformity collapses at exactly the point where our `θ → 1` and `κ → ∞` collapse — the same
> tangency, approached from the other side. A `q`-uniform claim extracted from that limit would be
> vacuous, and a *numerical* one would silently be measuring the wrong group.
> **Mitigation, to be written into any future brief:** any use of Fedosova's matrix must (i) state
> `w > 2` and "infinite volume, free" in the same sentence, (ii) carry `P_N`'s `(2/w)^{−N}` with it
> so the degeneration is visible, and (iii) never be evaluated at `w = λ_q`, where `ψ_{±1}(D) ⊄ D`
> and the "matrix" is a formal expression with no operator behind it. Secondary risk, much smaller:
> mis-citing Pohl–Wabnitz as giving a construction **uniform in the group** — they are explicit that
> uniformity is "for all sets of branches", i.e. of the *procedure*, one group at a time; the `GAP`
> at `LAW_T2_DETERMINANT` §2.6 (no `lim_{q→∞}` theorem) is untouched.

**Recommendation, ranked.**
1. **Do not build the induced `G_q` operator.** `B5-J` §6 item 2 → **CLOSED-negative**; `V3`/`V4` are
   the reasons. Amend `LAW_U1EFF_ENTRYWISE` §7's "where U1-eff should go next" and `LAW_TAIL_SCOPING`
   §335 accordingly: "induce/accelerate" is no longer a live lever.
2. **Do not attempt `w → 2⁺` as a proxy for `q → ∞`.** Risk (c).
3. **The board is unchanged, and now has one fewer competitor above it:** `LAW_SH_EFFECTIVIZATION_SKELETON`
   §7 item 1 (certified winding deep-pole counts) and `LAW_B5J_JENSEN` §6 item 4 remain top-ranked.
   The `(T2′)` Vitali+Hurwitz replacement (`LAW_T2_DETERMINANT` §3) is *further* corroborated by this
   note: it is the reformulation that drops the transfer operator from the tail argument, and every
   finding here says the operator cannot carry a `q → ∞` comparison.
4. **One optional half-day with a real consumer, if and only if a `Γ_θ` number is wanted.** The repo's
   only `Γ_θ` evaluator is a truncated Selberg Euler product valid on `Re s > 1`
   (`law_probes/probe_t2_shape.py`), and `LAW_U1EFF_ENTRYWISE` G4 records that no `Γ_θ`
   transfer-operator evaluator exists. Fedosova's `F_N` is *not* it (wrong side of `w = 2`), but her
   **method** — one fixed disc, Bergman basis, entries in `ζ(2s+i+j)`, certified `N`-tail — is the
   template for deriving one at `λ = 2`, where the group is genuinely parabolic and Pohl–Wabnitz
   Thm A guarantees a strict approach exists. That would give the lane a *certified* `Z_{Γ_θ}` inside
   the strip, which `LAW_T2_DETERMINANT` §4 and `LAW_U1EFF_ENTRYWISE` Lemma E currently only have on
   `Re s > 1` / entrywise. **Estimate 1–3 weeks, `GAP`-status derivation, and it is a `Γ_θ` deliverable
   only — it does not restore Route A.** Rank it below items 3's incumbents.

---

## 6. What this document claims, and does not

**Claims.** (i) A fixed-dimension, parameter-analytic, strict-determinant transfer-operator
representation of the Hecke triangle family exists in the literature, with explicit entries and a
certified error bound, **for `w > 2` only** (Fedosova, retrieved and quoted). (ii) It cannot be
transplanted to `λ_q < 2`: the single-disc condition is exactly `|n|w ≥ 2`, tangential at `w = 2`.
(iii) The determinant identity survives induction/acceleration **exactly**, with no regularization
factor (Pohl–Wabnitz Thm A, eq. (5)); regularized determinants are the price of *not* inducing
(Rugh). (iv) The brief's induced device is already spent — the repo's nuclear, determinant-identity-
satisfying MMS operator is on the *fast* side of Pohl–Wabnitz's slow/fast dichotomy — and could not
have helped anyway, because on `λ < 2` the obstructing element is elliptic of finite order `q`, not
parabolic, so there is no transience and no excursion-length series. (v) Therefore `κ(q) = q − 2` is
irreducible within transfer-operator representations of `G_q`, and Route A revival by this means is
NOT FEASIBLE. (vi) `LAW_B5J_JENSEN` §6 item 2 is closed, negatively.

**Does not claim.** That no fixed-dimension representation of `G_q` exists by some route not
considered here — Lemma T2-C (`PROVED-repo`) is strong evidence against any `λ`-analytic one, but
"no fixed-dimension representation at all" is **not proved**, and this note adds no proof. That MMS
is the cuspidally-accelerated operator in Pohl–Wabnitz's precise sense — that is **`INFERRED`** from
(nuclear + strict identity) against their stated dichotomy, and their citation list attaches the
Hecke acceleration to `[15,43,56,58]` while listing MMS as `[41]`; a reader who needs this exactly
should check Möller–Pohl (their `[43]`) directly. That the `q^{1−2σ}` growth of the induced `k`-sum
is proved (it is `HEURISTIC` in the parent, imported as such). That Fedosova's `Γ_w` bears any proved
relation to our `G_q` — it does not, and §5(c) is a warning against manufacturing one. Any statement
about `Γ_θ`'s explicit transfer operator: Pohl–Wabnitz Thm A gives **existence**; no matrix was
found in the literature or derived here (`GAP`). Nothing here was measured, computed, or certified —
**this note contains no numbers of its own**; every figure quoted is attributed to a parent note or a
retrieved source. The flagship `G_5` theorem and `Q₀ = 1465` are untouched.

---

**Sources retrieved this session** (all text-extracted from the PDF, not cited from memory):
arXiv:2509.17936 (Fedosova); arXiv:2209.05927 (Pohl–Wabnitz, = Memoirs AMS 1616);
arXiv:chao-dyn/9610011 (Rugh); arXiv:0902.3953 (Mayer–Mühlenbruch).
**Consulted via search index only, not extracted:** arXiv:0912.2236 (MMS — already `PROVED-cited` in
the repo), arXiv:0804.4837 (Strömberg, computation of `Z` on Hecke groups), arXiv:1909.11432
(Pohl et al., infinite-covolume Hecke eigenfunctions), CMP 2015 thermodynamic formalism for
infinite-area Hecke surfaces, arXiv:1710.05666 (large covers / sharp resonances).
**No git was run. No existing file was modified. No probe was executed.**
