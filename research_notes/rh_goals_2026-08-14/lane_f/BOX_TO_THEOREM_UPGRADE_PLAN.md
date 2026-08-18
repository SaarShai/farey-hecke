# BOX → THEOREM upgrade plan for the finite base q ∈ {5,7,8,9,10,11,12}

Lane F, 2026-08-18. Planning document only. No new theorem is declared here.

## Executive ruling

The finite base is not presently at one uniform evidence grade.

- **q=5** already has a declared computer-assisted existence theorem after five
  adversarial rounds plus the Kimi K3 hostile audit. Its full R3b certificate
  uses closed-subarc Taylor enclosures and a proved Fredholm-determinant
  comparison, not merely point samples.
- **q=7** has the same full R3b/Fredholm chain and a complete theorem assembly,
  but only one adversarial round. It remains **ASSEMBLED, NOT DECLARED**; its
  Selberg-zero/resonance conclusion is **CONJECTURAL** pending the open
  primary-source and review gates.
- **q=8,9,10,11,12** have strong, reproducible box evidence: at least two
  reported `winding = 1` runs per q, finite-matrix Arb/Acb evaluation, explicit
  boundary nonzero balls at the sampled points, and (for q=8–12) independent
  container reproduction. They do **not** yet have the analytic-contour and
  infinite-dimensional tail proof used at q=5 and q=7.

The decisive upgrade is therefore not prose assembly. It is to replace the
q=8–12 lightweight sampled-contour path by the q=5/q=7 theorem-valid path:

1. exact q-specific evaluator identification;
2. a proved, uniform Fredholm tail bound;
3. closed-subarc enclosures over every point of the contour;
4. Hilbert-to-MMS determinant identification on an enlarged domain;
5. factorization, divisor, pole and strip gates;
6. five adversarial rounds per newly assembled theorem.

Until those gates pass, every claimed Selberg-zeta zero or resonance for
q=8–12 is **CONJECTURAL**, even though the box evidence is compelling.

## Status vocabulary

- **CERTIFIED** — follows from a replayable ball receipt plus the stated
  analytic lemma, with the receipt inputs and source bytes bound.
- **PROVED/CITED** — a paper or formal result is applicable with its hypotheses
  checked.
- **SUPPORTED** — strong finite numerical evidence, but one or more theorem
  hypotheses are not certified.
- **GAP** — required implication is missing.
- **CONJECTURAL** — the conclusion is plausible but not proved by the current
  artifacts.

## 1. What the two certificate families actually establish

### 1.1 Full R3b family: q=5 and q=7

The q=5 and q=7 certificates cover every closed contour subarc by an Acb Taylor
enclosure, prove the finite determinant and its `F_R`-inflated enclosure exclude
zero on every subarc, and use a proved trace-norm/Fredholm comparison to preserve
winding under the homotopy from `det(I-LP_N)` to `det(I-L)`. See
`lane_g/R3B_FLAGSHIP_CERT.md:29-40,52-83` and
`lane_f/F7_R3B_ASSEMBLY_CERT.md:145-170,186-244`.

Subject to the evaluator-identification links in the theorem assemblies, these
receipts prove:

- the Fredholm determinant is nonzero on the entire closed box boundary;
- its boundary winding is exactly one;
- it has exactly one zero in the box, counted with multiplicity;
- because the function is holomorphic on the box neighborhood, that one
  `L_{s,+}` zero is unique and simple.

The lower-N arms are falsification controls, not second positive certificates:
q=5 passes at N=160 and fails at N=128; q=7 passes at N=256 and fails at N=224.
A second passing N is not logically required once the uniform Fredholm comparison
is proved.

### 1.2 Lightweight sampled family: q=8–12

The q=8–12 driver evaluates `cert_det` at finitely many boundary points, inflates
each returned finite determinant by `4*tail`, and sums argument differences of
successive endpoint balls when `Re(B*conj(A))>0`; see
`lane_f/f9f12_certify_r3b_flagship.py:92-163,210-288` and its q=8 source
`lane_f/f8_certify_r3b_flagship.py:83-150,196-277`.

What is rigorous in those artifacts, conditional on the implemented evaluator
being the intended MMS operator, is narrower than the reports' wording:

- Arb/Acb outward-rounded evaluation of each **finite matrix** determinant at
  each sampled binary64 contour point;
- rigorous balls for the observed finite-section increments used by the
  dimension-tail estimator;
- rigorous arithmetic for the reported endpoint argument polygons;
- exact reproduction of the recorded q=9–12 gating fields on Kaggle, using the
  same embedded source bytes.

Two theorem-level breaks remain.

1. **The dimension tail is not proved.** `cert_det` calls
   `dim_tail_from_matrix`, which observes four recent finite-section determinant
   increments, checks that three observed ratios are below `q_cap=0.85`, then
   extrapolates `g_last*q/(1-q)` to all future dimensions
   (`zeta_cert_rosen_q5.py:419-452`; odd/even dispatch at
   `zeta_cert_rosen.py:243-250` and `zeta_cert_rosen_even.py:326-337`). No
   theorem in the current q=8–12 artifacts proves that the unobserved future
   ratios remain below that `q`. Arb rigor encloses the observed values; it does
   not prove the geometric continuation. The even engine itself calls the
   identical signed version a “heuristic” and “NOT a proven uniform tail bound”
   at `zeta_cert_rosen_even.py:278-285`.
2. **The segment interiors are not enclosed.** `certify_segment` evaluates only
   its two endpoints and bisects only when their endpoint values fail the
   half-turn test. It supplies no interval evaluation or derivative/Taylor bound
   for `det(I-L_s)` at the intervening `s` values. Thus the receipts do not rule
   out an unsampled zero or extra argument turn along a segment. In contrast,
   the q=5/q=7 full R3b path proves a closed-subarc Taylor enclosure and checks
   that the entire inflated tube excludes zero.

There is also an exact-geometry issue: the intended decimal center and
half-width are converted to Python floats before the contour is built
(`f9f12_certify_r3b_flagship.py:170-173`). The receipts therefore bind a nearby
binary64 rectangle, not literally the decimal rectangle printed in `s_box`.
This is harmless numerically but must be repaired before the exact box appears
in a theorem statement.

**Acceptance decision:** the q=8–12 `certified_integer = 1` fields are retained
as **SUPPORTED sampled finite-section polygon winding evidence**. They are not
accepted as referee-grade analytic Fredholm winding certificates until the two
breaks above are closed. Cross-N and Kaggle agreement test stability and
reproducibility; neither supplies the missing theorem.

## 2. Per-q inventory

All boxes use sign `+1` (MMS `+` sector) and coordinate half-width `10^-6`.
Winding radii and determinant/tail bounds below are receipt values; they do not
upgrade the q=8–12 evidence beyond §1.2.

| q | Box center | Engine sector | Current N evidence | Arb/Acb and current conclusion | Theorem status |
|---:|---|---|---|---|---|
| 5 | `0.4538951800749447 + 5.7635372417301305 i` | odd, eq. (34), κ=3 | N=160: full R3b winding 1, margin ≥ `3.4378649e-8`; N=128: designed failure | 384-bit, 284 closed subarcs, theorem-valid `F_R` homotopy to the Fredholm determinant | **DECLARED existence theorem**; simple `L_+` zero proved |
| 7 | `0.4751647621098225 + 4.668743786424289 i` | odd, eq. (34), κ=5 | N=256: full R3b winding 1, margin ≥ `2.4128527e-6`; N=224: designed failure | 384-bit, 192 closed arcs, all seams and wrap reverified, theorem-valid `F_R` homotopy | **ASSEMBLED, NOT DECLARED**; Selberg zero/resonance **CONJECTURAL** pending source and review gates |
| 8 | `0.4252310423737965 + 4.345760788321986 i` | even, eq. (32), κ=3 | N=32: reported winding 1, radius ≈`2.05e-7`, no escalation; N=30: reported winding 1, radius ≈`7.52e-7`, but one contour point escalates to N=34; N=28 also reports 1 with one point escalated to N=32 | 300-bit finite sampled values; min sampled `|det|` ≈`3.001027e-6`; heuristic dimension tail; no segment-interior enclosure | Selberg zero/resonance **CONJECTURAL** |
| 9 | `0.3742488091325338 + 4.080139082773367 i` | odd, eq. (34), κ=7 | N=32 and N=28 both report winding 1; radii ≤`3.353e-14` and `2.692e-11`; no N escalation | 300-bit finite sampled values; min sampled `|det|` ≥`3.378614e-6`; Kaggle matches 8/8 gating keys | Selberg zero/resonance **CONJECTURAL** |
| 10 | `0.333692861999034 + 3.853631836813213 i` | even, eq. (32), κ=4 | N=36 and N=32 both report winding 1; radii ≤`5.760e-9` and `6.239e-8`; no N escalation | 300-bit finite sampled values; min sampled `|det|` ≥`3.399660e-6`; Kaggle matches 8/8 gating keys | Selberg zero/resonance **CONJECTURAL** |
| 11 | `0.3055125027342933 + 3.6592963976938098 i` | odd, eq. (34), κ=9 | N=32 and N=28 both report winding 1; radii ≤`2.487e-14` and `1.948e-11`; no N escalation | 300-bit finite sampled values; min sampled `|det|` ≥`3.782894e-6`; Kaggle matches 8/8 gating keys | Selberg zero/resonance **CONJECTURAL** |
| 12 | `0.28732580259283225 + 3.4924075186049106 i` | even, eq. (32), κ=5 | N=36 and N=32 both report winding 1; radii ≤`2.607e-9` and `3.695e-8`; no N escalation | 300-bit finite sampled values; min sampled `|det|` ≥`3.775289e-6`; Kaggle matches 8/8 gating keys | Selberg zero/resonance **CONJECTURAL** |

Sources for q=8 are `F8_CERT_PLAN.md:439-475,500-572` and the three
`f8_receipts/F8_R3B_RECEIPT_N*.json` files. Sources for q=9–12 are
`F9_F12_BASE_EXTENSION.md:91-179,185-229,252-276` and every local/container
receipt under `f9_receipts` through `f12_receipts`.

### q=5 — reference theorem, not a new upgrade target

Already closed for the existence statement:

- full continuous-contour/Fredholm certificate;
- finite-section identity, trace-norm comparison and argument principle;
- E1 enlarged-domain Hilbert→Banach determinant equality;
- `det(1-K_s)` nonvanishing;
- MMS factorization, pole set and resonance interpretation;
- five adversarial rounds plus Kimi K3.

Remaining if the new family statement demands more than the declared q=5
theorem:

- **Simple Selberg zero/resonance is CONJECTURAL.** Winding one proves the
  `L_{s,+}` zero is simple. The assembly only proves the Selberg-zero
  multiplicity is *at least* that of the `+` factor; it does not exclude a
  simultaneous zero of `det(1-L_{s,-})` in the box. A box-wide `-`-sector
  nonvanishing certificate is needed to state that the Selberg zero itself is
  unique and simple.
- The q=5 K_s artifact records a center-to-lattice distance rather than a box
  distance. The current proof has ample geometric margin and remains sound, but
  a regenerated box-distance receipt would make the seven-q presentation
  uniform.
- Any rerun must repair latent code notes 1-C3/1-C4 and derive all gates from
  raw fields rather than hard-coded summary booleans (`R3B_FLAGSHIP_CERT.md:
  86-108`).

### q=7 — theorem chain complete; review depth incomplete

Assembled at the proof-chain level by G7, but not yet declaration-grade:

- all numerical Fredholm-contour links;
- q-independent finite-rank and determinant-comparison joints;
- q=7 E1 enlarged-disc contraction and Hilbert→MMS transport;
- q=7 K_s box margin and certified nonvanishing product bound;
- factorization, pole-set and resonance interpretation are provisionally linked
  from citations, with the primary MMS text still to be banked and checked;
- G7 V1 independently replayed the receipt chain and found no theorem-level
  defect after repairs.

Remaining:

- keep the q=7 Selberg-zero/resonance conclusion **CONJECTURAL** until the
  primary-source check and all five adversarial rounds pass;
- run adversarial rounds 2–5; do not relabel `DECLARED` after V1 alone;
- bank and verify the MMS primary text for the eq. (34) heading and journal
  theorem numbering (`THEOREM_G7_OFFLINE_ASSEMBLY.md:518-524`);
- restore or vendor the exact certified engine bytes before a rerun; the primary
  engine path drifted after the certification (`F7_R3B_ASSEMBLY_CERT.md:69-83`);
- add the 1-C3/1-C4 assertions before any rerun and keep the 1-C5 raw-field
  re-derivation;
- optional but desirable: formalize the q=7 K_s lattice (current link-table row
  9 is a minor GAP);
- **Simple Selberg zero/resonance remains CONJECTURAL** until the `-` sector is
  certified nonzero on the box.

### q=8 — first full even-q pilot

Assets already present:

- an even eq. (32) block manifest and TB-V2 contraction certificate with
  hardened geometry and `rho* < 1`;
- three sampled box runs and a completed Kaggle canary;
- the smallest matrix dimension in the unfinished set (κ=3).

New work:

1. Resolve the evaluator validation caveat before expensive certification:
   `F8_CERT_PLAN.md:130-162` records a maximum entry discrepancy
   `6.18e-5`, about 60 times the engine header's stated FFT scale. Produce an
   independent high-precision branch-by-branch evaluator, not another wrapper
   around the same builder.
2. Replace float-built box endpoints by exact decimal/rational Arb endpoints.
3. Port the full q=7 R2/R3b continuous-subarc and theorem-valid tail pipeline to
   eq. (32); produce primary and predeclared comparison/control arms.
4. Produce q=8 E1 enlarged-disc data (`rho_hat<1`, positive pole/cut clearance)
   for the Hilbert→MMS identification. TB `rho*<1` is not E1.
5. Recompute a true closed-box K_s margin and nonvanishing product bound.
6. Certify `det(1-L_{s,-}) != 0` on the box if simplicity/uniqueness is in the
   theorem statement.
7. Assemble the theorem and pass adversarial rounds 1–5.

### q=9 — first general odd-q extension beyond the validated q=5/q=7 pair

The odd engine's own header says its generalized block placement was checked
against the independent double-precision builder at q=5 and q=7, not q=9 or
q=11 (`zeta_cert_rosen.py:21-38`). Therefore the q=9 evaluator-to-MMS match is
**CONJECTURAL** for theorem purposes despite the stable two-N receipt.

New work: exact odd-q block/partition manifest; independent evaluator
comparison at q=9; TB/R2/full-R3b/E1 receipts for κ=7; exact box and strip
residency; K_s box/product certificate; optional minus-sector exclusion;
theorem assembly; five adversarial rounds.

### q=10 — second even-q target

The even engine explicitly says “no q != 8 claims” in its validation scope
(`zeta_cert_rosen_even.py:46-61`). Thus the q=10 eq. (32) evaluator identity is
**CONJECTURAL** until independently checked.

New work: q=10 exact block/partition manifest and independent evaluator;
TB/R2/full-R3b/E1 for κ=4; exact box/domain and K_s gates; optional minus-sector
exclusion; theorem assembly; five adversarial rounds.

### q=11 — largest operator, schedule last

Same odd-evaluator GAP as q=9, but κ=9 makes every matrix and block-envelope run
the most expensive in this base. The current N=28/32 sampled receipts are useful
budget priors only.

New work: q=11 evaluator, TB/R2/full-R3b/E1, exact box/domain, K_s, optional
minus-sector, theorem assembly and five rounds. Do not start long contour jobs
until the q=9 odd pipeline has passed its evaluator and E1 gates.

### q=12 — later even-q scale test

The exact radical `lambda_12=sqrt(2+sqrt(3))` is implemented, but exact lambda
does not certify the eq. (32) evaluator or its functional-analytic domain. The
q=12 two-N/Kaggle agreement remains **SUPPORTED**, not a theorem.

New work: q=12 evaluator equivalence, TB/R2/full-R3b/E1 for κ=5, exact
box/domain and K_s gates, optional minus-sector exclusion, theorem assembly and
five adversarial rounds.

## 3. Referee-grade theorem contract

Each q-specific theorem must name the exact closed box `B_q` and discharge all
of the following. A conditional statement with any unchecked item is not the
target deliverable.

### H0. Exact statement and non-overclaim

State one of two conclusions and do not mix them:

- **Existence theorem:** `Z_{S,q}` has a zero in `int(B_q)`; hence, after the
  strip gate, there is an off-line resonance. This does not claim the Selberg
  zero is simple.
- **Unique-simple theorem:** `Z_{S,q}` has exactly one simple zero in `B_q`.
  This stronger statement additionally requires the `-`-sector nonvanishing
  gate H8.

Any priority, “first”, completeness, nearest-resonance, or strip-exhaustion
claim is outside the local box theorem and remains **CONJECTURAL** unless
separately audited.

### H1. Exact box and in-domain residency

- Construct all endpoints from exact decimal strings or rationals in Arb; no
  binary64 conversion in the proof path.
- Certify `B_q` is contained in the common holomorphy domain `Omega_q*` of the
  Hilbert and MMS Banach operator families.
- Certify `B_q subset {0<Re(s)<1/2}` and `0 notin Im(B_q)`. These elementary
  inequalities give the off-critical-line gap and exclude the real-axis
  determinant pole set.
- Prove boundary nonvanishing on the literal stated box, so the counted zero is
  in the interior.

### H2. Evaluator correctness

The receipt must bind a q-specific mathematical specification to the executable:

- odd q uses the correct MMS eq. (34) partition, branch families, signs and κ;
  even q uses eq. (32);
- every matrix entry equals the normalized-H2-basis coefficient of the stated
  `P_N L_{s,+} P_N` operator;
- exact Hurwitz-tail closure, branch choices and power/log conventions are
  valid on the certified discs and throughout `B_q`;
- an independent implementation or symbolic branch manifest agrees
  entry-by-entry at multiple exact test balls, including a salted negative
  control that must fail;
- code, manifest, engine, inputs, precision, python-flint version and receipt
  schema are hash-bound.

“The generic engine returned κ” and “Kaggle reproduced the same bytes” are
useful provenance checks but do not prove evaluator correctness.

### H3. Analyticity and the pole/zero dichotomy

- Cite and instantiate the theorem giving meromorphic/nuclear continuation of
  the MMS determinants.
- Prove the closed box and an open neighborhood avoid every allowed operator
  pole. Since all present boxes have nonzero imaginary part, the cited real pole
  set should make this a short exact interval proof once the citation is fixed.
- Explicitly state that argument principle gives `zeros - poles = winding`.
  Only after the pole count is certified zero may winding one be read as one
  zero.

The primary reference to bank is Mayer–Mühlenbruch–Strömberg,
“The transfer operator for the Hecke triangle groups,” arXiv:0912.2236v2 / DCDS
32 (2012), 2453–2484. It gives the nuclear/meromorphic operator framework and
the quotient
`Z_S=det(1-L_{s,+})det(1-L_{s,-})/det(1-K_s)`; the exact
journal/e-print numbering and parity headings must be quoted from the source,
not from a derived note.

### H4. Theorem-valid infinite-dimensional comparison

- Replace `dim_tail_from_matrix` extrapolation by the R2/R3b bound
  `|det(I-L)-det(I-LP_N)| <= T_tail(N) exp(1+||L||_1+||LP_N||_1)`.
- Certify q-specific branch contraction, full-column norms, output-tail
  corrections and `T_tail(N)` uniformly where required.
- Keep `rho*`, E1 `rho_hat`, arc self-consistency `rH`, and determinant error
  `F_R` distinct.
- Predeclare a primary N and a lower comparison/control N. A comparison may be
  a second pass or a designed failure, but its role must be fixed before the
  run. Two passes through the same heuristic tail are not independent proof.

### H5. Continuous closed-contour certificate

- Cover all four sides by closed Arb parameter arcs whose union is exactly the
  literal box boundary.
- On every accepted subarc, certify a Taylor/derivative enclosure for the finite
  determinant and prove both the finite and `F_R`-inflated tubes exclude zero.
- Recheck all junctions and the wrap; record coverage, overlaps, subdivisions,
  minima and failures from raw fields.
- Derive the integer winding from the closed nonzero tubes, then transport it by
  a nonvanishing straight-line homotopy to the Fredholm determinant.

### H6. Uniqueness and simplicity of the `+`-sector zero

With H3–H5, winding one and zero poles imply exactly one zero counted with
multiplicity. Therefore the `L_{s,+}` zero is unique and simple. This deduction
must be explicit; “one visible pin” is not a simplicity proof.

### H7. Hilbert → MMS Banach determinant identity

Reuse the q-independent R5 paper proof only after q-specific E1 is supplied:

- enlarged discs with every branch holomorphic;
- positive pole/branch-cut clearance after enlargement;
- all block families map enlarged sources strictly into targets with
  `rho_hat<1`;
- q-specific block coverage and source hashes;
- determinant equality on a connected `Omega_q*` containing the box.

The G7 template establishes the proof architecture; q=8–12 still owe their own
E1 data.

### H8. Selberg factorization, divisor and opposite sector

- Prove `det(1-K_s)` is finite and nonzero on the closed box. Prefer one generic
  lemma: certify `0<b_q<1`, derive the lattice
  `s=-n+i*pi*k/a_q`, and use `inf Re(B_q)>0`; then emit per-q quantitative
  product bounds with the corrected G7 upper-bound formula
  `prod(1+t_n)`, never `1+tail`.
- Prove `det(1-L_{s,-})` is analytic on a neighborhood of the box. This is
  enough for the **existence theorem**, because it cannot cancel the `+` zero
  by a pole.
- For the **unique-simple Selberg theorem**, also certify
  `det(1-L_{s,-}) != 0` throughout the box. Without this, Selberg simplicity
  and uniqueness are **CONJECTURAL** even though the `+` zero is simple.

### H9. Resonance interpretation

Once the exact box lies in `0<Re(s)<1/2` and off the real axis, cite the standard
finite-area Selberg/scattering result that such a Selberg zero is a resonance
rather than a real small-eigenvalue parameter or a critical-line tempered zero.
No geometric parity label follows from MMS `P`-sector sign; retain the G5/G7
sector-honesty language.

## 4. What the G7 template closes, and what it does not

### Reusable without new mathematical invention

- Link 2 finite-rank restriction/Sylvester identity and its Lean proof.
- Link 3 Gohberg–Krein/Simon comparison inequality and q-independent Lean
  joints; only the constants are q-specific.
- Link 4 argument-principle logic after analytic boundary data exist.
- R5's q-independent smoothing, Jordan-chain, canonical-determinant and
  identity-theorem framework.
- The K_s proof pattern and the corrected upper-product bound from G7 V1.
- MMS quotient/factorization structure and standard resonance interpretation,
  once exact source applicability is checked.
- Review defenses already learned: no stale R1 Steps 3–4; box rather than point
  K_s distance; distinguish budget from achieved subdivision; rederive gates
  from raw fields; do not conflate `rho*`, `rho_hat` and `rH`; disclose latent
  paths; remove unaudited priority claims.

### New work at every unfinished q

- q-specific evaluator equivalence, especially q=9/11 and q=10/12, which lie
  outside the engines' stated validation sets;
- exact-decimal box construction;
- TB/R2 endpoint and full continuous R3b receipts;
- q-specific E1 enlarged-domain certification;
- q-specific K_s receipt or one genuinely parametric theorem plus instantiation;
- `-`-sector exclusion if simple Selberg zeros are claimed;
- five adversarial rounds and repair/re-review receipts.

### G7 itself is not yet the review-depth template's endpoint

G7 V1 closed the false `det(1-K_s)` upper bound, link-number collision,
mis-attributed erratum, unaudited priority claim, and missing MMS-heading
disclosure. It did not open the primary Simon/Grothendieck/MMS sources, run a
Lean build, rerun the 107.8-hour contour job, or independently implement E1
(`ADVERSARIAL_REVIEW_G7_V1.md:309-352`). Those tasks belong in G7 rounds 2–5
and in the corresponding rounds for q=8–12.

## 5. Five-round adversarial protocol

Each assembled q theorem must pass all five rounds. Repairs made after a round
receive a targeted cold re-review; an edited file is not covered merely because
an earlier version passed.

1. **R1 — receipt and arithmetic attack.** Recompute every printed constant,
   rounding direction, exact box bound, K_s product/distance, raw-field minimum,
   coverage count, hash and cross-N outcome. Use an independent arithmetic
   route where possible.
2. **R2 — evaluator attack.** Derive the q-specific eq. (32)/(34) block manifest
   from the primary source; compare to code entry-by-entry; audit basis,
   projection, sign, κ, Hurwitz closure, branch cuts, exact coordinates and
   salted negative controls. Same-code Kaggle replay is not enough.
3. **R3 — analytic certificate attack.** Audit the uniform `T_tail`, endpoint
   norms, `F_R`, Taylor arc enclosure, seam closure, homotopy, E1 enlarged discs
   and Hilbert→Banach determinant identity. Recompute winding by an unrelated
   method from raw enclosures.
4. **R4 — statement and factorization attack.** Check zeros-minus-poles,
   analyticity, box residency, K_s noncancellation, opposite-sector status,
   simplicity wording, resonance interpretation, primary-source theorem
   numbering and every dependency label. Any unproved statement is marked
   **CONJECTURAL** or removed.
5. **R5 — cold end-to-end and provenance attack.** In a clean environment,
   replay all cheap generators and at least one full primary contour; verify
   banked bytes for expensive runs, build the Lean joints, inspect all repair
   diffs, and issue the final `THEOREM-GRADE YES/NO` ruling.

An additional independent hostile audit, as q=5 received from Kimi K3, is
recommended before circulation of the seven-q family statement.

## 6. Prioritized execution order

### Priority 0 — shared proof infrastructure; no new theorem labels

1. Freeze the theorem contract H0–H9 and exact box schema.
2. Replace the sampled `certify_segment` and heuristic
   `dim_tail_from_matrix` path with one parity-parameterized full R2/R3b path.
3. Build independent odd/even evaluator specifications directly from the MMS
   source, with exact branch manifests and negative controls.
4. Generalize the G7 E1 and K_s generators without weakening raw-field or hash
   gates.
5. Add a `-`-sector box-exclusion mode, but keep it outside the minimal
   existence theorem if it becomes the cost bottleneck.

**Exit gate:** q=5 and q=7 reproduce with the new shared harness, or the harness
explains exactly why the banked theorem receipts remain the authority. No
q=8–12 long run begins before this gate.

### Priority 1 — q=7 declaration closure

Run G7 adversarial rounds 2–5, bank the MMS primary text, fix rerun provenance,
and declare only if every repair is cold-reviewed. This is the fastest new
declared theorem because its mathematical links are already assembled.

### Priority 2 — q=8 full theorem pilot

Resolve the even-evaluator discrepancy first. Then use q=8's existing TB
geometry and κ=3 cost advantage to validate the full even R2/R3b/E1/K_s chain.
Complete five rounds. This is the parity-pilot for q=10 and q=12.

### Priority 3 — q=9 full theorem pilot

Validate the odd evaluator beyond q=7, then run the full κ=7 chain and five
rounds. This is the general-odd pilot for q=11.

### Priority 4 — q=10 then q=12

After q=8 passes, reuse the reviewed even harness at κ=4 and κ=5. Run q=10
first because it is cheaper; run q=12 next. Do not collapse their q-specific
E1/evaluator/K_s receipts into “same parity, therefore same proof.”

### Priority 5 — q=11

Run last because κ=9 is the largest operator and the q=9 pilot should remove
odd-path design risk first. Precompute TB/R2 budgets before launching any
multi-day contour work.

### q=5 maintenance lane

Do not recertify q=5 merely for symmetry. Use it as the positive regression
oracle. Add `-`-sector exclusion only if the family theorem will explicitly
claim unique-simple Selberg resonances.

## 7. Per-q completion checklist

For each q, completion means all boxes below are checked and the receipt hashes
are copied into the assembly.

- [ ] Exact `B_q`, strip/gap and nonreal residency.
- [ ] Primary-source parity formula and exact q-specific branch manifest.
- [ ] Independent evaluator equivalence plus negative control.
- [ ] TB contraction and pole/cut clearance.
- [ ] Theorem-valid R2 endpoint norms and `T_tail`/`F_R`.
- [ ] Full closed-subarc R3b winding; all seams/wrap; raw minima rederived.
- [ ] Predeclared lower-N comparison/control arm.
- [ ] E1 `rho_hat<1` on enlarged discs; Hilbert→MMS determinant identity.
- [ ] K_s finite and nonzero on the literal closed box.
- [ ] MMS determinants analytic/pole-free on a neighborhood of the box.
- [ ] `+` zero uniqueness and simplicity deduced from the multiplicity count.
- [ ] `-` sector nonzero if and only if Selberg simplicity/uniqueness is claimed.
- [ ] Factorization and resonance interpretation with exact citations.
- [ ] Five adversarial rounds, all repairs re-reviewed.
- [ ] Final label is `DECLARED`; otherwise all stronger conclusions remain
      **CONJECTURAL**.

## 8. Immediate next actions

1. Write the exact odd/even evaluator specifications and audit the two engine
   validation scopes. This can falsify the project cheaply before any long run.
2. Port the q=7 closed-subarc/Taylor and endpoint-tail machinery to q=8 and
   reproduce one q=8 box with exact endpoints.
3. In parallel with q=8 numerical work, execute G7 review rounds 2–5.
4. Only after q=8 passes, freeze the even harness and schedule q=10/q=12.
5. Only after the q=9 evaluator passes, budget q=11.

No theorem statement for q=8–12 should be drafted as proved before actions 1–2
close. A draft may be prepared, but every zero/resonance/simplicity assertion in
it must remain visibly **CONJECTURAL**.
