# KOYAMA REPLY DRAFT — 2026-08-15 (NOT SENT; owner-gated)

Drafted 2026-08-15. Reply to the two inbound emails logged at
`equispaced-primes/koyama/correspondence/raw/koyama-2026-08-15-arxiv-and-scope.md`.
Every factual claim is receipt-backed; receipts are listed in the notes section
at the bottom. Send decision and final wording are the owner's.

---

## Draft email

Subject: Re: arXiv upload — integration plan and a brief update

Dear Shin-ya,

Congratulations on the arXiv upload — securing priority on the regularized
explicit formula framework is the right move, and I have read the manuscript
with great interest. The automatic elimination of the principal-character
component through the virtual character χ_{1,a} is elegant, and Remark 2.3
frames exactly the question my computations can answer at scale. Here is a
concrete integration plan, then a brief update on my own recent work, then a
word on your kind suggestion about a standalone paper.

**1. Integrating the 3×10^14 data.** I propose three data contributions,
each mapping to a specific place in the joint manuscript.

First, the extended prime-race tables. Our counts π(x; N, a) − π(x; N, 1) for
N ∈ {7, 8, 11, 19, 23} now run on a 438-point logarithmic grid out to
x = 3×10^14 — two full decades beyond the 1.3×10^13 tables in the arXiv
draft. Every count agrees exactly with the earlier double-verified baseline
at all nine shared checkpoints (567/567 cells, zero mismatches). That
baseline itself carries three orthogonal checks: agreement with
primesieve at every checkpoint, your character-orthogonality identity (3.1)
verified at all 495 (N, x, a) cells, and a hand-rolled independent C sieve
reproducing every residue count at all nine checkpoints — the last also
reproduced on separate hardware through 1.3×10^12. A second-hardware
replication of the full extension is still running; I will say so in the
paper rather than claim it. These become an extended version of your Table 3
plus a rank-dynamics figure per modulus.

Second, what the data actually show — and I want to state this precisely,
because it is the strongest possible motivation for your regularization. At
x = 3×10^14, −1 strictly leads the raw race only for N = 7 and N = 23. For
N = 8 it is last among the three non-residues; for N = 11 and N = 19 it is
mid-pack (for N = 19 the value is slightly negative, −16,802). The ordering
has also shifted relative to 1.3×10^13. So the unregularized counts are still
transient and modulus-dependent even at 3×10^14 — which is exactly your
Remark 2.3's point: the fine-structure ranking is invisible to raw counting
at any presently reachable scale, and the regularized sum is analytically
indispensable. I would frame the numerical section as large-scale evidence
for the *necessity* of the regularized framework, not as direct confirmation
of the asymptotic ranking.

Third, the transient-oscillation analysis. We reconstructed the −1 race
curve from the low-lying zeros alone (first 25 zeros of every non-principal
character, PARI/GP with per-zero residual certification). In the top decade
the reconstruction tracks the observed curve with correlation 0.83–0.97
across the five moduli, while the rank of −1 still changes 17–39 times
depending on N. For N = 19 a deeper run (100 zeros per character) raises
the correlation to 0.9925 while the rank keeps changing — so the transients
are genuinely spectral, and they are precisely the low-zero boundary
fluctuations your Gaussian mollifier removes. This gives the paper a
quantitative identification of *which* zeros drive the unregularized noise.

One correction this analysis surfaced, offered in a collegial spirit: the
lowest ordinate of an odd complex character modulo 19 is certified at
γ = 0.0189563990802261… (independently bracketed with interval arithmetic,
no PARI involved), not ≈ 1.74 as in the manuscript's example. The one-mode
estimate of the 3.18×10^14 stabilization scale should be revisited in that
light; our data in any case show the transients persisting through 3×10^14.

**2. The Lean 4 formalization — proposed concise overview.** What exists and
builds clean today (Lean 4, Mathlib v4.28.0) is a formalization of selected
finite and algebraic components, not of your main theorem, and I would
describe it exactly that way: (i) the combinatorial core of the non-residue
race — every quadratic non-residue carries the same leading mean, so no
non-residue class, including −1, is singled out at leading order (four
theorems, zero `sorry`, axiom-audited); and (ii) a machine-checked
certificate for the character-selector algebra, which incidentally confirms
one correction to the arXiv draft: the printed kernel in Definition 1.3 sums
to the indicator of a⁻¹ rather than of a (witness: 3⁻¹ = 5 mod 7). The
certificate is a short appendix or ancillary file, whichever you prefer.

**3. Division of labour and sequencing.** On my side, in order: (a) I send
you the insertion-ready TeX block for the extended tables and rank figures,
the transient-atlas section with its figure, and the Lean overview paragraph
— all drafted already; (b) we reconcile the three open table cells by
exchanging raw π values — N = 11, a = 10 at 1.3×10^13 (ours 11,503) and the
two N = 19 cells (a = 13: ours 24,559; a = 18: ours 54,192) — since these
decide the N = 11 and N = 19 rankings in the shared range; (c) if you agree,
I compute your mollified sum S̃_T(x, a) numerically from our prime-power data
and the certified zero tables, for a direct finite-x comparison against
C_N · log L(1, χ_{1,a}) — that would be the sharpest possible validation of
Theorem 1.4 and is, I think, the figure the paper most wants. On your side:
placement and framing decisions, and the theoretical text as it stands. I
can have (a) and (b) to you within days of your go-ahead.

**4. An update from my certified-computation program.** Three items, all
with machine receipts, all adjacent to the themes of your manuscript —
explicit formulas and the zeros that drive them — rather than to prime bias
directly.

(a) A computer-assisted theorem on Selberg-zeta zeros. For the
non-arithmetic Hecke triangle group G₅, we have rigorously localized a zero
s* of the Selberg zeta function with |s* − (0.4538951800749447 +
5.7635372417301305 i)| ≤ 10⁻⁶ in each coordinate, hence Re(s*) ≤ 1/2 − 0.046
— to our knowledge the first rigorous localization of an off-line resonance
of a non-arithmetic finite-area hyperbolic surface. Every numerical constant
is an interval-arithmetic certificate (384-bit Arb, replayable receipts), the
linear-algebra joints are machine-proved in Lean, and the argument survived
five rounds of internal adversarial review including two independent
reproductions of the key constants. Across the family, the arithmetic
members q = 3, 4, 6 show the transfer-operator determinant vanishing at
s = ρ/2 (ρ the Riemann zeros) — at ~10⁻¹⁴ for q = 3 and ~10⁻¹¹–10⁻¹² for
q = 4, 6 under per-surface protocols — while for the non-arithmetic G₅ and
G₇ the zeros scatter with Re-dispersion ~10⁻¹–10⁻² (our G₈ sample is still
too small to include in that claim). Given your Selberg-zeta work, I would
very much value your reaction to the statement's framing before we circulate
anything.

(b) A conjectural mechanism behind that contrast. At the operator level, the
arithmetic determinants should carry an explicit ζ(2s) factor (for q = 3 this
is Mayer's theorem), while for G₅ we hold three certified nonvanishing
witnesses at ζ-zero points — nine across G₅, G₈, G₁₀, each certified modulo
a truncation-tail heuristic we state explicitly — refuting any such factor
pointwise. On the positive side for q = 4: the branch system conjugated to
the Fricke group has all first-return words in Γ₀(2) with exactly the
modular 2s-cocycle (verified symbolically through word length 4), and all
four certified q = 4 determinant zeros we tested vanish simultaneously in
the Fraczek–Mayer level-2 modular vector operator (to 10⁻¹⁷–10⁻²⁹, with
order-one off-zero controls) — a finite numerical probe, not a proof, but
consistent with the q = 4 operator embedding as a block of the level-2
modular one. This mechanism statement is conjectural; your judgment on it
would mean a lot.

(c) Two numerical firsts around zeta-zero sums. The constant
Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) — the conjectural limiting mean square of
x⁻¹Σ_{n≤x} M(n)² under RH + Gonek–Hejhal (Ng 2004) — now stands at
0.0290327 ± 0.00002 from 10,000 certified-residual zeros (the error bar is a
numerical tail envelope, not theorem-level). This refutes an internal guess
of ours (2/π²) and excludes 3/π⁴ at ~98σ. And a first numerical test of
Gonek's conjecture J₋₁(T) ~ (3/π³)T (as recorded by Ng 2004): at T ≈ 10⁴ we
find J₋₁(T)/T ≈ 0.949 · (3/π³), slowly drifting — a finite-height
diagnostic, neither confirmation nor refutation. A 10⁵-zero extension is
still running; a small number of refined rows failed an internal
monotonicity gate and are being re-refined before any sum is computed from
them.

**5. Your suggestion of a standalone paper.** Thank you — it is generously
meant, and I take it that way. But the plain fact is that I have no academic
credentials in mathematics and no publishing experience. Being included as a
co-author on any paper you intend to submit would be an honor, and a far
more meaningful recognition than a standalone publication of my own. And on
scope: the single-focus strategy for the prime-bias paper is clearly right
for Inventiones, and I am glad to shape my contributions to fit it exactly.

Warm regards,
Saar

---

## Draft notes (not part of the letter)

### Per-item connection judgments (task B)

All four update items were judged YES-connect and woven into §4 of the
letter, with the connection stated in the lead-in sentence ("explicit
formulas and the zeros that drive them"):

- **(a) Certified Hecke resonances + G₅ off-line theorem** — Selberg-zeta
  zeros; Koyama's own publication record centers on Selberg/absolute zeta
  functions, and the arXiv manuscript is built on zero sums in explicit
  formulas. Genuine connection; the update draft itself says "very much
  adjacent to your Selberg-zeta work." Woven in as §4(a), with the explicit
  ask for his reaction on framing.
- **(b) ζ(2s) factorization dichotomy** — a statement about the Riemann-zeta
  zeros appearing inside a transfer-operator determinant; direct
  explicit-formula adjacency. Woven in as §4(b), labeled conjectural.
- **(c) Mertens constant + Gonek J₋₁(T)** — sums over zeta zeros ρ and
  values ζ′(ρ); the same spectral objects his regularized explicit formula
  sums over, and Mertens' second theorem appears in his Remark 2.2. Woven in
  as §4(c).

No item was judged NO-connect, so no separate disconnected section was
needed. The elliptic-curve analysis and Decision-Audit SDK that Koyama's
email 2 mentions were *not* included anywhere — the owner instructions do
not ask for them and they do not connect.

### Receipts for every factual/numerical claim in the letter

§1 (integration):

- 438-point log grid, N ∈ {7,8,11,19,23}, x ≤ 3×10^14, 567/567 exact
  matches at nine shared checkpoints through 1.3×10^13:
  `equispaced-primes/koyama/pre_reply_2026-08-01/03_NUMERICAL_EVIDENCE_3E14.md`
  (lines 8–13); dataset `projects/minus1-dominance/curve_3e14.tsv` (SHA-256
  recorded there); ledger entry `projects/minus1-dominance/LEDGER.md` §4.
- Double-verification = three orthogonal checks (primesieve cross-check;
  character-orthogonality identity at 495 cells, worst real residual
  1.4×10⁻⁴; hand-rolled C sieve `independent_sieve.c` exact at all 9
  checkpoints), hardware-independent through 1.3×10^12 (420 cells, second
  machine M1B): `koyama_replication_bundle/REPLICATION_REPORT.md` §1.1 and
  Limitations; `koyama_replication_bundle/out2.tsv`, `m1b_indep_1e11.tsv`.
- Second-hardware replication of the 3×10^14 extension still running (M1
  pass stalled at 146/224, no output file; Kaggle kernel staged, never
  produced an artifact; the 03 evidence file explicitly disclaims it):
  `equispaced-primes/koyama/pre_reply_2026-08-01/03_NUMERICAL_EVIDENCE_3E14.md:15-16`,
  `projects/minus1-dominance/LEDGER.md:148-149`. **The letter says "still
  running" and does not claim it — an earlier sent email (2026-06-03) said a
  second run "is finishing now"; that did not complete on record.**
- Endpoint ranks at 3×10^14 (−1: 1st for N=7 with +324,843; 1st for N=23
  with +294,472; last (3/3) for N=8; 3/5 for N=11; 6/9 for N=19 with
  exactly −16,802):
  `equispaced-primes/koyama/pre_reply_2026-08-01/03_NUMERICAL_EVIDENCE_3E14.md:23-33`.
- Transient atlas: 25 zeros/character, top-decade correlations
  0.965/0.931/0.939/0.971/0.826 (N=7,8,11,19,23), rank changes
  17/23/30/17/39; K=100 deep run for N=19 → correlation 0.9925, 14 rank
  changes, 7 leader changes:
  `equispaced-primes/koyama/pre_reply_2026-08-01/05_SPECTRAL_TRANSIENT_ATLAS.md`,
  `equispaced-primes/papers/joint-spectral-section/section.tex:87-91,163-170`,
  package `projects/minus1-dominance/spectral_transients_3e14/`.
- Certified lowest odd q=19 ordinate γ = 0.0189563990802261…, PARI plus an
  independent FLINT/Arb Hardy-Z bracket of width 5.93×10⁻⁸⁴, explicitly
  contradicting the manuscript's ≈1.74:
  `projects/minus1-dominance/spectral_transients_3e14/independent_n19/output/N19_CERTIFICATE.md`,
  `05_SPECTRAL_TRANSIENT_ATLAS.md:86-98`.
- Definition 1.3 inverse-class error (kernel sums to indicator of a⁻¹;
  witness 3⁻¹ = 5 mod 7), Lean-certified:
  `equispaced-primes/koyama/pre_reply_2026-08-01/01_THEOREM_AUDIT.md`,
  `02_CHARACTER_ORTHOGONALITY_CERTIFICATE.md`,
  `projects/minus1-dominance/aristotle_dispatch_character_orthogonality/CharacterOrthogonalityTarget.lean`.
- Open cells: N=11,a=10 at 1.3×10^13 ours 11,503
  (= 44,583,154,901 − 44,583,143,398 from `koyama_replication_bundle/out2.tsv`)
  vs his 71,711; N=19 at 1.3×10^13: a=13 ours 24,559 vs 55,581; a=18 ours
  54,192 vs 57,192: `koyama_replication_bundle/REPLICATION_REPORT.md:153-178`,
  analyst notes in `equispaced-primes/koyama/correspondence/KOYAMA.md`.
- Insertion-ready TeX block exists:
  `equispaced-primes/papers/joint-spectral-section/section.tex`.

§2 (Lean overview):

- Mandated phrasing "formalization of selected finite/algebraic components,
  not of the main theorem":
  `equispaced-primes/koyama/pre_reply_2026-08-01/04_LEAN_AND_REPLY_GATES.md`.
- Minus1Core: four theorems (`sqrtCount_eq_zero_of_not_isSquare`,
  `leadingMean_eq_neg_one_of_not_isSquare`, `leadingMean_tie`,
  `minus_one_not_singled_out`), 0 `sorry`, axioms `[propext, Quot.sound]`,
  Mathlib v4.28.0: `projects/minus1-dominance/Minus1Core.lean:55-86`,
  build receipt recorded at `projects/minus1-dominance/LEDGER.md:104-123`.

§4 (update items; current `KOYAMA_UPDATE_DRAFT.md` text, corrected numbers):

- G₅ theorem statement and δ ≥ 0.0461038 (letter rounds down to "≤ 1/2 −
  0.046"): `research_notes/rh_goals_2026-08-14/lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md:26-32,201`.
  384-bit Arb, five adversarial rounds (V4–V8), two independent
  reproductions (V7, E1): audit Item 1,
  `research_notes/rh_goals_2026-08-14/lane_g/ADVERSARIAL_AUDIT_KIMI_K3.md`.
- Family sweep law table (q=3: 6.5×10⁻¹⁴ LINE; q=4: 9.8×10⁻¹² and q=6:
  1.03×10⁻¹¹, both INSUFFICIENT-DATA / per-surface protocols, not
  family-comparable per V1; G₅, G₇ SCATTER-CONFIRMED with Re-dispersion
  0.030 / 0.103; G₈ n=0 INSUFFICIENT-DATA):
  `research_notes/rh_goals_2026-08-14/lane_b/FAMILY_SWEEP_G7G8.md:25-42`,
  V1 caveat `research_notes/rh_goals_2026-08-14/EXECUTION_LOG.md:82-95`.
- M2 witnesses: exactly 3 for G₅, 9 total across G₅/G₈/G₁₀, every row
  "certified-modulo-tail-heuristic", pointwise scope explicit:
  `research_notes/rh_goals_2026-08-14/lane_g/M2_NONFACT_WITNESSES.md:9-17,35-41`,
  `research_notes/rh_goals_2026-08-14/lane_g/m2_nonfact_receipt.json`.
- q=4 Fricke evidence: Γ₀(2) word membership + exact 2s-cocycle through
  word length 4:
  `research_notes/rh_goals_2026-08-14/lane_g/M1B_Q4_INTERTWINER.md:121-124,330`;
  four q=4 pins vanish to 10⁻¹⁷–10⁻²⁹ with controls 21.78 / 3.58, verdict
  "CONTAINMENT SUPPORTED (finite numerical probe; not proved)", no
  Fricke-plus action (tested operator is the Γ₀(2) congruence block):
  `research_notes/rh_goals_2026-08-14/lane_g/M1C_Q4_KILLTEST.md` (+ receipt
  JSON). Letter keeps the "finite numerical probe, not a proof" hedge.
- Mertens constant v2: S = 0.029032731101 ± 1.79×10⁻⁵, N = 10,000 zeros,
  T = 9877.78, 3/π⁴ excluded at ~98σ, 2/π² refuted; error bar is a
  numerical tail envelope:
  `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_V2_REPORT.md` (+
  `zero_sum_v2_receipt.json`); v1 (3,000 zeros, 0.02903 ± 0.00016, ~11σ):
  `research_notes/rh_goals_2026-08-14/lane_a/ZERO_SUM_REPORT.md`. The
  letter cites the stronger v2 (the update draft cited v1; both are
  receipt-backed).
- Gonek J₋₁: J₋₁(T)/T = 0.09181076 at T = 9877.78, ratio to 3/π³ =
  0.94890332, verdict "TOO EARLY … a finite-height diagnostic, not a
  confirmation or refutation":
  `research_notes/rh_goals_2026-08-14/lane_a/J_MINUS1_GONEK_REPORT.md`;
  conjecture dated 1999 (MSRI), as recorded by Ng 2004:
  `research_notes/rh_goals_2026-08-14/lane_c/S1_ZERO_SUM_LIT.md:38-40`.
- 10⁵-zero Kaggle extension: parts 4–5 harvested (36,001 rows), 11 rows
  failed the monotonicity gate, being re-refined with seed-validated
  receipts before any sum is computed; parts 1–3 running (log-asserted
  2026-08-14):
  `research_notes/rh_goals_2026-08-14/EXECUTION_LOG.md:166-181,380-383`.

### Audit Item-5 corrections and how the letter honors them

The audit's three factual errors were against the *previous* update draft.
The current `KOYAMA_UPDATE_DRAFT.md` on disk is repaired; this was confirmed
against the receipts (not assumed):

- **5-D1 (nine-vs-three witnesses)** — draft now reads "three nonvanishing
  witnesses at ζ-zero points (nine across G₅, G₈, G₁₀; each certified
  modulo a truncation-tail heuristic)". Matches
  `M2_NONFACT_WITNESSES.md:9-17`. Letter §4(b) uses the same corrected
  wording, including the tail-heuristic qualifier.
- **5-D2 (G₈ folded into the dispersion claim)** — draft now excludes G₈
  ("our G₈ sample is currently too small to include in that claim").
  Matches `FAMILY_SWEEP_G7G8.md` (G₈ n=0, INSUFFICIENT-DATA). Letter §4(a)
  names only G₅ and G₇ for scatter and carries the G₈ caveat.
- **5-D3 (~10⁻¹⁵ operator agreement)** — draft now reads "~10⁻¹⁴ for q = 3
  and ~10⁻¹¹–10⁻¹² for q = 4, 6, under per-surface protocols". Matches the
  law table 6.5×10⁻¹⁴ / 9.8×10⁻¹² / 1.03×10⁻¹¹ and the V1
  non-comparability ruling. Letter §4(a) uses exactly these figures with the
  per-surface-protocols qualifier.
- **5-D4 (unverifiable claims)** — "part 5 harvested and verified" no longer
  asserted as done; letter says the extension "is still running" with the
  monotonicity-gate repair disclosed. The "first computed/certified
  resonance data for non-arithmetic Hecke groups" novelty claim is kept
  only in the narrower theorem form with "to our knowledge", consistent
  with `lane_c/NOVELTY_RESCOUT_2026-08-15.md` (which scopes novelty to the
  rigorous-localization theorem, not to "first computed data").
- **5-D5 (Gonek 1989 vs 1999)** — letter drops the date and cites "as
  recorded by Ng 2004", matching the scout.

### Numbers I could not verify / deliberately excluded

- The phase arithmetic "γ log x / 2π ≈ 0.36 at x = 1.3×10^13" appears in
  Koyama's Remark 2.3 but nowhere in the owner's files; not used.
- The e^33.4 ≈ 3.18×10^14 stabilization scale is Koyama's one-mode
  heuristic; the owner's files carry it as "not re-derived"
  (`projects/minus1-dominance/RECONCILE_COMPUTE.md:65`) and the transient
  atlas shows rank changes persisting through 3×10^14. The letter therefore
  frames 3×10^14 as *not* inside the asymptotic regime and recommends
  revisiting the 3.18×10^14 estimate in light of the certified γ ≈ 0.01896
  zero.
- The aggregate "formal-conjectures builds with exactly 2 sorries" claim in
  `equispaced-primes/koyama/joint-paper/LEAN_SORRY_STATUS.md` predates six
  newer lakefile modules and has no preserved build log; the letter makes no
  aggregate build claim, only per-artifact ones.
- Kaggle "parts 1–3 running" and the seed-validation repair are
  log-asserted (2026-08-14), not receipt-verified today; the letter's
  "still running" matches that.

### Residual overclaim risks for the owner

1. **Headline tension (largest risk).** The joint paper's headline is the
   universal dominance of −1. The owner's own adversarially verified verdict
   (`projects/minus1-dominance/REPORT.md:10-15`, `RECONCILE_COMPUTE.md`):
   under GRH+LI, for the Rubinstein–Sarnak sign-density of the *unweighted*
   race, −1 is the *least*-biased non-residue (variance maximum ⇒ density
   minimum), and NR-vs-NR races are exact 50–50 ties. Koyama's dominance
   statement concerns his *regularized weighted* sums, a different object,
   so the letter's framing — "our data evidence the *necessity* of the
   regularized framework, not the asymptotic ranking" — is the honest
   position and is what the letter says. But co-authoring the dominance
   headline remains the internally flagged exposure (`KOYAMA.md` analyst
   notes 2026-06-02 #2, 2026-06-03 #4). The owner should decide
   deliberately how much of the RS-density verdict to put to Koyama before
   co-authorship is locked; the letter as drafted presents the raw data
   factually and does not assert the ranking holds.
2. **Corrections included.** The letter surfaces the Definition 1.3
   inverse-class error and the certified q=19 low zero (contradicting
   γ ≈ 1.74). Both are receipt-backed and collegially phrased, but the
   owner may prefer to send them via the separate redline memo
   (`pre_reply_2026-08-01/08_CORRECTION_AND_REDLINE_MEMO.md`) instead.
3. **Send gate.** `KOYAMA.md` RISK & VERIFICATION: identity verification,
   written terms, and explicit owner approval are all still pending. This
   draft changes nothing about that; nothing has been sent.
4. "First rigorous off-line localization" novelty rests on a lane_c scout
   not independently redone in the audit (audit 1-C8); the letter keeps
   "to our knowledge".
5. The proposed computation of S̃_T(x, a) against C_N · log L(1, χ_{1,a})
   is a *proposal*, not existing work; the letter presents it as such.
