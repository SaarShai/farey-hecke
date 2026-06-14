# GOAL-4 (other half) — discharge the carried genuine-map facts P1, P2 (2026-06-13/14)

**Files (all under `projects/aristotle_dispatch_v15/uniform_q5to18/`, no `_VERIFIED`
file edited, `fcorr_lb`/`L1bArcCoverage` untouched):**

- `GenuineMapFactsP1.lean` (new) — **(P1) PROVED**, axiom-clean. Independent of the
  slow window files.
- `GenuineMapFacts.lean` (new) — Step 3 q=19,20,21 unconditional extension (imports the
  three window files + `GenuineMapFactsP1`).
- `ToplevelStitch.lean` (edited) — added the P1-discharged class `GenuineClassP2`, its
  constructor `GenuineClassP2.toGenuineClass`, and `perq_Xomega_lb_qge19_P1discharged`.
  Now imports `GenuineMapFactsP1` (not the window files).
- `ToplevelStitchQ5to21.lean` (new) — the q≤21-unconditional, (P1)-discharged top-level
  theorem `Xomega_lb_allq_q5to21_P1` (imports `GenuineMapFacts` → window files).
- Copied `BCZHeckeG{19,20,21}_window_VERIFIED.lean` into the subproject (byte-identical
  to the `mimo-mini-project` originals; `diff -q` confirmed) + lakefile globs updated.

---

## P1 (hScalarDcorr) — **PROVED**, fully, from the existing genuine-map definition.

**Claim.** A genuine orbit point on the SCALAR branch (`IsFstep_concrete`, i.e.
`branchIdx = q-1 = m+1`) lies in the F-corridor `Dcorr` (both Taha edges + positivity).

**It needed no new construction** — only the existing `HeckeS1.branchIdx` /
`IsFstep_concrete` selector + the `cheb` boundary data. Mechanism (the branch-partition
geometry the task anticipated):

`UQ.Dcorr l (a,b) = (0<a ∧ a≤1 ∧ 0<b ∧ b≤1 ∧ a+l·b>1 ∧ l·a+b>1)`. The carried
`GenuineClass` fields already supply `0<a`, `a≤1`, `b≤1`, and `l·a+b>1` (the Taha lower
edge `1−l·a<b`). The two missing facts come from the scalar branch:

- `a + l·b > 1`: minimality of `branchIdx = m+1` applied at the strictly-smaller index
  `m` (requires `1 ≤ m`) gives `1 < L_m` (`scalar_entry_bound`); the boundary data
  `cheb(m+2)=0, cheb(m+1)=1` force `cheb m = l`, so
  `L_m = a·cheb(m+1) + b·cheb(m) = a·1 + b·l = a + l·b` (`L_at_m_eq`). Hence `a+l·b>1`.
- `0 < b`: from `a+l·b>1` and `a≤1`, `l·b > 1−a ≥ 0`, so `b>0` (`l>0`).

**Lemma (verified).** `GenuineMapFacts.scalar_implies_Dcorr` (in `GenuineMapFactsP1.lean`):
```
theorem scalar_implies_Dcorr (l a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1)
    (h1 : 1 < l) (hm : 1 ≤ m)
    (ha : 0 < a) (ha1 : a ≤ 1) (hb : b ≤ 1) (htaha : 1 - l * a < b)
    (hsc : IsFstep_concrete l a b m (branch_exists l a b m hq0 hq1 hb)) :
    (a, b) ∈ UQ.Dcorr l
```
`#print axioms` (quoted from `lake build`):
```
'GenuineMapFacts.scalar_implies_Dcorr' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `sorryAx`. (`1 ≤ m` is free in the assembly: `m = q-2 ≥ 3` for `q ≥ 5`.)

**Wired into the top-level theorem.** `ToplevelStitch` now defines `GenuineClassP2`
(same per-point data as `GenuineClass` minus the `hScalarDcorr` field — carries only
the (P2) bridge `hEject`) and
```
theorem GenuineClassP2.toGenuineClass (h1 : 1 < l) (hm1 : 1 ≤ m)
    (G : GenuineClassP2 l orbit n m) : GenuineClass l orbit n m
```
which rebuilds the full `GenuineClass` by FILLING `hScalarDcorr` from
`scalar_implies_Dcorr`. So `perq_Xomega_lb_qge19_P1discharged` accepts a genuine-map
definition that supplies **only (P2)**; (P1) is no longer a raw hypothesis.
`#print axioms` (quoted):
```
'ToplevelStitch.GenuineClassP2.toGenuineClass'       : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.perq_Xomega_lb_qge19_P1discharged'   : [propext, Classical.choice, Quot.sound]
```

---

## P2 (hEject) — **NOT provable** from the current genuine-map definition (HONEST).

**Claim P2 asks for.** On a deep-mid point (`IsDeepMid_concrete`, `branchIdx < m`),
`Pgen l (orbit n) < 1/l³  ⟹  1/l³ ≤ Pgen l (orbit (n+1))`, where the orbit evolves by
the SCALAR map `orbit (n+1) = UQ.Tmap l (orbit n)` and `Pgen p = p.1(p.1+l·p.2)/l`.

**Why it is blocked — precise obstruction.** The ejection arithmetic IS fully proved:
- `HeckeEjectionUniform.ejection_kick_uniform` (`EjectionUniform.lean`, axiom-clean)
  proves `thr ≤ λv² − uv` on `(u,v,r) = (L_{i-1}, L_i, X_{i-2}/X_{i-1})` at the active
  deep-mid branch `i = branchIdx`;
- `HeckeGenuine.succ_prod_lb` / `genStep_prod` (WIP file) lift it to the GENUINE
  successor PRODUCT `(genStep …).1·(genStep …).2 = L_i·L_{i+1} + kλL_i² ≥ λv² − uv`.

But this bounds the **genuine multi-branch successor** `genStep` on the *active* branch
`i = branchIdx < m`, with observable the *product* `succA·succB`. P2 instead needs:
(a) the observable `Pgen` (= `ab + a²/l`, NOT the product `ab`), and (b) the **scalar**
`Tmap`-successor (branch `q-1`), at `orbit (n+1) = Tmap l (orbit n)`.

On a deep-mid point `genStep ≠ Tmap l (orbit n)` (the genuine map acts on branch
`i = branchIdx`, the scalar `Tmap` on branch `q-1`). Identifying the two — i.e. that the
`Tmap`-orbit successor equals the genuine deep-mid successor and that the product bound
transfers to a `Pgen` bound at that point — IS the genuine measure-preserving-map orbit
invariance. That construction does not exist in any file: it is exactly the open item
"**Package `branchIdx` + the piecewise multi-branch map; discharge the assembly's
`hrec`/`hkick`**" recorded in `projects/mimo-mini-project/FINDINGS_genuinemap_wiring_2026-06-05.md`
§3/§4 (still OPEN there). `genStep` is defined (`BCZHeckeGenuineMap_allq_WIP.lean` §11) but
no lemma equates `genStep`-orbit dynamics with `Tmap`-orbit dynamics, and the WIP file
is NOT imported by the assembly (S1 only re-states `branchIdx`/`L`/`cheb`).

**Status: P2 remains carried** (now the SOLE genuine-map carry, in `GenuineClassP2.hEject`).
It is genuine new construction (the all-q genuine measure-preserving map), not a
defeq/rewrite — proving it would be the substantial "genuine piecewise map assembly"
work, out of scope for a rewrite-level discharge. Not faked.

---

## Step 3 — q = 19, 20, 21 unconditional extension (no `fcorr_lb`).

The window files `BCZHeckeG{19,20,21}_window_VERIFIED` are all **6-window** with EXACTLY
the `UQ.FwindowHyp6` shape (verified by reading their signatures: `hps` = per-q minpoly,
same `hposc/hcap/hreg/hgen/hrec` + 6-conjunct negation). So they discharge `FwindowHyp6`
verbatim and feed `UQ.perq_essSup_ge6` identically to q=17,18 — NO corridor, NO
`fcorr_lb`. Per-q minpolys (verbatim `hps`):
- q19: `l^9 = l^8 + 8l^7 − 7l^6 − 21l^5 + 15l^4 + 20l^3 − 10l^2 − 5l + 1`
- q20: `l^8 = 8l^6 − 19l^4 + 12l^2 − 1`
- q21: `l^6 = −l^5 + 6l^4 + 6l^3 − 8l^2 − 8l − 1`

New decls (in `GenuineMapFacts.lean`): `mpoly19/20/21`, `hF19/20/21 : UQ.FwindowHyp6`,
`Xomega_lb_q19/20/21`, `mpolyq21`, and the combined `Xomega_lb_q5to21` over the **17
indices** `{5,7,…,18,19,20,21}` (delegates {5..18} to `Xomega_lb_q5to18`, {19,20,21} to
the new discharges). Top-level (P1-discharged, q≤21-unconditional)
`ToplevelStitch.Xomega_lb_allq_q5to21_P1` in `ToplevelStitchQ5to21.lean` then needs the
corridor/`fcorr_lb` route only for **q ≥ 22**.

**Build status of Step 3: COMPLETE and axiom-clean.** `lake build GenuineMapFacts`
and `lake build ToplevelStitchQ5to21` both `Build completed successfully`. `#print
axioms` (quoted):
```
'GenuineMapFacts.Xomega_lb_q19'    : [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.Xomega_lb_q20'    : [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.Xomega_lb_q21'    : [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.Xomega_lb_q5to21' : [propext, Classical.choice, Quot.sound]   (17 indices, NO fcorr_lb)
'ToplevelStitch.Xomega_lb_allq_q5to21_P1' : [propext, sorryAx, Classical.choice, Quot.sound]  (sorryAx = fcorr_lb, q≥22)
```
The window files compile (first time, `maxHeartbeats 400000000`, 7-variable degree-9
`nlinarith`) very slowly (G19 alone ~4h wall) but axiom-clean. Two wiring bugs found
and fixed during build: (a) `mpolyq` is top-level not `UQ.mpolyq` (used `_root_.mpolyq`);
(b) needed an explicit `end` to close the `noncomputable section` before `end GenuineMapFacts`.

---

## Updated top-level `#print axioms` (all quoted from successful `lake build`):

```
'GenuineMapFacts.scalar_implies_Dcorr'               : [propext, Classical.choice, Quot.sound]   (P1 PROVED)
'ToplevelStitch.GenuineClassP2.toGenuineClass'       : [propext, Classical.choice, Quot.sound]   (P1 discharge)
'ToplevelStitch.perq_Xomega_lb_qge19_P1discharged'   : [propext, Classical.choice, Quot.sound]   (q≥19, P2-only)
'ToplevelStitch.genuine_orbitdata'                   : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.perq_Xomega_lb_qge19'                : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.L1b_carried'                         : [propext, sorryAx, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq'                      : [propext, sorryAx, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq_clean_modulo_B1'      : [propext, Classical.choice, Quot.sound]   (sorryAx isolation)
'GenuineMapFacts.Xomega_lb_q5to21'                   : [propext, Classical.choice, Quot.sound]   (17 indices, UNCONDITIONAL)
'ToplevelStitch.Xomega_lb_allq_q5to21_P1'            : [propext, sorryAx, Classical.choice, Quot.sound]   (P1-discharged, q≤21 uncond.)
```

`fcorr_lb` (in `L1bArcCoverage.lean:606`) is still the SOLE `sorryAx` source (q ≥ 22 only).

## Exact remaining set (after this session)

1. **`fcorr_lb`** — the uniform arc-width inequality (a different agent owns it). Unchanged.
2. **P2** — the genuine-orbit-invariance bridge = the all-q genuine measure-preserving
   map assembly (genStep↔Tmap orbit identification + product↔Pgen transfer on deep-mid).
   Genuine new construction; carried as `GenuineClassP2.hEject`. NOT a rewrite.
3. (For q ≥ 22 only) the block-sequence↦essSup corridor wiring of finding (2) in
   `toplevel_stitch_2026-06-13.md` — unchanged by this session.

## Net reduction

- **P1 eliminated** from the GenuineClass conditionality (proved, axiom-clean).
- Genuine-map carry reduced from {P1, P2} to {P2} (P2 honestly blocked + precisely
  reduced to the open genuine-map assembly).
- Unconditional partial extended 14 → **17 Hecke groups** ({5,7,…,21}); corridor +
  `fcorr_lb` needed only for q ≥ 22 (wiring done; compile pending slow window files).
