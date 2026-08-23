# SCAT-1 divisor gate check — literature verification

**Status: UNREFEREED.** Date 2026-08-23. Lane G. Scope: discharge (or refuse to
discharge) the single `TODO-VERIFY` gate of
`SCAT1_PHIQ_ZERO_CERTIFIER_SOL.md` §3.3 — the Selberg-zeta divisor theorem for
a cofinite Fuchsian group with elliptic elements and one cusp, scalar trivial
character, in the precise form used by Lemma 3.1 step (i):

> The nonreal zeros of `Z_Γ` in `0 < Re s < 1/2` are exactly the poles of the
> scattering determinant `φ`, with matching multiplicity; every spectral zero
> lies on `Re s = 1/2` or on the real segment, and every identity / elliptic /
> parabolic trivial divisor point is real.

## (a) Exact statements found

### Primary pinned source — FJS, verbatim against a sha-receipted PDF

**Friedman–Jorgenson–Smajlović**, *Super-zeta functions and regularized
determinants associated to cofinite Fuchsian groups with finite-dimensional
unitary representations*, arXiv:2011.12795 (the "FJS" of the PGT-1 lane).
Verification chain: `/tmp/fjs.pdf` present on this machine,
`shasum -a 256` = `36c9d020…7228`, matching the banked receipt at
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:380` and the PGT-1 referee's
check #1. All quotations below re-extracted by me from `/tmp/fjs.txt`
(pdftotext of that PDF; note the known mangling `21` = `1/2`).

Setting (abstract, line 10 of the extraction): finite-volume non-compact
hyperbolic quotient, "possibly with elliptic fixed" points — an orbifold.
Scalar trivial character = the `h = 1`, `χ = 1` case; one cusp ⇒ `k = 1`.

**Divisor of `φ(s)`** — §2.4, sourced to "[23, pp. 59–60]" = Venkov,
*Spectral theory of automorphic functions* (Trudy Mat. Inst. Steklov
translation). Six items; the only nonreal ones are

- item 5: "Poles of the form 1 − ρ and 1 − ρ̄" with `Re(ρ) > 1/2`, `Im(ρ) > 0`;
- item 6: "Zeros of the form ρ and ρ̄" with `Re(ρ) > 1/2`, `Im(ρ) > 0`.

Items 1–4 are finitely many real zeros/poles. So **every nonreal pole of φ
lies in `Re s < 1/2`** and is the reflection `1 − ρ` of a nonreal φ-zero ρ in
`Re s > 1/2`; this is the `φ(s)φ(1−s) = 1` bookkeeping (FJS eq. before §2.5;
Venkov Thm 3.5 is the cited continuation/functional-equation source).

**Divisor of `Z(s)`** — §2.5, sourced to "[24, p. 49]" (Venkov,
*Spectral theory of automorphic functions and its applications*) and
"[12, p. 499]" (**Hejhal, LNM 1001 Vol. II**). Seven items, re-extracted in
full:

1. zeros at `s_j` on `Re s = 1/2` and in `(1/2, 1]` (discrete spectrum), each
   "multiplicity m(s_j) = m(λ_j)";
2. zeros at `s_j ∈ [0, 1/2)` (small discrete eigenvalues, real), multiplicity
   `m(λ_j) − q(1−s_j) ≥ 0`;
3. the point `s = 1/2`, order `a = 2d_{1/4} − k/2 − tr Φ(1/2)/…` (real);
4. poles at `s = −n − 1/2`, multiplicity `k` (real);
5. finitely many real zeros `1 − ρ_i < 1/2` (real);
6. "Zeros at each s = 1 − ρ, 1 − ρ̄ where ρ is a zero of φ(s)" with
   `Re(ρ) > 1/2`, `Im(ρ) > 0`;
7. zeros at `s = −n`, `n = 0, 1, 2, …`, with explicitly displayed
   identity-plus-**elliptic** multiplicities (the `d_R`-sum) — real axis only.

**Item 6 is the sole source of nonreal zeros off `Re s = 1/2`**, and they all
lie in `Re s < 1/2` (reflections of φ-zeros from `Re s > 1/2`). This is the
same conclusion the PGT-1 referee's check #4 recorded (see (f) below).

### Secondary — Hejhal LNM 1001 Vol. 2

FJS cite the `Z`-divisor to Hejhal LNM 1001 **p. 499** (and `q(σ_i) ≤ k` to
"[12, Eq. 3.33 on p. 299]"). The gate's own pointer "Theorem 5.3" could NOT be
page-verified: the repo's only Hejhal scan is
`lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf` (section 7 only,
pp. 568–600), which does not contain the divisor theorem, and no full copy of
the book is on hand. The theorem NUMBER therefore remains unpinned; the
theorem STATEMENT is pinned through FJS's p. 499 citation plus the verbatim
FJS list above. Venkov 1979 (`/tmp/venkov1979.pdf`) is an image-only scan;
pdftotext yields nothing, so its Theorem 3.5 page is likewise not
independently re-read here (same standing as the LAW note's Venkov-citation
caveat, `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:466-470`).

## (b) Multiplicity

Covered — but by a two-step derivation from pinned statements, not by one
verbatim sentence. Adversarial detail: FJS `Z`-divisor item 6 does **not**
print a multiplicity clause. The matching is nevertheless forced by FJS §3.3
(Definition 3.8 and the line following it), all verbatim in the extraction:

- `Z_+ = Z / (G_1(s) Γ(s−1/2)^k)` (trivial identity/elliptic/parabolic
  factors removed — all real-axis divisor), `Z_− = Z_+ φ`;
- the zero set of `Z_+` is listed with multiplicities for items 1–3, item 4
  being the `1−ρ` reflected zeros; and
- "N(Z_−) = 1 − N(Z_+) … s is a zero of Z_+ if and only if 1 − s is a zero,
  necessarily with the same multiplicity, of Z_−."

Derivation of Lemma 3.1(i) with multiplicity: let `Z(s*) = 0`, `Im s* ≠ 0`,
`0 < Re s* < 1/2`, order `m`. The trivial factors are nonvanishing there, so
`ord Z_+(s*) = m`. By the quoted symmetry, `ord Z_−(1−s*) = m`. In
`Re s > 1/2` off the real axis `Z_+` has no zeros (items 1–3 real or on-line;
item 4 lands in `Re < 1/2`), so `ord Z_+(1−s*) = 0`, hence
`ord φ(1−s*) = ord Z_−(1−s*) − ord Z_+(1−s*) = m`: φ has a zero of order `m`
at `ρ = 1−s*`, and by `φ(s)φ(1−s) = 1` a pole of order `m` at `s*`. This is
exactly Lemma 3.1 steps (i)+(ii), multiplicity included — in fact it delivers
Claim 3.2's φ-zero directly.

## (c) Orbifold / elliptic elements (G_5 has them)

Covered explicitly. FJS's standing hypothesis allows elliptic fixed points
(abstract; §1 notes the extra elliptic considerations; §3.1 is titled "The
trivial zeros stemming from the identity motion and elliptic elements"). The
elliptic contribution enters ONLY through the `s = −n` trivial zeros of
`Z`-divisor item 7 (the `d_R`-sum), i.e. on the real axis — precisely the
fact §3.3 of SCAT-1 asked to pin. No torsion-free hypothesis anywhere in the
divisor lists.

## (d) Scalar φ vs determinant φ, one cusp

Immaterial here. FJS's `φ(s)` is the determinant of the automorphic
scattering matrix `Φ(s)`; for one cusp and trivial (scalar) character the
matrix is `1×1` and the determinant IS the scalar scattering coefficient —
Hejhal (7.5) in the banked §7 scan writes that scalar directly for `G_N`, and
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` §3 already identifies the two
(`k = κ = 1`). No determinant-vs-entry gap can open with `k = 1`.

## (e) VERDICT

**DISCHARGED-modulo-page-check.**

- The full divisor statement (orbifold, elliptic allowed, one cusp, scalar φ,
  nonreal off-line `Z`-zeros = reflected φ-zeros = φ-poles, multiplicity
  matched via §3.3) is pinned verbatim against the sha-receipted FJS PDF
  (hash matches the repo bank). Lemma 3.1(i) follows with no unquoted input.
- The two residues keeping this short of a bare DISCHARGED: (1) the
  multiplicity step is a two-line derivation from FJS Def 3.8 + the
  "same multiplicity" sentence, not a single printed sentence; (2) the
  gate's named primary "Hejhal LNM 1001 Vol. 2, Thm 5.3" was not opened —
  FJS's citation is to **p. 499** of that volume (and Venkov p. 49 / pp.
  59–60), so the theorem-number-and-page confirmation in Hejhal/Venkov
  themselves remains the one outstanding page-check. Nothing load-bearing
  depends on the number: the statement itself is pinned.

**Single most load-bearing citation:** Friedman–Jorgenson–Smajlović,
arXiv:2011.12795, §2.4–§2.5 and §3.3 (divisors of `φ` and `Z`, completed
zeta symmetry), citing Venkov (Trudy Steklov transl., pp. 59–60; book p. 49)
and Hejhal LNM 1001 Vol. II, p. 499.

## (f) Relation to the PGT-1 referee's item 6

`PGT1_EXPLICIT_FORMULA_COROLLARY_REFEREE.md` checks #2–#4 already extracted
the same FJS `Z`-divisor item 6 and `φ`-divisor item 5 verbatim from the same
sha-receipted PDF, and its check #4 verified that item 6 is the ONLY source
of nonreal off-line `Z`-zeros and that they lie in `Re s < 1/2`. That is the
SET-level content of SCAT-1's gate — the same statement, so the gate is
already 80% discharged by the sibling note. What PGT-1's extraction does NOT
carry is (i) the multiplicity matching (its item 6 quote has no multiplicity
clause; SCAT-1's Lemma 3.1 needs order `m`) and (ii) the explicit
elliptic-coverage receipt. Both are supplied above from FJS §3.1/§3.3. So:
SCAT-1's gate = PGT-1's item 6 statement PLUS multiplicity PLUS the orbifold
hypothesis check; PGT-1 alone discharges the weaker, multiplicity-free form.
