# KOYAMA REPLY — v2 MERGED (NOT SENT; owner-gated)

Base: Kimi K3 draft `KOYAMA_REPLY_2026-08-15_DRAFT.md` (kept intact for comparison).
This version merges in an independent pass over the same inputs (arXiv PDF read
directly, receipts re-derived). Changes vs base are listed in the notes.

---

## Draft email

Subject: Re: arXiv upload — integration plan, and a brief update

Dear Shin-ya,

Congratulations on the arXiv posting. Anchoring the regularized explicit
formula and the dominance framework is the right move, and I have now read the
manuscript closely. Below: a concrete integration plan for the 3×10¹⁴ data and
the spectral work, four points I think must be settled before the Inventiones
version, a short update on my own recent results, and a word on your kind
suggestion about a standalone paper.

**1. The 3×10¹⁴ data, and where it goes in the manuscript.**

Our counts π(x; N, a) − π(x; N, 1) for N ∈ {7, 8, 11, 19, 23} now run on a
438-point logarithmic grid to x = 3×10¹⁴ — two decades past the 1.3×10¹³ tables
in Table 3. The extension reproduces the earlier double-verified baseline
exactly: 567/567 integer cells, zero mismatches, at the nine shared
checkpoints. That baseline carries three orthogonal checks — primesieve
agreement at every checkpoint, the character-orthogonality identity verified at
all 495 (N, x, a) cells, and an independent hand-written C sieve reproducing
every residue count, the last also reproduced on separate hardware through
1.3×10¹². A second-hardware replication of the full extension is still running;
I will describe it that way in the paper rather than claim more.

What the data show, stated precisely, because I think it is the strongest
available motivation for your regularization. At x = 3×10¹⁴, −1 strictly leads
the unregularized race only for N = 7 and N = 23. For N = 8 it is last among
the three non-residues (a = 5 leads); for N = 11 it is mid-pack; for N = 19 its
difference is negative, −16,802. The ordering has also moved since 1.3×10¹³ —
for N = 8 the leader changed. So the raw races are still transient and
modulus-dependent two decades beyond your Table 3, which is exactly the point
of Remark 2.3, only sharper: the fine-structure ranking is not visible to
unregularized counting at any presently reachable height, and the mollified
statistic is analytically indispensable. I would write the numerical section as
large-scale evidence for the *necessity* of the regularized framework, not as
confirmation of the asymptotic ranking. That framing is also the one a referee
cannot attack.

This becomes an extended Table 3 plus one rank-dynamics figure per modulus.

**2. The spectral transients — what drives them.** We reconstructed the −1 race
curve from low-lying zeros alone (first 25 positive zeros of every
non-principal character; PARI/GP, per-zero residual certification). Over the
top decade the reconstruction tracks the observed curve with correlations
0.826–0.971 across the five moduli, while the rank of −1 still changes many
times. For N = 19, extending to 100 zeros per character raises the correlation
to 0.9925 — and the reconstructed race *still* shows 14 rank changes and 7
leader changes. So the transients are genuinely spectral, and they are exactly
the low-zero boundary fluctuations your Gaussian mollifier removes. This gives
the paper a quantitative identification of *which* zeros drive the
unregularized noise — a five-panel figure and a transition table, both drafted.

**3. Four points to settle before the submission version.** I raise these
because my name would be on the paper and because a referee at that level will
raise them first. All four have receipts, and I have written out the exact
replacement wording in a short memo I can send with the TeX.

(i) *The parameter T in Theorem 1.4.* The theorem states C_N as depending only
on N, for fixed T > 0, but the diagonal contribution (2.5) carries an explicit
factor T/(4√π), and I did not find the cancellation that removes it. Related:
in §2.2 the off-diagonal terms are said to decay as O(e^{−cT²}) for fixed T as
x → ∞. That is a per-pair statement; the sum runs over pairs (p^k, q^m) whose
logarithmic separations can tend to zero as x grows, so the *summed* bound does
not follow uniformly from the per-pair one. The safe route is a two-parameter
statement — a joint regime x → ∞ with T = T(x), an explicit coefficient
C_{N,T(x)}, and an error uniform over the reduced classes — with the fixed-T
form retained as a conjecture until the summed off-diagonal estimate, order
interchange, prime-power and Archimedean terms are proved. I would rather we
publish the two-parameter theorem we can defend than the fixed-T one.

(ii) *Definition 1.3 is now inconsistent with Theorem 1.4.* Equation (1.3) and
Remark 1.6 print the kernel with (1 − χ(a)); the definition of log L(1, χ_{1,a})
under Theorem 1.4 uses (1 − χ̄(a)). The conjugated form is the correct one:
(1/φ(N)) Σ_χ (1 − χ̄(a)) χ(x) = 1_{x=1} − 1_{x=a}, whereas as printed (1.3)
selects the class a⁻¹ (witness: 3⁻¹ = 5 mod 7). For a ≡ −1 the two agree, so
the dominance discussion is unaffected — but the general-a statements and every
coefficient downstream need the convention fixed once and propagated. I have a
short Lean 4 certificate for the corrected finite identity.

(iii) *Remark 2.3's modulus-19 example.* For the primitive character of Conrey
index 13 mod 19 (odd, χ(−1) = −1) there is a positive ordinate at
γ = 0.0189563990802261…, far below the γ ≈ 1.74 used as the lowest complex
zero. Two PARI mesh runs agree; direct evaluation gives residual < 1e−28; and
an independent Python FLINT/Arb computation gives a sign-definite Hardy-Z
bracket of width 5.94×10⁻⁸⁴ certifying a critical-line zero there (existence,
not uniqueness or completeness). The e^{33.4} ≈ 3.18×10¹⁴ settling estimate
rests on that mode being lowest, so it should be revisited — and independently,
our data show the transients still active at 3×10¹⁴. The defensible replacement:
a low-zero truncation reproduces much of the modulus-19 trajectory, but a very
low odd-character mode remains active, so this range is not a universal
stabilization threshold.

(iv) *One table cell, now public.* Table 3(c) gives π(x; 11, 10) − π(x; 11, 1)
= 71,711 at 1.3×10¹³; our identity-reconstructing, lower-checkpoint-consistent
value is 11,503. Two modulus-19 cells differ similarly (a = 13: ours 24,559;
a = 18: ours 54,192). These decide the placement of −1 for N = 11 and N = 19,
so I would like to reconcile them against raw class counts before a replacement
version rather than after a referee finds them.

Separately, and only as protection for the paper: Conjecture 1.7 is a statement
about the special values log L(1, χ_{1,a}), not about prime counts. Our race
data neither support nor contradict it, and I think the manuscript should say
so explicitly — the inference from a regularized ordering to eventual
unregularized dominance needs its own transfer theorem.

**4. The Lean 4 formalization — proposed scope.** What builds clean today
(Lean 4, Mathlib v4.28.0) is a formalization of *selected finite and algebraic
components*, not of your main theorem, and I would describe it in exactly those
words: (a) the combinatorial core of the non-residue race — every quadratic
non-residue carries the same leading mean, so no non-residue class, including
−1, is singled out at leading order (four theorems, zero `sorry`,
axiom-audited); and (b) a machine-checked certificate for the character-selector
algebra of point (ii) above. One short subsection, or an ancillary file —
whichever you prefer. I would not want any sentence suggesting Lean verifies
the paper.

**5. Division of labour and sequencing.** On my side, in order: (a) I send the
insertion-ready TeX for the extended tables, the rank-dynamics and spectral
figures, and the Lean paragraph — all drafted; (b) we reconcile the table cells
in 3(iv) by exchanging raw π values; (c) if you agree, I compute your mollified
S̃_T(x, a) numerically from our prime-power data and the certified zero tables,
for a direct finite-x comparison against C_N · log L(1, χ_{1,a}) — that would be
the sharpest validation of Theorem 1.4 available to us, and I suspect it is the
figure the paper most wants. On your side: placement, framing, and the
theoretical text. To do (a) and (b) properly I need your current TeX source,
bibliography, figures and tables, plus the arXiv identifier and version I should
work against; with those I can turn (a) and (b) around within days.

Two housekeeping items for a submission at this level: I have drafted a
contribution statement recording the theoretical, numerical, software and
formalization roles separately, and a short computational-assistance disclosure
(it states that language-model and automated-proof assistance were used in a
limited, supervised way, that the Lean certificate covers only selected finite
algebraic statements, and that responsibility rests with us as the human
authors). Both are ready for your review, and I think having them in the file
from the start is safer than adding them under referee pressure.

**6. Separately — an update from my certified-computation program.** Three
items, all with machine receipts, none yet circulated. These are unrelated to
the prime-bias manuscript and I am not proposing them for it; I mention them
because the first two touch the Selberg zeta functions you have worked on for
years, and your judgment on them would be worth more to me than anyone
else's.

(a) *A computer-assisted theorem on Selberg-zeta zeros.* For the
non-arithmetic Hecke triangle group G₅ we have rigorously localized a zero s*
of the Selberg zeta function with
|s* − (0.4538951800749447 + 5.7635372417301305 i)| ≤ 10⁻⁶ in each coordinate,
hence Re(s*) ≤ 1/2 − 0.046 — to our knowledge the first rigorous localization
of an off-line resonance of a non-arithmetic finite-area hyperbolic surface.
Every numerical constant is an interval-arithmetic certificate (384-bit Arb,
replayable receipts), the joints of the abstract chain are machine-proved, and
the argument has survived five rounds of internal adversarial review including
two independent reproductions of the key constants. Across the family, the
arithmetic members q = 3, 4, 6 show the transfer-operator determinant vanishing
at s = ρ/2 (ρ the Riemann zeros) — at ~10⁻¹⁴ for q = 3 and ~10⁻¹¹–10⁻¹² for
q = 4, 6, under per-surface protocols — while for the non-arithmetic G₅ and G₇
the zeros scatter with Re-dispersion ~10⁻¹–10⁻² (our G₈ sample is still too
small to include in that claim). Given your work on Selberg zeta functions, I
would value your reaction to the framing before we circulate anything.

(b) *A conjectural mechanism behind that contrast.* At the operator level the
arithmetic determinants should carry an explicit ζ(2s) factor — for q = 3 this
is Mayer's theorem; for q = 4, 6 I found no published operator-level
factorization — while for G₅ we hold three certified nonvanishing witnesses at
ζ-zero points (nine across G₅, G₈, G₁₀, each certified modulo a
truncation-tail heuristic we state explicitly), refuting such a factor
pointwise. On the positive side for q = 4: the branch system conjugated to the
Fricke group Γ₀⁺(2) has all first-return words in Γ₀(2) with exactly the modular
2s-cocycle (verified symbolically through word length 4), and all four certified
q = 4 determinant zeros we tested vanish simultaneously in the Fraczek–Mayer
level-2 modular vector operator (to 10⁻¹⁷–10⁻²⁹, with order-one off-zero
controls) — a finite numerical probe, not a proof, but consistent with the
q = 4 operator embedding as a block of the level-2 modular one. The mechanism
statement is conjectural; your judgment on it would mean a great deal.

(c) *Two numerical results on zero sums.* The constant Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) —
the conjectural limiting mean square of x⁻¹ Σ_{n≤x} M(n)² under RH plus
Gonek–Hejhal, as recorded by Ng — now stands at 0.02903 ± 0.00002 from 10,000
zeros with certified residuals; the receipt certifies three significant digits,
the error bar being a numerical tail envelope rather than a theorem-level
bound. This refutes an internal guess of ours (2/π²) and excludes 3/π⁴ by a
wide margin. And a first numerical test of Gonek's conjecture J₋₁(T) ~ (3/π³)T:
at T ≈ 9.88×10³ we find J₋₁(T)/T = 0.949 · (3/π³), with a top-half linear fit
at 0.959 and slow drift — a finite-height diagnostic, neither confirmation nor
refutation; the height is far too low for an asymptotic claim. A 10⁵-zero
extension is still running.

**7. Your suggestion of a standalone paper.** Thank you — it is generously
meant, and I take it that way. The plain fact is that I have no academic
credentials in mathematics and no experience publishing. Being included as a
co-author on a paper you intend to submit would be an honor, and a far more
meaningful recognition than a standalone publication of my own. On scope: the
single-focus strategy is clearly right for Inventiones, and I am glad to shape
my contributions to fit it exactly. (For the boundary-identity note in
particular I would not want to press it as a standalone research paper in any
case — I completed the identity, then found prior work already supplying the
substantive framework, so its honest role is a technical note.)

Warm regards,
Saar

---

## Merge notes (not part of the letter)

### What this version changes vs the Kimi K3 base draft

Kept from the base: overall structure, the integration plan, the update section
(§6 here), and the standalone-paper answer. Its numbers were spot-checked
against receipts and were sound except where noted below.

**Added — §3(i), the T-dependence and summed off-diagonal gap.** The single
substantive omission in the base draft. Verified directly in the *new arXiv
PDF*, not in the older attached draft: Theorem 1.4 states C_N as depending
"solely on the modulus N" for fixed T, while (2.5) carries an explicit
T/(4√π) prefactor, and §2.2 asserts O(e^{−cT²}) off-diagonal decay for fixed T
as x → ∞ (per-pair, not summed; separations → 0). Receipts: extracted PDF text
lines 140–150 (Thm 1.4), 278–288 ((2.5) and the off-diagonal sentence);
`pre_reply_2026-08-01/08_CORRECTION_AND_REDLINE_MEMO.md` §2, which had already
flagged this on the 31 July draft and prescribed the two-parameter replacement.
It is unrepaired in the arXiv version. Raising it is not optional: he is
submitting to Inventiones with the owner as co-author.

**Sharpened — §3(ii), Definition 1.3.** The base draft called it an error. It
is now an *internal inconsistency*: (1.3) and Remark 1.6 print (1 − χ(a)), but
the log L(1, χ_{1,a}) definition under Theorem 1.4 already uses (1 − χ̄(a))
(PDF lines 122–128, 140–152, 179). Also noted that for a ≡ −1 the two agree, so
the dominance headline is unaffected — a materially friendlier and more
accurate framing. Source for the correction:
`08_CORRECTION_AND_REDLINE_MEMO.md` §1.

**Added — §3(iv), the table cell is now public.** The N = 11, a = 10 conflict
(71,711 in Table 3(c), 11,503 ours) is in the posted arXiv version, so the fix
path is a replacement version, not a private note. Receipts:
`pre_reply_2026-08-01/03_NUMERICAL_EVIDENCE_3E14.md` "Open numerical item";
PDF line 412 (Table 3(c)).

**Added — the Conjecture 1.7 guard.** Conjecture 1.7 is about minima of
log L(1, χ_{1,a}) — L-values, not prime counts (PDF lines 209–215). Saying so
explicitly defuses the largest residual risk the base draft flagged (our own
verdict that −1 is the *least*-biased non-residue in the unweighted RS race,
`03_NUMERICAL_EVIDENCE_3E14.md`) without withholding anything: the race data
neither support nor contradict an L-value conjecture, and it is the transfer
step that needs its own theorem.

**Added — logistics.** Request for his current TeX source, bibliography,
figures/tables and arXiv identifier/version; offer of the contribution
statement and the AI/computational-assistance disclosure. All four are prepared
artifacts (`09_AUTHOR_CONTRIBUTION_STATEMENT.md`,
`11_AI_AND_COMPUTATIONAL_ASSISTANCE_DISCLOSURE.md`,
`13_EXECUTION_OUTCOME_AND_REPLY_PACKET.md` "Remaining owner inputs"). For an
Inventiones submission in 2026 the disclosure is close to mandatory; the base
draft omitted all of this.

**Corrected — the Mertens digits.** The base draft wrote 0.0290327 ± 0.00002.
The receipt (`research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_receipt.json`,
`final_estimate.digits_claimed`) certifies *three* significant digits and says
explicitly that four are not certified by the tail bar. Changed to
0.02903 ± 0.00002. Also dropped the "~98σ" figure: the receipt's
`sigma_units: 98.386` for 3/π⁴ is measured in units of a conservative tail
envelope that the same file calls "not a theorem-level bound", so quoting it as
a sigma to a number theorist overstates it — replaced with "by a wide margin".

**Tightened — J₋₁.** Base draft's 0.949 is correct (endpoint row N = 10000,
T = 9877.78, `ratio_to_3_over_pi_cubed = 0.9489033`) but is a single
checkpoint; added the top-half fit ratio 0.9589406 and the receipt's own
verdict `TOO EARLY` / "T ≈ 10⁴ is far too low"
(`lane_a/j_minus1_receipt.json`).

**Restructured.** Corrections moved out of the data narrative into one clearly
labelled §3 block, prefaced by why they are being raised. Rationale: in a
congratulations email, two corrections scattered through the prose read as
sniping; six corrections gathered under "before the submission version" read as
co-authorship.

### Connection verdict for the update items (corrects the base draft)

The base draft judged all four update items YES-connect and wove them into the
body, justified as "explicit formulas and the zeros that drive them". Checked
against the arXiv text directly, that does not hold:

- `grep -in "selberg|absolute zeta|transfer operator|resonance|hyperbolic|Gonek|zeta'|mobius|Hecke"` over the
  extracted PDF returns **zero** hits.
- The one "Mertens" hit (line 370) is Mertens' theorem Σ_{p≤√x} 1/2p ~ ½ log log x,
  not the Mertens function M(n).
- Bibliography is four entries: Aoki–Koyama, Feuerverger–Martin,
  Iwaniec–Kowalski, Rubinstein–Sarnak (lines 488–494). No spectral geometry.

The paper's apparatus is Dirichlet L-functions, Weil's explicit formula, and
DRH. Our items are Selberg-zeta resonances of hyperbolic surfaces and ζ-zero
sums weighted by 1/|ζ′(ρ)|². Shared vocabulary, no shared object, no shared
theorem. A "both concern explicit formulas" link would connect almost any
zero-sum result to almost any analytic-number-theory paper — it is a category,
not a connection.

Verdict: **NO-connect for all four**, per the owner's instruction that a forced
link is worse than clean separation. §6 is therefore explicitly labelled as
unrelated to the manuscript. The one honest reason to include it at all is
Koyama's own research record on Selberg and absolute zeta functions — a reason
to ask his opinion, not a reason to integrate. The single item with a real
bearing on the joint paper (the certified low ordinate γ = 0.01896 for χ mod 19)
is not from the update draft at all; it is in §3(iii), where it belongs.

### Receipt index for every factual claim in the letter

| Claim | Source |
|---|---|
| 438-point grid to 3×10¹⁴; 567/567 cells | `pre_reply_2026-08-01/03_NUMERICAL_EVIDENCE_3E14.md`; `projects/minus1-dominance/curve_3e14.tsv` (sha256 in that file) |
| Three orthogonal baseline checks; 495 cells | `pre_reply_2026-08-01/02_CHARACTER_ORTHOGONALITY_CERTIFICATE.md`, `03_…md` |
| Second-hardware replication still running | `03_…md` "not a second full independent-hardware replication" |
| Ranks at 3×10¹⁴ (N=7,23 lead; N=8 last; N=19 −16,802) | `03_…md` rank table |
| Correlations 0.826–0.971; K=100 → 0.9925; 14 rank / 7 leader changes | `10_EMAIL_REPLY_DRAFT.md`; `08_CORRECTION_AND_REDLINE_MEMO.md` §3; `projects/minus1-dominance/spectral_transients_3e14/` |
| γ = 0.0189563990802261…, Arb bracket 5.94e−84 | `08_…md` §3; `spectral_transients_3e14/independent_n19/` |
| Def 1.3 / (1 − χ̄(a)) inconsistency | arXiv PDF lines 122–128, 140–152 |
| T/(4√π) in (2.5); off-diagonal e^{−cT²} | arXiv PDF lines 278–288; `08_…md` §2 |
| N=11 a=10: 71,711 vs 11,503; N=19 cells | arXiv PDF line 412; `03_…md`; `08_…md` §5.3 |
| Lean scope, four theorems, zero `sorry` | `pre_reply_2026-08-01/04_LEAN_AND_REPLY_GATES.md` |
| G₅ theorem constants, 10⁻¹⁴ / 10⁻¹¹–10⁻¹², G₈ excluded, 3-of-9 witnesses | `research_notes/rh_goals_2026-08-14/lane_d/KOYAMA_UPDATE_DRAFT.md` (post-audit), `lane_g/ADVERSARIAL_AUDIT_KIMI_K3.md` Item 5 |
| Mertens 0.02903 ± 0.00002, 10,000 zeros, 3 digits | `lane_a/zero_sum_v2_receipt.json`, `ZERO_SUM_V2_REPORT.md` |
| J₋₁ 0.949 endpoint / 0.959 fit, TOO EARLY | `lane_a/j_minus1_receipt.json` |
| Boundary identity: prior art, not standalone | `pre_reply_2026-08-01/12_STANDALONE_THEOREM_NOVELTY_GATE.md`, `13_…md` decision 3 |

### Stale-file flag for the owner

`research_notes/rh_goals_2026-08-14/lane_d/KOYAMA_UPDATE_DRAFT.md` still carries
the v1 Mertens numbers (0.02903 ± 0.00016, 3000 zeros, ~11σ) and "J₋₁ ≈ 0.95 …
supportive". The v2 receipt (10,000 zeros, ±1.79e−5, TOO EARLY) supersedes
both. Worth syncing that file so the next reader does not re-import v1.

### Open decisions for the owner

1. **Length.** This is a long letter. If it should be shorter, §3 can be
   compressed to two sentences plus "details in the attached memo"
   (`08_CORRECTION_AND_REDLINE_MEMO.md`) — that is the intended attachment
   anyway.
2. **Tone on §3(i).** Telling a senior collaborator his main theorem is not yet
   proved as stated, days after he announced an Inventiones submission, is the
   hardest sentence here. It is written as "I would rather we publish the
   two-parameter theorem we can defend". Softening further would mean not
   really saying it.
3. **The last parenthesis in §7** (boundary identity / prior art) is optional.
   It is honest and it was already planned in the 1 Aug draft, but it does add
   a second "no" to a paragraph whose job is to say yes.
4. Attachments to name explicitly if sending: the compiled spectral-section
   preview, the redline memo, the contribution statement, the disclosure.
