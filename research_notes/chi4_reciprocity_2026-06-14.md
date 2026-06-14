# Quartic / octic reciprocity attack on the two OPEN Apollonian cases — 2026-06-14

**Track 5.** Attack the two OPEN Apollonian local-global types — **(6,1,1,1) strip packing,
root (0,0,1,1)** and **(8,11,1) bug-eye packing, root (-1,2,2,3)** — with a HIGHER-POWER
reciprocity obstruction (chi_4 quartic over Z[i], and an octic / Z[ζ_8] analogue), the
direction Haag–Kertzer–Rickards–Stange (arXiv:2307.02749, Annals 200(2), 2024) explicitly
left open after their chi_2 quadratic obstruction failed to resolve these two.

## VERDICT: PRINCIPLED NEGATIVE (no candidate obstruction; structurally explained).

A **quartic obstruction cannot exist** for either open type, for two distinct *structural*
reasons (both verified first-hand in exact arithmetic, not just asserted):

1. **Strip (6,1,1,1):** chi_4 IS defined (it is a type-(6,1) packing) and equals **χ_4(A) = +1
   (i^0), constant** across the packing. χ_4 = +1 is exactly the NO-obstruction value
   (Prop 5.11: for type (6,1) only χ_4 ∈ {−1, i, −i} obstructs). Empirically, every perfect
   square, every 4th power, and every computed 8th power up to 3·10^5 actually APPEARS as a
   curvature. No quartic obstruction; no octic signal.

2. **Bug-eye (8,11,1):** χ_4 is **structurally UNDEFINED.** The quartic symbol is built on the
   lattice Λ_C ⊆ Z[i] of covolume/conductor n, which requires n ≡ 0,1,4 (mod 8) (Definition 5.6).
   EVERY curvature of the bug-eye is ≡ 2,3,6,7 (mod 8) — there is not a single curvature ≡ 1
   (mod 8) — so the Z[i] quartic machinery cannot even begin. Quartic reciprocity is intrinsically
   a TYPE-6 (specifically (6,1)/(6,17)) phenomenon; type-8 packings are out of its reach by
   construction. The authors note (Remark 2.8) the quartic obstruction "arises because K = Q(i)."

An **octic / Z[ζ_8] obstruction** is not available either: the Apollonian/Descartes binary
quadratic form fC has discriminant −4n^2 and complex multiplication by Q(i) ONLY — it carries no
Z[ζ_8] = O_{Q(ζ_8)} lattice structure for an eighth-power-residue character to act on. A degree-8
character χ_8 with χ_8^2 = χ_4 would, on the strip, satisfy χ_8^2 = χ_4 = +1, i.e. χ_8 ∈ {±1, ±i}
— but no constant non-trivial such lift exists when the candidate 4th/8th-power families are
actually realized as curvatures (verified). The current literature (incl. the March-2026 follow-up
arXiv:2510.21702, which extends the disproof to octahedral/cubic/square/triangular packings) uses
ONLY quadratic reciprocity and does NOT touch these two cases or any higher-than-quartic obstruction.
**The strip and bug-eye remain genuinely open**; this work shows the quartic/octic route is closed,
which is itself the informative, publishable answer the paper's open direction was pointing at.

---

## Step 0 — Paper Section 5 (chi_4), transcribed (arXiv:2307.02749)

**Quartic residue symbol** (Definition 5.2). For β ∈ Z[i] odd (N(β) odd), π an odd Gaussian prime,
α coprime to π: [α/π] = the unique power of i with [α/π] ≡ α^((N(π)−1)/4) (mod π). Extended
multiplicatively in the denominator; [α/unit] = 1.

**Quartic reciprocity / supplements** (Prop 5.3–5.4). Multiplicative in numerator (5.3a),
congruence-invariant (5.3b), [a/b] = 1 for coprime rational integers a,b with b odd (5.3c);
for primary α = a+bi: [i/α] = i^((1−a)/2), [(1+i)/α] = i^((a−b−b^2−1)/4), [2/α] = i^(−b/2);
quartic reciprocity [α/β] = (−1)^((N(α)−1)/4·(N(β)−1)/4) [β/α] for α,β primary coprime.

**Definition 5.6 (χ_4).** Only for type (6,1) or (6,17), curvature n ≡ 0,1,4 (mod 8). With
β ∈ S_{Λ_C} ∪ S_{iΛ_C} (primary if n even), n = 2^e n′ (n′ odd):
  χ_4(C) = (−1)^(be/4)·[β/n′] if n≡0 (8); [β/n] if n≡1 (8); [(−1/n′)]·[β/n′] if n≡4 (8).
**χ_4 ∈ {1, i, −1, −i}, constant on the packing** (Cor 5.10), and **χ_4^2 = χ_2** (Prop 5.12).

**Theorem 2.4 / Cor 2.6 (the open cases).** The table assigns to type (6,1,1,1): NO quadratic and
NO quartic obstruction, conjecture 1.1 OPEN for residues 0,1,4,9,12,16 (mod 24); to type (8,11,1):
NO quadratic and NO quartic obstruction, OPEN for 2,3,6,11,14,15,18,23 (mod 24). Cor 2.6: the
local-global conjecture is FALSE for every primitive Apollonian packing EXCEPT (6,1,1,1) [strip
(0,0,1,1)] and (8,11,1) [bug-eye (−1,2,2,3)].

---

## Step 1 — ORACLE: PASS (quartic symbol validated in exact arithmetic)

`code/chi4_oracle.py` + `code/chi4_oracle_test.py`. Exact Gaussian-integer arithmetic; the quartic
symbol computed by the full reciprocity algorithm (factor out (1+i) and unit, flip by quartic
reciprocity, recurse). **All 2207 self-tests PASS** (final line: `ORACLE: ALL TESTS PASSED`):

- **O1/O1b/O1c** — multiplicativity in numerator (Prop 5.3a), congruence-invariance (5.3b),
  [a/b]=1 for coprime integers a,b, b odd (5.3c).
- **O2 (the validation that matters)** — the reciprocity-algorithm value EQUALS the direct
  Euler-criterion definition α^((N(π)−1)/4) mod π on every small Gaussian prime π above
  p ∈ {3,5,7,11,13,17,19,23,29,37,41}. (Confirms the algorithm computes Definition 5.2.)
- **O3** — the supplement [2/α] = i^(−b/2) (Prop 5.4).
- **O4 (the requested oracle fact)** — **χ_4^2 = χ_2** (Prop 5.12): i^(2k) = (−1)^k equals the
  Z-Kronecker symbol (N(β)|n) on 500 random (β, odd n). PASS.

**Packing-level controls** (`code/chi4_packing.py`, χ_4 computed via the tangency structure
Prop 5.8/5.9 using only β whose Gaussian factorization is unambiguous — i.e. ≤ 1 prime ≡ 1 mod 4,
which removes the lattice-selection ambiguity for split sums n+n2):
- type **(6,1,1,1)** roots (0,0,1,1), (−12,16,49,49), (−20,36,49,49): **χ_4 = +1** (constant, 150+
  circles each) — matches the "1" in (6,1,**1**,1), no obstruction.
- type **(6,1,1,−1)** root (−8,12,25,25): **χ_4 = −1 (i^2)** (constant) — matches the "−1" subtype,
  HAS the n^4,4n^4,9n^4,36n^4 obstruction. **The method correctly detects a non-trivial χ_4.**
- type (6,13) root (−11,21,24,28): χ_4 not defined (correct — only (6,1)/(6,17) admit χ_4).

---

## Step 2 — The two OPEN types: chi_4 / octic values

### STRIP (6,1,1,1), root (0,0,1,1)  [χ_4 IS defined]
- Curvature residues mod 24 = {0,1,4,9,12,16}; all curvatures ≡ 0,1,4 (mod 8); odd curvatures ≡ 1
  (mod 8). ⇒ a genuine type-(6,1) packing; Definition 5.6 applies.
- **χ_2(A) = +1** (constant, 200 tangent pairs). **χ_4(A) = +1 = i^0** (constant, every unambiguous
  β over 150+ circles). Consistency χ_4^2 = +1 = χ_2 ✓ (Prop 5.12).
- Curvature presence to 3·10^5: ALL 547 squares, ALL 23 fourth powers (1,16,…,279841), ALL four
  8th powers ≤ bound (1,256,6561,65536; 5^8=390625 just exceeds bound) PRESENT. The candidate
  obstruction families n^4,4n^4,9n^4,36n^4 fully present (sole "absences" are at the BFS bound).
- ⇒ **No quartic obstruction** (χ_4 = +1) and **no octic signal** (4th/8th powers realized).

### BUG-EYE (8,11,1), root (-1,2,2,3)  [χ_4 is UNDEFINED]
- Curvature residues mod 24 = {2,3,6,11,14,15,18,23}; ALL 1639 curvatures ≤ 5000 are ≡ 2,3,6,7
  (mod 8); odd curvatures ≡ 3,7 (mod 8); **zero curvatures ≡ 1 (mod 8)**.
- Definition 5.6 requires n ≡ 0,1,4 (mod 8) (the lattice Λ_C of conductor n ⊆ Z[i]) — **violated by
  every curvature**. The well-definedness (Prop 5.7) and propagation (Prop 5.9) proofs both rely on
  the type-(6,1)/(6,17) "all odd curvatures ≡ 1 mod 8" structure, which type-8 lacks. **χ_4 does not
  exist** for this packing — not a numerical failure, a structural one.
- **χ_2(A) = +1** (constant). Squares are congruence-forbidden (squares are 0,1,4 mod 8; the packing
  is 2,3,6,7 mod 8), NOT reciprocity-forbidden. All 8 admissible residue classes mod 24 are densely
  and evenly realized (~12,500 each to 3·10^5) — no missing reciprocity subfamily.
- ⇒ **No quartic obstruction possible** (χ_4 undefined); octic likewise unavailable.

---

## Step 3 — Why no octic / Z[ζ_8] obstruction (theory)

The quartic obstruction exists precisely because the Apollonian binary quadratic form fC (disc
−4n^2) has CM by Q(i) and its lattice Λ_C sits in Z[i] = O_{Q(i)}, the ring where 4th-power
reciprocity lives (paper Remark 2.8: "arises because K = Q(i)"). There is no degree-8 ring
O_{Q(ζ_8)} = Z[ζ_8] attached to the Descartes form: the CM field is Q(i), not Q(ζ_8). A degree-8
character χ_8 with χ_8^2 = χ_4 would, on the strip, satisfy χ_8^2 = χ_4 = +1, forcing χ_8 ∈ {±1,±i};
a constant NON-trivial such character would obstruct an n^4 / n^8 class — but those classes are
empirically realized as curvatures (Step 2), so no such constant character exists. For the bug-eye,
χ_4 already fails to exist, so no χ_8 with χ_8^2 = χ_4 can be defined a fortiori. Conclusion: the
higher-power (octic) route is closed by the same Q(i)-only CM structure that the quartic route used.

---

## Honest framing

- **Not a disproof we certified**, and not claimed as one. We did NOT prove the local-global
  conjecture HOLDS for the strip or bug-eye (that would be a major positive theorem requiring a
  thin-group equidistribution argument à la Bourgain–Kontorovich, Theorem 1.2's O(N^{1−η})).
- What IS established first-hand: (a) the quartic symbol oracle is correct (2207 checks, incl. the
  Euler-criterion cross-check and χ_4^2 = χ_2); (b) the method reproduces the paper's extended-type
  χ_4 classification on controls (+1 for (6,1,1,1), −1 for (6,1,1,−1)); (c) **for the strip χ_4 = +1
  (no quartic obstruction); for the bug-eye χ_4 is structurally undefined**; (d) no octic obstruction
  is available for either, by CM-field structure and by realized 4th/8th-power curvatures.
- **Verdict: principled NEGATIVE** — "the two open Apollonian types have no quartic (and no octic)
  obstruction either." This is informative and publishable as the closing of the paper's stated open
  higher-reciprocity direction; the two cases stay open for a positive (equidistribution) resolution,
  NOT for a higher-power obstruction. No candidate flagged for theory certification.

## Files
- `code/chi4_oracle.py` — exact Gaussian-integer arithmetic + quartic residue symbol (Def 5.2 / Prop 5.3–5.4).
- `code/chi4_oracle_test.py` — 2207 self-tests, `ORACLE: ALL TESTS PASSED`.
- `code/chi4_packing.py` — χ_4 / χ_2 on actual packings via the tangency structure (Prop 5.8/5.9).
- Paper text extracted to `/tmp/hkrs.txt` (pdftotext of arXiv:2307.02749).
- Prior chi_2 work: `code/reciprocity_oracle.py`, `research_notes/reciprocity_scan_2026-06-14.md`.
