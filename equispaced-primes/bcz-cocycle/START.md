# D1 — Per-step Farey lens as a BCZ / horocycle cocycle

Handoff 2026-05-15. Direction D1. Author: incoming dynamics/ANT researcher.

Scope: embed the **per-step** Farey lens (prime = only-new equispaced points,
composite = always overlap; differential of the static Farey↔Mertens identities)
as a **cocycle / first-return functional** over the Boca–Cobeli–Zaharescu (BCZ)
map, itself the Poincaré first-return of the horocycle flow on
`X = SL₂(ℝ)/SL₂(ℤ)` (Athreya–Cheung). Target: a dynamical reading of the
Mikolás L² second moment `J(N)` and the verified constant `C` in `N·W(N)→C`.

**Bottom line up front.** The dictionary
{Farey per-step quantity ↔ BCZ cocycle ↔ horocycle ergodic integral} is set up
and **verified by exact arithmetic** (V1–V5): the BCZ map is the full Farey
orbit (V1); the Mertens/Δ-A identities hold (V2); the Farey discrepancy `E_Q`
is **exactly** the Birkhoff sum `S_j` of an explicit BCZ cocycle (V4, after a
boundary-convention bug was found and fixed); the prime/composite dichotomy is
exactly lattice-point primitivity/visibility, anchored to the one in-repo
verified citation BCZ2000 (V5). Goal 2 status is a **reduction with a newly
identified obstruction**, NOT a theorem. **Honest negative (V6):** the *raw*
cocycle is **not uniformly L²** and its correlations are **not summable**
(heavy Farey-gap tail), so `C` is **NOT** a naive Green–Kubo sum — the earlier
hoped-for "Birkhoff CLT for a bounded cocycle" is **false as stated**. The
correct reduction is to the **renormalized/truncated** cocycle (Mikolás's
`Σ A²/m² + O(1)` IS that renormalization). Closing it needs a variance
asymptotic for the *truncated* cocycle via **effective horocycle
equidistribution (Strömbergsson)** — plausibly in reach, not done in the
literature. Weak mixing alone (Cheung–Quas) is insufficient. Reported as a
clean, honestly-bounded reduction with its obstruction made explicit.

Confidence labels used throughout: **[PROVEN]**, **[HEURISTIC]**,
**[CONJECTURAL]**, **[NUMERICAL-ONLY]**, **[CITATION-UNVERIFIED]** (statement
known from the literature but **not** checked here against the primary PDF with
page/theorem numbers — treat as a claim to verify, never as established).

---

## 0. Citation honesty (read first)

The project's #1 documented failure mode is fabricated/misattributed theorem
numbers. Local PDF availability was checked:

- **Available locally and used verbatim:** Boca–Cobeli–Zaharescu, *Distribution
  of lattice points visible from the origin*, Comm. Math. Phys. **213** (2000),
  433–470 (`paper/main.tex` `\bibitem{BCZ2000}`, confirmed in repo). Franel
  (Göttinger Nachrichten 1924, 198–201) and Landau (ibid. 202–206), confirmed
  in repo bibliography.
- **CITATION LOCK COMPLETED 2026-05-15 (D1 continuation).** Primary PDFs
  pulled and checked verbatim. See `THEOREM_R_2026-05-15.md` §0 for the full
  adversarial citation dossier (verbatim quotes + exact theorem/eq numbers).
  Summary of locked sources:
  - **[CITATION-LOCKED]** Athreya & Cheung, *A Poincaré section for horocycle
    flow on the space of lattices*, **IMRN 2014, no. 10, 2643–2690**;
    arXiv:1206.6597v2 (23 Jul 2012). **Theorem 1.1** (Poincaré section, eq
    (1.2) Ω, return time eq (1.3) `R(a,b)=1/(ab)`, BCZ map eq (1.4)),
    **Theorem 1.2** (ergodic, zero-entropy, unique a.c. invariant measure
    `dm = 2 da db`), `∫_Ω R² da db = π²/3`. Verbatim in §0.1.
  - **[CITATION-LOCKED]** Cheung & Quas, *BCZ map is weakly mixing*,
    arXiv:2403.14976 (22 Mar 2024). **Theorem 1: "The BCZ map is
    weak-mixing."** (discrete map, NOT suspension; mixing & rigidity stated
    open). Verbatim in §0.3.
  - **[CITATION-LOCKED]** Strömbergsson, *On the deviation of ergodic averages
    for horocycle flows*, **J. Mod. Dyn. 7 (2013), 291–328**. **Theorem 1**,
    eq (1.4): effective ergodic-average bound with explicit error; for
    Γ=PSL(2,ℤ) (no small eigenvalues, s₁=½) the saving is the power
    `O(‖f‖_{W⁴} · r^{−1/2} log³(r+2))`. Companion: Strömbergsson, *On the
    uniform equidistribution of long closed horocycles*, **Duke Math. J. 123
    (2004), 507–547** (subsegment threshold ℓ^{1/2+ε}, optimal). Verbatim §0.2.
  - **[CITATION-LOCKED, in-repo + Springer abstract]** Boca, Cobeli &
    Zaharescu, *Distribution of lattice points visible from the origin*,
    **Comm. Math. Phys. 213 (2000), 433–470** (in-repo `\bibitem{BCZ2000}`,
    confirmed). Anchors the **visibility/primitivity** claim (§3). NOTE: the
    BCZ *map/section* itself is attributed by Athreya–Cheung to BCZ, *A
    conjecture of R. R. Hall on Farey points*, **J. Reine Angew. Math. 535
    (2001), 207–236** (AC ref [8]); the section/first-return *identity* is now
    carried by the locked Athreya–Cheung Thm 1.1, not by CMP 213. Verbatim §0.4.
  - **[CITATION-UNVERIFIED, downgraded]** Mikolás, *Farey series …*, Acta Sci.
    Math. Szeged (1949/1951) — primary not pulled; the `J=ΣA²/m²+O(1)`
    identity is used only as V3-checked exact arithmetic, NOT on Mikolás's
    authority. Cox–Ghosh–Sultanow arXiv:2105.12352 / 2407.10214 — not
    load-bearing for (R); left unverified.

Nothing below is asserted as a theorem on the strength of an unverified
citation; the proven content (V1–V5, the cocycle algebra) stands on its own
exact arithmetic. The four locked citations above carry the analytic inputs
to theorem (R) (`THEOREM_R_2026-05-15.md`).

---

## 1. Poincaré-section setup and the dictionary

### 1.1 The space, flow, and section (standard; structure used here is [PROVEN] internally by V1)

`X = SL₂(ℝ)/SL₂(ℤ)` = space of unimodular lattices in ℝ², Haar prob. `μ_X`.
Horocycle flow `h_s = [[1,0],[ -s,1]]` (sign convention immaterial here),
geodesic `g_t = diag(e^{t/2}, e^{-t/2})`.

The BCZ section (Athreya–Cheung framing; **[CITATION-LOCKED]** —
Athreya–Cheung IMRN 2014 eq (1.2), (1.3), (1.4), Thm 1.1–1.2, verbatim in
`THEOREM_R_2026-05-15.md` §0.1; **[PROVEN]** here as a self-contained
combinatorial map by V1):

> Ω = { (a,b) ∈ ℝ² : 0 < a ≤ 1, 0 < b ≤ 1, a + b > 1 },
> with invariant probability measure `dν = 2 da db` on Ω (area of Ω = 1/2).

The **BCZ map** `T : Ω → Ω`:

> T(a,b) = ( b , −a + ⌊(1+a)/b⌋·b ),  return time `r(a,b) = 1/(ab)` (roof
> function for the horocycle flow; ∫_Ω r dν = π²/3 ↔ `μ_X` normalization).

Athreya–Cheung: `T` is the first-return map of `h_s` to the section
`{ lattices with a horizontal vector of length ≤ 1 }` (equivalently the
"visible point" section), and the horocycle orbit segment of length ~N²
through the standard lattice scaled by `g_{2 log N}` enumerates exactly the
Farey neighbour pairs of `F_N`. **[CITATION-LOCKED]** at the level of the
precise section identity (Athreya–Cheung IMRN 2014, Thm 1.1: Ω is a Poincaré
section for the horocycle flow `N` on `X₂`, first return time
`R(a,b)=1/(ab)`, first return map = BCZ map eq (1.4) — verbatim §0.1);
**[PROVEN] here** at the level of the explicit map: see V1.

### 1.2 Farey ↔ section chart (this is exact and [PROVEN], V1)

For `F_Q` on (0,1], consecutive neighbours `h/k < h'/k'` satisfy
`h'k − hk' = 1` (unimodularity) and `k + k' > Q`. The chart

> (a, b) = (k/Q, k'/Q) ∈ Ω,  and in integer coordinates the map is
> **(k, k') ↦ (k', κk' − k), κ = ⌊(Q+k)/k'⌋**

is **exactly** the next-Farey-neighbour recurrence (Stern–Brocot/mediant).
V1 confirms machine-exactly that iterating this map traverses the entire
ordered Farey sequence, orbit length `|F_Q|−1`, with the Ω constraint
`k+k'>Q` holding at every point. So:

> **[PROVEN]** The ordered Farey sequence `F_Q` IS one periodic BCZ orbit; the
> "order Q→Q+1" passage is a change of section scale (Q is the cutoff defining
> Ω's chart), not a single return — see §1.5 for the correct per-step object.

### 1.3 The BCZ gap cocycle and the discrepancy as a Birkhoff sum ([PROVEN], V4)

Farey gap formula (classical, re-derived & V4-checked):
`f_{j} − f_{j−1} = 1/(k_{j−1} k_j)` (interior). With `Φ = |F_Q|`,
`E_Q(x) = #{f≤x} − Φx`, define the cocycle on consecutive nodes

> **g_j := 1 − Φ·(f_j − f_{j−1})**, a function of the section point
> (since gap = 1/(k_{j−1} k_j) = (1/Q²)/(ab)).

**Correct boundary convention (a real bug was found and fixed — reported per
project culture).** The orbit must start at the node **f_0 = 0** (left
endpoint of (0,1]); the first and last steps use the cusp gap `1/Q` (the
section's return at the cusp), NOT a `k k'` product — this is part of the
cocycle definition, not an error. My first V4 attempt omitted `f_0=0` and
mis-indexed the gap; it FAILED at j=0. With the corrected convention,
**[PROVEN] (V4, exact Fraction arithmetic, Q ≤ 600, every node):**

> **S_j := Σ_{i=1}^{j} g_i = E_Q(f_j) = j − Φ·f_j** exactly, for every node,
> with `S_0 = 0` and `S_{|F_Q|} = 0` (closed orbit).

This is the load-bearing identification: **discrepancy = Birkhoff sum of an
explicit BCZ cocycle**, `Σ g` telescoping to 0 on the closed orbit.

### 1.4 The second moment as a roof-weighted second moment of S_j ([PROVEN] identity, V3)

`J(Q) = ∫₀¹ E_Q² dx`. Since `E_Q` is piecewise linear between nodes with
node values `S_j = E_Q(f_j)` (the Birkhoff sums of §1.3), exact quadrature
gives the **[PROVEN] identity**

> `J(Q) = Σ_j ∫_{f_j}^{f_{j+1}} (S_j − Φ(x−f_j))² dx`
> `      = Σ_j gap_j·( S_j² − S_j Φ gap_j + (Φ gap_j)²/3 )`.

The leading term is `Σ_j gap_j · S_j²` = the **roof-weighted (r ∝ gap) mean
square of the Birkhoff sum**. Whether this equals a *Birkhoff variance σ²·n*
is **NOT proven and is in fact false for the raw cocycle (V6, §2.0)** — the
identity above is exact, but its asymptotics need the renormalized cocycle.
V3 checks `J_direct` (exact) against Mikolás `(1/2π²)Σ A_Q(m)²/m²` (matches to
`+O(1)`) and tabulates `N·W(N)` (rises toward ≈0.66).

### 1.5 The per-step / prime-step object ([PROVEN] algebra, V2)

The genuinely novel object (the surviving zone vs. Cox–Ghosh–Sultanow static
identities) is the **increment** `A_Q(m) − A_{Q−1}(m)`. Verified facts,
re-derived and V2-checked exactly:

- `A_Q(m) = Σ_{f∈F_Q} e(mf) = Σ_{d|m} d·M(⌊Q/d⌋)` (Mertens identity), real.
- Prime step: `ΔA(m) = A_p(m) − A_{p−1}(m) = −1 + p·𝟙[p|m]`.

Dynamically: passing `Q−1 → Q` **inserts the φ(Q) new fractions h/Q,
gcd(h,Q)=1**. In the lattice/section picture these are exactly the **new
visible (primitive) bottom-row vectors (h,Q)**. The per-step increment of the
discrepancy/second-moment is therefore a **first-return-type cocycle indexed by
the new primitive vectors appearing at scale Q** — the BCZ "differential"
nobody in the dynamical literature has written down (they study gap
distributions/equidistribution, not increments).

> **Dictionary (all [PROVEN] internally except the horocycle-realization line):**
>
> | Farey per-step quantity | BCZ cocycle | Horocycle integral |
> |---|---|---|
> | gap `f_{j+1}−f_j` | roof `r=1/(ab)` (×1/Q²) | return time of `h_s` |
> | discrepancy `E_Q(f_j)` | Birkhoff sum `S_j=Σ_{i≤j} g_i`, `g=1−Φ·gap` (f_0=0) | ∫ of cocycle along horocycle piece |
> | second moment `J(Q)` | roof-weighted mean-square of `S_j` (NOT a raw Birkhoff variance — §2.0) | `L²` mass of horocycle ergodic integral |
> | `A_Q(m)` | character cocycle `Σ e(m·f)` over orbit | twisted horocycle integral (Hecke/Eisenstein freq. `m`) |
> | prime step `ΔA(m)=−1+p𝟙[p|m]` | increment from φ(p)=p−1 new primitive vectors | first-return increment, scale `p` |
> | prime "only-new", composite "overlap" | primitivity (visibility) of `(h,Q)` | BCZ visible-point section condition |

---

## 2. The dynamical reduction of the Mikolás constant `C` (honest)

**Claim [HEURISTIC; the raw-cocycle form is FALSE per V6, see §2.0].** With
`g_j=1−Φ·gap` the BCZ cocycle of §1.3 and `S_n` its Birkhoff sums under `T`
(invariant ν), one would *like* `N·W(N)→C` to be **equivalent to**

>  `Var_ν(S_n) ~ σ²·n`,  `σ² = ∫ ĝ² dν + 2 Σ_{j≥1} ∫ ĝ·(ĝ∘Tʲ) dν`
>  (Green–Kubo). **V6 shows this fails for the RAW cocycle** (no uniform L²,
>  correlations ~1/j). It holds only after renormalization/truncation
>  (§2.0); the *truncated* statement is the live target (R).

Reasoning (sketch, [HEURISTIC] where marked):
- §1.4 makes `J(Q)` a roof-weighted second moment of `S_j`. **[PROVEN]**
- `W(N)=J(N)/Φ+O(1/Φ)` and `Φ~3N²/π²` (verified fact), so
  `N·W(N) = N·J(N)/Φ + o(1)`. Plugging the verified `J(N)~c·N`
  (triple-cross-verified, N≤3·10⁵) gives `N·W(N)→C` with `C` a fixed
  multiple of `c`. **[PROVEN given the verified J(N)~cN fact]**
- The Parseval/Mikolás side `J(N)=(1/2π²)Σ A_N(m)²/m²+O(1)` makes `c`, hence
  `C`, a sum over frequencies `m` of mean-square character cocycles. Under
  RH + Good–Churchhouse/Ng-2004 zero-statistics this is the
  `Σ_ρ 1/(|ρ|²|ζ'(ρ)|²)` form (verified-fact, conditional). **[CONJECTURAL]**
  (conditional on RH and the moment input — *as already flagged in the
  project's verified facts*).
- The **dynamical content** is that the SAME `c` is the Green–Kubo sum
  `σ²` of `g` over `T`. This is **[HEURISTIC]** until a quantitative CLT or
  variance theorem for `S_n` is proven; it is the precise open slot.

So Goal 2 reduces to **one analytic input** (stated correctly for the
*renormalized* cocycle after §2.0):

> **Needed theorem (R).** A quantitative variance/CLT for the **Hall-normalized
> truncated** BCZ cocycle `g^{(M)}` (§2.0, §5):
> `Var_ν(S_n^{(M)}) = σ²(M)·n + O(n^{1−δ})` with summable autocovariances
> uniformly in `M`, plus `σ²(M) → (π²/3)·c` as `M→∞` with the discarded
> tail = Mikolás's `+O(1)`. (The raw-cocycle form of (R) is false: V6.)

### 2.0 Honest obstruction discovered numerically (V6) — sharpens (R)

**[NUMERICAL-ONLY, but decisive].** V6 estimates the lag-`j` autocovariance
`c_j` of the centered raw cocycle `ĝ = ĝ_j` over one `F_Q` orbit and the
running Green–Kubo sum `σ²(L) = c_0 + 2Σ_{j≤L} c_j`. Findings:

- `c_0` (the variance of the raw cocycle) **grows with Q** (1.57 at Q=200 →
  2.08 at Q=800 → 2.42 at Q=2000): the raw `g = 1 − Φ·gap` is **NOT L² with
  Q-uniform norm**. This is expected — the Farey gap has Hall's heavy-tailed
  distribution, so `Φ·gap` has a fat tail and a Q-growing second moment.
- `c_j` decays only like ≈ `1/j` (e.g. Q=2000: c_1≈0.78, c_4≈0.087,
  c_8≈0.051, c_16≈0.021, c_40≈0.0071), so `Σ c_j` is **borderline /
  not absolutely summable**, and `σ²(L)` **drifts downward** rather than
  stabilizing.

> **Honest consequence:** the *naive* "Birkhoff CLT for the raw bounded
> cocycle" picture is **FALSE as stated** — `g` is not uniformly L² and its
> correlations are not summable. The earlier claim in §1.3 that `E_Q` is
> "the object for which CLT theory applies" is **downgraded**: it is a
> Birkhoff sum, but of a NON-uniformly-integrable cocycle. Clean negative.

**V7 sharpens the renormalization (also [NUMERICAL-ONLY]).** Truncating the
gap at `1/(T·Q)` with **fixed T** does NOT stabilize `c_0` across Q either
(T=8: c_0 = 0.91→1.16→1.42→1.67 for Q=500..4000). BUT along the **diagonal
where the cutoff scales like Q** the variance is Q-stable: e.g. (Q=500,T=8)
c_0≈0.914 vs (Q=1000,T=16) c_0≈0.912 — equal. **Reading:** the correct
renormalization is in **normalized-spacing (Hall) units** `s = gap·Φ = O(1)`,
NOT `gap·Q`. The stable cocycle is `g` truncated at a fixed multiple of the
*mean* spacing — exactly the Mikolás **frequency cutoff** `m ≤ M` (high-`m`
= heavy Hall tail = the discarded `+O(1)`). So (R) must be stated for the
**Hall-normalized truncated cocycle**; `c` lives in that truncated second
moment. This is the concrete, executed refinement of the next step.

### 2.1 Which ergodic theorem would close it, and reachability (honest)

- **Cheung–Quas weak mixing [CITATION-LOCKED]:** *qualitative*. Cheung–Quas
  arXiv:2403.14976, **Theorem 1: "The BCZ map is weak-mixing"** (verbatim
  §0.3 of `THEOREM_R_2026-05-15.md`). Weak mixing gives ergodicity of the
  cocycle but **NOT** a variance rate or summable correlations (the abstract
  itself states quantitative *mixing and rigidity remain open*).
  **Insufficient for (R).** Honest verdict: necessary context, not the
  closing tool.
- **Effective horocycle equidistribution (Strömbergsson) [CITATION-LOCKED]:**
  Strömbergsson, J. Mod. Dyn. 7 (2013), 291–328, **Theorem 1** eq (1.4):
  effective ergodic-average bound, power saving `r^{−1/2} log³(r+2)` for
  Γ=PSL(2,ℤ) (no small eigenvalues ⇒ s₁=½); companion Duke 123 (2004)
  optimal subsegment threshold ℓ^{1/2+ε}. Verbatim §0.2. This is the **right
  machinery**: a power-saving equidistribution of the horocycle piece that
  BCZ-codes `F_N` gives the autocovariance decay needed for the Green–Kubo
  sum. **Plausibly in reach** — but no worked variance/CLT for *this
  specific* BCZ cocycle (`1−Φ·gap`) exists in the literature; see (R) below
  for the precise reduction now achieved.
- **Existing CLTs for BCZ-type cocycles:** CLTs for Birkhoff sums over
  horocycle/BCZ-type systems exist, but matching the *exact* cocycle `g` and
  the *roof-weighted* variance to the Mikolás `c` is the unfilled step. The
  sharpened reduction is in `THEOREM_R_2026-05-15.md`.

**Negative-result honesty:** I did **not** obtain a dynamical *proof* of `C`,
and V6 shows the *raw*-cocycle Green–Kubo equivalence is **false** (no uniform
L², non-summable correlations). What is rigorously established: (i) the exact
Birkhoff/identity structure (§1.3–1.4, V1–V5); (ii) a clean *conditional*
reduction — `C` ⇔ the `M→∞` limit of σ²(M) for the **Hall-normalized
truncated** cocycle, with the truncation tail = Mikolás's `+O(1)`. The closing
input is named (effective horocycle equidistribution: plausible; weak mixing
alone: insufficient) and the obstruction (raw cocycle not L²-uniform) is made
explicit rather than hidden.

---

## 3. The founding dichotomy in BCZ/horocycle terms ([PROVEN], V5)

Prime = only-new vs composite = always-overlap is **exactly the primitivity
(visibility) of the bottom-row lattice vector**:

- At scale `Q`, the new Farey points are `h/Q` with `gcd(h,Q)=1`; the lattice
  vector `(h,Q)` is **primitive ⇔ visible from the origin** (BCZ2000,
  *Distribution of lattice points visible from the origin*, the exact paper in
  the repo bibliography). Count of new = **φ(Q)**.
- **Prime p:** φ(p)=p−1, every `(h,p)`, 1≤h≤p−1, is primitive ⇒ p−1 new
  equispaced points, **zero re-trace** (V5).
- **Composite n:** φ(n)<n−1 strictly; the `h` with gcd(h,n)>1 give
  `h/n = (h/d)/(n/d)` — a fraction already present at the smaller denominator
  `n/d`, i.e. a **non-primitive lattice vector that re-traces an earlier
  visible point**. Re-trace count `(n−1)−φ(n)>0` (V5).

> **[PROVEN]** "Prime = only new lines, composite = always overlap" ≡ "bottom-
> row vector `(h,Q)` is primitive ⇔ visible (BCZ2000) ⇔ a new BCZ section
> point; non-primitive ⇒ re-trace." The prime-step `ΔA(m)=−1+p𝟙[p|m]` is the
> character-cocycle increment of inserting exactly the φ(p) visible vectors at
> scale p (V2).

This ties the founding lens directly to the one cited paper that is verified
in-repo (BCZ2000), which is the strongest citation anchor available.

---

## 4. Numerical verification (exact arithmetic)

Script: `verify_bcz_cocycle.py` (this dir). Output: `verify_output.txt`.
All Farey-side and identity-side computation uses Python `int`/`Fraction`
(exact); float only for the Mikolás tail constant and the asymptotic.

| Check | What it proves | Status |
|---|---|---|
| **V1** | BCZ map `(k,k')↦(k',κk'−k)` traverses all of `F_Q`, orbit length `|F_Q|−1`, `k+k'>Q` always | exact |
| **V2** | `A_Q(m)=Σ_{d|m}d·M(⌊Q/d⌋)` matches Ramanujan-sum `A_Q(m)`; `ΔA=−1+p𝟙[p|m]` | exact |
| **V3** | `J_direct` (exact ∫E²) vs Mikolás `(1/2π²)ΣA²/m²`; `N·W(N)` table → constant | exact + float tail |
| **V4** | interior gap `=1/(k k')`; `S_j=E_Q(f_j)` exactly every node; closed `S_end=0`; Q≤600 | exact Fraction |
| **V5** | #new at `Q` `=φ(Q)`; prime⇒retrace 0, composite⇒retrace>0 | exact |
| **V6** | Green–Kubo pre-check (raw): `c_0` grows with Q, `c_j~1/j`, σ²(L) drifts | numerical-only |
| **V7** | truncated cocycle: fixed-`T` cap fails; Q-scaled (Hall-unit) cap stabilizes `c_0` | numerical-only |

Run: `verify_output.txt`. **V3 headline:** `N·W(N)` rises monotonically
0.509 (Q=50) → 0.642 (Q=200) → 0.652 (Q=3200), consistent with the verified
`C≈0.66` (slow convergence, as the verified-fact note anticipates). The
Mikolás truncated sum tracks `J` to within the expected `+O(1)`. **V6 is the
honest negative:** raw cocycle not uniformly L², correlations not summable —
see §2.0.

---

## 5. Honest assessment + single highest-value next step

**Established (proven internally / exact):** the full Farey↔BCZ-cocycle
dictionary; discrepancy = Birkhoff sum `S_j=E_Q(f_j)` of the explicit cocycle
`g_j=1−Φ·gap` with the *corrected f_0=0 / cusp-gap boundary convention*
(V4, exact, every node, closed orbit); `J(N)` = roof-weighted second moment of
`S_j` matching Mikolás `+O(1)` and `N·W(N)→≈0.66` (V3); prime/composite
dichotomy = primitivity/visibility, anchored to **in-repo BCZ2000** (V5);
prime-step `ΔA(m)=−1+p𝟙[p|m]` algebra and the Mertens identity (V2);
BCZ map = full Farey orbit (V1).

**Failed / negative (reported honestly):**
1. No dynamical *proof* of Mikolás or of `C` — only a reduction.
2. **V6: the naive Birkhoff-CLT picture is false.** The raw cocycle
   `g=1−Φ·gap` is not uniformly L² (`c_0` grows with Q) and its
   autocovariances are not summable (`c_j~1/j`); Green–Kubo `σ²(L)` does not
   stabilize. So `C` is NOT a Green–Kubo sum of the *raw* cocycle. The valid
   reduction is to the **renormalized/truncated** cocycle (Mikolás `Σ A²/m²`
   with its `+O(1)` is precisely that truncation; the heavy gap tail = high-`m`
   frequencies = the discarded `O(1)`).
3. Weak mixing (Cheung–Quas) insufficient (qualitative). Athreya–Cheung,
   Cheung–Quas, Strömbergsson, BCZ2000 are now **[CITATION-LOCKED]** with
   verbatim primary-source quotes (`THEOREM_R_2026-05-15.md` §0); Mikolás /
   Cox–Ghosh–Sultanow remain **[CITATION-UNVERIFIED, not load-bearing]**.

**Single highest-value next step:** attack **theorem (R) for the
Hall-normalized truncated cocycle**. Concretely: change variables to the
normalized spacing `s = Φ·gap` (the BCZ section in Hall coordinates, where the
gap density is the explicit Hall–Boca–Cobeli–Zaharescu distribution), define
`g^{(M)} := 1 − min(s, M)` for fixed cutoff `M = O(1)` (equivalently the
Mikolás partial sum `m ≤ M`), and prove
`Var_ν(S_n^{(M)}) = σ²(M)·n + O(n^{1−δ})` with **summable correlations
uniformly in M**, then `M→∞` controlling the discarded tail by the verified
`A_Q(m)` decay (this tail IS Mikolás's `+O(1)`). The closing input is
**effective horocycle equidistribution (Strömbergsson power-saving rate)** for
the truncated twisted correlation `c_j = ∫ ĝ^{(M)}·ĝ^{(M)}∘Tʲ dν`. First
concrete actions: (a) **DONE 2026-05-15** — Athreya–Cheung + Strömbergsson +
Cheung–Quas + BCZ2000 PDFs pulled; section measure / return time locked with
verbatim page/theorem citations (`THEOREM_R_2026-05-15.md` §0); (b) rerun V7
in Hall units `s=Φ·gap` to confirm
`σ²(M)` is Q-stable per fixed `M` (cheap, immediate — V7 already shows the
Q-scaled diagonal stabilizes; just reparametrize); (c) then the analytic
equidistribution bound. **Hard constraint from V6/V7: do NOT pursue a CLT for
the raw or `gap·Q`-truncated cocycle — only the Hall-normalized one.**
