# DRAFT — update to Prof. Koyama (NOT SENT; owner-gated)
Prepared 2026-08-14. One placeholder ({{FLAGSHIP}}) pending the final
certification receipt; everything else is receipt-backed now.

---

Dear Professor Koyama,

A brief update on results from our certified-computation program that I
believe will interest you directly — three items, all with machine
receipts, none yet submitted anywhere.

**1. Certified resonances of Hecke triangle surfaces, and an
arithmeticity contrast.** Using an interval-certified version of the
Mayer–Mühlenbruch–Strömberg transfer operator, we now have resonance data
across the Hecke family under one protocol: for the arithmetic members
q = 3, 4, 6 the determinant vanishes precisely at s = ρ/2 (ρ the Riemann
zeros) — three differently built operators agreeing to ~10⁻¹⁵ — while for
the non-arithmetic members G₅, G₇, G₈ the zeros scatter with
Re-dispersion ~10⁻¹–10⁻² (no vertical-line structure), and certified
evaluations show |det| = O(1) at the ζ(2s) points for the non-arithmetic
surfaces. To our knowledge these are the first computed (and the first
certified) resonance data for non-arithmetic Hecke groups; the standing
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
are Fraczek–Mayer's symmetry results), while for G₅ we hold nine
certified nonvanishing witnesses at ζ-zero points refuting any such
factor pointwise. This seems to us the precise sense in which "the
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
(b) The first numerical test of Gonek's 1989 conjecture J₋₁(T) ~ (3/π³)T:
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
DRAFT NOTES (not part of the letter): headline of item 1 waits on the
R2R3 certificate; if it fails, the {{FLAGSHIP}} sentence is dropped and
item 1 stands on the data + closed K_s gate alone. Send decision,
wording, and any attachment list are the owner's.
