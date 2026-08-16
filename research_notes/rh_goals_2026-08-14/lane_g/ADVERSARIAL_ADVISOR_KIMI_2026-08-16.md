# ADVERSARIAL ADVISOR AUDIT — Kimi, 2026-08-16

**Scope.** The last ~24h of the LAW program: MAP.md bullets dated 2026-08-16
(LAW crux update through NEGATIVE CONTROL) and the ten lane_g notes
`LAW_STRIP_AND_MIRROR`, `LAW_MIRROR_Q3_DISCRIMINATOR`, `LAW_TEO_KAPPA_CORRECTED`,
`LAW_P_CONTINUATION_CHECK`, `LAW_Q3_BRANCH_DIAGNOSIS`, `LAW_DETK_IMPACT_AUDIT`,
`LAW_U1PHI_PROOF_ROUTE`, `LAW_MINIMAL_HYPOTHESES`, `LAW_NEGATIVE_CONTROL`,
`LAW_U2B_CLOSURE`, plus `lane_p/FLAGSHIP_PAPER_DRAFT.tex` (abstract, §1.2,
thm:main, Links 5–6).

**Method, disclosed.** I read the MAP and all ten notes in full myself. I then
ran four independent receipt spot-checks (delegated read-only auditors) covering
*every* receipt the notes cite: the mirror chain (`mirror_u4`, `mirror_arith`,
`mirror_nconv_q12`, `mirror_q3`, `mirror_q3_exponent`, `mirror_q3_signflip`,
`strip_confirm`, `strip_method_validation`, `strip_phi_continuation`,
`mirror_direct_phi`), the correction chain (`mirror_u4_corrected`,
`_sigmasweep`, `q3cont_*` ×6), the diagnosis/impact chain (`q3diag_*`,
`q3impact_*`), and the control chain (`negctrl_*`, `d1_q*`, `probe_d1_scan.py`,
`probe_negctrl.py`), plus the flagship paper's `det(1−K_s)` lines. The defect
list below quotes exact receipt values produced by those checks. I did **not**
re-execute any probe; where a claim could not be verified from receipts I say
so. No git commands were run; no file other than this one was written.

**One-line verdict.** The receipts are real and the headline chain (two
structural bugs found and fixed at the theorem level; U4 rehabilitated at
q = 3, 4, 6) checks out to the last cited digit — but the program's ledger
compresses away load-bearing caveats, one central table contradicts its own
receipts in four cells, the engine repair has not been applied to code, and the
strategic centre of gravity is still a crux that the program's own measurements
say is adverse, while a cheaper donor route (effectivize Selberg–Hejhal) sits
blocked on a library errand.

---

## A. TASK SELECTION — mostly right, and not for the stated reason

**The mirror/impact/negative-control lanes were not displacement activity.**
They were validation debt being repaid late. The sequence
mirror → q3-discriminator → Teo correction → P-continuation → q3-diagnosis
found that the repo's determinant engine — the instrument behind §7.3's guard,
§10's addendum, §4.3's retrodiction, and every published magnitude — (i) had
Teo's `Γ₂` inverted (reciprocal of `barnesg`), and (ii) computes only the
**numerator** of MMS's theorem, omitting `det(1−K_s)`. These are not cosmetic:
they invalidated what looked like a 10¹⁹ refutation of U4, and they corrected
every magnitude in the lane. That is higher expected value than another week
grinding `(U1-φ-a′)`. The fair criticism is prospective: **the instrument was
used to draw crux-relevant conclusions (§7.3, §10, §4.3) *before* it was
validated anywhere off its trivial region.** All three "structurally blind
checks" were blind for the same reason — they probed where the answer is ≈ 1 or
≈ 0 by construction. The lane's own new rule ("a check has to be run where the
object is not near-trivial") is correct and should have been the standing rule
before §7.3 was ever written.

**What is actually being neglected, ranked:**

1. **The repair is not in the code.** `LAW_Q3_BRANCH_DIAGNOSIS.md` §7 item 1:
   "No code was fixed." `LAW_DETK_IMPACT_AUDIT.md` §7 item 1: "the one-line
   `det(1−K_q)` divisor in `zeta_cert_rosen*.py` is still not applied." The
   diagnosis is banked in notes; the engines still return the bare numerator.
   Every future magnitude any lane computes risks re-contamination, and two
   stale artifacts are live *now* (C.2 below). Meanwhile the genuinely cheap
   code fix that *was* owed from the negative control (the `probe_d1_scan.py`
   Re-clamp) **did** land (`cfd7bec`) — so the bottleneck is prioritization,
   not process. This is the single clearest misprioritization of the last 24h:
   a fifth audit note was written while the one-line engine repair sat
   unapplied.
2. **`zeta_cert_rosen_even.py` and `zeta_cert_rosen_q5.py` have never faced an
   independent evaluator.** The q=3 branch was vindicated operator-by-operator
   against Mayer's classical determinant. The even-q module is confirmed only
   by *consistency* (`LAW_Q3_BRANCH_DIAGNOSIS.md` §4, honest about this), and
   the q=5 flagship branch's own validations (`selfcheck_q5`, Maass zeros,
   Hejhal point-matching — `LAW_P_CONTINUATION_CHECK.md` §5) are all
   **zero-location checks, which are structurally blind to exactly the genus of
   defect found twice this week** (zero-free multiplicative factors). No q = 5
   *magnitude* has ever been checked against an independent computation.
3. **Lemma E2 is the load-bearing unproven lemma.** The program's most
   consequential negative result — Theorem E3, hence "(U1-φ-a) is FALSE", hence
   "route 2 dead" — rests on `min C_q = λ_q`, `N_q(λ_q) = 1`, whose written
   proof the lane's own reviewer marked **INVALID-AS-WRITTEN**
   (`LAW_U1PHI_PROOF_ROUTE.md` §2.2 [REPAIRED] block: attainment ≠ minimality;
   the `a, d ∈ λ_q Z` multiplicity step unjustified). It is numerically
   confirmed at 15 levels, and `CITATION(Iwaniec Thm 3.4)` was never opened.
   The note flags both honestly; the MAP ledger (line 99) then states
   "(U1-phi-a) REFUTED" with neither flag. If E2 is wrong, the strategic
   picture inverts. Re-proving E2 (Ford isometric circles, or Aristotle target
   B1) is worth more than any further measurement.
4. **The decisive datum against U1-min was found and then delegated away.**
   `LAW_MINIMAL_HYPOTHESES.md`'s addendum ran its own "cheapest decisive
   experiment" and got the adverse answer: `dU_2` (Re s = 1/4, *inside* the
   minimal domain) grows at slope **+1.056** over q = 12…100 while its mirror
   `dU_6` is flat (−0.039). That is the one adverse point the
   identification-domain argument cannot dissolve. The note delegates
   adjudication to "the running strip measurement lane" — which then measured
   `|φ_q|` **growing** at t = 1.5, 3.5 on the strip. The two results point the
   same way. Nobody has owned the direct question (a finer t-scan at Re = 1/4,
   and interval arithmetic on the dU_2 series) as a named task.
5. **HITL library items are on the critical path of the only healthy route.**
   Hejhal Vol. 2 §7 (the effectivity donor) and Schmidt–Sheingorn 1995
   (systole priority, `LAW_U2B_CLOSURE.md` U2b.5) are both human errands, both
   days old, both blocking.

---

## B. PROGRESS REALITY-CHECK — the U4 chain verifies; the "0 flips" headline needs a patch

**The bug chain is real and the numbers match the receipts.** Spot-check
results, in brief: every receipt-cited number in `LAW_STRIP_AND_MIRROR`,
`LAW_MIRROR_Q3_DISCRIMINATOR`, `LAW_TEO_KAPPA_CORRECTED`,
`LAW_P_CONTINUATION_CHECK`, and `LAW_Q3_BRANCH_DIAGNOSIS` matches its receipt
to the printed precision — the 10¹²–10¹⁹ mirror failures, the N-convergence
drifts ≤ 4e−16, the back-solved exponents, the corrected ratios
(1.308486/1.663338/1.982774 at q = 3; 0.455610/0.701397/0.840166 at q = 4;
0.879730/1.546651/2.054840 at q = 6), the independent-evaluator identity
1.000000005/004/003, the `b_q` table (b₃ = φ⁻⁴ = 0.145898033750315 ✓), T1/T2/T3
(rel err ≤ 4.5e−9 on 27 banked rows), and the q = 4 near-zero mechanism
(0.108344 at σ = 1.00, det(1−K₄) zero 0.0615 away). The two bug *diagnoses*
are anchored in primary sources, not fits: Teo's Prop. 2.5 / Thm 2.2 / p.24
recursion were re-quoted from arXiv:1901.07898v2 and the `Γ₂ = 1/G` lemma was
independently re-verified numerically against the paper's true product formula;
the MMS quotient was quoted from the arXiv **LaTeX e-print** of 0912.2236, not
OCR. The provenance claims also check out: `q3cont_mayer_indep.py` imports no
repo module; `q3diag_detK.py` reads only banked JSONs; the kernels under test
were byte-identical imports.

**Caveat on "U4 + corrected Teo JOINTLY CONFIRMED AT THREE q" (MAP line 107).**
At q = 3 the confirmation is genuinely two-sided (independent classical
Mayer/Gauss-map determinant, three classical validations, ≤ 3e−7). At q = 4, 6
it is **mutual consistency of three repaired components with no independent
target** — `LAW_Q3_BRANCH_DIAGNOSIS.md` §4 says exactly this ("contrived, but
logically possible" that two are wrong in compensating ways). The note carries
the caveat; the ledger drops it. U4 at q = 4, 6 should read
"consistency-confirmed, independent check owed", not "confirmed".

**"0 conclusion-flips" (LAW_DETK_IMPACT_AUDIT) — credible in direction,
published before its own table reconciled.** The (a)/(b)/(c) classification is
honestly applied, the one awkward case (item 12, the U4 identity *as written*
being false) is disclosed in §0 rather than hidden, and the reproduction gate
(recomputing every published slope before correcting it) is exactly the right
protocol. Two problems:

- **Its central corrected-guard table contradicts its own receipts in four
  cells** (`q3impact_u1_sup_corrected.json`): q=12 all-8 corrected is **85.21**,
  not the note's **179.24**; q=16 all-8 corrected is **74.62**, not **111.03**;
  q=12 dU₀ corrected is **0.5715**, not **0.6531**; q=16 dU₀ is **0.5166**, not
  **0.5171**. The same two wrong all-8 values propagate to §2 item 1. No
  *conclusion* flips as a result (the corrected slopes were computed from the
  correct receipt values, not from the table), but a note whose headline is "0
  flips" cannot stand on a table that disagrees with its own receipts.
- **The coverage gap is materially live, not archival.** DK.14 scopes the sweep
  to lane_g + the paper. Outside that scope, uncorrected class-(c) material is
  sitting in places people actually read: `EXECUTION_LOG.md` (~line 1144) still
  presents the uncorrected guard (`25.14 → 49.47 → 92.81 → 99.40`, slope
  `+1.50`) and the uncorrected U4 bonus; `lane_c/S5_FACTORIZATION_PRIOR_ART.md`
  (lines 18, 34, 64) still asserts `Z(s) = det(1−L⁺)det(1−L⁻)` for *all*
  q ≥ 3 — the false form, in a prior-art note that exists to be cited. "0
  flips" is true of the swept scope; the program's outward-facing surfaces were
  not in that scope.

**Smaller confirmed number defects** (all receipt-verified; none moves a
verdict, each erodes the receipts discipline that is this program's whole
pitch): see the ranked list in §F.

---

## C. MISTAKES — confirmed defects, suspicions, and remaining blind checks

### C.1 CONFIRMED (receipt-quoted)

1. **`LAW_DETK_IMPACT_AUDIT.md` §3.2 table, 4 cells wrong vs own receipt**
   (values above); plus §0's "sup column falls by up to **1.7×**" — with
   receipt values the all-8 column falls up to **2.0×** (q=12: 170.01 → 85.21).
2. **`LAW_TEO_KAPPA_CORRECTED.md` §1.3 — the "verbatim" Γ₂ product quote is
   garbled.** The paper reads `Γ₂(s+1) = (2π)^{−s/2} e^{s/2+(γ+1)s²/2} ∏…`;
   the note quotes `… · s · e^{((γ+1)/2)s²} · …` (the paper's `e^{s/2}` became
   `s·`). The conclusion (Γ₂ = 1/G) survives — independently re-verified
   against the true formula — but in a note whose entire contribution is
   transcription fidelity, a garbled verbatim-quote block under a `CITATION`
   label is a discipline failure of the same species as the bug it fixes.
3. **`LAW_TEO_KAPPA_CORRECTED.md` §4.3 — "~10⁹ contamination across q = 12→100
   at σ = 1.25" is irreproducible.** Recomputation gives a ~10²·¹ trend
   discrepancy (or 10¹²–10¹⁴ pointwise); no reading yields 10⁹. Same section's
   slope table is endpoint-fit, not the LSQ fit banked elsewhere — labelled
   nowhere.
4. **`LAW_TEO_KAPPA_CORRECTED.md` line 18 — "failing by 10⁵–10¹⁹ at q = 3, 4,
   6"** overstates: at q = 3,4,6 the old failure is 10⁵–10¹³ (as the note's own
   line 25 says); 10¹⁹ occurs only at q = 12–30.
5. **`LAW_P_CONTINUATION_CHECK.md` §2 / PC.6 — "rel drift(32→64) ≤ 1.8e−16
   everywhere"** is false: `q3cont_repo_builder.json` max is **2.51e−16**
   (σ = 1.40).
6. **`LAW_Q3_BRANCH_DIAGNOSIS.md` §0 — the T2 row is scrambled**: it lists
   "`6.3e−12`, `1.1e−10`, `9.3e−10`" against "σ = 2, 3, 4"; the correct order
   is 9.3e−10, 1.1e−10, 6.3e−12 (§3.2 and the receipt are right). And Q3D.1's
   "agreeing to **1.5e−10**" overstates: the worst gate error is **4.42e−10**
   (its own §2 table shows it). Also the header promises a
   `q3diag_rosen_mp.json` receipt that does not exist, and
   `q3diag_rosen_mp.py` hardcodes the Arb reference values instead of reading
   them from the banked JSON — a small provenance break in a provenance-driven
   lane.
7. **`LAW_MIRROR_Q3_DISCRIMINATOR.md`** — §2: "(1−2/q)/2 runs 0.167 (q=3) →
   **0.458** (q=30)": (1−2/30)/2 = **0.4667**. §0: exponents agree "to **1–4
   %**": recomputed relative deviations are **2.2–10.4 %** (absolute
   0.0062–0.0260).
8. **`LAW_STRIP_AND_MIRROR.md`** — the q-slope of the disagreement is
   **+5.67/+5.74** (recomputed), not "+5.6"; §0's "q^{+5.9} over q = 12→22"
   recomputes to +5.98; §2.2/§8's value-error range "0.7 % to 28 %" starts
   actually at **0.24 %**.
9. **`LAW_NEGATIVE_CONTROL.md`** — grid min|det| run B **0.10497**, not
   0.10500; run C **1.31619**, not 1.31600 (truncation presented as rounding);
   "nine orders of magnitude above 1e−12" is ~10.5; "strict minimum of the 3×3
   window" — both scripts use non-strict `== min(window)`; §1.3 calls the
   widened box "D1's own 'viable' rule" — D1 hard-coded `re < 0.5`, not
   `RE_HI + 0.10`.
10. **`LAW_DETK_IMPACT_AUDIT.md` §6** — `1.6259 × 1.000107 = ` **1.62607**, not
    1.62608; `b_6^{3.5} = ` **9.9e−5**, not 5.3e−5; DK.7's "worst 1.6e−3 →
    5.6e−4" contradicts its own §2 item 11 (the q=40 row stays 1.6e−3).
11. **MAP-ledger compression drops load-bearing caveats** in at least two
    places: line 107 ("JOINTLY CONFIRMED AT THREE q" vs the q=4,6
    consistency-only caveat) and line 99 ("(U1-phi-a) REFUTED" vs E2's
    invalid-as-written proof + unopened Iwaniec citation).

### C.2 SUSPICIONS (not confirmed; stated with what would settle them)

- **S1. b₅ has no independent check.** The odd-q `b_q` come from the orbit
  product of MMS's Proposition; the odd-q closed form carries an unresolved
  symbol `R` (Q3D.10, labelled "cosmetic"). But `b₅ = 0.013092084695` feeds the
  flagship reference corrections (|det(1−K₅)| ≈ 0.9026 / 0.8563). If the r₅
  word or orbit product is off, those reference numbers are wrong. Settle by:
  independent computation of the r₅ = [0;1,2,2] orbit and its multiplier, or
  the Γ₀⁺(5)-side classical expression.
- **S2. The q = 5 flagship engine may hide a same-genus defect.** All its
  validations are zero-location checks (C.A.2 above). A zero-free factor
  `R₅(s)` analogous to the q=3 one would be invisible to every check ever run
  on it — and would now be *absorbed* into the "known" det(1−K₅), since the
  detK correction at q = 5 is an inference from the MMS theorem + the q=3,4,6
  pattern, not a measurement against an independent q=5 determinant. Settle
  by: an independent odd-q ≥ 5 determinant (e.g. a Rosen-operator
  re-implementation at a second disc/basis, as `q3diag_rosen_mp.py` did for
  q = 3) compared on magnitudes, or a q = 5 scattering-zero magnitude check.
- **S3. The §4.3 retrodiction survives correction suspiciously well.**
  +0.893 → +0.890 under the detK correction. This is explained by the factor's
  q-flatness (d log|det(1−K)|/d log q ≤ 0.051, DK.5 — verified), so it is not
  evidence of a problem; but it means the retrodictive "agreement with +1.00"
  was never sensitive to the instrument's largest known error, i.e. it is a
  weak discriminator dressed as a strong one. Treat accordingly.
- **S4. The Weyl-count completeness check certifies totals, not spectra.**
  A(120)/(C_q·120²) ∈ [0.988, 1.004] checks the *count*; a q-dependent missing
  modulus class of relative size < 1 % would pass. The q = 3 totient check is
  exact but q = 3 is the degenerate λ = 1 case. No exact per-modulus
  completeness check exists for any non-arithmetic q.

### C.3 Are there more structurally blind checks still trusted? Yes — at least three.

1. **Every zero-location validation of every builder** (Maass zeros, Hejhal
   point-matching, scattering-zero recovery, the negative control's pins) is
   blind to zero-free multiplicative factors — the exact genus of *both* bugs
   found this week. The lane knows this abstractly ("a zero-free R cannot move
   a zero") but still cites those validations as if they certify the builder;
   they certify only its zero set. The q = 5 case (S2) is where this bites.
2. **The detK "insulation" argument itself is trusted where untested.** The
   claim "flagship zero claims UNAFFECTED" rests on det(1−K_s) zero-free on
   Re s > 0 — analytic and fine — but the claim "flagship *needs nothing*"
   additionally assumes the q = 5 builder's only defect is the known divisor
   (S2). DK.12 verified the paper is det(1−K)-aware (abstract l. 68, Link 5
   ll. 442–448, Link 6 ll. 450–456 — the audit's line refs are off by one;
   substance confirmed), and §1.2 contains nothing contradicted by the
   omission. True — but "already aware" is not "independently validated".
3. **Consistency closures substituting for independent ones** (q = 4, 6). The
   pattern "three repaired parts agree, therefore each is right" is the same
   shape as "three blind checks pass, therefore the assembly is right". It is
   stronger here (the parts were repaired from independent primary sources),
   but the q = 4, 6 closure should be labelled what it is until an independent
   Z_{Γ₄} evaluator exists.

---

## D. EPISTEMICS — the taxonomy is good; the compression layer is where honesty leaks

**What is genuinely good.** Statuses inside the notes are the most disciplined
I have seen in an autonomous program: pendency is inherited explicitly
("every number below inherits that pendency"), the vacuous dU₀ agreement is
flagged *proactively* as worth "exactly nothing as evidence", adverse results
are reported with the word "adverse" in the headline, the strip lane says in
its first paragraph that it missed the brief's 6-digit bar, and the
reframes/withdrawals (U4 "refuted" → "the unless clause fired") are tracked
with SUPERSEDED/WITHDRAWN markers rather than silently edited. The
"refutation was actively sought" boilerplate at the end of each note is
formulaic, but for once the receipts back it: the two biggest refutations of
the week landed on the lane's own instrument.

**Where it leaks.**

- **"PROVED (numerically)" is doing too much work.** N-convergence, assembly
  checks, and float identities are labelled `PROVED`. The convention is
  declared, but "U4 at q = 3 + corrected Teo jointly confirmed, PROVED
  numerically" (PC.5) is a ≤3e−7 float agreement at three abscissae — strong
  evidence, not proof; the q=3 case happens to also be Mayer's theorem, which
  is what actually makes it safe. The label should be reserved; the word
  "confirmed-measured" already exists in the lane's vocabulary and is the
  honest one.
- **The ledger is the weak layer.** Notes carry caveats; MAP bullets compress
  them away (C.1.11). Two of the three most decision-relevant compressions
  (U4 "confirmed at three q"; U1-φ-a "REFUTED") drop exactly the caveats a
  decision-maker needs. Recommend a ledger rule: a MAP bullet may not upgrade
  a status beyond the note's own most-caveated phrasing.
- **One quiet favorable reframing.** `LAW_STRIP_AND_MIRROR.md` Task A: the
  brief demanded 6 digits and an honest stop if unreachable; the lane
  delivered 1–2 digits, redefined the estimand from value to slope, validated
  the slope on three arithmetic levels (one degenerate), and proceeded to an
  adverse verdict on the non-arithmetic family. The note *discloses* all of
  this (§2.2 "inferred, not shown"; §2.5 "does not establish growth in the
  limit") — so it is not hidden — but the trajectory from "stop honestly" to
  "verdict anyway" deserves its own adversarial round, because the verdict
  (crux measured-adverse) is now load-bearing for strategy. The 7-point,
  non-monotone q-grid is thin ice for a sup-over-t failure claim; interval
  arithmetic and a finer grid are owed before "MEASURED-ADVERSE" hardens into
  "abandon the route".
- **Not self-congratulatory beyond evidence — but note what the scoreboard
  shows.** The week's narrative is "refutation machinery works". The
  scoreboard is: the qualitative law turned out to be Selberg–Hejhal 1983
  (honestly recorded); the lane's own crux was refuted at the abscissa it was
  posed; the instrument had two structural bugs; the flagship survived
  everything. The machinery is genuinely good at finding errors; it has not
  yet produced a positive advance on the law itself. That is not a criticism
  of the machinery — it is the argument for changing what it is pointed at.

---

## E. STRATEGY — the bet should move

Facts that should drive the decision, all from the program's own receipts:

1. The qualitative large-q law is **already a theorem** (Selberg–Hejhal 1983,
   Hejhal Vol. 2 Thm 7.11/Cor 7.12) — acknowledged in MAP's LAW REFRAME bullet.
   The novel content is effectivity (Q₀), the certified finite base, the
   dichotomy mechanism, and per-surface certificates.
2. The lane's *own* route to effectivity (Rouché/Vitali + U1-min via
   (U1-φ-a′)) is measured-adverse at every place it has been measured: the
   strip sup fails at t = 1.5, 3.5 (+0.477/+0.391 at σ = 0.90/0.95,
   truncation- and budget-stable); dU₂ inside the minimal domain grows at
   +1.056; route 2 (FE from σ ≥ 3.5) is dead by Theorem E3; and E3 itself
   rests on the unproven Lemma E2 (A.3).
3. The **donor route does not need U1-min at all.** Hejhal Vol. 2 §7 contains
   a complete *ineffective* proof. Effectivizing an existing proof skeleton is
   a different, strictly lower-risk task than rescuing a measured-adverse
   crux — and it is currently blocked on a library errand, not on analysis.
4. The flagship G₅ paper is clean under the week's findings (detK-aware,
   class (a)/(b) throughout, zero-location insulation analytic). The dichotomy
   side (M1d/M1e/M1f: φ₄, φ₆ closed forms, machine-verified finite
   obligations, confirmed resonance predictions at two arithmetic levels) is
   the strongest *positive* new mathematics in the program and is independent
   of the tail crux.

**Recommendation, in order:**

1. **Ship the flagship paper now.** It needs nothing from the open lanes;
   waiting couples a finished result to an adverse one.
2. **Publish the dichotomy/arithmetic-side results as the second paper** (M1
   family + systole theorem, after the Schmidt–Sheingorn priority check),
   framed with the negative control and the instrument-validation story —
   which is itself a contribution (two named structural bugs in a transfer-
   operator pipeline, with the repair and the blast-radius audit).
3. **Re-aim the law effort at effectivizing Selberg–Hejhal** (donor skeleton +
   certified finite base q = 5 done, q = 7 running), and get the HITL Hejhal
   Vol. 2 §7 text this week. **Stop new compute on (U1-φ-a′) as posed** until
   the strip measurement is hardened (interval arithmetic, finer q-grid): if
   the growth survives, the honest write-up is a *negative structural result*
   — the natural Vitali/FE route to effectivity fails because |φ_q| does not
   decay on the strip at generic heights — which both explains Selberg–
   Hejhal's ineffectivity and redirects the field. That is a publishable
   theorem, and it is the direction the measurements actually point.
4. **Pay the engineering debt before any further magnitude-dependent work:**
   apply the one-line det(1−K_q) divisor to `zeta_cert_rosen*.py` with the
   q = 3, 4, 6 mirror identity as the revalidation gate; fix
   `LAW_U1_GROWTH.md` §3.1's code block and `probe_u1_growth.py` ll. 121–123
   (both flagged TODO, both still live traps); correct the four cells and the
   stale surfaces (EXECUTION_LOG, lane_c/S5).
5. **Close the validation asymmetry:** independent even-q and q = 5
   determinant checks (S2), and the Ford-circle re-proof (or Aristotle B1) of
   Lemma E2 before the E3 kill is cited strategically.

Do **not** "wait for Hejhal" as the whole strategy (the finite base and the
dichotomy proceed regardless), and do not pivot *everything* to the dichotomy
mechanism — M3 (deformation probe) is precisely the question the literature
scout (`LAW_DEFORMATION_PRIOR_ART.md`) may answer for free; finish that read
first.

---

## F. Ranked lists

### F.1 Defects found (ranked by consequence)

1. **Engine repair unapplied** — `zeta_cert_rosen*.py` still return the bare
   numerator; every future magnitude is exposed; two stale surfaces live
   (EXECUTION_LOG ~l. 1144; lane_c/S5_FACTORIZATION_PRIOR_ART ll. 18/34/64).
2. **`LAW_DETK_IMPACT_AUDIT` central table contradicts its own receipts in 4
   cells** (85.21 vs 179.24; 74.62 vs 111.03; 0.5715 vs 0.6531; 0.5166 vs
   0.5171) — the "0 conclusion-flips" note must be patched before its headline
   is quoted again.
3. **Ledger-level overstatement of U4 at q = 4, 6** ("confirmed" vs
   "consistency-confirmed") and of the U1-φ-a refutation (E2 invalid proof +
   unopened citation dropped).
4. **q = 5 / even-q builders never independently validated on magnitudes** —
   the same-genus blind spot as both bugs found this week (S2; suspicion, not
   confirmed defect).
5. **Lemma E2 unproven but load-bearing** for the program's biggest negative
   result.
6. **Garbled "verbatim" Teo quote** in the transcription-fidelity note
   (conclusion unaffected, independently verified).
7. **dU₂ = +1.056 inside Ω̃_min unowned** — the single most decision-relevant
   open datum in the program.
8. Cluster of receipt-vs-prose arithmetic defects (C.1.4–C.1.10): scrambled T2
   row, 1.8e−16 vs 2.51e−16, 0.458 vs 0.4667, "1–4 %" vs 2.2–10.4 %, +5.6 vs
   +5.67, 0.10500/1.31600 truncations, 1.62608 vs 1.62607, b₆^3.5 arithmetic,
   DK.7 self-contradiction, "~10⁹" irreproducible, missing
   `q3diag_rosen_mp.json`, hardcoded reference values in `q3diag_rosen_mp.py`.

### F.2 Recommendations (ranked)

1. Ship the flagship paper; it is clean.
2. Apply the det(1−K_q) divisor to the engines + revalidate (q = 3, 4, 6
   mirror identity as gate); fix the two flagged wrong-code survivors
   (U1_GROWTH §3.1 block, probe_u1_growth.py); patch the detK audit's four
   cells and the two stale surfaces.
3. Move the law effort to effectivizing Selberg–Hejhal via the donor proof;
   freeze new compute on (U1-φ-a′) pending interval-hardening of the strip
   measurement; if the adverse result hardens, write it up as the negative
   structural theorem it is.
4. Re-prove Lemma E2 (Ford circles / Aristotle B1) — it currently carries the
   E3 kill.
5. Commission an independent even-q and a q = 5 magnitude check (the
   `q3diag_rosen_mp.py` pattern at a second basis/disc); settle b₅ (S1).
6. Ledger rule: MAP bullets may not exceed the note's own most-caveated
   status; add a "caveats carried" field.
7. Own the dU₂ question: finer t-scan at Re = 1/4 + interval arithmetic, as a
   named task, not a delegation.
8. Clear the HITL errands (Hejhal Vol. 2 §7; Schmidt–Sheingorn) — they gate
   the two healthiest remaining items (donor route; systole priority).
9. Label q = 4, 6 as "consistency-confirmed" everywhere; commission the
   independent Z_{Γ₄} evaluator or stop calling it confirmed.
10. Adopt the lane's own new rule prospectively: no check counts unless it
    probes where the object is non-trivial — and audit existing "validations"
    against it (the zero-location validations are the exposed class).

### F.3 What the program is doing right (brief)

- Pre-registered rules quoted before numbers (mirror q3 discriminator,
  negative control, n_head sweep) — and followed when they fired against the
  lane's preferred answer.
- Primary sources opened and quoted from e-print LaTeX, not OCR; two bug
  diagnoses anchored in sources, not fits.
- Independent evaluators built with zero shared code when it mattered (Mayer
  determinant; mpmath operator re-implementation).
- The negative control found a real latent bug (the Re-clamp) and the fix
  landed in code the same day.
- Honest reframes with markers (SUPERSEDED/WITHDRAWN/[REPAIRED]), pendency
  inheritance, and the Selberg–Hejhal downgrade recorded in the ledger itself.
- Machine verification where it is cheap (Aristotle receipts with axiom
  audits), and a blast-radius audit that classified *before* correcting.
- The flagship theorem survived a week of hostile attention essentially
  untouched — that is the program's proof that its certificate discipline
  works.

---

*Audit ends. Receipts for this audit: the ten notes and the four delegated
spot-check reports (mirror chain; Teo/P-continuation chain; q3diag/q3impact
chain; negative control + flagship paper), whose match/mismatch tables are the
basis for every "CONFIRMED" entry above.*
