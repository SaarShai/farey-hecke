# TRACK-1 — Discharge of P2 (`hEject`): honest result + precise residual (2026-06-14)

**Goal:** make `ToplevelStitch.Xomega_lb_allq` fully unconditional by discharging the
carried genuine-map fact P2 = `GenuineClassP2.hEject` (the deep-mid ejection bridge).

**Headline:** P2 in its **current scalar-`Tmap` orbit form is FALSE** (verified
numerically, decisively). The honest, machine-verified progress made: a new
axiom-clean file `GenuineMapP2.lean` that builds the genuine successor `genStep`,
proves the exact observable identity, and **reduces the genuine-map version of P2 to a
single named analytic inequality** `PgenEjectTarget` (numerically certified for all
`q ≥ 5`, machine-proof OPEN — it is irreducibly branch-index-dependent new math). No
`sorry`; the residual is an explicit hypothesis. SEALED files untouched.

---

## 1. First-hand build / axiom state (quoted)

`~/.elan/bin/lake build GenuineMapP2 ToplevelStitch` → `Build completed successfully (8048 jobs).`

```
'GenuineMapP2.Pgen_genStep_eq'           : [propext, Classical.choice, Quot.sound]
'GenuineMapP2.genStep_prod'              : [propext, Classical.choice, Quot.sound]
'GenuineMapP2.Pgen_genStep_ge_prod'      : [propext, Classical.choice, Quot.sound]
'GenuineMapP2.genuine_hEject_of_target'  : [propext, Classical.choice, Quot.sound]
'GenuineMapP2.target_of_box'             : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq'          : [propext, Classical.choice, Quot.sound]
```

NOTE (stale-note correction): `L1bArcCoverage.fcorr_lb` is now **axiom-clean**
`[propext, Classical.choice, Quot.sound]` (no `sorryAx`) — L1b has been SEALED since
`genuine_map_facts_2026-06-13.md` was written, so `Xomega_lb_allq` carries **no
`sorryAx`**. The only remaining non-unconditionality is the carried hypotheses
(`hCorr`, the `GenuineClassP2.hEject` field = P2), not any `sorry`.

A separate clean type-check confirms `genuine_hEject_of_target`'s conclusion is
literally `1/l³ ≤ UniformOnset.Pgen l (genStep …)` (the exact P2 conclusion type).

## 2. THE decisive finding — P2's scalar-orbit form is FALSE (M1, mpmath/np, dps≥40)

P2 (`hEject`) asks, on the orbit `orbit (n+1) = UQ.Tmap l (orbit n)` (the **scalar**
branch-`q−1` map): deep-mid ∧ `Pgen(orbit n) < 1/λ³` ⟹ `1/λ³ ≤ Pgen(orbit (n+1))`.

Test over genuine deep-mid sub-threshold cells (q=7,12,19; ~16–34 k cells each):
- **SCALAR `UQ.Tmap` successor:** `Pgen(succ) < 1/λ³` in **100 %** of cells (worst
  margin ≈ −2.4). ⇒ P2-as-stated is FALSE.
- **GENUINE multi-branch successor `genStep`:** `Pgen(succ) ≥ 1/λ³` in **0** violations,
  all q. ⇒ P2 is TRUE only over the genuine map.

So P2 is **not a wiring gap**: the engine `perq_Xomega_lb_qge19` (and the whole q≥19
leg) is instantiated on the scalar `UQ.Tmap`, which is the WRONG dynamics on deep-mid
branches. (Consistent with the round-3/4 findings that scalar `Tmap` does not even
preserve Taha; only the genuine map does.)

## 3. What `GenuineMapP2.lean` proves (axiom-clean, the real progress)

* `genStep` = genuine multi-branch successor on the active branch
  `i = HeckeS1.branchIdx`: `(L_i, L_{i+1} + kλL_i)`, restated standalone over the
  imported `HeckeS1.cheb`/`L`/`branchIdx`.
* `Pgen_genStep_eq`: **exact** observable `Pgen(genStep) = L_i·L_{i+1} + kλL_i² + L_i²/λ`
  (sympy-matched). The `+L_i²/λ` slack is what makes ejection true on the FULL deep-mid
  range, beyond the product-only `ejection_kick` box.
* `Pgen_genStep_ge_prod`: `Pgen(genStep) ≥ (genStep product)` (slack ≥ 0).
* `genuine_hEject_of_target`: **REDUCTION** — the genuine-map `hEject` conclusion
  `1/λ³ ≤ Pgen(genStep)` follows from the single named inequality `PgenEjectTarget`
  (using `branchIdx ≥ 1` + the `L`-recurrence `L_{i+1}=λL_i−L_{i-1}` + floor `k≥0`).
* `target_of_box`: the verified product-box bound `1/λ³ ≤ λv²−uv` ⟹ `PgenEjectTarget`
  (the slack only helps), so the named target SUBSUMES the verified `ejection_kick_uniform`
  content; the residual is exactly the cells the box misses.

## 4. The named residual `PgenEjectTarget` — TRUE, but branch-dependent new math

With `u=L_{i-1}`, `v=L_i` at the deep-mid active branch `i=branchIdx`:
```
PgenEjectTarget :  1/λ³  ≤  λ·v² − u·v + v²/λ .
```
Equivalently (×λ³ > 0):  `1/λ³ ≤ … ⟺ u ≤ λv + v/λ − 1/(λ³v)`.

- **Numerically certified for ALL q ≥ 5** (M1): min margin 1.4e-3 … 6.4e-3 over 10⁵+
  deep-mid cells per q; equality tangent at `(u,v) = (1, 1/λ)`.
- **NOT implied by the uniform branch-local box** `{u≥1, v≤1, λv−u≤1, 2λv−u≥1, 1<λ<2}`:
  LP/sampling gives min `λ⁴v²−λ³uv+λ²v²−1 ≈ −4.8` at `(λ,u,v)=(1.996, 2.97, 0.995)`.
  The realized deep-mid `u` is far tighter (`u ≤ 1.65`); the missing upper bound on `u`
  comes from Taha membership `0<a≤1` via the **Casorati** inversion
  `a = u·c_i − v·c_{i-1}`, which depends on the individual Chebyshev values `c_{i-1},c_i`
  — i.e. **on the branch index `i`**. Sympy confirms `Pgen(a,b)` (hence the P2 premise
  `Pgen(a,b)<1/λ³`) is NOT a function of `(u,v,λ)` alone; it depends on `c_{i-1},c_i`.
- The existing `ejection_kick_uniform` is a uniform `(u,v,r,thr)` box statement whose
  premise is the BRANCH observable `Pobs = uv − rv² < thr`. On the genuine deep-mid
  cells, `Pobs ≈ 0.4–0.6 ≫ 1/λ³`, so that premise is essentially never met (q=7: 0 of
  9776), and the box `r∈[0.88,1.26]` is exceeded by the realized `r∈[0.50,1.32]`. So the
  verified machinery does NOT cover P2's actual antecedent.

## 5. Exact residual ledger (what remains for FULLY-unconditional `Xomega_lb_allq`)

1. **Architectural (the big one):** re-instantiate the q≥19 engine on the **genuine
   self-map** `Tgen : ℝ×ℝ→ℝ×ℝ` (floor computed = `genFloor`, branch-existence discharged
   from Taha), prove `Tgen` preserves Taha, and re-derive `perq_Xomega_lb_qge19` over
   `Tgen` instead of `UQ.Tmap`. This is the "genuine piecewise map assembly" repeatedly
   flagged open (mimo `FINDINGS_genuinemap_wiring` §3/§4; WF4/WF5 `genMapTrue`/`genFloor`
   were scratch, never committed/sealed). NON-trivial: includes Taha-invariance edge E1
   (`0<a'`) which was only partial.
2. **Analytic:** machine-prove `PgenEjectTarget` (branch-index-dependent; needs the
   Casorati `(u,v)↔(a,b)` relation + Taha `a≤1`, per branch). True (numerics), but a new
   ejection-grade lemma, NOT a rewrite and NOT covered by `ejection_kick_uniform`.

Both are genuine constructions/new math, out of scope for a wiring-level discharge.
`GenuineMapP2.lean` does ALL the definitional/algebraic work that is honestly provable
and isolates the residual to exactly (1)+(2) above. Not faked.

## Artifacts
`projects/aristotle_dispatch_v15/uniform_q5to18/GenuineMapP2.lean` (new, axiom-clean),
`lakefile.toml` (+1 lib entry). SEALED files (`L1bArcCoverage.lean`, `EjectionUniform.lean`,
`BCZHeckeS1_trichotomy.lean`, `*_VERIFIED`) NOT modified. M1 experiments
`/tmp/p2_*.py` (scalar-vs-genuine successor, target certification, branch-coordinate
analysis).
