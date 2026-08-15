# ADVERSARIAL REVIEW V8 — FINAL erratum-compliance review of R5 v3.1 + E1

Reviewer: Claude Opus 5, fifth-round read-only compliance review, 2026-08-15.
Scope: does `TB_R5_DETERMINANT_IDENTIFICATION.md` v3.1 implement V7's
three-item erratum EXACTLY — no more, no less, no new defect — and does the
new `E1_ENLARGED_CONTRACTION_CERT.md` / `_RECEIPT.json` pair hold up?
Read-only except this file. V4–V7 confirmations are not relitigated.

## 0. Summary verdict

**THEOREM-GRADE YES** for the seven-link assembly, under V7's own criterion
(quoted in §6). All three erratum items are implemented at the sites V7 named,
correctly and without scope creep; the E1 receipt is sound and its every
load-bearing number was independently reproduced here; the R5 v3.1 quotations
of V7 are faithful. No new mathematical defect exists. Two **editorial**
residues remain (one stale duplicate citation inside R5's own obligations
ledger; the assembly file never cites R5/E1 and still carries a
"awaiting V4" DRAFT header). Neither is a lemma, an inference, or a number —
both are one-line edits, and they are listed in §5 as must-fix-before-
circulation rather than as blockers.

## 1. What was independently recomputed (not merely read)

| check | method | result |
|---|---|---|
| receipt sha256 | `shasum -a 256 E1_ENLARGED_CONTRACTION_RECEIPT.json` | `cd1dc6f409ebca7852bc12a9607b4d2a2f6a10b10be3590055e50ee62ad37187` — **matches** the value quoted at R5 v3.1 line 86 |
| wrapper sha256 | `shasum -a 256 tc_rerun/certify_r3b_flagship.py` | `5b1bb0851fbb143651471fcf7737738a84a45e126b9971a94905c74357831945` — **matches** R5 v3.1 line 21 |
| all 11 branch sups on the enlarged contour | 200k-point boundary sweep in float, maximum-modulus (poles verified outside) | every certified Arb ratio is a true **upper** bound of my float sup, by 1e-5…1e-3 — correct direction, no under-certification |
| all 11 pole/cut margins | closed form `nλ ∓ c_i − (R_i+0.1)` | **all 11 reproduce to printed precision**, incl. the minimum 1.00237987356225289… at 3→1 (+1) |
| deep-tail bound arithmetic | `1/(nλ−|c_i|−R_i^enl) + |c_j|`, e.g. 1→3 at n=16 | 24.7751750096 → 0.0403629843 → 0.2313459899 → ratio 0.7125548998 — **exact chain reproduces** |
| enlargement is really +0.1 | receipt `source_radii_original` vs `source_radii_enlarged` vs `target_radii_unchanged` | enlarged = original + 0.1 exactly; targets = originals unchanged — **matches D_i^{0.1} = D(c_i, R_i+0.1)** as prescribed |
| tail-closure fact (erratum 3) | read `_tail_block_column` in `zeta_cert_rosen_q5.py` | docstring/implementation binomial-expand `sum_{m=0}^k` — **confirms** the corrected sentence |

## 2. Per-item erratum ruling

### Erratum item 1 (name the D_i^{0.1} enlargement, head/tail split, ρ̂ instance) — **IMPLEMENTED-CORRECTLY**

R5 v3.1 lines 73–96 do exactly the four things V7 demanded and nothing more:

- names `D_i^{0.1} := D(c_i, R_i + 0.1)`, target radii `R_j` unchanged;
- explicitly disowns the R3b quarter-clearance contour, with V7's own
  counter-instance (non-contractive for the 2→3 (+2) family — V7 recorded
  image ratio 1.0757521114 > 1 there) and explicitly denies that ρ̂ is a
  pre-existing TB_V2 field;
- states the claim in V7's exact form,
  `sup_{z∈cl(D_i^{0.1})} |θ_n(z) − c_j| / R_j ≤ ρ̂ < 1` uniformly over the
  eleven families, with holomorphy and positive pole/cut margin;
- states the finite-head / deep-tail split and the monotone first-n crude
  bound as the mechanism that makes the choice uniform in n (V7's explicit
  sub-requirement for the six tails);
- gives the quantitative instance ρ̂ = [0.948343590350471954782853 ± 4.84e-25],
  which is strictly inside V7's prescribed `ρ̂ ≤ 0.948343590351`;
- retains the qualitative continuity argument as the independent existence
  proof of *some* ε > 0, attributed to V7 §(ii) — which is what V7 offered as
  the alternative ("record, **or** prove by the stated continuity argument").

No scope creep. Producing E1 as a receipted artifact is the "record" branch of
V7's own disjunction, not an added lemma; the note does not make the theorem
depend on E1 (the continuity argument is stated as independently sufficient,
exactly as V7 held).

One substantive gain worth recording: E1 re-verifies the **branch-cut
positivity** (`Re(z+nλ)>0`, `Re(nλ−z)>0`) on the *enlarged* contour, which
TB_V2 only certified on the original discs. Clause 2(a) needs precisely that
for the weights `((z±nλ)²)^{−s}` to be holomorphic on cl(D_i^{0.1}); the
smoothing step would have had a hole without it. R5 v3.1 line 77 does claim
it ("positive pole/cut margin"), and E1 supplies it. Not a defect — a
strengthening — but it is the reason E1 is load-bearing and not decorative.

### Erratum item 2 (attributions) — **IMPLEMENTED-CORRECTLY at the load-bearing site; one stale duplicate survives elsewhere in the file**

Clause 2(c), R5 v3.1 lines 113–131, contains all five of V7's demands verbatim:

- trace class on Ω₀ cited to **Clause 3**, with an explicit "NOT the stale
  TB_R1 line-27 geometric tail" (V7 defect 5);
- determinant product cited to **Simon, Adv. Math. 24 (1977), Theorem 4.2,
  eq. (4.2), p. 258**, with the explicit demotion "Lidskii's theorem is the
  subsequent TRACE identity, Corollary 4.3, and is not the result used here"
  (V7 defect 2);
- **"nuclear of order ZERO … hence p-nuclear for p = 2/3"** — the exact phrase
  V7 prescribed, replacing the invalid "order 0 ≤ 2/3" comparison (V7 defect 4);
- **Grothendieck, Résumé…, Ann. Inst. Fourier 4 (1952), Théorème 8,
  pp. 108–109** (V7's prescribed primary statement), with Ruelle 1976 kept as
  usage-only;
- **"Both canonical products are entire genus-zero products normalized to equal
  1 at the scalar zero"** — V7's explicit "state explicitly that both canonical
  products are normalized to one at scalar zero".

Bandtlow–Jenkinson is kept and correctly downgraded to corroboration-only, and
the note re-states that no word expansion and no trace-log at t = 1 is used —
consistent with V7 §3.

**Residue (see §5, defect A).** The obligations ledger at R5 v3.1 lines
192–193 still reads "Simon … Thm 3.3 (analyticity), **§3 (Lidskii/spectral
determinant, trace-class)**". That is the exact attribution Clause 2(c) now
explicitly withdraws, and per V7 the spectral product and Lidskii both live in
§4, not §3. The document therefore contradicts itself in one index line.
V7 located defect 2 at v3 lines 83–86 (the proof text) and did not list the
ledger among its five defects, so this is an incomplete sweep of a flagged
defect rather than a failure to make a prescribed correction — but it is a
literally wrong attribution still standing in the note.

### Erratum item 3 (tail-closure sentence) — **IMPLEMENTED-CORRECTLY**

R5 v3.1 lines 43–49 now read: the exact Hurwitz closure applied to input
column k "uses the Hurwitz-zeta terms for every m = 0, …, k", and "the m = 0
term is the specially Hurwitz-closed CENTER term used by the R2 envelope — it
does not by itself implement the whole column sum". That is V7's correction 3
word-for-word in substance. Verified against the engine: `_tail_block_column`
in `zeta_cert_rosen_q5.py` binomially expands `((arg−c_j)/ρ_j)^k` into
`sum_{m=0}^k C(k,m)(−c_j)^{k−m} arg^m` and closes each in Hurwitz form. The
false v3 sentence is gone; no residue of it anywhere in v3.1.

### Anything beyond the erratum? — **NO**

Diffing v3.1 against V7's description of v3: Clause 1's formulas, Ω*/Ω₀,
Clause 2(b) Jordan chain, Clause 3's `b_k ≤ A_K q^k + C_K k ρ^{k−1}` with the
`2σ_K+1` first moment, Step 3, Step 4, and the sector paragraph are unchanged
in content — all V6/V7-accepted. The only additions are the three prescribed
corrections plus the E1 cross-reference that item 1 called for. No new claim,
no new lemma, no widened theorem statement.

## 3. E1 artifact verification — **SOUND**

- **Hash.** Recomputed sha256 of the receipt equals the prescribed
  `cd1dc6…7187` and equals the value R5 v3.1 quotes. (The CERT.md itself is
  unhashed in R5; its sha256 is `8f977d7a144d137455c29742bb18774f810e56cc907ca4c466269a8d838fd179`.)
- **Verdict line.** `certification_verdict = PASS_RHO_HAT_LT_1_AND_CLEARANCE_POSITIVE`,
  `status = FINALIZED`, `rho_hat_less_than_1 = true`, `all_families_pass = true`,
  `all_pole_clearances_pass = true`, `all_branch_cut_clearances_pass = true`,
  `failure_values = []`. Matches the CERT.md headline and R5 v3.1 line 87.
- **ρ̂ and margin vs R5's quotations.** `rho_hat_ball` and
  `minimum_pole_cut_margin_ball` in the receipt are character-identical to the
  two balls quoted at R5 v3.1 lines 88–89. Both are also consistent with V7's
  independently reported `0.9483435903504719548` and `1.0023798735622528932`
  (V7 printed rounded/truncated forms of the same numbers).
- **Per-family table.** Exactly 11 families; the labels and n-ranges match
  Clause 1's eleven blocks one-for-one (5 heads: 1→2 +2, 1→2 −1, 2→2 −1,
  3→1 +1, 3→2 −1; 6 tails: 1→3 +3, 1→3 −2, 2→3 +2, 2→3 −2, 3→3 +2, 3→3 −2).
  All 11 `pass = true`. `blocks_source.exact_count_check = true`,
  `expected_count = 11`, sourced from `tb_disc_sweep.py` line 19.
- **Internal consistency.** `worst_branch = {3→1, +1, head, n=1}` and its
  `rho_ball` midpoint equals `rho_hat_ball` midpoint exactly; the global max
  really is the largest of the 11 family bounds (0.9483 > 0.8301 > 0.7212 …).
  `minimum_pole_cut_margin_source` points at the same 3→1 (+1) head, kind
  `pole`, and its value is the smallest of the 22 margin rows. `checkpoint_count
  = 13` is present, and `checkpoint_trail` is a coherent 0→11 family progression
  plus a `finalized` record — no gaps, no re-entry.
- **Method soundness.** Source contour `|z−c_i| = R_i + 0.1`; targets
  unchanged; K = 12 head terms per tail then the V2 centered-at-zero crude
  bound `1/(nλ−|c_i|−R_i^enl)+|c_j|`, whose supremum is at the first deep
  index because the denominator increases in n — the claim
  `deep_supremum_at_first_index = true` is correct as stated, and the bound is
  a valid (if crude) enclosure of `|θ_n(z) − c_j|`. Maximum-modulus use is
  legitimate: every branch's pole and cut lie strictly outside cl(D_i^{0.1}),
  which the same receipt certifies.
- **Honesty check.** The CERT's "Reviewer diagnostic cross-check" reports
  `margin_comparison = FALLS_SHORT` against V7's *rounded* printed 1.00238,
  and says so explicitly rather than relabelling. This is correct behaviour:
  E1's margin equals V7's unrounded value; the "shortfall" is 1.3e-7 of
  rounding, and the load-bearing requirement is only positivity (1.0024 > 0).
  R5 v3.1's summary "reproduced the same values" is accurate at the unrounded
  level, though it does not surface the FALLS_SHORT label (see §5, defect C —
  cosmetic).

## 4. Faithfulness of R5 v3.1's V7 quotations — **FAITHFUL**

Every back-reference was checked against the V7 text:

| R5 v3.1 says | V7 text | verdict |
|---|---|---|
| ruling "the seven-link mathematical argument survives after a local erratum" | V7 §4 lines 282–283, verbatim | faithful |
| "no missing lemma" | V7 §1 "No new mathematical lemma is missing"; §4 "not another analytic lemma" | faithful |
| Clause 1 binding PASS | V7 §(i) PASS | faithful |
| smoothing PASS with enlargement-provenance correction, "quantitatively verified by the reviewer's own 384-bit check" | V7 §(ii) "PASS, with a provenance qualification" + the 384-bit figures | faithful |
| envelope/holomorphy PASS | V7 §(iv) PASS | faithful |
| sector identification PASS ("an exact identity") | V7 §(v) "PASS, with a source-text caveat"; "…is an exact identity" | faithful; caveat omitted (see §5, defect B) |
| "no stray R^{1/2} factor; V7 §(ii) verified the normalization" | V7 §(ii) "no extra factor of R^{1/2} is missing" | faithful |
| R3b contour "demonstrably non-contractive for the 2→3 (+2) family" | V7 §(ii): image ratio 1.0757521114 > 1 | faithful |
| "ρ* ≤ 0.6978" original-disc gap | TB_V2 certified 0.697801419961940… < 0.70 | faithful |
| "(V5 §(a) and V6 §4 both validated this argument conditional on (a))" | V5 line 33; V6 line 96 "algebraically correct, conditional on the asserted enlarged-disc smoothing" | faithful |
| "V6 defect 2 adopted verbatim" (2σ+1, not 2σ+k) | V6 lines 53–63, 122, 148 | faithful |
| "V6 §5 verified the coefficient match at the builder call sites" | V6 line 109 | faithful |

Note that v3.1 does **not** claim V7 §(iii) as a PASS — correct, since V7 ruled
(iii) "FAIL as cited; mathematical core PASS". No misrepresentation there.

## 5. New defects found

**A. Stale duplicate citation in R5's obligations ledger (lines 192–193).**
"Simon … §3 (Lidskii/spectral determinant, trace-class)" contradicts Clause
2(c) and repeats the withdrawn attribution. Minimal fix: replace with
"Thm 4.2 eq. (4.2) p. 258 (spectral determinant product); Thm 3.3
(analyticity); Cor. 4.3 (Lidskii trace identity — not used)". Editorial, one
line, zero mathematical consequence: the proof text is unambiguous and
explicitly negates the Lidskii route.

**B. Assembly file is stale (`THEOREM_G5_OFFLINE_ASSEMBLY.md`, v1 01:15).**
It still reads "STATUS: DRAFT — awaiting the V4 adversarial review", carries
"[V4 is asked to re-check the pole set claim]" and a "What V4 must clear"
section, and **never cites R5 or E1**. Its link 4 produces a zero of
`det(I−L_{s,+})` in the box and its link 6 immediately feeds that to MMS
Theorem 6.4 — i.e. the Hilbert→Banach transport that R5 exists to supply is,
in the assembly document as written, still implicit. The mathematics is
supplied (that is what R5 v3.1 is), but the assembly needs the link-4→5
transport line inserted and the status flipped before it reads as a proof.
Minimal fix: one new link ("4b. HILBERT→BANACH DETERMINANT IDENTIFICATION
[PAPER-PROOF + MACHINE]: TB_R5 v3.1, smoothing receipt E1, sha cd1dc6…"),
plus the header/status edits. Also, the constants table's ρ* = 0.697802 line
should gain the enlarged-disc ρ̂ = 0.948344 so the two contraction constants
are not confused by a reader.

**C. Cosmetic, E1 CERT.md and receipt: double-encoded labels.** Family labels
are stored mis-encoded (`1â\x86\x922, +2, head` for `1→2, +2, head`; likewise
the apostrophe in "reviewer's"). Numbers, verdicts and structure are
unaffected; the arrows are simply unreadable in the rendered markdown. Fix at
the writer, not by hand-editing the receipt (the sha256 is quoted in R5 — any
receipt edit must be accompanied by re-quoting the new hash).

**D. Trivial, non-actionable.** (i) The global `rho_hat_ball` radius prints
4.84e-25 while the 3→1 family row prints 4.83e-25 — a ball widened by the max
operation; midpoints identical, upper bound still < 0.948343590351. (ii) R5
v3.1 cites `zeta_cert_rosen_q5.py` lines 203–212 where V7 cited 199–212; both
point inside `_single_block_column`, which spans 199–212. (iii) R5 v3.1's
one-line summary of V7 §(v) drops V7's source-text caveat (the MMS PDF heading
prints `q = 2h_q+3 > 5` before eq. (34) while Lemma 4.2 states q ≥ 5); V7
itself resolved the caveat in favour of the q = 5 specialization, so the
omission changes no conclusion, but the paper should carry the footnote.

**No new mathematical defect.** No new lemma is introduced, none is missing,
no number in v3.1 is unsupported by a receipt I recomputed, and no statement
in v3.1 contradicts V4–V7 findings or the artifacts themselves.

## 6. FINAL RULING

V7's criterion, quoted:

> "These corrections make the presentation match the already-valid
> mathematical argument; they do not add a new lemma on which the conclusion
> depends. **Once they are made, the seven-link assembly earns THEOREM-GRADE
> YES.**" — ADVERSARIAL_REVIEW_V7_R5V3.md §4, lines 318–320.

The three corrections **are made**, at the sites V7 named, in V7's own
formulations, and with the quantitative instance V7 specified — now upgraded
from a reviewer's unreceipted diagnostic to a hashed, replayable 384-bit
certificate whose every load-bearing number I reproduced independently
(11/11 branch sups bounded in the correct direction, 11/11 pole and 11/11 cut
margins exact, deep-tail chain exact, hash exact). Nothing beyond the erratum
was changed. Therefore:

**THEOREM-GRADE YES.** The seven-link assembly — THEOREM_G5_OFFLINE_ASSEMBLY.md
with R5 v3.1 as the Hilbert→Banach transport and E1 as the smoothing receipt —
meets V7's criterion. The single GAP of V4 is closed.

**Nothing mathematical blocks YES.** Two publication-blocking editorial items
remain, both one-line, both named exactly above:

1. **Defect A** — R5 v3.1 obligations ledger lines 192–193 still carry the
   withdrawn "Simon §3 (Lidskii/spectral determinant)" attribution. Replace it
   so the note does not contradict its own Clause 2(c).
2. **Defect B** — THEOREM_G5_OFFLINE_ASSEMBLY.md must cite R5 v3.1 (+ E1 hash)
   as an explicit link between its link 4 and link 6, and its header must stop
   saying it awaits V4.

If the standard applied is V7's literal one — no false attribution sentence
anywhere in the note — then defect A is the *entire* remaining distance to a
clean YES, and it is a single-line edit with no mathematical content. I do not
consider it grounds to withhold the ruling, and I record the reasoning here so
a later reviewer can overrule it deliberately rather than by omission.
