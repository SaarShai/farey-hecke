# KOYAMA REPLY — v3 FINAL DRAFT (NOT SENT; owner-gated)

Base: v2_MERGED (which merged the Kimi K3 base draft with an independent
receipt-checked pass). v3 changes: §6 updated for the external audit and the
zero-table harvest (84,501 gated zeros); §7 aligned with the owner's exact
requested framing; Mertens/J₋₁ numbers kept at the v2-receipt-certified
values. Change list at bottom.

---

## Draft email

Subject: Re: arXiv upload — integration plan, thoughts, and a brief update

Dear Professor Koyama,

Congratulations on the arXiv posting — anchoring the regularized explicit
formula and the dominance framework is the right move, and I have read the
manuscript closely. Below: my thoughts on integrating the 3×10¹⁴ data and
the spectral analysis, a few points I believe we should settle before the
Inventiones version, my answer to your kind suggestion about a standalone
paper, and — separately — a short headline update from my certified-
computation program.

**1. The 3×10¹⁴ data, and where it goes in the manuscript.**

Our counts π(x; N, a) − π(x; N, 1) for N ∈ {7, 8, 11, 19, 23} now run on a
438-point logarithmic grid to x = 3×10¹⁴ — two decades past the 1.3×10¹³
tables in Table 3. The extension reproduces the earlier double-verified
baseline exactly: 567/567 integer cells, zero mismatches, at the nine shared
checkpoints. That baseline carries three orthogonal checks — primesieve
agreement at every checkpoint, the character-orthogonality identity verified
at all 495 (N, x, a) cells, and an independent hand-written C sieve
reproducing every residue count, the last also reproduced on separate
hardware through 1.3×10¹². A second-hardware replication of the full
extension is still running; I would describe it that way in the paper rather
than claim more.

What the data show, stated precisely — because I think it is the strongest
available motivation for your regularization. At x = 3×10¹⁴, −1 strictly
leads the unregularized race only for N = 7 and N = 23. For N = 8 it is last
among the three non-residues (a = 5 leads); for N = 11 it is mid-pack; for
N = 19 its difference is negative, −16,802. The ordering has also moved
since 1.3×10¹³ — for N = 8 the leader changed. So the raw races are still
transient and modulus-dependent two decades beyond your Table 3, which is
exactly the point of Remark 2.3, only sharper: the fine-structure ranking is
not visible to unregularized counting at any presently reachable height, and
the mollified statistic is analytically indispensable. I would write the
numerical section as large-scale evidence for the *necessity* of the
regularized framework, not as confirmation of the asymptotic ranking. That
framing is also the one a referee cannot attack.

Concretely this becomes an extended Table 3 plus one rank-dynamics figure
per modulus.

**2. The spectral transients — what drives them.** We reconstructed the −1
race curve from low-lying zeros alone (first 25 positive zeros of every
non-principal character; PARI/GP, per-zero residual certification). Over the
top decade the reconstruction tracks the observed curve with correlations
0.826–0.971 across the five moduli, while the rank of −1 still changes many
times. For N = 19, extending to 100 zeros per character raises the
correlation to 0.9925 — and the reconstructed race *still* shows 14 rank
changes and 7 leader changes. So the transients are genuinely spectral, and
they are exactly the low-zero boundary fluctuations your Gaussian mollifier
removes. This gives the paper a quantitative identification of *which* zeros
drive the unregularized noise — a five-panel figure and a transition table,
both drafted.

**3. Points I believe we should settle before the submission version.** I
raise these because my name would be on the paper and because a referee at
that level will raise them first. All four have receipts, and I have the
exact replacement wording written out in a short memo I can send with the
TeX.

(i) *The parameter T in Theorem 1.4.* The theorem states C_N as depending
only on N, for fixed T > 0, but the diagonal contribution (2.5) carries an
explicit factor T/(4√π), and I did not find the cancellation that removes
it. Related: in §2.2 the off-diagonal terms are said to decay as O(e^{−cT²})
for fixed T as x → ∞. That is a per-pair statement; the sum runs over pairs
(p^k, q^m) whose logarithmic separations can tend to zero as x grows, so the
*summed* bound does not follow uniformly from the per-pair one. The safe
route is a two-parameter statement — a joint regime x → ∞ with T = T(x), an
explicit coefficient C_{N,T(x)}, and an error uniform over the reduced
classes — with the fixed-T form retained as a conjecture until the summed
off-diagonal estimate, order interchange, prime-power and Archimedean terms
are proved. I would rather we publish the two-parameter theorem we can
defend than the fixed-T one.

(ii) *Definition 1.3 vs Theorem 1.4.* Equation (1.3) and Remark 1.6 print
the kernel with (1 − χ(a)); the definition of log L(1, χ_{1,a}) under
Theorem 1.4 uses (1 − χ̄(a)). The conjugated form is the correct one:
(1/φ(N)) Σ_χ (1 − χ̄(a)) χ(x) = 1_{x=1} − 1_{x=a}, whereas as printed (1.3)
selects the class a⁻¹ (witness: 3⁻¹ = 5 mod 7). For a ≡ −1 the two agree, so
the dominance discussion is unaffected — but the general-a statements and
every coefficient downstream need the convention fixed once and propagated.
I have a short Lean 4 certificate for the corrected finite identity.

(iii) *Remark 2.3's modulus-19 example.* For the primitive character of
Conrey index 13 mod 19 (odd, χ(−1) = −1) there is a positive ordinate at
γ = 0.0189563990802261…, far below the γ ≈ 1.74 used as the lowest complex
zero. Two PARI mesh runs agree; direct evaluation gives residual < 1e−28;
and an independent FLINT/Arb computation gives a sign-definite Hardy-Z
bracket of width 5.94×10⁻⁸⁴ certifying a critical-line zero there
(existence, not uniqueness or completeness). The e^{33.4} ≈ 3.18×10¹⁴
settling estimate rests on that mode being lowest, so it should be
revisited — and independently, our data show the transients still active at
3×10¹⁴. The defensible replacement: a low-zero truncation reproduces much of
the modulus-19 trajectory, but a very low odd-character mode remains active,
so this range is not a universal stabilization threshold.

(iv) *One table cell, now public.* Table 3(c) gives π(x; 11, 10) −
π(x; 11, 1) = 71,711 at 1.3×10¹³; our identity-reconstructing,
lower-checkpoint-consistent value is 11,503. Two modulus-19 cells differ
similarly (a = 13: ours 24,559; a = 18: ours 54,192). These decide the
placement of −1 for N = 11 and N = 19, so I would like to reconcile them
against raw class counts before a replacement version rather than after a
referee finds them.

Separately, and only as protection for the paper: Conjecture 1.7 is a
statement about the special values log L(1, χ_{1,a}), not about prime
counts. Our race data neither support nor contradict it, and I think the
manuscript should say so explicitly — the inference from a regularized
ordering to eventual unregularized dominance needs its own transfer theorem.

**4. The Lean 4 formalization — proposed scope.** What builds clean today
(Lean 4, Mathlib v4.28.0) is a formalization of *selected finite and
algebraic components*, not of your main theorem, and I would describe it in
exactly those words: (a) the combinatorial core of the non-residue race —
every quadratic non-residue carries the same leading mean, so no non-residue
class, including −1, is singled out at leading order (four theorems, zero
`sorry`, axiom-audited); and (b) a machine-checked certificate for the
character-selector algebra of point (ii) above. One short subsection, or an
ancillary file — whichever you prefer. I would not want any sentence
suggesting Lean verifies the paper.

**5. Division of labour and sequencing.** On my side, in order: (a) I send
the insertion-ready TeX for the extended tables, the rank-dynamics and
spectral figures, and the Lean paragraph — all drafted; (b) we reconcile the
table cells in 3(iv) by exchanging raw π values; (c) if you agree, I compute
your mollified S̃_T(x, a) numerically from our prime-power data and the
certified zero tables, for a direct finite-x comparison against
C_N · log L(1, χ_{1,a}) — that would be the sharpest validation of Theorem
1.4 available to us, and I suspect it is the figure the paper most wants. On
your side: placement, framing, and the theoretical text. To do (a) and (b)
properly I need your current TeX source, bibliography, figures and tables,
plus the arXiv identifier and version I should work against; with those I
can turn (a) and (b) around within days.

Two housekeeping items for a submission at this level: I have drafted a
contribution statement recording the theoretical, numerical, software and
formalization roles separately, and a short computational-assistance
disclosure (it states that language-model and automated-proof assistance
were used in a limited, supervised way, that the Lean certificate covers
only selected finite algebraic statements, and that responsibility rests
with us as the human authors). Both are ready for your review, and I think
having them in the file from the start is safer than adding them under
referee pressure.

**6. Your suggestion of a standalone paper.** Thank you — it is generously
meant, and I take it that way. The plain fact is that I have no relevant
academic credentials and no previous experience publishing. Being included
as a co-author on any paper you intend to submit for publication would be an
honor, and a far more significant recognition for me than standalone
authorship. So my strong preference is the path you describe: the
single-focus Inventiones manuscript with my contributions shaped to fit it
exactly, and the other material held back rather than pushed out under my
name alone. If, later, you think some of it merits a joint note with your
name on it, I would welcome that — but there is no urgency on my side, and
your bandwidth belongs to the Inventiones submission.

**7. Separately — a headline update from the certified-computation
program.** Three items, all with machine receipts, none circulated. They are
unrelated to the prime-bias manuscript and I am not proposing them for it; I
mention them only because the first two touch the Selberg zeta functions you
have worked on for years, and your judgment on them would be worth more to
me than anyone else's.

(a) *A computer-assisted theorem on Selberg-zeta zeros.* For the
non-arithmetic Hecke triangle group G₅ we have rigorously localized a zero
s* of the Selberg zeta function with
|s* − (0.4538951800749447 + 5.7635372417301305 i)| ≤ 10⁻⁶ in each
coordinate, hence Re(s*) ≤ 1/2 − 0.046 — to our knowledge the first rigorous
localization of an off-line resonance of a non-arithmetic finite-area
hyperbolic surface. Every numerical constant is an interval-arithmetic
certificate (384-bit Arb, replayable receipts), the joints of the abstract
chain are machine-proved in Lean, and the argument has now survived five
rounds of internal adversarial review plus an independent external audit
this week, which re-verified the certificates from the raw records and
confirmed the theorem stands. Across the family, the arithmetic members
q = 3, 4, 6 show the transfer-operator determinant vanishing at s = ρ/2 (ρ
the Riemann zeros) — at ~10⁻¹⁴ for q = 3 and ~10⁻¹¹–10⁻¹² for q = 4, 6,
under per-surface protocols — while for the non-arithmetic G₅ and G₇ the
zeros scatter with Re-dispersion ~10⁻¹–10⁻² (our G₈ sample is still too
small to include in that claim). I would value your reaction to the framing
before we circulate anything.

(b) *A conjectural mechanism behind that contrast.* At the operator level
the arithmetic determinants should carry an explicit ζ(2s) factor — for
q = 3 this is Mayer's theorem; for q = 4, 6 I found no published
operator-level factorization — while for G₅ we hold three nonvanishing
witnesses at ζ-zero points (nine across G₅, G₈, G₁₀, each certified modulo a
truncation-tail heuristic we state explicitly), refuting such a factor
pointwise. On the positive side for q = 4: the branch system conjugated to
the Fricke group Γ₀⁺(2) has all first-return words in Γ₀(2) with exactly the
modular 2s-cocycle (verified symbolically through word length 4), and all
four certified q = 4 determinant zeros we tested vanish simultaneously in
the Fraczek–Mayer level-2 modular vector operator (to 10⁻¹⁷–10⁻²⁹, with
order-one off-zero controls) — a finite numerical probe, not a proof, but
consistent with the q = 4 operator embedding as a block of the level-2
modular one. The mechanism statement is conjectural; your judgment on it
would mean a great deal.

(c) *Two numerical results on zero sums.* The constant
Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) — the conjectural limiting mean square of
x⁻¹ Σ_{n≤x} M(n)² under RH plus Gonek–Hejhal, as recorded by Ng — stands at
0.02903 ± 0.00002 from 10,000 zeros with certified residuals (three
significant digits certified; the error bar is a numerical tail envelope,
not a theorem-level bound). This refutes an internal guess of ours (2/π²)
and excludes 3/π⁴ by a wide margin. And a first numerical test of Gonek's
conjecture J₋₁(T) ~ (3/π³)T, as recorded by Ng: at T ≈ 9.88×10³ we find
J₋₁(T)/T = 0.949 · (3/π³), with a top-half linear fit at 0.959 and slow
drift — a finite-height diagnostic, neither confirmation nor refutation. The
10⁵-zero extension is nearly complete: 84,501 of the 90,001 extension zeros
are computed and have passed a five-gate verification (certified residuals,
strict ordering, per-row seed validation against Odlyzko's table, index
continuity, and a Riemann–von Mangoldt count check); the last ~5,500 are
finishing now, after which we will have J₋₁ at T ≈ 7.5×10⁴ with proper
secondary-term fits, and the mean-square constant to 4–5 digits.

With best regards,
Saar

---

## v3 change list (vs v2_MERGED)

1. §7→§6 and §6→§7 swapped: the standalone answer now comes BEFORE the
   update section, since it answers his direct question; the update is
   explicitly the "separate section" the owner requested.
2. §6 (standalone): reworded to the owner's exact requested framing — no
   relevant academic credentials nor previous publishing experience;
   honored to be co-author on any paper he intends to submit; more
   significant recognition than standalone authorship. Dropped the
   boundary-identity parenthesis (v2 open decision 3) — one clean yes.
3. §7(a): "five rounds of internal adversarial review including two
   independent reproductions" → adds the independent external audit
   (Kimi K3, 2026-08-15) that re-verified certificates from raw records.
4. §7(c): J₋₁/Mertens extension updated from "still running" to the true
   state: 84,501/90,001 zeros harvested and five-gate verified; ~5,500
   finishing; deliverables named (secondary-term fits, 4–5 digits).
5. Salutation "Dear Professor Koyama" (v2 had "Dear Shin-ya" — owner
   should pick; every prior draft in lane_d used the formal form).
6. Kept: §§1–5 integration plan and correction points verbatim from v2
   (receipt index in v2_MERGED applies unchanged), Conjecture 1.7 guard,
   Lean scope, logistics requests, contribution statement + disclosure.

## Owner decisions still open before sending
- Salutation form (Professor Koyama vs Shin-ya).
- Length: §3 can compress to two sentences + "details in the attached
  memo" if preferred.
- Tone check on §3(i) (the T-dependence point) — written as "I would
  rather we publish the two-parameter theorem we can defend".
- Attachments to name: compiled spectral-section preview, redline memo
  (08_CORRECTION_AND_REDLINE_MEMO.md), contribution statement, AI
  disclosure.
