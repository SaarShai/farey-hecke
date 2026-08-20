# Cold referee — q=8 Hardy/Hilbert operator, basis and norm binding

Date: 2026-08-20. Target: `lane_g/HARDY_HILBERT_BINDING_SOL.md` (769 lines,
commits `9b46c72` + `766c5f7`), verdict **REDUCED**, 6/8 sub-lemmas PROVED,
plus its dated B2 addendum banking `lane_g/MMS_arxiv_0912.2236.pdf`.

Referee independence: I did not write the target, did not read the author's
working context, and re-derived every load-bearing number from the tracked
code and the pinned receipts. Read-only on the work product: no file other
than this one was created or modified; nothing was committed or pushed.

```text
$ git status --porcelain research_notes/rh_goals_2026-08-14/lane_f \
                         research_notes/rh_goals_2026-08-14/lane_g/l_out
(empty)
```

Interpreter `/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0,
Arb/Acb balls, `ctx.prec = 384`). Scratch scripts live in the session
scratchpad, not in the repo.

## House verdict

**CONFIRMED at stated scope.** The gate verdict **REDUCED** is upheld. Every
load-bearing claim (a)–(g) reproduces under independent receipts, and two of
the note's own residuals (**R-B2-1**, **R-B8-1**) are additionally discharged
by this pass. **One §5 receipt line is REFUTED** (D1 below) and three grading
/ staleness defects (D2–D4) must be corrected before any downstream citation.
None of the four propagates to `rho_hat_H`, to B7, or to the verdict.

---

## 1. Per-claim verdict table

| # | claim | my independent evidence | verdict |
|---|---|---|---|
| **a** | Gate assembled faithfully from the most-caveated phrasings; nothing weaker substituted | `sed -n '108p' lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_SOL.md` → `2. Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm binding.`; `:388` of `..._REFEREE.md`, `:205` of `..._REPAIR_REFEREE.md`, `L_OUT_RECEIPT_SOL.md:9-11`, `SCHUR_SUBSTITUTION_DERIVATION_SOL.md:314-326`, `Q8_OUTPUT_TAIL_SOL.md:76-101` — all six quotes are verbatim. Gate (HH)(i)–(iv) is strictly **stronger** than (G-a)–(G-d): it adds orthonormality, the `P_N` projection property, Parseval, occurrence-for-occurrence operator identity, sup→Hilbert domination, and trace-class + determinant equality. Nothing in "operator / basis / norm" is dropped | **PASS** |
| **b** | H0 (orthonormality + Parseval for the weighted basis) PROVED | Re-derived independently. `u = (z−c)/r` is a unitary `H²(D(c,r)) → H²(𝔻)` carrying `e_m ↦ u^m`; `⟨u^m,u^k⟩ = (1/2π)∫e^{i(m−k)φ}dφ = δ_{mk}`; completeness = `H²`-convergence of Taylor partial sums. Hence `P_N` orthogonal, `‖P_N‖=‖I−P_N‖=1`, `Σ_m|X[m,k]|² = ‖Xe_k‖²`. The identification `T[m,k] = ⟨Te_{j,k},e_{i,m}⟩` is verified against the code: `q8_r3b_engine._single_block_allcols_with_s_derivative` writes `z = c_i + rho_i*u` (row index `m` = output-disc coefficient) and `base = (argument − c_j)/rho_j` (column index `k` = input-disc coefficient). Correct, and it does genuinely discharge what `SCHUR_SUBSTITUTION_DERIVATION_SOL.md:314-326` marks "**CONJECTURAL, inherited**" | **PASS** |
| **c1** | Margin semantics: `pole_margin` / `branch_cut_margin` subtract `radius_i`, i.e. are distances from the **base-disc boundary** | `q8_tb_support.py:99-107`: `pole_margin = (acb(pole)−acb(center_i)).abs_lower() − radius_i`; `branch_cut_margin = n*lam − center_i − radius_i` (neg) / `center_i + n*lam − radius_i` (pos). Confirmed — the note's whole B6a rests on this and it is right. If it had been a centre distance the argument would collapse; it is not | **PASS** |
| **c2** | Probe rule `e = min(clearance/4, 0.15 r)` ⟹ enlarged margin ≥ (3/4)·margin > 0, worst row `0.678884` | Re-ran `clearance_rows` + the `q8_e1_probe.py:38-44` rule myself. 16 rows (8 pole + 8 cut). `e_1=0.1188845008358304095034`, `e_2=0.06725122937519476771716`, `e_3=0.08117941502192954765996`; the binding term is `0.15 r_i` on **all three** discs. All 16 rows have `margin − e > 0`; worst `≥ 0.6788848240412253624964` at block `[2,1,1,False,False]` (θ₁); worst `(margin−e)/margin ≥ 0.909867…`, above the 3/4 the argument needs. Numbers reproduce the note's §5/V4 to every printed digit | **PASS** |
| **c3** | Even-q Hurwitz corollary `Re(a) ≥ 0.809619 > 0` at `n₀ = 1` | `λ·Re(a_±)` is exactly `branch_cut_margin`, so I recomputed `(margin − e_i)/λ` on the enlarged disc for all 6 tail families at both `n₀` and `n₀+4` (`n_head = 4`, `f8_source_builder.py:99-106`): 12/12 strictly positive, worst `Re(a) ≥ 0.8096194077712558908605` at block `(3,3,1,True,True)`, `n = 1`. Exactly the note's V7 | **PASS** |
| **d1** | Even-q structural deltas (eq.(32) not (34), κ=h=3 discs, 8 occurrences, one CF family, negative tails from `n₀=1`) | Verified against the banked PDF itself, not against attestations. `pdftotext -layout` p.14: `N_{1,h_q}=Z≥2, N_{1,−h_q}=Z≤−1; N_{i,i−1}={1}, N_{i,h_q}=Z≥2, N_{i,−h_q}=Z≤−1, 2≤i≤h_q`. p.21 line 607 of the extraction: "For `q = 2h_q + 2` and `κ_q = h_q`". p.8: `φ_i = f_q^i(−λ_q/2) = [[0;1^{h_q−i}]], 0 ≤ i ≤ h_q = κ_q` — a **single** family. p.21 eq.(34) for `q=2h_q+3` has `L_{2,s}` **and** `L_{1,s}` and lands tails in **two** columns (`2h_q`, `κ_q`); q=7 (`h=2, κ=5`) gives `4+3+3·4 = 19` occurrences. All deltas confirmed from source | **PASS** |
| **d2** | `\|c_3\|/r_3 = 1/2` **EXACT**, forced by `φ_3 = 0` and `a_3 = 2` | Arb: `c_3 + h_3 ∋ 0` **True**, `r_3 − 2h_3 ∋ 0` **True**, `\|c_3\|/r_3 − 1/2 ∋ 0` **True**. Also `\|c_1\|/r_1 ≤ 1.065685424949238…`, `\|c_2\|/r_2 ≤ 1.457106781186547…` — both `> 1`, so the note's §2.3 hazard is real. I confirmed the escape **from source**: MMS `N_{i,±h_q}` sends *every* tail to disc `h_q = 3`, and `q8_r2_local.py:180-185` routes the two heads through `single_block_tail` with no `q` at all, while `:206` computes `q = (abs(centers[j-1])/radii[j-1]).upper()` only on the tail branch | **PASS** |
| **d3** | `ρ̂_H ≤ 0.879829 < 1`, recomputed from the pinned receipts | Two independent routes. (i) Re-ran `tb.certify_block` on `enlarged_radii` exactly as `q8_e1_probe.py:53` does: `ρ̂_e ≤ 0.765068270705029641495394`, **string-identical** to the pinned receipt, all 8 rows identical; `1.15·ρ̂_e ≤ 0.8798285113107840877197035991`. (ii) **Bypassing the 1.15 conversion entirely**, I recomputed each block's sup with the *enlarged source* radius and the *base* target radius: max `= 0.8798285113107840877197033990 < 1`, worst block `3→2, +1, head`. Both routes agree. `ρ̂_H < 1` **confirmed** | **PASS** |
| **d4** | The 1.15 denominator conversion is the correct and only one (note's own attack item 3) | `q8_e1_probe.py:53` passes `enlarged_radii` into **both** slots of `tb.certify_block`, and `q8_tb_support.py:117` divides by `radii[j-1]` — so the pinned `rho_hat_upper_bound` is **enlarged-target-relative**. `r^e/r ≤ 1.15` holds rigorously (`enlargement = 0.15*radius.lower() ≤ 0.15*r`), in the safe direction. I additionally settled the question the note declined to answer: q=7's `F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json` is **base-target-relative** — recomputing block `5→3,+1,head` gives `sup/base r_j = 0.9152411798` vs the receipt's `0.9152411837…`, while `sup/enlarged r_j = 0.7958…`. So the q8 probe publishes a *different convention under the same field name*, the note's correction is necessary and correct, and the `0.879829 < 0.915242` comparison is **valid**, not merely indicative | **PASS (stronger than claimed)** |
| **e1** | Addendum's eq.(32) transcription is faithful to the banked PDF | `shasum -a 256 MMS_arxiv_0912.2236.pdf` → `a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`, matching the claim, `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:382` and `LAW_SECOND_AUDIT_REFEREE.md:7`. I then **re-fetched from arXiv myself**: `curl -sSL https://arxiv.org/pdf/0912.2236v2` → identical `a10020bd…`, 391565 bytes. `pdfinfo`: *The transfer operator for the Hecke triangle groups*, 30 pages. `pdftotext -layout -f 19 -l 23` p.21 prints, verbatim: `For q = 2hq + 2 we get` / `(Ls,± g)_1(z) = L∞_{2,s} g_{hq}(z) ± L∞_{−1,s} g_{hq}(z)` / `(32) (Ls,± g)_i(z) = L_{1,s} g_{i−1}(z) + L∞_{2,s} g_{hq}(z) ± L∞_{−1,s} g_{hq}(z), 2 ≤ i ≤ hq`. The addendum's transcription is exact | **PASS** |
| **e2** | The addendum's 4 consistency checks | (i) `q = 2h_q+2` → `h_q = 3`, and `κ_q = h_q` (extraction line 607) → 3 discs ✓. (ii) `2 + 3(h_q−1) = 8` ✓ (row 1 carries 2 occurrences, rows 2..3 carry 3 each). (iii) `L^∞_{−1,s}` present, and p.21 defines `L^∞_{−i,s}g(z) = Σ_{n≥i}(z−nλ_q)^{−2s}g(1/(z−nλ_q))` → `n₀ = 1` ✓, corroborated by `N_{i,−h_q}=Z_{≤−1}` ✓. (iv) one `L_{1,s}` ✓ — but see **D5**: the phrasing conflates the *operator* family with the *φ-CF word* family. Both are singular at even q, so the substance holds | **PASS** (iv phrased loosely) |
| **e3** | **Deep attack** — re-derive the checker's row consumption directly from eq.(32); do the engine's five blocks `(2,1),(3,2),(1,3),(2,3),(3,3)` faithfully represent the printed rows? | Derived from eq.(32) at `h=3` **before** reading the code: row 1 → col 3 only (two `L^∞` occurrences); row 2 → `L_{1,s}` at col 1 + `L^∞`×2 at col 3; row 3 → `L_{1,s}` at col 2 + `L^∞`×2 at col 3. Nonzero blocks = **exactly** `{(1,3),(2,1),(2,3),(3,2),(3,3)}`, 8 occurrences. `q8_r3b_engine.py:235` declares `{"A2":(2,1),"A3":(3,2),"B1":(1,3),"B2":(2,3),"B3":(3,3)}` and `:200-206` assembles `infinite(i,3,2,False)`, `infinite(i,3,1,True)` with `prefactor=signed`, `single(i,i−1,1,False)` — indices, ± sector (on `L^∞_{−1,s}` **only**, matching eq.(32)), tail starts (`+`: n₀=2, `−`: n₀=1), the rows carrying the `L^∞` tails (all three), and the disc-3 landing that pins the envelope at `q=1/2` are all faithful. Branch maps `θ_{+n}=−1/(z+nλ)`, `θ_{−n}=+1/(z−nλ)` and the squared-denominator principal weight match MMS p.21 and the convention `(n+z)^{2s} := ((n+z)²)^s` (MMS p.21 line 188). Schur reduction `C = B₃ + A₃B₂ + A₃A₂B₁` re-derived by hand from `g=Lg`: correct. **No row misidentification.** | **PASS** |
| **e4** | *(referee-added, not in the note)* Does the **production** code path carry the same 8 occurrences? | The note's V8 only compares `f8_source_builder`'s unroll to the `BLOCKS` constant. I closed two further links. **(A)** `SB.validate_against_generic_builder(s_pin, N=10, sign=1)` → max entrywise diff **`0.0`** against `zeta_cert_rosen_even.build_reduced_matrix_ball` — the engine independently cross-validated from the paper in `mpmath` at q=12 to `2.07e−30` (`EVENQ_CROSSVAL_KIMI.md`, different interpreter, `n_head=6` vs 4). **(B)** `q8_r3b_engine.build_q8_block_matrices_and_s_derivative` vs `f8_source_builder`'s 3N matrix at F1024, at the flagship pin, N=10: worst diff `2.45e−91`, and the four non-declared `(i,j)` blocks are **identically zero**. B2's chain is stronger than the note claims | **PASS** |
| **f** | B8's citations carry their assigned weight; 3 residuals honestly graded | **Simon**, Adv. Math. 24 (1977) Thm 4.2/eq.(4.2) p.258 = canonical spectral product, Thm 3.3 = trace-class-valued analyticity — roles match the independently-receipted ledger at `Q_GENERIC_SCHUR_REDUCTION_REFEREE.md:455-470`. Critically, B8 does **not** invoke Simon for *multiplicativity* (Thm 3.8) — the exact misattribution that referee caught in the q-generic note. **Grothendieck**, *Résumé…*, Ann. Inst. Fourier 4 (1952), Thm 8 — that referee fetched it (`aif.46`, sha `03834fc3…`) and recorded Thm 8 as "for `p ≤ 2/3` the determinant is genus zero and equals the eigenvalue product", i.e. **exactly** the role B8 assigns it, and *not* the 1956 multiplicativity law B8 does not need. **MMS Thm 4.10** — I read it in the banked PDF: "`L_s : B → B` is nuclear of order zero for `Re(s) > 1/2` … meromorphic … poles only at `s_k = (1−k)/2`" — verbatim as cited, and stated parity-independently. **MMS Lemma 5.1** — "`P` and `L_s` commute for all `s ∈ C\{s₁,s₂,…}`", also parity-independent. The eigenvector/Jordan-chain argument (`v = μ^{-1}L_s^H v ∈ B`, chain by induction, `B ⊂ H` conversely) is correct and gives common nonzero spectrum with algebraic multiplicity; genus-zero canonical products on both sides then coincide. **R-B8-1 is DISCHARGED by this pass** (I checked both against the even-q text, not the q=7 receipt). **R-B8-3** is trivially true (`Re s = 0.4252310423737965 > 0`, `Im s = 4.345760788321986 > 1`, half-width `1e-6`, from `F8_R3B_RECEIPT.json`) and correctly graded as un-receipted. **R-B8-2** stands, and is graded *more* conservatively than the source warrants — see D5 | **PASS** |
| **g** | LEDGER: gate not claimed CLOSED; REDUCED stands; no theorem-grade q=8 closure anywhere | Full read of all 769 lines. §Status "**REDUCED — NOT PROVED, NOT OPEN**", §6 "**REDUCED**", and an explicit non-claim list (no determinant, Fredholm, Selberg, zeta, scattering, resonance, winding, parity, automorphic, LAW). `full_tail_certified` is `false` in every `lane_g/l_out/*.json` I checked and no lane_f file was touched. `plans/wayfinder/rh-goals/MAP.md` (commit `766c5f7`) records "REDUCED", "binding UNDER REFEREE", "authority pending on (3)". No closure claim anywhere. One ambiguity, graded strict and flagged: "**NOT OPEN**" is a status the six upstream files still record as OPEN, and the note nowhere says its own grade is a *proposal* pending referee | **PASS**, with the "NOT OPEN" wording flagged |

---

## 2. Defect list

**D1 — REFUTED receipt line (§B6b and §5/V5).** The note states "the six tail
families all sit at `≤ 0.577`" (B6b) and "per-block base-relative ratios,
tails all `≤ 0.577`" (V5). **False.** Base-relative per-block ratios, both
from the pinned E1 rows × 1.15 and from my direct recomputation:

```text
1→3, +2, tail   0.571176296185      2→3, −1, tail   0.574808808402
1→3, −1, tail   0.576630576818      3→3, +2, tail   0.568886055091
2→3, +2, tail   0.569601968106      3→3, −1, tail   0.735201608898   <-- > 0.577
```

Five of six, not six of six. *Where*: `HARDY_HILBERT_BINDING_SOL.md:436-437`
and the V5 row of §5. *Why missed*: five values cluster at `~0.57` and the
outlier is the one family whose leading term sits at `n = 1` — precisely the
even-q novelty the note emphasises elsewhere; the author appears to have read
the cluster and not the maximum. *Blast radius*: **none**. `ρ̂_H` is set by the
head `3→2` at `0.879829`; B7 uses only the global `ρ̂_H`. The line must be
corrected, not the verdict.

**D2 — stale pre-addendum grading in three places.** §Status still says "No
file outside this one was created or modified" and "**No PDF was
downloaded** (see residual R-B2-1)"; §3's table still grades B2 "REDUCED (2
residuals)"; §4/B2 still says "**I did not download the PDF**"; §6 still lists
"bank the even-q source text" as remaining work. The dated addendum banks the
PDF and the same commit also touched `plans/wayfinder/rh-goals/MAP.md`. The
note therefore carries two mutually contradictory grades for B2. *Why missed*:
the addendum was appended by the orchestrator without reconciling the body.

**D3 — unstated step inside a PROVED sub-lemma (B6a).** `clearance_rows`
(`q8_tb_support.py:228-239`) evaluates the pole and cut margin **only at
`n = n₀`**, one row per block per kind — that is where the "16 rows" come
from. B6a concludes "every pole and every branch cut stays strictly outside",
which additionally needs monotonicity in `n`. It is true (`c_i ∈ (−λ/2, 0)`,
so both margins are affine and strictly increasing in `n`), and I verified it,
but a sub-lemma graded PROVED should state it.

**D4 — false etymology (§2.1).** "`F1024` is the label formed by concatenating
them" — `"10" + "4" + "2" = "1042"`, not `1024`. The receipt does carry
`radius_multipliers_exact_strings = ["10","4","2"]` and `F1024` is the
established repo label for that geometry, so this is cosmetic; but it is a
stated fact that is wrong.

**D5 — citation over-assigned, residual over-graded (B8).** B8 attributes to
"MMS Lemma 5.1" the `P`-eigenspace invariance, the `(I±P)/2` complementation
and the induced operator on `B_{κ_q}`. Lemma 5.1 states only `P L_s = L_s P`;
the rest is the unnumbered paragraph immediately following on the same page
(p.21), ending "the transfer operator `L_s` restricted to the spaces `B_±`
induces operators `L_{s,±}` on the Banach space `B_{κ_q}`", followed directly
by eq.(32). Consequence: **R-B8-2** ("the conjugacy … is asserted, not proved
here") understates the source — MMS itself performs that passage in print.
Correcting the label would *shrink* R-B8-2 to "the identification of MMS's
`D_i` with the checker's `D(c_i, a_i h_i)` discs", which is B1 and is PROVED.

**D6 — "exactly 1.15" (§B6b, §5/V4).** The code uses
`0.15 * radius.lower()`, so `r^e ≤ 1.15 r` with equality only up to the ball
width. Direction-safe (the conversion needs the upper bound), but "exactly" is
not what the code computes.

Nothing in D1–D6 is out of scope, and I found **no out-of-scope diff**:
`9b46c72` = 1 file / 730 insertions; `766c5f7` = the note (+39), `MAP.md`
(+25) and the PDF. No code, receipt or lane_f file was altered.

---

## 3. What remains OPEN after this pass

Discharged by me, beyond the note's own grade:

* **R-B2-1** — fully closed. The PDF is banked, hash-pinned, and I re-fetched
  it live from arXiv to a byte-identical SHA-256, then read eq.(32), the
  `N_{i,j}` table and `κ_q = h_q` out of it directly.
* **R-B8-1** — closed. Thm 4.10 and Lemma 5.1 read in the banked even-q text;
  both are stated parity-independently for the full operator.
* The q=7/q=8 `ρ̂` denominator-convention question (note's attack item 3, left
  "indicative only") — closed in the note's favour: q7 is base-relative, q8's
  probe is enlarged-relative, the 1.15 correction is required and correct.
* Attack item 6 (`|c_j|/r_j > 1` hazard) — closed *from source*: MMS's
  `N_{i,j}` table forbids any tail into disc 1 or 2.

Still OPEN, unchanged:

1. **R-B8-2**, in its reduced form: identifying MMS's discs `D_i` with the
   checker's `D(c_i, a_i h_i)` for the induced `L_{s,±}` on `B_3`. B1 proves
   the partition-point geometry; the *disc-radius* choice (multipliers 10,4,2)
   is a repo optimization, and MMS Lemma 4.4 only asserts *existence* of
   admissible enlarged intervals. Nobody has bound the two.
2. **R-B8-3** containment of the whole winding contour in `Ω*` — the pin box
   is inside, the contour is the separately-open continuous-contour gate.
3. **B6b receipt grade.** `Q8_E1_ENLARGED_PROBE_RECEIPT.json` is
   `status: "DIAGNOSTIC_ONLY"`, no `verdict`, no `immutable_inputs`, no `η`
   field, per-source-disc not per-block, and its own `scope` string reads
   "OPEN: full E1 weight holomorphy, contour, R2/R3, Ks and MMS linkage remain
   open". `Q8_GENERIC_CERTIFICATION_SOL.md:188` confirms "**E1 enlarged-disc
   contraction — OPEN.** No q=8 E1 receipt has been made." The q=7 analogue
   `F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json` carries `verdict`,
   `eta_max_upper_bound = 20/23`, and a per-block
   `remaining_pole_cut_clearance_lower_bound`; the q=8 probe carries none of
   these. The **mathematics** of B6a/B6b is proved from certified interval
   data — I reproduced all of it — but the **artifact** is not receipt-grade.
   Mechanical to fix, and it should be fixed before the gate is cited.
4. **Threshold inconsistency, confirmed.** `q8_candidate_tb_cert.py` never
   overrides `q8_tb_support.THRESHOLD` (default `arb("0.70")`, `:17-18`),
   while it writes `certification_verdict = "PASS_RHO_LT_0.99"` (`:79`). So
   `Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` gates its per-term
   `pass` / `ratio_less_than_0_70` flags at 0.70 and its headline verdict at
   0.99. Conservative direction (`ρ_* ≤ 0.696590428020637535884545 < 0.70`),
   so harmless — but two numbers in one hash-pinned receipt are gated
   differently. Re-emit.
5. Everything the note lists as not claimed: omitted-output tail,
   `recorded_tail_checks_pass` (independently false), `K_s` nonvanishing and
   word/lattice identification, common meromorphic continuation and Selberg
   factorization, the four-edge winding, and the `N=104` vs `N≥262` pin
   decision. `full_tail_certified` remains `false`. Nothing here flips it.
6. **Wording**, not mathematics: the six upstream files still record this gate
   as OPEN. Until they are updated, "REDUCED — NOT PROVED, **NOT OPEN**"
   should read as this note's proposed grade, now referee-supported, rather
   than as an accomplished ledger state.

---

## 4. Verdict

**CONFIRMED** at stated scope.

The gate verdict **REDUCED** is upheld. H0 (b) is genuinely proved and
genuinely discharges a hypothesis the entire L-OUT norm chain had inherited as
CONJECTURAL. Enlarged-disc weight holomorphy (c) and the even-q Hurwitz
corollary at `n₀ = 1` are proved, and I reproduced every certified number.
The even-q operator identification (d, e) is now bound to a hash-pinned,
independently re-fetched printed source, and the checker's five production
blocks are a faithful, occurrence-for-occurrence, sector-for-sector,
`n₀`-for-`n₀` realization of MMS eq.(32) — **no row misidentification, the
note's own named failure mode**. `ρ̂_H ≤ 0.879829 < 1` reproduces by two
independent routes, one of which bypasses the note's 1.15 conversion entirely.
B8's four printed results each carry exactly the weight assigned, and B8
avoids the multiplicativity misattribution a previous cold referee caught
elsewhere in this lane.

The gate is **not closed** and this note does not close it. Corrections D1–D4
are mandatory before citation; D1 is a false certified line and must not
survive into any downstream note. The remaining distance to a q=8 analogue of
the referee-CONFIRMED q=7 Link 4b is item 1 (MMS-disc ↔ checker-disc binding,
mathematical) and item 3 (a gated, hash-bound, η-bearing E1 receipt,
mechanical).

---

**READY FOR JUDGING**
