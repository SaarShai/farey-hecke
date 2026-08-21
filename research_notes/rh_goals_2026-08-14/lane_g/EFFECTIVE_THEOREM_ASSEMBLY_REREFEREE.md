# Cold re-referee — EFFECTIVE_THEOREM_ASSEMBLY_SOL.md (attacks 1b, 3, 5)

**Date:** 2026-08-20
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/EFFECTIVE_THEOREM_ASSEMBLY_SOL.md`
(working tree, carrying the D1-D5 dated correction block; committed at `848bf17`)
**First referee:** `EFFECTIVE_THEOREM_ASSEMBLY_REFEREE.md` (GAPS NOT REFUTED).
Its attacks 2, 4, 6 are complete and were NOT repeated.
**Scope of this pass:** the three attacks the first referee could not run
(1b Hejhal (7.22) scope; 3 hypothesis-table completeness; 5 the (RATE-A)
grade-conflict adjudication) plus fidelity of the D1-D5 block.
**Legs:** `pdftotext`/`pdftoppm` (poppler) + page-image read;
`/Users/za/.venvs/farey-rh/bin/python` (python-flint/Arb, dps=60); `git`.
**Edits made to the repo: NONE.**

---

## Attack 1b — Hejhal (7.22): page, verbatim text, hypothesis drift

**Path correction.** The excerpt is NOT at
`lane_g/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf` (no such file). It is at
`research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf`,
33 pages, PDF page k = printed page 567+k (verified page-by-page).

**PAGE: (7.22) is on printed page 577** (PDF page 10). Receipt: per-page
`pdftotext` shows `(7.22)` on PDF page 10 and `(7.23)`/`(7.24)` on PDF page 11,
whose footer number is `578`.

**Verbatim (7.22), read off the rendered page image** (the PDF text layer is
OCR-degraded and drops the formula entirely):

> **THEOREM 7.11.** Given t_o ∈ ℝ and 0 < δ < 1. The rectangle
> [½, ½+δ] × [t_o−δ, t_o+δ] must contain ZEROS of φ_N(s) whenever N is
> sufficiently large. It is understood here that N < ∞ .
>
> *Proof.* Take 0 < δ < ⅕t_o WLOG and suppose that the theorem is false. We can
> THEN select a subsequence 𝒥 such that:
>
>   φ_N(s) ≠ 0 on [½, ½+δ] × [t_o−δ, t_o+δ]  whenever N ∈ 𝒥 .
>
> Recall that |φ_N(½+it)| ≡ 1 for t ∈ ℝ. By the Schwarz reflection principle,
> φ_N(s) extends holomorphically to [½−δ, ½+δ] × [t_o−δ, t_o+δ]. In fact:
>
> **(7.22)   φ_N(½ − h + it) · conj( φ_N(½ + h + it) )  ≡  1
>            for 0 ≤ h ≤ δ  and  |t − t_o| ≤ δ .**
>
> In this equation N ∈ 𝒥 .

**Finding 1b-A — inside the excerpt: PASS.** p.577 ∈ [568, 600].

**Finding 1b-B — right family, no transplant: PASS.** `LAW_HEJHAL_S7_EXTRACT.md:19-24`
records that Hejhal's §7 `φ_N` is the scattering coefficient of the *Hecke*
group `G_N = ⟨E, S^λ⟩`, `λ = 2cos(π/N)`, `N ≥ 3`. So Hejhal's `φ_N` **is** the
project's `φ_q`. There is no deformation-family transplant.

**Finding 1b-C — the algebraic form matches the assembly's use exactly: PASS.**
Put `s = ½ + h + it`; then `½ − h + it = 1 − conj(s)`, so (7.22) reads
`φ(1 − conj s) · conj(φ(s)) ≡ 1`. A zero of `φ_q` at `s_q` kills the second
factor, forcing a pole of the first at `1 − conj(s_q)`, of the same order.
That is *precisely* §2(c). The Re-range is also right:
`Re s_q ∈ [5/8, 7/8] ⇒ Re(1 − conj s_q) ∈ [1/8, 3/8] < 1/2`. ✅
`R3_TRANSPORT_EXECUTION_SOL.md:92-93` uses it identically ("Hejhal's exact
reflection identity (7.22) then gives a pole at `1-conj(s_q)`").

**Finding 1b-D — HYPOTHESIS DRIFT: FAIL.** As *printed*, (7.22) is not a
free-standing identity. It carries three hypotheses the assembly states none of:

| printed hypothesis | assembly's situation |
|---|---|
| `N ∈ 𝒥`, the subsequence chosen so that **φ_N ≠ 0 on [½,½+δ]×[t₀±δ]** (contradiction hypothesis of Thm 7.11's proof) | the assembly invokes (7.22) **exactly at a point `s_q` where `φ_q(s_q)=0`** — the direct negation of the standing hypothesis. `LAW_HEJHAL_S7_EXTRACT.md:67-70` records this scoping correctly ("1. [E] Assume φ_N ≠ 0 on R_δ ... 2. ... with the functional identity (7.22)"); the assembly drops it. |
| local rectangle `0 ≤ h ≤ δ`, `|t−t₀| ≤ δ`, with `0<δ<1` **and** `δ < t₀/5` | satisfiable: `D̄_z` needs `h ≤ 3/8`, `|t−t₀| ≤ 1/8`; `δ = 3/8` obeys `3/8<1` and `3/8 < γ₁/10 = 1.4135`. **This part is fine but is nowhere checked in the assembly or in R3.** |
| the word "extends **holomorphically**" is what the no-zero hypothesis buys | at `s_q` the reflected extension is *meromorphic*, not holomorphic |

The **mathematical content** the assembly needs is true and standard (the
scattering functional equation `φ(s)φ(1−s) ≡ 1` together with `φ(s̄)=conj φ(s)`
holds as a meromorphic identity on all of ℂ; Hejhal's own **Corollary 7.12**,
printed p.579, converts 7.11's zeros into poles with "Proof. Trivial." from
`φφ̄ ≡ 1`). So this is a **citation defect, not a refutation**: (7.22) as
printed is the wrong pointer for a use at a zero. The repair is to cite the
unconditional functional equation / Cor. 7.12's mechanism and to state `δ=3/8`.

**Finding 1b-E — D4 is NOT repaired.** The first referee required "the assembly
should print the page of (7.22) and assert it lies inside the in-repo excerpt".
The D4 bullet only *defers* ("must not be cited until the page is printed").
The page is now supplied here: **p. 577**.

**Attack 1b verdict: PARTIAL PASS — page confirmed in range and the algebra is
exactly right; hypothesis drift on the printed scoping is a NEW confirmed defect.**

---

## Attack 3 — hypothesis-table completeness (ALL rows, no sampling)

Every quote below was re-fetched at its cited `file:line` with a fresh
line-indexed read. `✓` = verbatim and at the cited lines.

### (H-RATE) and its 8 sub-inputs

| row | cite | result |
|---|---|---|
| (H-RATE) headline | `BOUNDARY_ALPHA_THEOREM_SOL.md:728-734` | ✓ verbatim (source runs 728-734) |
| (H-RATE) headline | `AM_REFEREE.md:7` | ✓ verbatim, exact line |
| conflict row 1 | `HOLOMORPHY_GATE_SOL.md:579` | ✓ verbatim, exact line |
| conflict row 2 | `R5_MONOTONICITY_GATE_SOL.md` corrected bottom line | ✓ verbatim @ `:1018-1020` |
| `(FW)` | `FW_REFEREE.md:5` | ✓ exact |
| `(DH_{2,4})` | `TWOMARK_REFEREE.md:5` | ✓ exact |
| M1 localization triple | `M1_LOCALIZATION_TRIPLE_REFEREE.md:12` | ✓ exact |
| endpoint comparison `x_X ≤ y_X` | `BOUNDARY_ALPHA_THEOREM_SOL.md:311-313` | ✓ exact |
| **Lemma 3.1** | `BOUNDARY_ALPHA_THEOREM_SOL.md:333` | **✗ MISCITE.** `:333` is the heading `### 3.2 Theta-endpoint derivative lemma`. `**Lemma 3.1 — PROVED.**` is at **`:335`**. |
| Lemma 3.2 | `BOUNDARY_ALPHA_THEOREM_SOL.md:405` | ✓ exact |
| Lemma 3.2 bridge | `AM_REFEREE.md:405` | ✓ (`**Final verdict: CONFIRMED.**  The atom-moment bridge closes reason 1 of RATE_A_REFEREE.md:14-17`) |
| `sup_{K_15}|M(s)| < 2.775` | `M3_UNIFORMITY_EXECUTION_SOL.md:275` | ✓ exact |
| standalone N1-RATE | `BOUNDARY_ALPHA_THEOREM_SOL.md:681` / `:282-283` | ✓ both exact |

Grade check: the assembly grades each sub-input at the source's most-caveated
phrasing. Independently confirmed — including the honest carry of
`Canonical N1-RATE ... CONJECTURAL` even though it is not consumed.

### (H-HOL)

- `HOLOMORPHY_GATE_SOL.md:373-379` ✓ verbatim (ellipsis marked).
- `HOLOMORPHY_GATE_SOL.md:256-257` ✓ exact.
- attached negative `φ_q ≠ 0 ... FALSE` — ✓ verbatim, at `:572` (assembly cites
  only "§6", acceptable).
- `:230` NOT EVIDENCE ✓ exact.
- **Soft flag (not a fail):** `:258-259` continues "*the reflected `D_0` piece
  follows under `H_0(q)`*". §2(c)'s conclusion lands in `Re < 1/2` (the
  reflected side). The pole is a *conclusion*, not a premise, so nothing breaks;
  but "already discharged for the domains used here" quietly excludes `D_0`.

### (H-GEOM)

- `R3_TRANSPORT_EXECUTION_SOL.md:60-65` — ✓ verbatim; the display actually spans
  `:61-66` (off-by-one at both ends, content correct).
- ledger `:243-245` ✓ verbatim (`m_z` @244, `nu_z` @245).
- **✗ MISCITE.** The parenthetical "(as quoted in
  `R5_ACTIVATION_CLOSURE_REFEREE.md:244-245`)" is wrong.
  `R5_ACTIVATION_CLOSURE_REFEREE.md:244-245` is an unrelated `rg`/transcript
  fragment about Route-B vs A0 thresholds. The rows *are* quoted in that
  referee — at **its own lines 41-43**, which display the R3 file's line
  numbers 244/245. The assembly has conflated quoted-file line numbers with
  quoting-file line numbers.

### (H-SIDE)

- `R5_ACTIVATION_CLOSURE_SOL.md:116-118` ✓ verbatim, exact.
- `R5_ACTIVATION_CLOSURE_REFEREE.md:58-62` ✓ verbatim; quote actually begins on
  `:57`. Off-by-one at the start.
- historical `CONJECTURAL / MISSING family-uniformly` row @ `R3_TRANSPORT_EXECUTION_SOL.md:250` ✓ exact.
- side hypothesis `0 < E_R ≤ K_+` discharge @ `BOUNDARY_ALPHA_THEOREM_SOL.md:615-623` ✓ exact.
- Grade "CONFIRMED-conditional source input" matches the most-caveated phrasing. ✓

### (H-C4)

- `BOUNDARY_ALPHA_THEOREM_SOL.md:812-830` ✓ verbatim (content spans 813-829).
- `CR_REDUCTION_V2_REFEREE.md:44` ✓ exact.
- `CR_REDUCTION_V2_SOL.md:341` ✓ exact ("`C_R''` is an *unbanked candidate*").
- **Flag.** The quoted narrow re-referee `"RE-REFEREE: CONFIRMED — promotion
  unblocked"` has **no referee file anywhere in the repo**. Repo-wide grep
  finds it only in `BOUNDARY_ALPHA_THEOREM_SOL.md:853-854`, `MAP.md:1337`, and
  the assembly itself; `BOUNDARY_ALPHA` attributes it to an "orchestrating
  session, 2026-08-20". The assembly presents it as referee evidence without
  disclosing it is a session utterance, not a banked document.

### (H-ROUTE)

- `R5_ACTIVATION_CLOSURE_SOL.md:56-60` ✓ verbatim.
- `R5_MONOTONICITY_GATE_SOL.md` D3 correction ✓ verbatim @ `:639-648`.
- Independently confirmed the note honours it: the §4.1 program consumes only
  `K_+`, `m_z`, `nu_z`; the `K_F=109` pairing appears only as an excluded
  diagnostic. ✓

### The six "NOT assumed" rows — all six checked

| row | cite | result |
|---|---|---|
| finite `φ_q` evaluator + winding block | `KF_WALL_ATTACK_SOL.md:680` | ✓ exact |
| full all-q R5 closure | `R5_ACTIVATION_CLOSURE_REFEREE.md:342` | ✓ exact |
| effective analytic `q_0` + finite base | `HOLOMORPHY_GATE_SOL.md:580` | ✓ exact |
| remainder of `q_monotone` | `R5_MONOTONICITY_GATE_SOL.md` D-corr §item 3 | ✓ verbatim @ `:1046-1048`; the "all envelopes" definition ✓ @ `R3_R5_ASSEMBLY_PLAN_SOL.md:678-679` |
| determinant/winding boxes as evidence | `HOLOMORPHY_GATE_SOL.md:230` | ✓ exact |
| machine verification / Lean | `BOUNDARY_ALPHA_THEOREM_SOL.md:737-738` | ✓ exact |

### The §5(c) LAW quotes

- LAW statement blockquote — ✓ verbatim against `LAW_SECOND_AUDIT_REFEREE.md:50`.
- **✗ MISQUOTE.** The assembly prints `"The chain is unconditional on printed
  literature, at the generality **needed**"`. The source (`:50`) reads
  `"at the generality **used**"`. A one-word substitution inside a quotation the
  note frames as exact source phrasing.
- `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:5-6` self-grade ✓ exact.
- §5(b) item 1 receipt independently re-run: `git ls-tree -r HEAD -- engine/certify`
  returns **empty**. ✓ PASS.
- §5(b) item 4 quote ✓ verbatim @ `R5_MONOTONICITY_GATE_SOL.md:1023-1024`.
- other §5/§4.5 cites re-checked and correct: `R5_ACTIVATION_CLOSURE_SOL.md:483-488` ✓,
  `:490-493` ✓, `:360-368` ✓, `:377-382` ✓ (and `αν = 6/5·0.1552 = 0.18624 = 582/3125` ✓).
- **✗ MISCITE.** "the theorem uses **no simplicity assumption** on `ρ_1`
  (`R3_TRANSPORT_EXECUTION_SOL.md:110`)". `:110` is about `Γ`/`ζ` factors being
  nonzero. The sentence "No simplicity assumption on `rho_1` is used." is at **`:118`**.

### Walking §2's proof chain myself — consumed-but-unlisted

| step | assumptions actually used | listed? |
|---|---|---|
| (a) | (H-RATE) on `Γ_R^A`, (H-C4) | yes |
| (b) two-constants | `K_+` (H-SIDE); `ν_z` (H-GEOM); boundedness+holomorphy of `F_q` on `Ω̄` (H-HOL, incl. `φ_∞` pole-freeness — I verified `s=1`, `4^s=1` (Im ≈ 4.53, 9.06) and `ζ(2s)` zeros all lie outside `Ω`); the **theorem application itself** | yes, **only after** D3's (H-TRANS) |
| (c) Rouché | `m_z` (H-GEOM), strictness, `φ_∞(z_0)=0` via `ζ(2z_0−1)=ζ(ρ_1)=0` + `R3:109-112` | yes |
| (c) reflection | **Hejhal (7.22): unitarity `|φ_q(½+it)| ≡ 1`, meromorphic continuation across the critical line, and same-order pole transfer** | **NO — CONSUMED-BUT-UNLISTED** |

**NEW GAP (H-REFL).** (H-TRANS) as worded covers only "the two-constants/Rouché
transport implication". The reflection identity is a separate analytic input
with its own hypotheses (see 1b-D) and appears in **no** row of §3. §3's
promise "Nothing is omitted" is therefore *still* false after D3.

### Shape / staleness defects of the deliverable

1. **§2 still says "Assume the six named gates"** (`:89`) and lists six. With
   (H-TRANS) added by D3 there are **seven**; with (H-REFL), eight. The theorem
   statement and the D3 repair are mutually inconsistent as printed.
2. **§3's header sentence "Nothing is omitted." (`:153`) was left unedited**
   even though D3 concedes it was false.
3. **(H-TRANS) is in an appendix, not in the §3 table.** A reader of §3 alone
   still sees a table that claims completeness and omits it.
4. **The §1.1 hash receipt is now stale in exactly one entry.** I re-ran the
   note's own `shasum` command: 14 of 15 hashes still match; `BOUNDARY_ALPHA_THEOREM_SOL.md`
   is now `58ac377f…`, not the recorded `5a8d0bcc…`. Cause: commit `848bf17`
   ("Drain post-lockout queue: V3 promoted, assembly repaired") appended §10 to
   that file **in the same commit that appended D1-D5 to this note**. The note
   was edited without refreshing or disclosing that its source-state receipt moved.
5. **§4.4's constant table is stale, and its claim "the smallest is quoted" is
   now FALSE.** `BOUNDARY_ALPHA_THEOREM_SOL.md` §10 (2026-08-20) banks
   `C_4''' = 65459394456774532`, `C_R''' = 541656022363559883954520`, and
   `CR_REDUCTION_V3_REFEREE.md` §0/§Final grades it **CONFIRMED** with
   `q_A0''' = 2810199067910634377586449487575862960`. I reproduced that integer
   independently (Arb, dps=60) from the assembly's own Stage-2 formula:

   ```
   1/(alpha nu_z)         = 5.36941580756013745704467353951890034364...
   (1-nu_z)/(alpha nu_z)  = 4.53608247422680412371134020618556701031...
   T_0 = 38.3855535814978294420003556268   e^T0 = 46841857142466893.0558...
   nu*dT0/dnu = -42.35403186049595954   alpha*dT0/dalpha = -38.38555358149782944
   C_R''  -> q_A0  = 11761546420922598622910053339543258496   log10 = 37.07046442700542...
             alpha*dlogQ/dalpha = -85.35789877998874367
   C_R''' -> q_A0  = 2810199067910634377586449487575862960    log10 = 36.44873708539722849
   ```

   The boxed `Q_0 = 1.176e37` is a factor **4.19 larger** than the smallest
   referee-CONFIRMED value now available (`2.810e36`).

**Attack 3 verdict: FAIL.** Four miscites/misquotes, one new consumed-but-unlisted
assumption (H-REFL), one still-false completeness claim, one arity contradiction
(six vs seven gates), one stale hash receipt, one stale-and-now-false §4.4 claim.

---

## Attack 5 — ADJUDICATION of the (RATE-A) grade conflict

All four sources read in full: `AM_REFEREE.md`, `RATE_A_REFEREE.md`,
`BOUNDARY_ALPHA_THEOREM_SOL.md` §7-§10, `HOLOMORPHY_GATE_SOL.md`,
`R5_MONOTONICITY_GATE_SOL.md` (+ its referee).

### The promotion trail, re-derived

1. `RATE_A_REFEREE.md:5` — **primary verdict GAPS**, with exactly **two** stated
   reasons (`:13-21`): (1) the required `Σ_{x≤Y}(1+A²)` atom moment is not the
   literal `(DH_{2,4})` statement; (2) the fresh `φ_q` checks are not certified
   Arb enclosures. Reason (2) is a *rigor-tier* caveat, not a hole in the
   analytic argument; `:388-392` states "I could not refute RATE-A's analytic
   inequality … Subject to accepting the two-mark/Ford paper proof, the exponent
   6/5, activation 12, and explicit constant … are confirmed."
2. `AM_REFEREE.md:7` CONFIRMED; `:405-407` — "The atom-moment bridge **closes
   reason 1 of `RATE_A_REFEREE.md:14-17`**. The result remains a paper theorem…".
   Reason (1) is discharged; reason (2) survives *as the label* "paper-level,
   not machine-verified".
3. `BOUNDARY_ALPHA_THEOREM_SOL.md:728-740` — promotion, with its scope printed
   in the same breath: "**on the stated balanced/matched boundary Γ_R^A**, with
   exponent 6/5, activation q_RATE=12 … **No whole-tail monotonicity, finite
   base block, all-gates activation, or final q_0 status is promoted here.**"

### RULING: DIFFERENT SCOPES. Both grades are correct. Neither is stale.

The first referee's untested prior is **confirmed with receipts**.

**Scope 1 — `(RATE-A)` as a boundary-rate theorem.** `E_R(q) = sup_{Γ_R^A}|φ_q − φ_∞| ≤ C_R q^{-6/5}`
for `q ≥ 12`, on the *single fixed right edge* `Γ_R^A = {11/10 + it : |t−t₀| ≤ 1/2}`,
conditional on the two-mark/Ford paper inputs, **not machine-verified**.
→ **CONFIRMED at paper level. CORRECT.** (`AM_REFEREE.md:7`; `BOUNDARY_ALPHA:728-734`.)

**Scope 2 — positive *full-boundary* RATE together with *whole-tail /
family-uniform N-independent* monotonicity, as consumed downstream by R5/DH2
activation.** → **GENUINELY OPEN. ALSO CORRECT.**

Decisive receipt, and it already exists in the lane: **`R5_MONOTONICITY_GATE_SOL.md:847-863`
(referee correction D9)**, echoed at `R5_MONOTONICITY_GATE_REFEREE.md:460-471`:

> The `HOLOMORPHY_GATE_SOL.md:579` row reads *"Positive full-boundary RATE
> **and** whole-tail monotonicity | **GENUINELY OPEN**"*. That is a
> **conjunction**, and its stated reason is the first conjunct (`alpha=0`). A
> conjunction with an open conjunct is open, so the row is **correct as written,
> not stale**.

Two independent scope separators, both verified by me:

- **"full-boundary" ≠ `Γ_R^A`.** `Γ_R^A` is one of four sides of `∂Ω`; the other
  three are covered *not* by RATE but by `K_+ = 117` (H-SIDE). A "positive
  full-boundary RATE" is a strictly larger object than RATE-A. Assembly §1.2 /
  `R3_TRANSPORT_EXECUTION_SOL.md:22-52` confirm the four-sided geometry.
- **"rigorous campaign" ≠ "paper level".** `HOLOMORPHY_GATE_SOL.md:579`'s reason
  is "Current **rigorous** campaign proves only α=0". `BOUNDARY_ALPHA:728` promotes
  at "**paper level**", and `R5_MONOTONICITY_GATE_SOL.md:6-8` declares its own
  scope "paper-level. No … machine verification is claimed here". No source
  anywhere claims a rigorous/certified α>0. The two statements are compatible.

**On `R5_MONOTONICITY_GATE_SOL.md:1018-1020`** (the harder one, since it postdates
the promotion and names `(RATE-A)` by label):

> `(RATE-A)` with `alpha>0`. **Unchanged by this note**; the rigorous campaign
> still proves only `alpha=0`. This remains the single standing blocker for
> every conditional statement above.

Three findings: (i) "Unchanged by this note" is a **non-interference disclaimer,
not an adjudication** — the note declares it did not touch the object; (ii) the
reason clause is a *verbatim carry-forward* of `HOLOMORPHY:579`'s wording (that
string is quoted at `R5_MONOTONICITY_GATE_SOL.md:78`), so it inherits :579's
full-boundary scope; (iii) the object this note actually consumes is `(G2)`'s
hypothesis — `R5_MONOTONICITY_GATE_SOL.md:18` grades (G2) "PROVED here, §3,
conditional on `alpha>0` **and N-independent `K_+, K_F, nu_seed, omega_*`**",
i.e. a *family-uniform, N-independent, two-stage route-H* rate. That is Scope 2,
not Scope 1.

**Consequence for the assembly.** §2(a) consumes `sup_{Γ_R^A}` only — **Scope 1**.
It consumes neither full-boundary RATE (the other sides go through `K_+`) nor
family-uniform whole-tail monotonicity (§4.5 keeps `q_monotone` symbolic).
Therefore the assembly's `(H-RATE)` gate is **CONFIRMED-conditional at paper
level**, and the two OPEN rows do **not** bear on it. The assembly's §3 posture
("I do not adjudicate this conflict") is *safe but over-cautious*: it invites
the reader to believe the theorem might be conditional-on-a-conjecture, when the
receipts show the OPEN gradings target a strictly larger object. Not a defect —
an available strengthening.

### Specified repair text

**Target file: `R5_MONOTONICITY_GATE_SOL.md`** — the only file whose wording is
genuinely under-scoped *and* postdates the promotion. (`HOLOMORPHY_GATE_SOL.md:579`
needs **no** edit; it is already exonerated as a correct conjunction by that
note's own D9.) Append-only, at the end of the dated correction sequence:

> ### Correction (2026-08-20, re-referee D12): the bare label `(RATE-A)` in the OPEN list is under-scoped
>
> Defective sentence (§ "OPEN", verbatim):
>
> > - `(RATE-A)` with `alpha>0`. Unchanged by this note; the rigorous campaign
> >   still proves only `alpha=0`. This remains the single standing blocker for
> >   every conditional statement above.
>
> **Corrected statement.**
>
> ```text
> - Positive FULL-BOUNDARY RATE, and family-uniform N-independent whole-tail
>   monotonicity -- i.e. `(RATE-A) with alpha>0` in the form consumed by (G2)
>   and by the R5/DH2 activation, which additionally requires N-independent
>   K_+, K_F, nu_seed, omega_*. Unchanged by this note; no RIGOROUS
>   (machine-certified) campaign proves alpha>0. This remains the single
>   standing blocker for the conditional statements above.
>
>   NOT open, and not what this row grades: `(RATE-A)` restricted to the single
>   matched boundary Gamma_R^A with exponent 6/5 and activation q_RATE=12. That
>   statement is CONFIRMED AT PAPER LEVEL (BOUNDARY_ALPHA_THEOREM_SOL.md:728-734;
>   AM_REFEREE.md:7, which closes reason 1 of RATE_A_REFEREE.md:14-17). The two
>   gradings are different scopes, not a conflict; cf. this note's own D9, which
>   rules HOLOMORPHY_GATE_SOL.md:579 "correct as written, not stale" because it
>   is a conjunction whose first conjunct is the FULL-boundary rate.
> ```
>
> No ledger promotion is licensed by this correction; it narrows a label, it
> does not upgrade a status.

**Secondary (optional, target `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md` §3):** replace
"**Status: CONFIRMED-conditional (paper level), WITH A LIVE LEDGER CONFLICT.**"
with "**Status: CONFIRMED-conditional (paper level).** The two banked OPEN rows
(`HOLOMORPHY_GATE_SOL.md:579`, `R5_MONOTONICITY_GATE_SOL.md:1018-1020`) grade a
*larger* object — positive **full-boundary** RATE plus family-uniform whole-tail
monotonicity — and do not bear on the `Γ_R^A` statement this theorem consumes
(re-referee attack 5, 2026-08-20)."

**Attack 5 verdict: ADJUDICATED. Both gradings correct at their own scopes;
the conflict is an equivocation on the label `(RATE-A)`.**

---

## Fidelity of the D1-D5 correction block (side-by-side)

| # | referee's required text | block's text | fidelity |
|---|---|---|---|
| D1 | "**Repair text:** replace `1/(αν_z)≈4.47` with `1/(αν_z)=5.3694…` (and … `(1−ν_z)/(αν_z)=4.5357…`)" | "…the true value is 1/(alpha nu_z) = 5.36941580756…; the neighbouring K_+ coefficient is (1-nu_z)/(alpha nu_z) = **4.5357**…" | **PARTIAL + NEW DEFECT.** (i) §5(b) `:604` still literally reads `1/(\alpha\nu_z)\approx4.47` — the body was never corrected, only annotated. (ii) **`4.5357` is itself wrong.** My Arb leg: `(1−0.1552)/(1.2·0.1552) = 0.8448/0.18624 = 4.53608247422680412…`. The block (inheriting the first referee's slip) prints `4.5357`, off in the 4th decimal. |
| D2 | "ν_z is the most elastic parameter of the C_R-independent floor e^{T₀} (elasticity −42.4 vs −38.4 for α). For the full Q₀ at C_R″, α is the most elastic parameter (elasticity −85.4) …" | same content, same three numbers | **FAITHFUL.** All three independently reproduced: `ν·∂T₀/∂ν = −42.354`, `α·∂T₀/∂α = −38.386`, `α·∂logQ₀/∂α = −85.358`. |
| D3 | new §3 row with "**Status: PAPER-LEVEL, UNREFEREED** — no `R3_TRANSPORT_EXECUTION_REFEREE.md` exists in lane G; the source's own header reads …"; discharge "(boundedness of F_q on Ω̄, the ω(s,Γ_R;Ω) interval cover, and the Rouché strictness on ∂D_z)" | block says "**adopted verbatim from the referee**", then prints a paraphrase: drops the "no referee file exists" clause from the Status line, and rewrites "on Ω̄"→"on the closed rectangle", "on ∂D_z"→"on the disc boundary" | **SUBSTANTIVELY FAITHFUL, but the word "verbatim" is false.** Content is equivalent. Independently verified: no `R3_TRANSPORT_EXECUTION_REFEREE.md` exists in lane G (`ls`), and `R3_TRANSPORT_EXECUTION_SOL.md:7-8` does read "**CONDITIONAL TRANSPORT THEOREM PROVED; CURRENT UNCONDITIONAL R3 REMAINS A GAP.**" ✓ |
| D4 | "the assembly should **print the page** of (7.22) and assert it lies inside the in-repo excerpt pp. 568-600" | "the assembly must not be cited until the page is printed and asserted to lie inside…" | **NOT REPAIRED — deferred.** The page is supplied by this pass: **p. 577**. |
| D5 | "it should say `B = K₊ ⟹ N_monotone-bound ≡ q_side″ by construction`" | "the q_side'' agreement is an algebraic identity (route-H B = K_+ makes the two closed forms the same function), not an empirical corroboration" | **FAITHFUL.** |

Also: the block leaves the §4.3 body text ("the same phenomenon … now
reproduced at C_R''") unedited, consistent with append-only house style.

---

## Combined defect list (both referee passes)

**Carried from referee 1 (unrepaired in body):**
1. `1/(αν_z) ≈ 4.47` still printed at `:604` · refuted number, annotated only.
2. "The binding parameter is ν_z" still unqualified at `:603-606` · annotated only.

**New in this pass:**
3. **D1's own replacement number `4.5357` is wrong** · correction block · true
   value `4.53608247…`. A refuted number *introduced by the repair*.
4. **Hejhal (7.22) hypothesis drift** · §2(c), `R3:92-93` · printed (7.22) is
   scoped to `N ∈ 𝒥` under a **zero-free** rectangle and to `0≤h≤δ, |t−t₀|≤δ`;
   the assembly invokes it exactly at a zero. Repair: cite the unconditional
   functional equation / Hejhal Cor. 7.12 (p.579) and state `δ = 3/8`.
   (Content is true; the pointer is wrong.)
5. **(H-REFL) consumed-but-unlisted** · §3 · the reflection identity's own
   hypotheses (unitarity on the critical line, meromorphic continuation,
   same-order transfer) appear in no gate row. "Nothing is omitted" is *still*
   false after D3.
6. **§2 says "six named gates"; D3 makes seven** · `:89-91` vs correction block ·
   the theorem statement and its own repair are inconsistent.
7. **(H-TRANS) placed in an appendix, not in the §3 table** · a §3-only reader
   still sees a table claiming completeness.
8. **Four cite errors** · `BOUNDARY_ALPHA:333` (Lemma 3.1 is at `:335`);
   `R5_ACTIVATION_CLOSURE_REFEREE.md:244-245` (quoted-file line numbers mistaken
   for quoting-file line numbers); `R3_TRANSPORT_EXECUTION_SOL.md:110` (the
   simplicity sentence is at `:118`); `LAW_SECOND_AUDIT_REFEREE.md:50` misquoted
   ("generality **needed**" for "generality **used**").
9. **§1.1 hash receipt stale** · `BOUNDARY_ALPHA_THEOREM_SOL.md` is now
   `58ac377f…`, not the recorded `5a8d0bcc…`; the note was edited in the same
   commit (`848bf17`) that moved that source, without refreshing the receipt.
10. **§4.4 "the smallest is quoted" is now FALSE** · a fourth, referee-CONFIRMED
    constant `C_R''' = 541656022363559883954520` (`BOUNDARY_ALPHA` §10 /
    `CR_REDUCTION_V3_REFEREE.md`) gives `Q_0''' = 2810199067910634377586449487575862960`
    (`log₁₀ = 36.4487`), **4.19× smaller** than the boxed value. Reproduced
    independently here.
11. **Undisclosed non-document evidence** · the `"RE-REFEREE: CONFIRMED —
    promotion unblocked"` quote supporting (H-C4) exists in no referee file; it
    is an orchestrating-session utterance (per `BOUNDARY_ALPHA:853-854`).

**Adjudicated (not a defect):** the `(RATE-A)` "live ledger conflict" is a scope
equivocation. Both gradings are correct; the assembly's own gate is Scope 1 and
is CONFIRMED at paper level.

---

## Combined verdict given both referee passes

# **GAPS NOT REFUTED**

Nothing in the theorem was refuted. On the contrary, this pass *strengthens* the
note: attack 5 resolves the (H-RATE) conflict in the assembly's favour, attack
1b confirms the Hejhal citation is in-range, in the right function family, and
algebraically exactly right, and 18 of ~20 hypothesis-table quotes are verbatim
and correctly graded at their most-caveated phrasing. Referee 1's attacks 2 and
4 already reproduced the hard arithmetic digit-for-digit, and I independently
reproduced `q_A0''` and the D2 elasticities again here.

It still cannot be graded CONFIRMED, for four independent reasons, any one of
which is disqualifying:

- **§3 is still incomplete** (defect 5) — the completeness claim that D3 was
  written to repair is *still* false, now for the reflection identity.
- **A repair introduced a new wrong number** (defect 3) — `4.5357` for
  `4.53608…`. A correction block that itself needs correcting cannot close.
- **The deliverable is internally inconsistent** (defect 6) — the boxed theorem
  assumes six gates; its own appendix says seven.
- **The headline integer is stale** (defect 10) — the note's central claim to be
  quoting the smallest available `Q_0` was overtaken, in the very same commit
  that installed the correction block, by a referee-CONFIRMED constant giving a
  `Q_0` 4.19× smaller.

Defects 4, 8, 9 and 11 are citation-hygiene failures in a note whose entire
value proposition is "every claim carries the status of its most-caveated
source, quoted verbatim at file:line". They are individually small and
collectively material.

**Recommended disposition.** One further append-only correction block on
`EFFECTIVE_THEOREM_ASSEMBLY_SOL.md` (defects 3, 5, 6, 7, 8, 9, 10, 11 + print
p.577 for D4 + the §3 (H-RATE) scope note from attack 5), plus the D12 block on
`R5_MONOTONICITY_GATE_SOL.md` specified above. Then a third narrow pass
confirming those repairs — after which CONFIRMED is reachable, since no
mathematical content in the note has survived attack as false.

READY FOR JUDGING
