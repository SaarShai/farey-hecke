# DRAFT — update to Prof. Koyama (NOT SENT; owner-gated)
Prepared 2026-08-14; flagship paragraph filled 2026-08-15 after the
theorem was declared (V8 THEOREM-GRADE YES). Everything below is
receipt-backed. A further independent audit (Kimi K3) is in progress;
hold send until it reports.

---

Dear Professor Koyama,

A brief update on results from our certified-computation program that I
believe will interest you directly — three items, all with machine
receipts, none yet submitted anywhere.

**1. Certified resonances of Hecke triangle surfaces, and an
arithmeticity contrast.** Using an interval-certified version of the
Mayer–Mühlenbruch–Strömberg transfer operator, we now have resonance data
across the Hecke family under one protocol: for the arithmetic members
q = 3, 4, 6 the determinant vanishes at s = ρ/2 (ρ the Riemann zeros) —
at ~10⁻¹⁴ for q = 3 and ~10⁻¹¹–10⁻¹² for q = 4, 6, under per-surface
protocols — while for the non-arithmetic members G₅ and G₇ the zeros
scatter with Re-dispersion ~10⁻¹–10⁻² (no vertical-line structure; our
G₈ sample is currently too small to include in that claim), and
certified evaluations show |det| = O(1) at the ζ(2s) points for the
non-arithmetic surfaces. To our knowledge these are the first computed
(and the first certified) resonance data for non-arithmetic Hecke
groups; the standing
literature (Bruggeman–Pohl) leaves them conjectural. And the headline: we now have a
computer-assisted THEOREM — the first rigorous localization, to our
knowledge, of an off-line resonance of a non-arithmetic finite-area
hyperbolic surface. G₅ has a Selberg-zeta zero s* with
|s* − (0.4538951800749447 + 5.7635372417301305 i)| ≤ 10⁻⁶ in each
coordinate, hence Re(s*) ≤ 1/2 − 0.046. Every numerical constant is an
interval-arithmetic certificate (384-bit Arb, replayable receipts), the
abstract chain's joints are machine-proved in Lean, the K_s divisor is
fully resolved (closed-form zero lattice Re(s) = −n ≤ 0,
machine-verified), and the whole argument survived five rounds of
internal adversarial review, including two independent reproductions of
the key constants. We would value your reaction on the statement's
framing before we circulate anything.

**2. A factorization dichotomy behind the contrast.** We are pursuing,
and would value your judgment on, the mechanism statement: at the
transfer-operator level the arithmetic members' determinants should carry
an explicit ζ(2s) factor (the q = 3 case is Mayer's theorem; for q = 4, 6
we found no published operator-level factorization — the closest tools
are Fraczek–Mayer's symmetry results), while for G₅ we hold three
nonvanishing witnesses at ζ-zero points (nine across G₅, G₈, G₁₀;
each certified modulo a truncation-tail heuristic we state explicitly)
refuting any such factor pointwise. This seems to us the precise sense in which "the
critical line is an arithmetic phenomenon" inside this family — very much
adjacent to your Selberg-zeta work, hence this note. Two fresh pieces of
evidence on the positive side: the q = 4 branch system, conjugated to the
Fricke group Γ₀⁺(2), has all its first-return words in Γ₀(2) with exactly
the modular 2s-cocycle (verified symbolically through word length 4), and
all four certified q = 4 determinant zeros we tested vanish
simultaneously in the Fraczek–Mayer level-2 modular vector operator
(to 10⁻¹⁷–10⁻²⁹, with order-one off-zero controls) — consistent with the
q = 4 operator embedding as a block of the level-2 modular one.

**3. Two numerical firsts in the Mertens direction.** (a) The constant
Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) — the conjectural limiting mean square of
x^{-1}Σ_{n≤x} M(n)² under RH + Gonek–Hejhal (Ng 2004) — computed for what
appears to be the first time: 0.02903 ± 0.00016 (3000 certified-residual
zeros; an extension to 10⁵ zeros targeting 4–5 digits is running). This
refutes an internal conjecture of ours (2/π²) and excludes 3/π⁴ at ~11σ.
(b) The first numerical test of Gonek's conjecture J₋₁(T) ~ (3/π³)T
(as recorded by Ng 2004):
at T ≈ 10⁴ we find J₋₁(T)/T ≈ 0.95 · (3/π³), slowly drifting — supportive
but not yet asymptotic; the 10⁵-zero extension will sharpen it.

On the joint prime-bias manuscript: our technical pre-reply packet
(theorem audit, character-orthogonality certificate, the 3×10¹⁴ spectral
transient analysis) is assembled separately and unchanged by the above.

All computations carry receipts (interval arithmetic where claimed,
scripts, checksums), and the negative results are documented with equal
care. We would welcome your reaction, particularly on item 2.

With best regards,
Saar

---
DRAFT NOTES (not part of the letter): the item-1 headline is now backed
by the declared theorem (THEOREM_G5_OFFLINE_ASSEMBLY.md v2; R3b winding
certificate; R5 v3.1 determinant identification; adversarial rounds
V4–V8). Item 3's 10^5-zero extension is still running on Kaggle (parts 1–3;
parts 4–5 harvested — 11 of 36,001 rows failed a monotonicity gate and
are being re-refined with seed-validated receipts before any sum is
computed). Kimi K3 audit REPORTED 2026-08-15: theorem STANDS; this
letter's three factual overstatements (nine-vs-three witnesses, G₈
inclusion, 10⁻¹⁵ agreement) were found by it and are now corrected in
the text above. Send decision, wording, and any attachment list are the
owner's.
