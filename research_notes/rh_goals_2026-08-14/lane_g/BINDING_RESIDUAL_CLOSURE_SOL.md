# Residual closure — the four definitive open items of the q=8 Hardy/Hilbert binding

Date: 2026-08-20. Lane `research_notes/rh_goals_2026-08-14/lane_g`.
Branch `codex/prime-step-review-economic-validation`.

Target: the definitive remaining-OPEN list of `lane_g/HARDY_HILBERT_BINDING_SOL.md`
(verdict **REDUCED**), as fixed by the cold referee
`lane_g/HARDY_HILBERT_BINDING_REFEREE.md` (verdict **CONFIRMED at stated scope**)
and restated at `HARDY_HILBERT_BINDING_SOL.md:804-810`:

1. **R-B8-2** — MMS-disc ↔ checker-disc (radius) binding.
2. **R-B8-3** — contour containment.
3. **E1 receipt regeneration** at the q=7 gated standard.
4. **Threshold-split hygiene** in `Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json`.

House rules observed: receipts before claims; upper bounds UP, margins DOWN;
unproved = CONJECTURAL; each residual graded independently, never forced. **No
existing file was modified.** Everything new lives under
`lane_g/binding_close/`. Nothing was committed or pushed.

```text
$ git status --porcelain research_notes/rh_goals_2026-08-14/lane_f \
                         research_notes/rh_goals_2026-08-14/lane_g
?? research_notes/rh_goals_2026-08-14/lane_g/binding_close/
```

Interpreter `/Users/za/.venvs/farey-rh/bin/python` (python-flint, Arb/Acb ball
arithmetic, `ctx.prec = 384`). Primary source read with `pdftotext -layout` from
the banked `lane_g/MMS_arxiv_0912.2236.pdf`, SHA-256
`a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`.

## 0. Artifacts

All four receipts are sorted-key, wall-clock-free, and were verified
**byte-identical on a second run** (no `runtime_seconds`, no timestamp — the
defect that made the predecessor E1 probe un-pinnable).

| artifact | SHA-256 |
|---|---|
| `binding_close/Q8_MMS_DISC_ADMISSIBILITY_RECEIPT.json` | `42736df08be23800f0d92a97d941cb6ef18411ed6a3f73dd427112230f5328be` |
| `binding_close/Q8_CONTOUR_CONTAINMENT_RECEIPT.json` | `4bfc10657db4c2aed39d5252803e30853f44cd3f1773c23d46a2346aacc1d5c4` |
| `binding_close/Q8_E1_ENLARGED_CONTRACTION_GATED_RECEIPT.json` | `0adb89b70291fd4f2ddba781bc16be722925345b44eb5fb59fd80f64a4b6f38e` |
| `binding_close/Q8_THRESHOLD_SPLIT_AUDIT_RECEIPT.json` | `c4767a585991b0348e099f25764d72ba159e88a892e84d3e9fc8efb4083235db` |
| `binding_close/q8_mms_disc_admissibility.py` | `8ace1486b31421aea43cf1eb3bede8c18cfc77608816c07990d10467e55c7098` |
| `binding_close/q8_contour_containment.py` | `d6cd2cb8af3af08fddada00f0b82d5cffcadd1e1e6aae8ec32a7248591f0df25` |
| `binding_close/q8_e1_gated_receipt.py` | `6af5a2610691f27b2ffc21c6de3e8623d6b072c402a2acfc5ade9da0f8c5246b` |
| `binding_close/q8_threshold_split_audit.py` | `253d21a72511d2d67594f07f9fe8ef980d31f5eba3d085e9e686fa93a18e6887` |

Immutable inputs pinned inside the receipts:
`Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json`
`5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c`,
`Q8_E1_ENLARGED_PROBE_RECEIPT.json`
`7b0f0df79dd7c98ac4ede0673ef9fb189c093d6cb5ea24da470df70131799c96`,
plus `F8_R3B_RECEIPT.json` and `Q8_W_ENVELOPE_F1024_RECEIPT.json`.
The E1 driver refuses to run if the first two hashes move (the q=7 guard at
`f7_stage4b_reopt.py:78-79`, ported).

---

## 1. R-B8-2 — MMS-disc ↔ checker-disc binding. **PROVED (certified).**

### 1.1 What the residual actually asks

The referee's reduced form:

> identifying MMS's discs `D_i` with the checker's `D(c_i, a_i h_i)` for the
> induced `L_{s,±}` on `B_3`. B1 proves the partition-point geometry; the
> *disc-radius* choice (multipliers 10,4,2) is a repo optimization, and MMS
> Lemma 4.4 only asserts *existence* of admissible enlarged intervals. Nobody
> has bound the two.

The framing "identify the checker's discs **with** MMS's discs" is the wrong
target, and pursuing it is what kept the residual open. The checker's discs are
**not** MMS's exhibited intervals, and they need not be. This is the pivot:

**MMS Lemma 4.4 (p.16) is an existence statement, and every downstream use in
MMS sections 4 and 5 consumes only its two defining conditions, never the
particular family exhibited in its proof.**

Lemma 4.4, verbatim from the banked PDF (extraction lines 1007-1008):

> **Lemma 4.4.** There exist open discs `D_i ⊂ C`, `i ∈ A_{κ_q}`, with
> `Φ_i ⊂ D_i` and `ϑ_n(D_i) ⊂ D_j` for all `n ∈ N_{i,j}`.

Its proof (line 1013) reduces discs to intervals — "Since the maps `ϑ_n` are
conformal it is clear that the discs `D_i` with center on the real axis and
intersection equal to the open intervals `I_i` then satisfy Lemma 4.4" — and
then *exhibits one* family (Lemma 4.7, and the enlarged
`I_i = ([[−1;(−1)^i, n_i]], λ_q/4)` at line 1198). That family is a witness,
not a definition. So the correct binding obligation is:

> **Show the checker's discs satisfy the two conditions of Lemma 4.4.**

That is a finitely checkable statement, and it is what the receipt certifies.

### 1.2 The objects, fixed from source

* `Φ_i` is **the Markov cell itself**, MMS eq.(13), extraction line 518:
  `Φ_i := [φ_{i−1}, φ_i]`, `Φ_{−i} := [φ_{−i}, φ_{−(i−1)}]`, `1 ≤ i ≤ κ_q`.
  For `q = 2h_q + 2` (line 869) `Φ_i = [[[0;1^{h+1−i}]], [[0;1^{h−i}]]]`,
  i.e. exactly the checker's `φ_i = [1]^{h−i}_λ` family with `φ_0 = −λ/2`
  (`f8_certify_tb_blocks.py:124-143`). **The checker's partition points are
  MMS's, not merely similar to them** — this is B1, already PROVED, and it is
  what makes the cell-based discs eligible at all.
* `ϑ_n = S T^n`, i.e. `ϑ_n(z) = −1/(z + nλ_q)`. Confirmed against MMS's own
  `q = 3` computation at line 1049 (`θ_n(−1) = −1/(−1+n)` at `λ_3 = 1`).
* `N_{i,j}` for even `q`, Lemma 4.2 (p.13-14, referee-verified from the PDF):
  `N_{1,h} = Z_{≥2}`, `N_{1,−h} = Z_{≤−1}`, and for `2 ≤ i ≤ h`
  `N_{i,i−1} = {1}`, `N_{i,h} = Z_{≥2}`, `N_{i,−h} = Z_{≤−1}`; all other pairs
  empty.
* Checker geometry (F1024 pin): `c_i = (φ_{i−1}+φ_i)/2`, `h_i = (φ_i−φ_{i−1})/2`,
  `r_i = a_i h_i`, `(a_1,a_2,a_3) = (10,4,2)`, `κ = h = 3`.
  `D_i := D(c_i, r_i)`, and — as MMS's own symmetry requires — `D_{−i} := −D_i`.

### 1.3 The conformal-image lemma (why disc inclusions are exactly computable)

`ϑ_n` is a Möbius transformation with **real** coefficients, so it commutes with
complex conjugation. `D(c,r)` with `c ∈ R` is the unique disc symmetric about
`R` whose real trace is `(c−r, c+r)`. If the pole `−nλ` lies outside the closed
trace `[c−r, c+r]`, then `ϑ_n` is holomorphic on a neighbourhood of the closed
disc, maps its boundary circle to a circle again symmetric about `R`, and meets
`R` exactly at `ϑ_n(c−r)` and `ϑ_n(c+r)`. Hence

    ϑ_n(D(c,r)) = the open disc with diameter [ϑ_n(c−r), ϑ_n(c+r)],

whose centre and radius are computed **exactly** from the two endpoint images.
This is MMS's own line 1013 argument, made explicit. The pole-clearance
hypothesis is certified per check; the minimum over all 50 checks is
`≥ 0.746136`.

### 1.4 The negative-index reduction (no extra computation)

Set `D_{−i} := −D_i`. Then `Φ_{−i} = −Φ_i` (eq.(13)),
`N_{−i,j} = −N_{i,−j}` (Lemma 4.2, line 917), and

    ϑ_{−n}(−z) = −1/(−z − nλ) = 1/(z + nλ) = −ϑ_n(z).

So every Lemma 4.4 condition at a negative source index is the exact mirror
image of one at a positive source index. Verifying `i ∈ {1,2,3}` verifies all of
`A_{κ_q} = {±1, ±2, ±3}`.

This same choice `D_{−i} = −D_i` is **also** the hypothesis MMS's Lemma 5.1
needs: extraction line 1334, "This operator is well-defined since `D_{−i} = −D_i`
for all `i ∈ A_{κ_q}`." Our family satisfies it by construction, so the `P`
symmetry, the `(I±P)/2` splitting and the induced `L_{s,±}` on `B_{κ_q}` — the
passage the referee's D5 correctly located in the unnumbered paragraph on p.21,
not in Lemma 5.1 itself — transport verbatim. **This is precisely the step that
licenses the checker's 3-disc (rather than 6-disc) working space.**

### 1.5 The certified checks

`binding_close/q8_mms_disc_admissibility.py`, 384-bit Arb, verdict
**`PASS_ADMISSIBLE`**, 50 explicit checks + 6 uniform-tail lemmas, **0 failures**.

| check | statement | count |
|---|---|---|
| **C0** | `Φ_i = [φ_{i−1}, φ_i] ⊂ D_i` | 3 |
| **C3** | `ϑ_1(D_i) ⊂ D_{i−1}`, `i = 2,3` (`N_{i,i−1} = {1}`) | 2 |
| **C1** | `ϑ_n(D_i) ⊂ D_3` for `2 ≤ n ≤ 8`, `i = 1,2,3` (`N_{i,h} = Z_{≥2}`) | 21 |
| **C2** | `ϑ_{−n}(D_i) ⊂ D_{−3}` for `1 ≤ n ≤ 8`, `i = 1,2,3` (`N_{i,−h} = Z_{≤−1}`) | 24 |
| **tail** | uniform lemma covering `n > 8` in both families, `i = 1,2,3` | 6 |

**Uniform tail lemma.** For `z ∈ D(c_i, r_i)`, `|ϑ_n(z)| = 1/|z + nλ| ≤ 1/(d_n − r_i)`
with `d_n = |c_i + nλ|`. And `D(0, ε) ⊂ D_{±3}` whenever `ε < r_3 − |c_3| = h_3`,
because `|c_3| = h_3` and `r_3 = 2h_3` **exactly** (`φ_3 = 0` forces `c_3 = −h_3`;
`a_3 = 2` forces `r_3 = 2h_3`) — the same exactness B1 already records. So it
suffices that `(d_n − r_i)·h_3 > 1`. `d_n` increases in `n` by exactly `λ` per
step, so certifying the criterion at `n = 9` certifies all `n ≥ 9`. Certified
criterion values `(d−r)h_3 − 1`, worst case: **`≥ 3.056980`** (positive family,
source disc 1); all six lie in `[3.056, 3.556]`. Not marginal.

**Worst certified margins** (`r_j − |c_j − c_img| − r_img`, DOWN):

```text
C3  ϑ_1(D_3) ⊂ D_2        margin ≥ 0.136339356039601210851
C2  ϑ_{−1}(D_3) ⊂ D_{−3}  margin ≥ 0.177743479094866625914
C0  Φ_3 ⊂ D_3             margin ≥ 0.270598050073098492199
C2  ϑ_{−1}(D_1) ⊂ D_{−3}  margin ≥ 0.285428196612412321204
C3  ϑ_1(D_2) ⊂ D_1        margin ≥ 0.296948392725219293604
min pole clearance over all 50 checks                ≥ 0.746136053416
```

**Independent cross-check.** The exact endpoint-image algebra was re-derived by
a completely different method: 4001-point boundary sampling of each source disc
in double precision, mapping each sample and testing membership in the target
disc, for all 50 (i, j, n) triples. **Zero failures**, and the sampled worst-case
image distances agree with the certified radii. A sign error or an
endpoint/centre confusion in §1.3 would show up here immediately.

### 1.6 What is proved

> The F1024 disc family `D_{±i} = ±D(c_i, a_i h_i)`, `(a_1,a_2,a_3) = (10,4,2)`,
> `i = 1,2,3` — the family every pinned q=8 receipt uses — satisfies both
> defining conditions of MMS Lemma 4.4 at `q = 8`, together with the symmetry
> `D_{−i} = −D_i` that Lemma 5.1 requires. It is therefore an **admissible
> realization** of MMS's discs, and MMS's `B = ⊕_{i∈A_κ} B(D_i)` construction,
> Theorem 4.10 and Lemma 5.1 apply to it verbatim.

Two honest strengthenings, both in our favour:

* Lemma 4.4 asks only for `⊂`. We certify **strict containment with positive
  margin**, i.e. `ϑ_n(D_i) ⋐ D_j`. MMS's Theorem 4.10 proof (extraction lines
  1291-1297) obtains nuclearity of `L^∞_{n,s}: B(D_i) → B(D_j)` "in a similar
  manner as for the transfer operator of the Gauß map", which *needs* relatively
  compact containment; MMS never records that as a hypothesis on the `D_i`. We
  supply it explicitly, so the transport of Thm 4.10 rests on a certified
  hypothesis rather than on an unstated one.
* The uniform tail lemma gives image radii `→ 0` at rate `O(1/n)` with all
  images inside a fixed `D(0,h_3) ⋐ D_{±3}`, which is the summability the
  nuclear-of-order-zero conclusion consumes.

### 1.7 What is *not* claimed

Not claimed: that the checker's discs equal MMS's exhibited intervals of Lemma
4.7 / p.19 — **they do not**, and the note explicitly does not assert it. Not
claimed: any statement about other `q`, other radius multipliers, or the
optimality of `(10,4,2)`. The multipliers remain a repo optimization; what is
now proved is that this particular optimization lands inside the admissible set,
which is the only thing the binding needed.

**Verdict: PROVED (certified).** R-B8-2 closes, in the stronger `⋐` form.

---

## 2. R-B8-3 — contour containment. **DISCHARGED-BY-RECEIPT.**

### 2.1 The three-part obligation

The residual, as stated at `HARDY_HILBERT_BINDING_SOL.md:569-574`, is that the
certification contour must lie inside the region where the disc / holomorphy /
clearance certificates hold, and that the containment was "stated here, not
certified in a receipt". It decomposes into:

(a) what the contour *is*; (b) whether it lies in `Ω*`; (c) whether the
certificates it must not escape are s-dependent at all.

### 2.2 (a) The contour

From `lane_f/q8_schur_contour.py:45-51` and `:765`, via
`q8_contour_helpers.closed_boundary_segments(re, im, hx, hy, K)` called with
`hx = hy = HALF_WIDTH`: the contour is the **boundary of the axis-aligned square**

    centre  s₀ = 0.4252310423737965 + 4.345760788321986 i,   half-width 1e−6,

traversed bottom → right → top → left, `K` subsegments per edge (`DEFAULT_K = 1`,
i.e. 4 arcs at the flagship setting). This is **exactly** the `s_box` of the
pinned `f8_receipts/F8_R3B_RECEIPT.json` (`re`, `im`, `half_width` all matching
as strings; certified `pin_box_matches_R3B_receipt: true`).

### 2.3 (b) Containment, certified on the closed box

`Ω* = {Re s > 1/2} ∪ {Re s > 0, Im s > 1}` (`HARDY_HILBERT_BINDING_SOL.md:474-475`),
open, connected, disjoint from the real pole lattice `s = (1−k)/2`.

`binding_close/q8_contour_containment.py` certifies the **closed box** — which
subsumes the boundary, hence the contour and every arc endpoint at every
subdivision `K`, since `Re` and `Im` are affine along each edge and extremal at
corners. Verdict **`PASS_CONTOUR_IN_OMEGA_STAR`**:

```text
component used            {Re s > 0, Im s > 1}
Re margin  (Re_min − 0)   ≥ 0.4252300423737965
Im margin  (Im_min − 1)   ≥ 3.345759788321986
distance to real pole lattice (Im_min)  ≥ 4.345759788321986
arc endpoints re-certified from closed_boundary_segments   true
```

**A fact worth stating plainly, because it is easy to miss and it changes what
the downstream argument must do:** the contour is **not** in the first component.
`Re_min − 1/2 = −0.0747699576…`, certified negative. The whole box lives only in
`{Re s > 0, Im s > 1}`. Therefore B7/B8 on this contour are *not* available from
the classical `Re s > 1/2` convergence region; they are available only through
the meromorphic-continuation/identity-theorem extension across `Ω*`. That
extension is B7's and B8's business and is already graded (B7 PROVED conditional
on B2; B8 REDUCED). Nothing here weakens those grades — but any future note
that cites "the pin is in `Ω*`" must not silently upgrade that to "the pin is in
the half-plane of absolute convergence".

### 2.4 (c) s-independence of the certificates

Audited mechanically by signature inspection, recorded in the receipt:
`q8_tb_support.clearance_rows`, `pole_margin`, `branch_cut_margin`,
`certify_block`, `contour_sup` **take no `s` argument** — they are pure
z-plane disc geometry in `(centers, radii, lam)`. Correspondingly neither
`Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` nor
`Q8_E1_ENLARGED_PROBE_RECEIPT.json` carries a `pin` field at all. Consequently
**no choice of `s` on the contour can invalidate a disc, pole, branch-cut or
enlargement certificate**; they hold uniformly along it.

The one genuinely s-dependent certified object, the `W` weight envelope
(`q8_weight_envelope.py:58-59`), is built as the single Acb ball
`acb(PIN_RE ± hx, PIN_IM ± hx)` — that is, the **entire box**, not the midpoint —
so its bound `W_{≥1} ≤ 31.7359279967148742842380` already holds for every `s` on
the contour. Certified `pin_matches_contour_box: true`.

### 2.5 Grade, and what stays open

The mathematical content is two strict inequalities on rational-decimal
endpoints plus a signature audit; there is no new mathematics here, which is why
the grade is **DISCHARGED-BY-RECEIPT** and not PROVED. It is now a hash-pinned
receipt rather than a sentence in a note, which was the whole of the complaint.

Explicitly still OPEN and untouched: the four-edge winding integral, the
continuous-contour gate of `Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_SOL.md`, the
`N = 104` run (never executed — `"The N=104 contour was not run."`), the
omitted-output row/projection tail, and `full_tail_certified`, which remains
`false`. R-B8-3 was co-listed with those; it is a much smaller object than they
are, and closing it does not move them.

---

## 3. E1 receipt regeneration at the gated standard. **DISCHARGED-BY-RECEIPT.**

### 3.1 The gap, precisely

`f8_receipts/Q8_E1_ENLARGED_PROBE_RECEIPT.json` (schema
`q8-e1-enlarged-probe/v1`) is `status: "DIAGNOSTIC_ONLY"`. Against the q=7
gated artifact `f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json` (schema
`f7-e1-enlarged-contraction/v2`, written by `f7_stage4b_reopt.py`) it is missing:
`verdict`, `immutable_inputs`, all three `eta` fields, `precision_bits`,
`backend`, `gate`, `enlargement_rule`, `enlargement_relative_cap`, `role`,
`radius_multipliers_exact_strings`, `rho_hat_worst_block_label`; its rows carry
4 keys where q=7 carries 12; clearances and enlargements are recorded
**per source disc**, not per block; and it carries `runtime_seconds`
(wall-clock), which alone makes it un-hash-pinnable.

### 3.2 What was regenerated

`binding_close/q8_e1_gated_receipt.py` → `Q8_E1_ENLARGED_CONTRACTION_GATED_RECEIPT.json`,
schema `q8-e1-enlarged-contraction/v2-gated`, verdict **`PASS_RHO_HAT_LT_1`**.

Same mathematics, same tracked lane_f routines, no lane_f edit: the `THRESHOLD`
override is applied in-process exactly as `q8_e1_probe.py:48-49` does, and is
now **recorded in the receipt**, which the diagnostic never did. Sorted keys, no
clock; verified byte-identical on re-run. Input-hash guard ported from
`f7_stage4b_reopt.py:78-79`.

**Fidelity gate.** The regenerated run reproduces the pinned diagnostic exactly:
`reproduces_pinned_diagnostic_probe: true`, the enlarged-relative `ρ̂` being
string-identical to the pinned `rho_hat_upper_bound`. So this is a re-grading of
the artifact, not a re-computation with different numbers.

### 3.3 The denominator-convention fix

The cold referee established that the q=7 receipt is **base-target-relative**
while the q=8 probe is **enlarged-target-relative** — two different conventions
published under the same bare field name `rho_hat_upper_bound`. Rather than pick
one, the regenerated receipt publishes **both**, each under an unambiguous name,
and derives the base-relative value directly from the certified sup divided by
the base target radius (not through the `1.15` inflation shortcut):

```text
rho_hat_upper_bound_enlarged_target_relative  ≤ 0.765068270705029641495394   (3→2, +1, head)
rho_hat_upper_bound_base_target_relative      ≤ 0.879828511310784087719702   (3→2, +1, head)
eta_max_upper_bound                           ≤ 0.869565217391304347826087   ( = 20/23 )
```

The base-relative value agrees with the referee's independent bypass
recomputation to 22 digits, and `η_max = 20/23` coincides **exactly** with the
q=7 receipt's `eta_max_upper_bound` — as it must, since `η = R/(R+0.15R) = 20/23`
whenever the relative cap binds, which it does on all three q=8 discs.

### 3.4 Per-block table (all 8 eq.(32) occurrences)

| label | tail | ρ̂ enlarged-rel | ρ̂ base-rel | η | remaining clearance |
|---|---|---|---|---|---|
| `1→3, +2, tail` | yes | 0.4966750401 | 0.5711762961 | 20/23 | ≥ 1.93944709 |
| `1→3, −1, tail` | yes | 0.5014178928 | 0.5766305768 | 20/23 | ≥ 1.78093442 |
| `2→1, +1, head` | no | 0.6900484741 | 0.7935557452 | 20/23 | ≥ 0.67888482 |
| `2→3, +2, tail` | yes | 0.4953060592 | 0.5696019681 | 20/23 | ≥ 2.52664388 |
| `2→3, −1, tail` | yes | 0.4998337464 | 0.5748088084 | 20/23 | ≥ 1.98544778 |
| `3→2, +1, head` | no | **0.7650682707** | **0.8798285113** | 20/23 | ≥ 0.95478549 |
| `3→3, +2, tail` | yes | 0.4946835261 | 0.5688860550 | 20/23 | ≥ 2.80254456 |
| `3→3, −1, tail` | yes | 0.6393057468 | **0.7352016088** | 20/23 | ≥ 1.49598159 |

All 8 blocks: `ratio_less_than_one` in **both** conventions, `η < 1`, remaining
pole/branch-cut clearance strictly positive. `block_count = 8 = block_count_expected`.

**This independently reconfirms referee defect D1.** The SOL note's B6b/V5 line
"the six tail families all sit at `≤ 0.577`" is false: five do
(0.5712, 0.5766, 0.5696, 0.5748, 0.5689), and `3→3, −1, tail` sits at
**0.7352016088**. The outlier is the family whose leading term is at `n = 1` —
the even-q novelty. The regenerated receipt records the true per-block values, so
the false line cannot propagate through this artifact. It does not touch `ρ̂_H`,
which is set by the `3→2` head.

The per-block `remaining_pole_cut_clearance_lower_bound` is new information the
diagnostic could not express: the worst is `0.678884824…` at `2→1, +1, head`,
which is exactly the worst enlarged margin the SOL note's V4 reports — the two
now agree per block rather than per source disc.

### 3.5 Grade

The obligation was to produce a receipt-grade artifact for mathematics that was
already proved (B6a/B6b) and already independently reproduced by the referee.
That is an artifact task, so the grade is **DISCHARGED-BY-RECEIPT**, not PROVED.

One caveat is recorded inside the receipt rather than hidden: the per-term key
`q8_tb_support` emits is the hardcoded literal `ratio_less_than_0_70`
(`q8_tb_support.py:125,154,166,183,211`), which is **misnamed** under the 0.99
override this run uses. The gate that matters — `ρ̂ < 1`, in both conventions —
is recorded explicitly per block and does not depend on that key. See §4.

---

## 4. Threshold-split hygiene. **DISCHARGED-BY-RECEIPT.**

### 4.1 The split, exactly

`Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` was written by two unconnected
gates:

| what | gated at | code |
|---|---|---|
| every **per-term** flag (`ratio_less_than_0_70`, `pass`, `deep_ratio_less_than_0_70`) | **0.70** | `q8_tb_support.py:17-18` (module default), read at `:118` and `:142` |
| every **block-level** `pass` (AND of its terms) | **0.70** transitively | `q8_tb_support.py:196,212` |
| top-level `rho_less_than_threshold` | **0.99** | `q8_candidate_tb_cert.py:73` (hardcoded literal) |
| top-level `certification_verdict = "PASS_RHO_LT_0.99"` | **0.99** | `q8_candidate_tb_cert.py:79` (hardcoded literal) |
| receipt fields `threshold` / `threshold_text` | `"0.99"` | `q8_candidate_tb_cert.py:71-72` |

**Root cause.** `q8_candidate_tb_cert.py` imports `f8_certify_tb_blocks` for
geometry only (`:31-33` — `lam_ball`, `disc_geometry_for`, `BLOCKS`) and never
calls its `run()`, so the 0.99 re-target at `f8_certify_tb_blocks.py:396-397`
never executes. `q8_tb_support.THRESHOLD` stays at its module default `0.70` for
the whole run, while the driver re-implements the global gate from scratch
against a hardcoded `"0.99"`. A secondary tell: `threshold` is written as a bare
Python string, whereas every sibling receipt writes an Arb ball text
(e.g. `F8_TB_BLOCK_CERTIFICATES_RECEIPT.json` has
`"threshold": "[0.990000000000000000000000 +/- 1e-29]"`).

### 4.2 Why the mixture is conservative — as a receipt, not an argument

`binding_close/q8_threshold_split_audit.py` re-reads **every certified ratio** out
of the pinned receipt and re-evaluates it in Arb against both thresholds.
Verdict **`PASS_MIXED_THRESHOLDS_ARE_CONSERVATIVE`**:

```text
terms audited                                        86   (80 head + 6 deep-tail)
all terms certified  < 0.70                          true
all receipt flags agree with the 0.70 recomputation  true
rho_star  ≤ 0.696590428020637535884545
rho_star  < 0.70   true          rho_star < 0.99   true
margin to 0.70  ≥ 0.003409571979362464115455
worst term:  3→2, +1, head  [head n=1]  ≤ 0.696590428020637535884545
```

The direction is unambiguous: **the per-term flags carry the stricter gate and
the headline verdict carries the looser one.** `0.70 < 0.99`, so every term that
passed at 0.70 passes at 0.99, and the published `PASS_RHO_LT_0.99` is implied
by — and strictly weaker than — what was actually certified. The residual risk
of the split runs the *other* way: a run whose declared gate is 0.99 could have
been rejected by the un-overridden 0.70 per-term gate (`certify_block` raises
when no `K` passes), producing a spurious **failure**, never a spurious pass.

That risk was not hypothetical here. `rho_*` clears 0.70 by only
**0.0034095719793624**. Had the `(10,4,2)` geometry pushed the `3→2, +1, head`
ratio ~0.5 % higher, the F1024 run would have failed under a gate it never
declared.

### 4.3 The key-name defect, and its blast radius

`ratio_less_than_0_70` is a hardcoded string literal
(`q8_tb_support.py:125,154,166,183,211`) that is never rewritten when
`THRESHOLD` is monkeypatched. In *this* receipt the name happens to be truthful
(the gate really was 0.70), which the audit confirms flag-by-flag. It is
**false-by-name elsewhere in the same family**, and that is the durable lesson:

* `F7_TB_BLOCK_CERTIFICATES_RECEIPT.json` — gated 0.80, `rho_* = 0.763212…`,
  yet its top terms (0.7632, 0.7629, 0.7597) all carry
  `"ratio_less_than_0_70": true`.
* `F8_TB_BLOCK_CERTIFICATES_RECEIPT.json` — gated 0.99, `rho_* = 0.907413…`,
  every term flagged `"ratio_less_than_0_70": true` at ~0.907.

**Standing rule this note asserts:** the field name `ratio_less_than_0_70` must
never be cited as evidence that a 0.70 gate was applied. Cite
`threshold_text` plus the certified `ratio_upper_bound`, or cite this audit.

### 4.4 Grade, and the residual left open

The obligation was to document precisely which threshold each certificate was
checked against and why the mixture stays conservative, as an auditable table.
That is delivered and receipted: **DISCHARGED-BY-RECEIPT**.

Left **OPEN** deliberately, because it requires editing tracked lane_f code and
re-emitting a hash-pinned receipt, neither of which is in this lane's authority:
re-emit `Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` from a driver that sets
`q8_tb_support.THRESHOLD` explicitly, records the value it used, and names the
per-term key after the live threshold. Until then the receipt's own field names
are not self-describing, and this audit is the citable evidence.

---

## 5. Final table

| Residual | Verdict | What a referee should attack |
|---|---|---|
| **R-B8-2** MMS-disc ↔ checker-disc binding | **PROVED (certified)** | The pivot: is Lemma 4.4 really consumed downstream only through its two conditions? Read MMS §4.3–5.1 for any use of the *specific* intervals of Lemma 4.7/p.19 — the load-bearing candidates are Thm 4.10's "similar manner as for the Gauß map" nuclearity step (which needs `⋐`, supplied here) and Lemma 5.1's `D_{−i} = −D_i` (satisfied by construction). Next: re-derive the conformal-image formula of §1.3 and confirm the endpoint (not centre) images define the image disc; a sign slip would flip a containment. Then re-run the uniform tail lemma at `n = 9` and confirm `d_n` really increases by exactly `λ` per step. Finally, check that `Φ_i` is the **cell** (eq.(13) line 518) and not a CF cylinder — the whole proof changes if it is not. |
| **R-B8-3** contour containment | **DISCHARGED-BY-RECEIPT** | Confirm the contour is the *box boundary* and not some other path: `q8_schur_contour.py:765` passes `hx = hy = HALF_WIDTH`. Then attack the s-independence audit — it is signature inspection, so look for an `s` smuggled through a closure, a module global, or a default argument in `contour_sup`/`certify_block`. Hardest: verify the claim that the certificates that *do* depend on `s` (the `W` envelope) were evaluated on the full box ball, not the midpoint. And note the honest finding of §2.3 — the contour is **outside** `{Re s > 1/2}`, so any downstream use of B7/B8 there must go through the continuation, never through classical convergence. |
| **E1 receipt regeneration** | **DISCHARGED-BY-RECEIPT** | Recompute `ρ̂` in the base-target-relative convention independently and confirm `0.879828511310784…`; then check that the *enlarged*-relative value is string-identical to the pinned diagnostic (fidelity gate). Verify byte-determinism by re-running. Check the per-block `remaining_pole_cut_clearance` against `q8_tb_support.clearance_rows` block by block — the diagnostic only ever had per-source minima, so this is genuinely new data and is the most likely place for an indexing error (source disc `i` vs target disc `j`). Confirm `η = 20/23` exactly on all three discs, i.e. that the relative cap binds and the clearance/4 branch never does. |
| **Threshold-split hygiene** | **DISCHARGED-BY-RECEIPT** (with an OPEN lane_f re-emission) | Verify the root cause by reading `q8_candidate_tb_cert.py:31-33` and confirming `f8.run()` is never called. Then confirm the conservativeness direction is stated correctly — the failure mode of this split is a spurious FAIL, not a spurious PASS. Attack the margin: `rho_*` clears 0.70 by 0.0034, so re-derive `0.696590428020637535884545` from geometry rather than consuming the receipt's string, which this audit deliberately does *not* do. And confirm the false-by-name claim against `F7_TB_BLOCK_CERTIFICATES_RECEIPT.json`. |

### Net movement

**R-B8-2 is closed and was the mathematical one.** The referee's own summary put
the remaining distance to a q=8 analogue of the referee-CONFIRMED q=7 Link 4b at
exactly two items: item 1 (MMS-disc ↔ checker-disc, *mathematical*) and item 3
(a gated, hash-bound, η-bearing E1 receipt, *mechanical*). Both are now
delivered, together with the two smaller items. The key that opened item 1 was
declining the stated framing — Lemma 4.4 is an existence statement, so the
obligation is admissibility, not identity.

### Explicitly NOT claimed

The gate `(HH)` is **not** claimed CLOSED by this note; grading the assembled
gate is the next referee's call, not this note's. No q=8 determinant, Fredholm,
Selberg, zeta, scattering, resonance, winding, parity, automorphic or LAW
statement. B2 and B8 keep their **REDUCED** grades and B7 stays PROVED
*conditional on B2* — nothing here bears on them beyond R-B8-2 and R-B8-3.
The omitted-output row/projection tail, `recorded_tail_checks_pass`
(independently false), `K_s` nonvanishing, word/lattice identification, common
meromorphic continuation and Selberg factorization, the four-edge winding, the
`N = 104` vs `N ≥ 262` pin decision, and the continuous-contour gate all remain
**OPEN** and untouched. `full_tail_certified` remains **`false`**.
Referee defects D2, D3, D4, D5, D6 are corrections owed to
`HARDY_HILBERT_BINDING_SOL.md` and are not addressed here; D1 is independently
reconfirmed in §3.4.

---

**READY FOR JUDGING**

---

## Dated correction block (2026-08-20, closure referee DEF-1..DEF-9, append-only)

Applied per BINDING_RESIDUAL_CLOSURE_REFEREE.md (verdict CONFIRMED at
stated scope; nine defects, none refuting a claim):

- **DEF-1 (material wording)**: the headline sentence "MMS §4-5 consume
  only its two defining conditions" is WITHDRAWN and replaced by the
  enumerated consumed-properties list: (a) open real-centred discs with
  holomorphy on D_i + continuity on the boundary; (b) D_{-i} = -D_i;
  (c) relatively compact containment (needed by Thm 4.10 nuclearity AND
  the trace fixed points); (d) the power convention
  (n+z)^{2s} := ((n+z)^2)^s, requiring (z+n*lambda)^2 off (-inf,0] on
  D_i.  All four are satisfied: (a)-(c) as certified in this note; (d)
  is implied by the certified pole clearance >= 0.746 (referee-derived)
  and matched by q8_weight_support.theta_prime's squared convention.
- **DEF-2**: "No existing file was modified" was true pre-commit; the
  banking commit ccba1e2 also appended +33/-0 to MAP.md per the
  standing wayfinder rule.
- **DEF-3**: "min pole clearance over all 50 checks" — over the 47 map
  checks; the 3 C0 point-in-disc checks carry no pole.
- **DEF-4**: "certify_block raises when no K passes" holds for tail
  blocks only; non-tail blocks return pass: False without raising and
  certification_verdict never consumes block pass — the split's other
  failure mode is a self-contradictory receipt, not a hard FAIL
  (conservativeness direction unaffected).
- **DEF-5**: the two *_has_no_pin_field entries in the containment
  receipt are hardcoded literals, not computed audits (referee verified
  both true by hand); flagged as the lane's own defect class.
- **DEF-6**: arc_endpoints_recertified has a latent fail-open path
  (non-dict segments -> vacuous pass); currently genuine (4 segments,
  8 endpoints verified).
- **DEF-7 (scope)**: R-B8-3 closes only the geometric-containment half
  of the residual as the prior referee worded it; the continuous-
  contour gate remains the open half and is item 5 of the
  still-standing list.
- **DEF-8**: q7's max_N has no q8 counterpart (q8 substitutes
  M_enlarged_contour_arcs/K_start/K_max) — omitted from §3.1's gap
  list.
- **DEF-9**: §4.3's F7 triple mixes head and deep-tail terms; F8's
  "~0.907" is the deep-tail maximum (heads top out at 0.8032).

The referee's 12-item still-standing list (its §3) is adopted verbatim
as the authoritative q8 flip ledger; items 1-6 are the operative
blockers; items 8 (continuation routing on the off-half-plane contour)
and 9 (correction-block supersession of the prior D1 lines) are
required reading before ANY citation of this chain.
