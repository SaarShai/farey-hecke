# Reciprocity-obstruction discovery scan — 2026-06-14

**Goal.** Hunt for a NEW Apollonian-style reciprocity obstruction (a chi_2 = Kronecker-symbol
local-global counterexample) in thin (semi)groups / integral packings, using a cheap exact-arithmetic
chi_2 primitive + a dim>1/2 certificate, then honestly flag any candidate for theory certification.

**Verdict: HONEST INFORMATIVE NEGATIVE.** Scanned 1377 SL(2,Z) finite-alphabet semigroups across
catalogs (b) + the open Apollonian cases (c); **no new reciprocity obstruction.** The oracle PASSED
(reproduced the published Rickards–Stange obstruction exactly, cross-checked against the authors' own
PARI/GP code). Every flagged orbit either reduces exactly to a published family or is falsified by
adversarial verification. The negative is *structurally explained* by Prop 2.2 of arXiv:2401.01860 —
the symbol-preserving semigroup Psi is EXACTLY characterized, so no new mechanism can hide in this class.

---

## Step 0 — Ground (cited)

**chi_2, SL(2,Z) semigroup version (Rickards–Stange, arXiv:2401.01860, Duke 174(15):3197–3244, 2025).**
The chi_2 invariant is the Kronecker symbol `(x|y)` on the orbit vector `[x,y]`. It is CONSTANT on
orbits of the maximal symbol-preserving semigroup
`Psi = { [[a,b],[c,d]] in Gamma_1(4)^{>=0} : a == 1 }` (Def 2.1, Prop 2.2: equivalently
`(ax+by | cx+dy) == (x|y)` for all coprime `x,y`, `y` odd). The transformation law is Prop 3.2
(transcribed verbatim from the authors' `paper.gp` `kronaction`, lines 70–87). A **reciprocity
obstruction** (Def 2.4 / Thm 2.5): an orbit whose numerators (or denominators) (1) are congruence-
admissible to be squares mod every n, yet (2) contain NO square. Forced when `(x|y) = -1` on a start
whose orbit congruences still admit squares.

**chi_2, Apollonian-curvature version (Haag–Kertzer–Rickards–Stange, arXiv:2307.02749, Annals 200(2),
2024).** Def 4.3: for a curvature `n` with quadratic-form residue `rho`,
`chi_2 = (rho|n)` if `n≡0,1 (4)`; `(-rho|n/2)` if `n≡2 (4)`; `(2rho|n)` if `n≡3 (4)`.
`chi_2` is constant on a packing; `chi_2 = -1` forces a missing square-class family (Prop 4.10).
A quartic `chi_4 : circles -> {1,i,-1,-i}` with `chi_4^2 = chi_2` exists for types (6,1)/(6,17) via
Z[i] quartic reciprocity (Sec 5.2). Revised **Conjecture 1.5**: the set of missing curvatures NOT in a
quadratic/quartic obstruction class is finite. **Two OPEN cases** (quadratic/quartic framework
inconclusive): type (6,1,1,1) **strip packing**, root `(0,0,1,1)`; type (8,11,1) **bug-eye packing**,
root `(-1,2,2,3)`. The authors explicitly do NOT claim completeness and expect more obstructions
(sextic/octic untested). Taxonomy of superintegral crystallographic packings is FINITE, all in
dim ≤ 20 (Kontorovich–Nakamura Finiteness Thm; arXiv:1903.03563 Thm 6).

---

## Step 1 — ORACLE: PASS (must pass before trusting any scan)

`code/reciprocity_oracle.py` (+ `code/reciprocity_oracle_test.py`): exact Kronecker symbol on Python
ints; the Prop 3.2 `kron_action` formula; orbit BFS; Apollonian curvature BFS + Def 4.3 chi_2.

All 18 self-tests PASS:
- **T1** exact Kronecker symbol == `sympy.jacobi_symbol` on 20000 random `(a, odd n)`; + known even/neg-n values.
- **T2-prop32** the Prop 3.2 `kron_action` identity holds on 5 matrices (validates our transcription).
- **T2a/b/c** Psi_1, Psi_2 generators preserve the symbol (Def 2.1); negative control `[[1,0],[1,1]]`
  correctly does NOT (witness `(x,y)=(2,1)`: `(2|1)=1 != (1|1)`... symbol flips).
- **T3 (the reproduction)** `Psi_1*(2,3)`: 19695 distinct numerators ≤ 20000, **zero squares**,
  squares locally admissible mod {8,16,9,5,7,11,24} (⇒ reciprocity, not congruence). `Psi_2*(3,8)`:
  2662 distinct denominators, **zero squares**, all ≡ 0 mod 4. Positive control `Psi_1*(7,3)`,
  `(7|3)=+1`, DOES contain a square.
- **T4** standard gasket `(-1,2,2,3)`: 66606 curvatures ≤ 2e5, exactly 8 residue classes mod 24
  `{2,3,6,11,14,15,18,23}`; chi_2 (Def 4.3) well-defined in {-1,0,1}.

**Independent cross-check against the authors' own code** (built `JamesRickards-Canada/Semigroup-
Reciprocity` against PARI/GP 2.17.3):
- `psi_isreciprocity([2,3], numerator) = 1` (reciprocity obstruction predicted) — matches T3.
- `psi_missingsquares([2,3], 200, numerator) = 1` (all squares missing up to 200^2) — matches T3.
- `test_kronaction_many(...)` → "All tests passed" — their Prop 3.2 formula clean; our transcription matches.

> Oracle quote (self-test final line): **"ORACLE: ALL TESTS PASSED"**.

---

## Step 2 — SCAN (parallel, M1 shard0 + M2 shard1; exact arithmetic)

`code/reciprocity_scan.py` enumerated **1377** SL(2,Z) finite-alphabet semigroups, 0 errors:
- (b1) **CF** semigroups (Thm 2.18 form `[[0,1],[1,a]]`), alphabets ⊆ {1..12}, 1–3 letters: 298.
- (b2) **L/R** unipotent semigroups `<L_b, R_c>`: 38.
- (b3) **GEN/MIX** general non-unipotent Psi-core matrices `[[1,b],[4k,1+bk·c]]` in Gamma_1(4)^{>=0},
  pairs/triples + mixes with anchors (the genuine discovery space): 1041.

Per-semigroup test: for each `chi_2 = -1` start, require (P1) chi_2 constant on the orbit,
(P2) no square present + squares congruence-admissible, (P3) dim estimate > 1/2.

**Catalog (a) — superintegral taxonomy.** Not separately swept as matrix orbits: by Margulis/Kontorovich-
Nakamura the superintegral catalog is FINITE (dim ≤ 20) and the disproof line already targets it; the
*reachable-from-our-engine* primitive is the SL(2,Z) form (b). Flagged for the higher-dim handoff below.

**Catalog (b) result.** 128 orbits flagged by the loose inline classifier. Rigorous reclassification
(`code/reciprocity_reclassify.py`, exact generator-wise Psi-membership):
- **120 → PUBLISHED**: every generator lies in Psi (the Gamma_1(4) core: `L_b` ∈ Psi for any b;
  `R_c` ∈ Psi iff c ≡ 0 mod 4; CF alphabets ⊆ 4Z+). These are real chi_2 obstructions but are the
  SAME published Rickards–Stange mechanism on larger sub-semigroups — NOT new.
- **8 → "non-published alphabet"** (CF[3,7,11], CF[4,7,8], CF[4,7,12], CF[4,8,9], CF[4,8,11],
  CF[4,9,12], CF[4,7,11], CF[4,11,12]) — the only candidates not obviously published.

**Adversarial verification of the 8 → ALL FALSE POSITIVES.** Pushed each to B = 2,000,000 (deep orbit):
the chi_2 invariant is **NOT constant** — `chi_set(coprime) = {-1, +1}` for every one (P1 FALSE), and
CF[3,7,11] additionally has a square denominator at 2M. The scan's "constant chi_2 = -1" was an artifact
of the truncated small orbit (these GL(2,Z) CF semigroups are THIN, dim ≈ 0.26–0.36 < 1/2, and grow so
slowly that the symbol only flips after deep iteration). So they fail BOTH P1 (symbol not preserved)
and P3 (dim < 1/2). No obstruction.

**Catalog (c) — the two OPEN Apollonian packings (higher-power angle).** Exact integer-curvature scan
to B = 4e5:
- **strip `(0,0,1,1)`**: residues `{0,1,4,9,12,16} mod 24`; **all perfect squares 1,4,9,…,225 PRESENT**;
  all `c·n^2` families present. No square-class absence ⇒ no obstruction at the integer level.
- **bug-eye `(-1,2,2,3)`**: residues `{2,3,6,11,14,15,18,23} mod 24`; `n^2` family empty, BUT this is a
  pure **congruence** obstruction (square residues `{0,1,4,9,12,16}` are disjoint from the packing's
  residues — squares are 0/1 mod 4, this packing is 2/3 mod 4), NOT reciprocity. `2n^2/3n^2/6n^2`
  present. No mod-24-admissible-but-empty square class found.

The integer-curvature scan cannot expose a higher-power (octic / Z[ζ_8]) obstruction — that lives in a
residue ring beyond Z and is exactly the un-attempted theory direction the paper flags. Recorded as a
handoff, not a finding.

---

## Step 3 — HONEST report

**Oracle:** PASS (quoted above; triple-validated: self-tests + sympy + authors' PARI/GP code).

**Flagged candidates that survive verification: NONE.** Every flagged orbit across catalogs (b)(c)
either (i) reduces exactly to a published Rickards–Stange family (120 cases, all generators in Psi),
or (ii) is a false positive killed by adversarial verification at large bound (8 CF cases — chi_2 not
actually constant, dim < 1/2). The open Apollonian cases show no integer-level reciprocity obstruction.

**Why the negative is principled (not just "didn't look hard enough").** Prop 2.2 (arXiv:2401.01860)
characterizes the symbol-preserving SL(2,Z)^{>=0} semigroup EXACTLY as `Psi = {a=1} ∩ Gamma_1(4)^{>=0}`.
Hence ANY finite-alphabet SL(2,Z)^{>=0} semigroup that preserves chi_2 is a sub-semigroup of Psi — the
published mechanism. A genuinely new SL(2,Z) obstruction would have to either (a) live in a generator
class that preserves chi_2 collectively but NOT generator-wise (none found; the 8 candidates that
looked like this were artifacts), or (b) use a HIGHER-POWER symbol (quartic/octic) beyond the quadratic
chi_2. The cheap quadratic catalogs (b)(c) are, as the task anticipated, effectively already covered.

**Precise next steps for a real discovery (theory-gated, beyond the cheap scan):**
1. **Higher-power obstruction on the two open Apollonian packings** (strip `(0,0,1,1)`, bug-eye
   `(-1,2,2,3)`). The quadratic chi_2 is inconclusive there by construction. Build the chi_4 (Z[i]
   quartic-residue, `chi_4^2 = chi_2`, paper Sec 5.2) and an octic/Z[ζ_8] analogue on the curvature
   form, and test square-class absence in the residue ring (NOT in Z). This is the authors' own
   stated open direction and the highest-ceiling lead.
2. **Superintegral taxonomy catalog (a) in dim 3–20** (Kontorovich–Nakamura finite list; arXiv:1903.03563,
   extended arXiv:2510.21702 already did octahedral/cubic/square/triangular). A new packing TYPE not yet
   checked, with an explicit tangent-circle parametrization + quadratic-reciprocity argument per the
   2510.21702 method, is the systematic-catalog gap. Reachable only with the higher-dim reflection-group
   machinery (Vinberg/Gram), not our transfer-operator engine.
3. **Collective (non-generator-wise) symbol preservation** in SL(2,Z) GL-mixed semigroups: search for a
   semigroup whose ORBIT preserves a Kronecker/quartic symbol without every generator doing so — would
   be a genuinely new phenomenon. Needs a deeper orbit walk (our scan's small node cap is the limiting
   factor; the artifact at B=2e4 vs flip at B=2e6 shows the bound must be ≥ 1e6 with a dim>1/2 filter
   applied FIRST to avoid thin-orbit false positives).

**Files:** `code/reciprocity_oracle.py`, `code/reciprocity_oracle_test.py`, `code/reciprocity_scan.py`,
`code/reciprocity_reclassify.py`. Raw scan output: `/tmp/out_shard0.jsonl`, `/tmp/out_shard1.jsonl`
(M1/M2). Authors' code built at `/tmp/Semigroup-Reciprocity` (PARI/GP 2.17.3).
