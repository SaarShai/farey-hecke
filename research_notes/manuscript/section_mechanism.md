# The rotation-arc mechanism on the conserved energy ellipse

*Draft technical section for the joint manuscript (Shai–Koyama). Every load-bearing
assertion is tagged with its verification status:*

- **[PROVEN:Lean `<lemma>` in `<file>`]** — a `sorry`-free, axiom-clean Lean 4 theorem
  (Mathlib v4.28.0). Every cited lemma was re-elaborated on 2026-06-20 with
  `lake env lean`; each `#print axioms` returns exactly
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`, no `nativeDecide`).
- **[CERTIFIED-NUMERIC]** — exact rational / high-precision (`mpmath` dps=50) arithmetic
  whose *integer* output is robust under refinement.
- **[HEURISTIC]** — double-precision / Monte-Carlo evidence, or a model-level claim not
  yet formalized.

All Lean paths are under
`projects/aristotle_dispatch_v15/uniform_q5to18/`. The energy invariant
`E(a,b)=a²−λ a b+b²` is exactly Koyama's conserved energy of the last-branch
elliptic step (see §1, "Tie to Koyama's energy").

---

## 1 · Setup: the last-branch step is an elliptic rotation on a conserved energy ellipse

Fix `q ≥ 5`, `θ = π/q`, `λ = 2cos θ = 2cos(π/q)`. On the last (scalar) branch `i = q−1`
of the Hecke–Taha BCZ map, the genuine successor with floor digit `k` is

>   `kstep k : (a,b) ↦ (b, −a + kλb)`.

When `k = 1` this is the linear map

>   `M = [[0, 1], [−1, λ]]`,    `det M = 1`,   `tr M = λ = 2cos(π/q)`.

Because `tr M = 2cos θ ∈ (−2, 2)`, `M` is an **elliptic** element of `SL₂(ℝ)` with
rotation number `θ/2π = 1/(2q)`. It preserves the positive-definite binary quadratic form

>   `E(a,b) = a² − λ a b + b²`   (discriminant `−4 sin²(π/q)`).

**[PROVEN:Lean `Mmap_preserves_E` in `BCZHeckeRotationArc.lean`]** `E(M p) = E p` for every
`p ∈ ℝ²`, parametric in `l = λ`.
**[PROVEN:Lean `det_M`, `trace_M` in `BCZHeckeRotationArc.lean`]** `det M = 1`, `tr M = λ`.
**[PROVEN:Lean `E_posdef` in `BCZHeckeRotationArc.lean`]** `E` is positive-definite for
`0 < l < 2` (`E p > 0` for `p ≠ 0`).
**[PROVEN:Lean `coord_sq_le` in `BCZHeckeRotationArc.lean`]** the ellipse confines the
orbit: each coordinate is bounded by `√(2E₀/(2−λ))`.

**`M` is the literal rotation by `−θ`.** Let `A = [[1,−λ/2],[−λ/2,1]] = LLᵀ` (Cholesky),
and pass to the whitening coordinates `y = Lᵀx` that diagonalise `E` to `|y|²`. In these
coordinates `M` is a planar rotation.

**[PROVEN:Lean `Mmat_conj_eq_rot` in `BCZHeckeRotationArc.lean`]** With
`Mmat θ = [[0,1],[−1,2cos θ]]`, `LTmat θ = [[1,−cos θ],[0,sin θ]]`, and
`Rotmat θ = [[cos θ, sin θ],[−sin θ, cos θ]]`, for `0 < θ < π`:

>   `LTmat θ · Mmat θ · (LTmat θ)⁻¹ = Rotmat θ`.

`Rotmat θ` is the clockwise rotation by `θ` (rotation by `−θ`), so **on every level set
`E = E₀` the state advances by exactly `−θ = −π/q` per `k=1` step**. This is the exact
(beyond det/trace) form of the elliptic-rotation claim; it was confirmed independently at
dps=50 (Rot-angle `= −π/q` to 12 digits, `det = 1`, `E(x) − E(Mx) ≈ 10⁻⁵²`)
**[CERTIFIED-NUMERIC]**.

**The k=1 step IS `M`, and the floor bracket.**
**[PROVEN:Lean `kstep_eq_Mmap_of_k1` in `BCZHeckeRotationArc.lean`]** when `k = 1`,
`kstep 1 = M`.
**[PROVEN:Lean `kfloor_eq_one_iff_bracket` in `BCZHeckeRotationArc.lean`]** the floor digit
`k = ⌊(1+a)/(λb)⌋` equals `1` exactly when the bracket `λb ≤ 1+a < 2λb` holds.
**[PROVEN:Lean `kfloor_ge_two_iff` in `BCZHeckeRotationArc.lean`]** the floor increments
(`k ≥ 2`) exactly when `2λb ≤ 1+a` — the *ejection criterion*.

**`E` constant along a run; termination at the first floor increment.**
**[PROVEN:Lean `E_run_const`, `E_run_pos` in `BCZHeckeRotationArc.lean`]** `E` is constant
(and positive) along an entire `k=1` run.
**[PROVEN:Lean `no_infinite_k1_run` in `BCZHeckeRotationArc.lean`]** no positive sequence
obeys the `M`-recurrence forever: every orbit must eventually hit a floor increment
(`k ≥ 2`). (The same qualitative termination is independently verified in
`projects/mimo-mini-project/lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` as
`HeckeNoRot.no_infinite_rotation`.)

### Tie to Koyama's energy `E`

The invariant `E(a,b) = a² − λ a b + b²` is precisely the conserved energy `E` Koyama
identifies for the corridor/last-branch dynamics: it is the unique (up to scale)
quadratic form fixed by the trace-`λ` elliptic element `M`, with `M` acting as a rigid
rotation of `E`'s level ellipses by the corridor angle `θ = π/q`. The whole mechanism
below is read off this single conserved quantity, so the "energy" language and the
"rotation-arc" language are two views of the same object: the last-branch dynamics is a
fixed-angle rotation of Koyama's energy ellipse, sampled at the discrete times when the
orbit returns to the last branch. The mechanism algebra is `q`-uniform — `E_conserved`
and `no_infinite_rotation` hold parametrically in `λ ∈ (0,2)`.

---

## 2 · `B(q)` = count of `π/q`-rotation lattice points in the sub-threshold arc of `E`

The cluster ceiling `B(q)` is the maximal length of a run of consecutive last-branch
points whose gap-product observable `P = a·b` stays below the onset threshold
`t = 1/λ³` (the `X_Ω(q) = 1/λ³` value). Combining §1:

- a maximal sub-threshold last-branch cluster lies on **one** energy ellipse `E = E₀`
  (`E` constant along the `k=1` run),
- its successive points are the images of the **`−π/q` rotation** of that ellipse, so
  they are equally spaced `π/q`-rotation lattice points,
- the run terminates at the first floor increment (`k:1→2`), which adds the translation
  `(k−1)λ·w_{q−1}` and kicks the state **off** the ellipse — the geometric "ejection".

Hence:

> **`B(q)` = the maximum, over energy ellipses `E₀` and phase offsets, of the number of
> consecutive `−π/q` rotation lattice points that are simultaneously last-branch and
> sub-threshold (`P < 1/λ³`), counting the terminal `k=2` sub-threshold point.**

The forward reduction — every such cluster *is* an `M`-rotation arc, so its length is
captured by the discrete rotation-arc count — is machine-verified:

**[PROVEN:Lean `run_isMRotArc_of_brackets` in `BCZHeckeRotationArc.lean`]** an
interior-bracket sub-threshold last-branch run is an `M`-rotation arc.
**[PROVEN:Lean `arc_E_const` in `BCZHeckeRotationArc.lean`]** all cluster points lie on
one `E`-ellipse.
**[PROVEN:Lean `cluster_is_rotation_arc` in `BCZHeckeRotationArc.lean`]** a maximal
sub-threshold last-branch cluster is a rotation arc.
**[PROVEN:Lean `cluster_le_rotation_arc` in `BCZHeckeRotationArc.lean`]** every
achievable cluster length is ≤ an achievable rotation-arc length (the forward `→`
direction of the characterization).
**[PROVEN:Lean `Bq_eq_rotation_arc` in `BCZHeckeRotationArc.lean`]** the full equivalence
`clusterCeiling ↔ rotationArcCount`, *given* the named realization bridge
`hrealize` (the converse / lower-bound inclusion). The bridge `hrealize`, the
interior-`k=1` confinement hypothesis, and the exact resonance value are carried as
**named hypotheses, not `sorry`** — they are the honest residuals (R1/R2/R3), discussed
where relevant below and itemized in §5.

The discrete rotation-arc count reproduces the genuine full-Taha-map `B(q)` for **all
`q = 7..40` with 100% agreement** (34/34, including the corrected `B(23) = 6`,
`B(24) = 6`), cross-checked against deep Monte-Carlo ground truth and dps=50 exact arc
dumps **[CERTIFIED-NUMERIC]**. The `k`-pattern of every maximal cluster is `[1,…,1,2]`:
`B(q)−1` interior `k=1` steps and one terminal `k=2` sub-threshold step.

> *Methodological note.* A *continuous* arc-width proxy `B₀(q) = ⌊W(q)·q/π⌋ + 1` does
> **not** equal `B(q)` in general — it is off by one at the resonance values (see §4). The
> exact law is the *discrete* lattice count, not a continuous closed form. This is the
> manuscript's honest headline: the mechanism is exact, the continuous formula is only an
> `O(1)` proxy / asymptotic-slope tool.

---

## 3 · Exact asymptotic slope `W_∞/π = 2 arcsin(1/3)/π = 0.216346895938785…`

The continuous governing width `W(q)` (the angular width of the full sub-threshold
last-branch arc on the governing ellipse `E₀ = (2−λ)/λ³`, peak `ab → t⁻`) has a closed
form. With `r = tan(θ/2) = √((2−λ)/(2+λ))`:

>   `W(q) = 2[ arccos( λ^{3/2} / √((1+λ)² + ((λ−1)r)²) ) − arctan( (λ−1)r / (1+λ) ) ]`.

**[CERTIFIED-NUMERIC]** (closed-form derivation in
`research_notes/Bq_width_resonance_closed_form_2026-06-18.md` §1; agrees with the repo
grid `goal1_Bq_arc_width_asymptotic.py` to all printed digits, e.g.
`W(7) = 0.9349194947`, `W(23) = 0.6786995407`, `W(61) = 0.6689641279`).

As `q → ∞`, `λ → 2` and `r → 0`; the boundary equation degenerates to
`3 cos α_∞ = 2√2`, i.e. `sin α_∞ = 1/3`, giving the **exact** limiting width

>   `W_∞ = 2 arcsin(1/3) = 2 arccos(2√2/3) = 0.679673818908243…`,

hence the **exact asymptotic slope**

>   `B(q) ~ (W_∞/π)·q ≈ 0.216346895938785 · q`,    `W_∞/π = 2 arcsin(1/3)/π`.

**[CERTIFIED-NUMERIC / HEURISTIC]** The constant `2 arcsin(1/3)/π = 0.216346895938785…`
is an exact closed form (replacing the earlier empirical "≈ 0.216"/"≈ 0.22"). The claim
that `B(q)` *tracks this line* (`B(q) ~ 0.216·q`) is a model-level asymptotic, supported
by the closed-form `W(q)` plus the 34/34 discrete-count match through `q=40`, but the
slope is **not** yet a Lean theorem — it sits in the L1b-family arc-width calculus that
remains open. The local expansion

>   `W(q) = 2 arcsin(1/3) − π/(3q) + (31√2·π²)/(18q²) + O(q⁻³)`

is **[HEURISTIC]** (Taylor expansion of the boundary equation at `θ = 0`; first-order
term cross-checked numerically, higher-order not independently certified).

---

## 4 · The parity gate: `+1` resonance occurs only at even run length `N`

The continuous proxy `B₀(q) = ⌊W(q)·q/π⌋ + 1` undercounts `B(q)` by exactly `1` at a
sparse set of "resonance" `q`. The mechanism is a **lattice-versus-notch** phenomenon and
is governed by a **proved parity gate**.

**Geometry of the notch.** On the observable `P(φ) = E₀(c₀ + amp·cos 2(φ − φ*))` — a
single double-angle cosine, peaked and reflection-symmetric at the symmetric point
`φ*` (`a = b`) — the super-threshold set `{P > t}` is a symmetric arc ("notch") of
half-width `δ` about `φ*`. A length-`N` symmetric run of `π/q`-rotation lattice points is
all sub-threshold iff none of its points lands in the notch. Writing the notch half-width
in `θ`-units `w = δ/θ`, the resonance regime is `δ < θ/2`, i.e. `0 < w < 1/2`.

**The parity gate (proved).** Index the symmetric `N`-point run by signed offsets
`rel N i = i − (N−1)/2` (in `θ`-units, measured from the peak).

**[PROVEN:Lean `rel_reflect` in `BCZHeckeRotationArcR3Parity.lean`]** reflection symmetry
of the offsets about the peak.
**[PROVEN:Lean `odd_center_on_peak` in `BCZHeckeRotationArcR3Parity.lean`]** if `N = 2m+1`
(odd) the central index `i = m` has `rel = 0` — a lattice point sits **exactly on the
peak**.
**[PROVEN:Lean `even_all_offpeak` in `BCZHeckeRotationArcR3Parity.lean`]** if `N = 2m`
(even) every index has `|rel| ≥ 1/2` — every point is at least a half-step off the peak.
**[PROVEN:Lean `straddle_of_even` in `BCZHeckeRotationArcR3Parity.lean`]** for even `N`
and any notch `w < 1/2`, every point avoids the notch (`w < |rel|`): the run **straddles**
the peak, all points sub-threshold.
**[PROVEN:Lean `impale_of_odd` in `BCZHeckeRotationArcR3Parity.lean`]** for odd `N` and
any notch `w > 0`, the central point is inside the notch (`|rel| = 0 < w`): the run is
**impaled**, one point super-threshold, the length-`N` run impossible.

These combine into the gate, in two equivalent forms (lattice and observable):

**[PROVEN:Lean `parity_gate` in `BCZHeckeRotationArcR3Parity.lean`]**
> for `0 < w < 1/2`: *every lattice point of a symmetric `N`-run avoids the notch*
> `⟺ N is EVEN`.

**[PROVEN:Lean `resonance_parity_gate` in `BCZHeckeRotationArcR3Parity.lean`]** the same
dichotomy phrased on notch membership (`inNotch w r := |r| < w`): the whole run is
sub-threshold `⟺ N` is even.

The observable side is also formalized:
**[PROVEN:Lean `Pphi_reflect` in `BCZHeckeRotationArcR3Parity.lean`]** `P(φ*+ψ)=P(φ*−ψ)`;
**[PROVEN:Lean `Pphi_peak` in `BCZHeckeRotationArcR3Parity.lean`]** `P(φ*) = E₀(c₀+amp)`;
**[PROVEN:Lean `impale_observable` in `BCZHeckeRotationArcR3Parity.lean`]** when the peak
pokes above threshold (`E₀(c₀+amp) > t`, the resonance ellipse `frac > 1`), the central
point of an odd run is super-threshold, so a length-`2m+1` symmetric sub-threshold run is
impossible;
**[PROVEN:Lean `superthreshold_iff_cos` in `BCZHeckeRotationArcR3Parity.lean`]** a flank
point at physical offset `ψ` is super-threshold iff `cos 2ψ > (t/E₀ − c₀)/amp`, the notch
equation, so `{P > t}` is exactly the symmetric interval `|ψ| < δ`.

**Gain form.**
**[PROVEN:Lean `gain_requires_even` in `BCZHeckeRotationArcR3Parity.lean`]** the resonance
gain (`+1`) is available **only when the target run length `N = B₀(q)+1` is even**
(equivalently `B₀(q)` odd).
**[PROVEN:Lean `odd_always_impaled` in `BCZHeckeRotationArcR3Parity.lean`]** if `N` is odd
the central point is always in the notch, irrespective of how narrow the arc near-fit —
no gain at odd target count.

The model prediction is then `B(q) = B₀(q) + R(q)`, where the resonance indicator
`R(q) = 1` requires `N = B₀(q)+1` even **and** the scalar near-fit window
`1 < ρ_min < ρ_max` (a one-line interval inequality in `q`, with
`ρ_min = (λ^{3/2}/D_N(q))²`, `ρ_max = 1/G(q)`; definitions in
`Bq_width_resonance_closed_form_2026-06-18.md` §3). **[HEURISTIC]** for the near-fit
half: the parity half of `R(q)` is the proved gate above; the interval inequality
`1 < ρ_min < ρ_max` is a scalar test verified numerically per `q`, not yet a Lean theorem.

**The rare resonance set.** A double-precision scan of the scalar gate up to `q = 10⁴`
gives the resonance values

>   `q = 23, 61, 126, 570, 1476, 1892, 6884`.

**[CERTIFIED-NUMERIC]** for `q ∈ {23, 61, 126, 570}` — high-precision symmetric-run checks
confirm the lower-bound witnesses (the actual symmetric lattice points are last-branch,
sub-threshold, with the terminal `k=2` ejection; e.g. `q=126`: `N=28`, `k`-pattern
`[1×27, 2]`, min domain margin `1.05e−5`, min threshold gap `2.62e−6`; `q=570`: `N=124`,
`k`-pattern `[1×123, 2]`, margins `8.4e−7 / 2.1e−7`). **[HEURISTIC]** for the larger three
`q ∈ {1476, 1892, 6884}` — double-precision scan only; these should be re-checked with
interval arithmetic before being treated as certified.

---

## 5 · "Parity beats proximity": the `q = 47` case

The parity gate is *unconditional in the near-fit*: it blocks an odd-length run **no
matter how nearly the arc fits**. The decisive natural experiment is `q = 47`. There
`B₀(47) = 10` (even), so the target run length `N = B₀+1 = 11` is **odd**. By
`odd_always_impaled`, the central lattice point lands exactly on the peak, which is
super-threshold whenever the resonance ellipse pokes above `t` — so the `+1` gain is
blocked **even though the arc near-fit at `q=47` is the closest yet** (arc only
`≈ 0.003·θ` short of the eleventh point). Parity beats proximity: the arithmetic of the
run length, not the analytic closeness of the arc width, decides the resonance.

By contrast `q = 23` has `B₀(23) = 5` (odd), target `N = 6` (even); by `straddle_of_even`
the six points straddle the peak and all stay sub-threshold, giving the genuine
`B(23) = 6` resonance. **[PROVEN:Lean]** for the dichotomy (the gate lemmas above);
**[CERTIFIED-NUMERIC]** for the specific `B₀` values and the `B(23)=6` / `B(47)=10`
witnesses.

---

## 6 · Honest residuals (the named hypotheses, not `sorry`)

The rotation-arc *mechanism* is machine-verified and axiom-clean; a fully unconditional,
all-`q` closed form for `B(q)` is **not** claimed. Three residuals remain, carried as
named Lean hypotheses (not `sorry` stubs):

- **R1 — interior-`k=1` confinement.** The bracket `λb ≤ 1+a < 2λb` at every interior
  cluster point. Its **lower** half (`k ≥ 1`) is now a theorem
  (`lower_bracket_preserved_on_ellipse`, `BCZHeckeRotationArcR1.lean` — verified
  axiom-clean), from the on-ellipse identity `1+a′−λb′ = (λa+b−1) + (2−λ²b)` with
  `λ²b < 2` on the sub-threshold ellipse. Its **upper** half is a phase-lattice residual
  (same family as R3). **[PROVEN:Lean lower half / HEURISTIC upper half]**.
- **R2 — realization bridge** (`hrealize`). The converse inclusion: every sub-threshold
  last-branch `M`-rotation arc is realized by a genuine cluster. Closed per-`q` for low
  `q` (`q=5,7` in `BCZHeckeRotationArcR2.lean`, axiom-clean); 34/34 numerically through
  `q=40`. A uniform all-`q` witness family needs the genuine-map measure assembly.
  **[PROVEN:Lean per-`q` low `q` / CERTIFIED-NUMERIC otherwise]**.
- **R3 — exact value / continuous-form gap.** The exact integer at resonance `q` exceeds
  the continuous proxy `⌊W(q)·q/π⌋+1` by 1; its **parity half** is now the proved gate of
  §4 (`resonance_parity_gate`), removing the parity component from the residual list. What
  remains is the scalar near-fit interval inequality `1 < ρ_min < ρ_max` (a small
  inhomogeneous-Diophantine / interval statement), and the L1b-family continuous arc-width
  calculus that would supply `W(q)` and the slope `W_∞/π` as Lean theorems.
  **[PROVEN:Lean parity half / HEURISTIC near-fit half]**.

**One-line standing.** `M` is the exact `−π/q` rotation of Koyama's energy ellipse
`E = a²−λab+b²` (det 1, trace `λ`); a sub-threshold last-branch cluster is one arc of
that rotation on a single `E`-level set, terminating at the first floor increment; the
cluster ceiling `B(q)` is the discrete count of `π/q`-rotation lattice points in the
sub-threshold arc, with a proved parity gate (`+1` only at even run length) accounting for
the rare resonances `{23, 61, 126, 570, …}` and the "parity beats proximity" failure at
`q=47`. The mechanism and the parity gate are `sorry`-free, axiom-clean Lean theorems; the
closed-form slope, the realization bridge, and the scalar near-fit are the honest open
residuals.

---

### Verification log (2026-06-20)

- `lake env lean uniform_q5to18/BCZHeckeRotationArc.lean` → exit 0; `#print axioms` of
  `Mmap_preserves_E, det_M, trace_M, Mmat_conj_eq_rot, E_posdef, coord_sq_le,
  kstep_eq_Mmap_of_k1, kfloor_eq_one_iff_bracket, genuine_step_eq_Mmap_of_bracket,
  kfloor_ge_two_iff, E_run_const, E_run_pos, no_infinite_k1_run,
  run_isMRotArc_of_brackets, arc_E_const, cluster_is_rotation_arc,
  cluster_le_rotation_arc, Bq_eq_rotation_arc` = `[propext, Classical.choice, Quot.sound]`
  (no `sorryAx`).
- `lake env lean uniform_q5to18/BCZHeckeRotationArcR3Parity.lean` → exit 0; `#print axioms`
  of `rel_reflect, odd_center_on_peak, even_all_offpeak, straddle_of_even, impale_of_odd,
  parity_gate, Pphi_reflect, Pphi_peak, impale_observable, superthreshold_iff_cos,
  resonance_parity_gate, gain_requires_even, odd_always_impaled` =
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`).
- (Subshell form: `( cd projects/aristotle_dispatch_v15 && lake env lean <file> )`.)

### Source notes
- `research_notes/Bq_rotation_arc_2026-06-14.md` (mechanism, corrected discrete
  characterization, 34/34 match, Lean status).
- `research_notes/Bq_width_resonance_closed_form_2026-06-18.md` (closed-form `W(q)`, exact
  slope `2 arcsin(1/3)/π`, scalar resonance gate, resonance set).
- Lean: `projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeRotationArc.lean`,
  `…/BCZHeckeRotationArcR1.lean`, `…/BCZHeckeRotationArcR2.lean`,
  `…/BCZHeckeRotationArcR3Parity.lean`;
  `projects/mimo-mini-project/lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`.
