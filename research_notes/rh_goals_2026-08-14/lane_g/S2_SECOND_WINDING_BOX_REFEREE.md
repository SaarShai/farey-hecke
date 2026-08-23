# COLD REFEREE — `S2_SECOND_WINDING_BOX_SOL.md`

- Date: 2026-08-23. Independent cold-referee seat. Read-only on the work
  product; this file is the only file written.
- Referee interpreter: `/Users/za/.venvs/farey-rh/bin/python` (python-flint /
  Arb, mpmath). All spot-checks single-core, `nice -19`, short; the d8 queue
  was not touched.
- I did not adopt the author's framing. Every number graded below was either
  re-derived by me or traced to a persisted artifact; anything I could not
  reproduce is marked as such.

## VERDICT: PROMOTABLE-WITH-CORRECTIONS

The three headline dispositions — **B7 root-caused and closed**, **B1 closed
for both candidates**, **the 0.4105437 fallback is the right second box** —
survive adversarial review, and I independently reproduced the two hardest
pieces of evidence (the §1.2 eight-way sector table and the §1.4 proof-by-fix
at M = 14 AND M = 22). The note is honest about what is open (B2, B3–B6,
UNREFEREED status) and its LEDGER-RULE grading discipline is real, not
decorative.

Seven corrections are required before any paper-level quotation. C1 is a
logic inversion in the load-bearing direction; C2 is a wrong number in a
paper-facing endpoint; C3 is a traceability failure against this program's
own standard.

---

## 1. Evidence table

| # | Criterion | Evidence I produced | Verdict |
|---|---|---|---|
| 1 | §1.2 sign-swap refutation: 8 `|det|` midpoints, N=22, n_head=4 | Ran `zeta_cert_rosen_q5.build_reduced_matrix_ball` + `_det_block(M,22,k,22)` UNMODIFIED at the four pins, both signs. Got `flagship +1 6.8215e-09 / -1 7.6113e-01`, `sonnet +1 3.5543e-01 / -1 8.3332e-01`, `fallback +1 2.2952e-08 / -1 3.1014e+00`, `sonnet_s2 +1 3.7532e-01 / -1 3.4684e+00`. All eight agree with §1.2 to every quoted digit | **PASS** |
| 2 | §1.4 root cause = factor-2 collocation coordinate error | Read `collocation_even_sonnet.py:119-167`. Physical node `z = c_i + radius_scale*r_i*u` with `radius_scale=0.5`, but `x_arg = (arg - c_j) / r_j` (FULL `r_j`). The mismatch is in the source, independent of any fix. The doc's derived operator `g ↦ weight(z)·g(c_j + (θ(z)-c_j)/2)` follows algebraically from `(w-c_j)/(0.5 r_j) = (θ-c_j)/r_j` | **PASS** |
| 3 | §1.4 proof-by-fix reproduces the flagship pin | Monkey-patched `single_branch_block`/`tail_closed_block` to receive `0.5*r_j` (my own fix, written without the author's script). Unfixed M=14: flagship `0.334`, sonnet `2.24e-6` (sonnet zero present). Fixed M=14: flagship `1.73e-5`, sonnet `0.355` (zero swaps sides). Newton, fixed, M=14 → `0.4538989810+5.7635394327i`; M=22 → `0.4538951801+5.7635372416i`, `|det|=1.01e-15`, distance to the flagship pin `8.9e-11`. Digit-for-digit identical to §1.4's four-row table | **PASS** |
| 4 | §1.3(a) line-by-line transcription of the q=5 reduced operator | Compared against the repo's VERBATIM LaTeX extraction `MMS_0912.2236_EXTRACTION.txt` (label `reduced3`, lines 1574–1585) and the negative-index definitions (lines 1587–1590). The three rows, the `±` on both negative-branch terms, and `L_{-i,s}g(z)=(z-iλ)^{-2s}g(1/(z-iλ))` match exactly. The engine's `build_reduced_matrix_ball:328-380` applies `prefac=sgn` to exactly the two negative-branch terms per row, so `sign=+1` is the `+` sector of `reduced3` | **PASS on content** (see C4 on the label) |
| 5 | §2 half-width arithmetic | Reproduced: `float((arb("0.4538951800749447")+arb(0,arb("1e-6"))).rad())` = `1.00000000458067e-06`; excess over `arb(10)**-6` = `4.580670065479353e-15`; midpoint carries no offset (center error 0.0) | **PASS on arithmetic** |
| 6 | §2 reconciliation LOGIC and object identity | See **C1**. The cited receipt itself stores `"half_width": "[1.00000000000000000000000e-6 +/- 1e-34]"` (`W_ENVELOPE_CERT_V2_RECEIPT.json:133-136`), and the contour is built by `closed_boundary_segments(PIN_RE, PIN_IM, arb(HALF_WIDTH), ...)`, where `arb("1e-6")` has radius `4.53e-23` — NOT the `1.00000000458067e-6` solid box | **FAIL** |
| 7 | §3 B1 fallback re-pin spread `1.03e-12` | Re-ran complex Newton on the certified builder's det midpoints (h=1e-9, `|dz|<1e-13`) from the stated seed at N=22/28/36: got `0.41054373549576567+7.819768247017059i` (1.9 s), then `0.4105437354947362+7.819768247015512i` at both N=28 (6.0 s) and N=36 (10.2 s). Decimal spread of the doc's four rows: re `1.02945e-12`, im `1.54720e-12` | **PASS** |
| 8 | §3 s_2 spreads `9.92e-11` / `1.19e-9` | Recomputed from the quoted rows: re `9.926451e-11`, im `1.18592602e-9`. Arithmetic self-consistent (I did not re-run the s_2 Newton — not selected, not load-bearing) | **PASS (arith)** |
| 9 | §4 ΔRe `0.0433514445` and `21675` box-widths | `0.4538951800749447 - 0.41054373549473627 = 0.04335144458020843`; truncated DOWN → `0.0433514445` ✓. `/2e-6 = 21675.72` → 21675 truncated DOWN ✓ (full-width convention, matching `SCAT1…SOL.md §8/C2`'s "box widths (2e-6)"). Spare `ΔRe - 2e-6 = 0.04334944458` → `0.0433494445` ✓ | **PASS** |
| 10 | §4 K_s clearances | Independent recompute against the exact lattice `s = -n + iπk/a_q`, `a_q = 5π/7.245792536496066 = 2.167873726556495`: fallback `0.7056870942707361`, flagship `0.45510024372206603`, s_2 `0.48194877778378137`. Matches `KS_GATE_REPORT.md` `g5_pin_2 = 0.705687094273`. Truncations DOWN are correct | **PASS on values**, see **C7** on the "certified" label |
| 11 | §4 B2 deep-tail `p = 2(σ-1e-6)` | fallback `2*(0.41054373549473627-1e-6) = 0.82108547098947254` → `0.8210854709` ✓; flagship `0.9077883601498894` → `0.9077883601` ✓; s_2 quoted `0.4860548468` is derived from the **N=22** value `0.24302842340131198`, not from the frozen `0.24302842350057649` (which gives `0.4860548470`) | **PASS (minor m3)** |
| 12 | §4 Lemma 3.1 reflected endpoint `Re ρ ≈ 0.5894543` | `1 - 0.41054373549473627 = 0.58945626450526373`. The doc's 7-digit figure is WRONG in the 6th decimal (`0.5894543` vs `0.5894563`). Cross-check on the same construction elsewhere: flagship `1-0.4538951800749447 = 0.5461048` ✓, and `SCAT1…SOL.md:384` uses `1 - 0.2430284 = 0.7570` for s_2 ✓, so the reflection map is `ρ = 1 - s` and the fallback figure is a transposition error | **FAIL** |
| 13 | §4 scan-level winding row (fallback): ball `[0.99999949, 1.00000051]`, `zero_certified: true`, K=28, hx=hy=0.012 | `grep -rn --include='*.json' --include='*.md' "1.00000051" .` → no hit anywhere in the repo. The s_2 counterpart `[0.99996722, 1.00003277]` IS traceable (`SCAT1…SOL.md:378`). The fallback's winding ball is quoted with no citation and no reachable artifact | **FAIL (part of C3)** |
| 14 | §1.3(b)(c) independent mpmath builder + 12-point cross-val grid | `find . -name mms_q5_indep.py -o -name crossval_grid.py -o -name repin_fallback.log` → nothing. Session-local scratchpad, not persisted. §7 lists them under "Receipts index". Unreproducible by any later referee | **FAIL (C3)** |
| 15 | §0.1 "12-point grid spanning … both pins' ordinates" | The grid ordinates are `5.76353724` and `10.56029678` = flagship and **s_2**. The SELECTED second pin (`|t| = 7.8198`) is absent from every cross-validation in §1.3 | **FAIL (C5)** |
| 16 | §5 "W V2 head-weight inflation 18.64 → 232.2 brackets p = 0.821" | Downstream Phase-1 measured `W^(≥1) = 44.66589` at the S2 box (`S2_PHASE1_WR2_RECEIPT.md §2`), inside the bracket. Projection was sound | **PASS** |
| 17 | §6 Phase 1 source directories | `code/tb_certify/` contains `certify_r2_flagship.py`, `r3b_endpoint.py` but NOT `certify_r3_flagship.py` / `certify_r3b_flagship.py`, which live in `code/tc_rerun/`. §6's instruction names the wrong directory for two of four files | **FAIL (C6.a)** |
| 18 | §6 Phase 1 "K_s receipts reused verbatim (no `s` dependence — prep §2)" | `SECOND_PIN_PREP.md:70-94` (§**3**, not §2) says the *lattice* is s-independent but "only the per-pin distance evaluation" is still required. §4 of this very note computes a NEW K_s distance for the new box, contradicting "no `s` dependence" | **FAIL (C6.b)** |
| 19 | §6 Phase 3 `N = 160`, 192 arcs, ~17 CPU-h, local-overnight option | Refuted by the downstream Phase-1 gate: `F_R(160) = 1.3958e12` vs a boundary det level of `4.2493e-6` — a ~18-order miss. The campaign actually dispatched **N = 288**, Kaggle-only, ~58 CPU-h (`S2_CONTOUR_CAMPAIGN_RECEIPT.md §C`, deviation 1). §6's central constant and its entire cost/route paragraph are now stale | **FAIL (C6.c)** |
| 20 | §0.4 "the fallback maximizes the probability that N=160 closes" | Falsified by the same gate | **FAIL (C6.c)** |
| 21 | Directed-rounding discipline across the note | Checked every truncation I could re-derive (items 9, 10, 11 above, plus `0.4819487` from `0.481948777…`). All are truncations in the conservative direction. No round-to-nearest passed off as directed | **PASS** |
| 22 | One-way implications not stated as equivalences | §0.5 "CLOSABLE, not yet closed", §4 "met by this pair **if** the second box certifies", §5 "must NOT be edited until … AND a cold referee passes". Correctly hedged, and `SCAT1…SOL.md §8/C3`'s one-way ruling is respected in substance | **PASS (minor m4)** |
| 23 | UNREFEREED items not cited as established | §0.1, §1.5, §5 all carry the caveat explicitly, including on the author's own B7 closure. Exemplary | **PASS** |

---

## 2. MAJORS

### C1 — §2's half-width "reconciliation" is aimed at the wrong object and its implication runs the wrong way.

Two distinct defects in one section.

**(a) Wrong object.** §2 identifies "the operative certified radius" as
`1.00000000458067e-6`, from `arb(center) + arb(0, arb("1e-6"))`
(`r3b_endpoint.flagship_s_box`). That solid box is what feeds the **enclosure**
computations (`compute_endpoint_trace_bound`, F_R, W/R2 sups). It is NOT the
object that produces the localization statement. The winding contour is built
by `certify_r3_flagship.closed_boundary_segments(PIN_RE, PIN_IM,
arb(HALF_WIDTH), arb(HALF_WIDTH), K)`, and `arb("1e-6")` has radius
`4.53e-23`, not `4.58e-15` (measured). Nor is `1.00000000458067e-6` what the
cited receipt records: `W_ENVELOPE_CERT_V2_RECEIPT.json` stores
`"half_width": "[1.00000000000000000000000e-6 +/- 1e-34]"` alongside the
printed `"re_interval": "[… +/- 1.01e-6]"`. The receipt therefore answers
`SCAT1…REFEREE.md` item 12 directly and far more cleanly than §2's argument
does — and §2 never cites it.

**(b) Inverted implication.** §2 concludes: "operative certified ball ⊃
declared closed box … Every enclosure certified over the ball holds on the
declared box a fortiori". The first half is true and the direction is right
**for sup/enclosure quantities**. It is exactly backwards for the load-bearing
claim of the whole lane, which is a zero-**existence/localization** statement:
"a zero lies in the box". A certificate that a zero lies in a LARGER region
does not certify that it lies in a SMALLER one. If `1.00000000458067e-6` really
were the operative contour radius, declaring `±1e-6` would be a
STRENGTHENING, not an a-fortiori weakening, and `THEOREM_G5_OFFLINE_ASSEMBLY.md:189`
would be overstated (by a physically irrelevant `4.6e-15`, but overstated).
The recommended paper footnote in §2 encodes the inverted reasoning verbatim
and must not be used.

**Required correction.** Rewrite §2 to (i) distinguish the enclosure box from
the contour, (ii) ground the `1e-6` declaration in
`closed_boundary_segments` + the receipt's `half_width = [1e-6 ± 1e-34]`
field, (iii) state the print explanation as what it is (Arb prints the radius
rounded UP to ~3 significant digits, hence `1.01e-6`), and (iv) drop the
"a fortiori" framing or restrict it explicitly to enclosure-type quantities.
`SCAT1…REFEREE.md` item 12 should be marked discharged **by the receipt
field**, not by §2's current argument.

Note also that §2's asserted mechanism — "the decimal string '1e-6' is not
binary-representable, so Arb stores an upward-rounded binary radius" — is a
root-cause claim given without evidence and is wrong: `arb("1e-6")`'s own
radius is `4.53e-23`. The `4.58e-15` comes from Arb's low-precision `mag_t`
radius representation in the `arb(mid, rad)` constructor.

### C2 — §4's reflected endpoint `Re ρ ≈ 0.5894543` is arithmetically wrong.

`1 - 0.41054373549473627 = 0.58945626450526373`. The note prints `0.5894543`
(digits transposed in the 6th–7th decimal). This is a paper-facing endpoint of
the NOGO-OPEN-1 closure argument, quoted to 7 digits. §6 Phase 5's 4-digit
`≈ 0.5895` is correct, so the error is localized to §4 — which makes it the
kind of defect that survives review by looking consistent with its neighbour.
Correct to `0.5894563` (or `0.58945626`).

### C3 — The B7 evidence chain is not traceable: three "receipts" do not exist.

Against this program's standard ("every numeric claim traceable to a
receipt/JSON"), §7 lists `mms_q5_indep.py`, `crossval_grid.py` and
`repin_fallback.log` under "Receipts index". None exists anywhere in the repo
or worktrees (`find` over the tree: no hits). §1.5's mitigation — "all
commands are in this session's transcript" — is not a receipt a later referee
can reach. Consequently §1.3(b) (the independent mpmath builder) and §1.3(c)
(the 12-point cross-validation grid, `WORST 8.134158228041616e-11`) are, as of
now, **unverifiable assertions**. Separately, §4's fallback winding row
(`ball [0.99999949, 1.00000051]`, `zero_certified: true`, `K=28`,
`hx=hy=0.012`) has no citation and no repo hit, while the s_2 row beside it is
traceable to `SCAT1…SOL.md:378`.

Mitigation, and why this is C3 and not a REJECT: I independently reproduced
the *decisive* part of B7 without the missing scripts — the code-level root
cause (item 2), and the proof-by-fix at both M=14 and M=22 (item 3), using a
fix I wrote myself. B7's conclusion stands on evidence I generated. But the
note's own §1.3 pillars must be re-run and persisted (commit the two scripts
plus a JSON receipt into `lane_g/second_pin/`), and the winding row must be
cited or deleted.

**On "is proof by fix sufficient?" (explicit referee charge).** By itself, no
— a one-line change that makes an answer agree with the target is confirmation
-biased by construction. Here it is sufficient, for three reasons I verified
independently: (i) the coordinate mismatch is visible in the source and is a
*defect on its own terms*, identified before and independently of the
agreement; (ii) the doc's derived wrong operator
`g ↦ weight(z)·g(c_j+(θ(z)-c_j)/2)` is an exact algebraic consequence of the
mismatch, and predicts (correctly) that the buggy code has its own M-stable
zeros; (iii) the fix is uniquely determined up to an equivalent
re-parametrisation (halve the normalisation radius, or move the nodes to the
full radius), not tuned. Item (i) is what makes the argument non-circular, and
the note does state it — but it states it *after* the fix, which understates
its own strongest evidence. Recommend reordering §1.4 to lead with the source
defect.

### C4 — "MMS eq. (34)" is a miscitation, and the 1-E7 caveat is dropped.

§1.3(a) and §1.5 attribute the three-row q=5 reduced operator to "MMS
arXiv:0912.2236 eq.(34)". Per the repo's own verbatim extraction
(`MMS_0912.2236_EXTRACTION.txt`, "NOTE ON EQUATION (34)"), eq. (34) is
`\label{LoverK}`, i.e. `Z_S(s) = det(1-L_s)/det(1-K_s)`. The three-row display
is `\label{reduced3}` (source lines 1574–1585). The content the note
transcribes is correct — I verified it character-for-character against
`reduced3`, including the `±` signs and the p.21 negative-index definitions —
but the label is wrong. The repo overloads "eq. (34)" for both objects
(`THEOREM_G5_OFFLINE_ASSEMBLY.md` does it too), so this is inherited, not
invented; it must still be pinned before publication.

Compounding it: the note asserts a clean "verified line-by-line" closure while
silently dropping the most-caveated form of that same source claim already on
the ledger — `THEOREM_G5_OFFLINE_ASSEMBLY.md` (V7/V8/Kimi 1-E7): "the heading
above MMS eq. (34) prints `q = 2h_q + 3 > 5` while Lemma 4.2 states q ≥ 5; the
q = 5 identification rests on the general incidence formula, not the displayed
heading. The paper must carry this footnote." A B7 closure that removes a
convention caveat must carry that footnote forward, not omit it. (The LaTeX
source's `h_q ≥ 1` does include q=5, which strengthens the position — but that
is an argument to *make*, not to leave out.)

### C5 — The cross-validation does not cover the pin that was selected.

§0.1 advertises the builder-vs-builder grid as "spanning both sectors and both
pins' ordinates". The ordinates are `5.76353724` (flagship) and `10.56029678`
(s_2). §4 then selects a THIRD pin at `|t| = 7.8198`, whose ordinate appears in
no cross-validation in §1.3. Since the note's own B2 analysis makes `|t|` the
dominant degradation driver, and since the observed relerr already degrades
`~1e-16 → 8e-11` between `t = 5.76` and `t = 10.56`, the un-probed value sits
in exactly the interval where the two builders' agreement is changing by five
orders. Add `t = 7.81976824701551188` to the grid, or reword §0.1 to say the
selected box's ordinate is not cross-validated. Related: the claim that the
`8.2e-11` worst case is "limited by 30-dps cancellation, not by any structural
difference" is asserted with no dps-doubling test — an unexplained anomaly
presented as explained.

### C6 — §6, the "frozen execution plan", contains three factual errors and its central constant is dead.

- **(a)** "Copies … of `certify_r2_flagship.py`, `certify_r3_flagship.py`,
  `r3b_endpoint.py`, `certify_r3b_flagship.py` from
  `.worktrees/aletheia-restore/code/tb_certify/`" — two of the four are in
  `code/tc_rerun/` (verified by `ls`). Caught downstream
  (`S2_PHASE1_WR2_RECEIPT.md §6.1`), but the frozen plan is wrong as written.
- **(b)** "TB V2 + E1 + K_s receipts reused verbatim (no `s` dependence — prep
  §2)". The reference is prep **§3**, and prep §3 explicitly requires a
  per-pin distance evaluation. The K_s *divisor lattice* is s-independent; the
  *clearance* is not — §4 of this same note computes a new one (`0.7057`).
  Assembly link 5 must be re-derived at the new box (trivially: half-diagonal
  `√2·1e-6` ≪ `0.7057`), and the plan should say so instead of implying no
  work.
- **(c)** Phase 3's `N = 160`, its `~17 CPU-h` budget and its "feasible
  overnight" local option are all void: the Phase-1 gate the plan itself
  specified returned `F_R(160) = 1.3958e12` against a boundary det level of
  `4.2493e-6`, and the campaign dispatched `N = 288` on Kaggle at ~58 CPU-h
  (owner-approved). §0.4's forward claim "the fallback maximizes the
  probability that `N = 160` closes" is likewise falsified. The plan is not
  "ready to dispatch"; §6 needs an errata header stating that Phases 3–5 were
  re-frozen at N = 288 and pointing to `S2_NSCALING_RECEIPT.md` (N* = 274
  measured) and `S2_CONTOUR_CAMPAIGN_RECEIPT.md`.

  Design observation on the gate itself (not a defect in the numbers): §6's
  GATE says to "inspect `F_R`(new box) against the flagship's `1.78e-6`" —
  i.e. it anchors the comparison to the flagship's F_R rather than to the new
  box's own boundary determinant level. Downstream, `S2_PHASE1_WR2_RECEIPT.md`
  §4–§5 misread that level as `4.2493` instead of `4.2493e-6` and recommended
  N = 256 on the strength of it; the error was self-caught in
  `S2_NSCALING_RECEIPT.md` and the campaign correctly ran N = 288, so nothing
  downstream is broken. But a gate phrased as "det lower bound at the NEW box
  minus F_R, with exponents printed" would have made the misread impossible.
  **`S2_PHASE1_WR2_RECEIPT.md` §0/§4/§5 still contain the uncorrected 1e6
  misread and should be errata-stamped** — it is not in my charge, but a
  reader hitting that file first will take away a wrong N.

### C7 — "the flagship's certified 0.455100" overstates a point margin (LEDGER RULE).

§4 contrasts the two candidates' "K_s point clearance [FLOAT, trunc down]"
with "the flagship's **certified** `0.455100`". Both figures come from the same
`KS_GATE_REPORT.md` table, and `THEOREM_G5_OFFLINE_ASSEMBLY.md` link 5 (Kimi
1-E6) states plainly: "the recorded G_5 distance 0.4551002 is center-to-lattice,
not box-to-lattice … the artifact itself records a point margin." Grading the
new numbers [FLOAT] while promoting the identically-derived old number to
"certified" is precisely the claim-inflation the LEDGER RULE forbids. Label
both as point margins, and carry the 1-E6 half-diagonal argument for the new
box.

---

## 3. MINORS

- **m1.** §3 quotes pins to 17–18 significant decimals
  (`PIN_IM = 7.81976824701551188`) from a double-precision midpoint Newton.
  My re-run returns the double `7.819768247015512`. The extra digits are the
  exact binary expansion, not converged information; harmless as a frozen
  constant (it is what the code parses), but say so, since the note elsewhere
  claims stability "to 12 decimals".
- **m2.** §3's B1 evidence varies **N only**. `n_head = 4`, `sign = +1` and
  double-precision midpoint arithmetic are held fixed. "Freezability" would be
  better supported by one perturbation of `n_head` (e.g. 6) at fixed N.
- **m3.** §4's s_2 row `B2 p = 0.4860548468` is computed from the N=22 value
  `0.24302842340131198`, not from §3's frozen `0.24302842350057649` (which
  gives `0.4860548470`). Internal inconsistency between §3 and §4.
- **m4.** §4 says the NOGO-OPEN-1 requirement "is met by this pair if the
  second box certifies". Per `SCAT1…SOL.md §8/C3` the implication also needs
  nonreal, off-line, and **strictly interior** `0 < Re s* < 1/2`. Both pins
  satisfy it numerically, so the conclusion holds — but the condition should be
  stated, not assumed, in the sentence that closes the lane's headline problem.
- **m5.** §4's `21675` box-widths vs `SCAT1…SOL.md §8/C2`'s `21676` for the
  same quantity: truncation-down vs round-up of `21675.72`. The note's
  direction is the conservative one; a one-word note prevents a future reader
  reading it as a contradiction. Also, "box-widths" should be stated as full
  widths (`2e-6`) — on the half-width reading the figure is `43351`.
- **m6.** §1.3(c) compares the mpmath builder against the Arb builder's
  **midpoints**. That validates the formula, not the ball radii / enclosure
  semantics. Worth one sentence, since "independent confirmation" reads
  stronger than what was done.
- **m7.** §1.2's table is quoted at N=22 with no dimension-tail bound, so the
  `6.821e-09` / `2.295e-08` entries are "small", not "zero". The note's
  [ARB-MID] grade covers this, and §4's framing is correct, but the phrase
  "zeros of NEITHER sector" is a hair stronger than midpoint evidence gives.

---

## 4. What I did NOT check

- The s_2 Newton re-pins at N=22/28/36/44 (§3, second block) — arithmetic of
  the quoted spreads verified, the runs not reproduced. s_2 is not the selected
  box.
- Anything downstream of this note beyond what item 19 / C6.c required
  (`S2_PHASE1_WR2_RECEIPT.md`, `S2_NSCALING_RECEIPT.md`,
  `S2_CONTOUR_CAMPAIGN_RECEIPT.md` are separately UNREFEREED and are not
  covered by this verdict).
- The MMS PDF itself: I graded §1.3(a) against the repo's committed verbatim
  LaTeX extraction, which is a stronger artifact than a PDF page read, but is
  itself an UNREFEREED extraction.

## 5. Disposition

**PROMOTABLE-WITH-CORRECTIONS** (C1–C7 + m1–m7). B7 and B1 may be cited as
closed once C3's artifacts are persisted and C4's caveat is restored. §2 must
not be cited at all until C1 is rewritten. No part of this note authorises the
`NO_VERTICAL_LINE_COROLLARY.md` upgrade — the note itself says so, and that
gate is unchanged by this review.
