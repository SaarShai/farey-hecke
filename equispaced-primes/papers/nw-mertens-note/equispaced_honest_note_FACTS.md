# Equispaced Honest Note — Ground-Truth Fact Sheet

**Purpose.** Verified facts for a consolidated honest note that keeps only three
real things: (1) the Bridge Identity, (2) the Sign law *as an observation*, (3) the
certified counterexample at p = 92,173 — plus the four-term decomposition framed as
a *diagnostic* isolating the open DiscrepancyStep inequality. Everything else is cut.

**Provenance.** All `file:line` references are into the repo at
`/Users/za/Documents/Farey NOW/primes-equispaced`.
Source paper read in full: `papers/math_paper/main.tex` (2655 lines).
Canonical Lean dir: `formal-conjectures/`.

**Verification gate (NOT YET DONE).** Static analysis only. No `lake build` was run
(Mathlib cache is gone). Fresh axiom re-verification of every kept Lean theorem
(`#print axioms` == `[propext, Classical.choice, Quot.sound]`, no `sorryAx`, EXIT=0)
is **PENDING** and is a hard gate before any submission. `*_unconditional` /
`_VERIFIED` names are aspirational until re-compiled.

---

## KEEP-1 — The Bridge Identity (REAL, Lean-proved unconditionally, modulo re-verify)

**Statement (thm:bridge).** `main.tex:340-346`:
> For every prime p ≥ 2:  ∑_{f ∈ F_{p-1}} e^{2πi p f} = M(p) + 2.   (eq:bridge)

**Short proof.** `main.tex:348-355`. Decompose by denominator: boundary f=0,f=1 give
1+1=2; for 2≤b≤p−1 the inner sum over coprime numerators is the Ramanujan sum
c_b(p)=μ(b) (since gcd(p,b)=1); summing gives 2 + Σ_{b=2}^{p-1} μ(b) =
2 + M(p−1) − 1 = M(p) + 2, using M(p−1) = M(p) + 1.

**Cosine form (remark).** `main.tex:357-361`: Σ cos(2πpf) = M(p)+2; imaginary part
vanishes by f ↔ 1−f symmetry. (This is the form used as "M(p) = Σcos − 2",
`main.tex:1821-1822`.)

**Lean status — REAL, sorry-free (static).**
- `formal-conjectures/FareyBridgeIdentity.lean:197-205`
  `theorem farey_bridge_identity_unconditional (p : ℕ) (hp : Nat.Prime p) : … = (mertens p : ℂ) + 2`
  — fully unconditional; discharges the Ramanujan hypothesis via
  `RamanujanSum.farey_ramanujan_decomp`.
- The conditional version `farey_bridge_identity` (FareyBridgeIdentity.lean:134-173)
  takes `h_ramanujan_decomp` as a hypothesis; the unconditional one removes it.
- Supporting engine `formal-conjectures/RamanujanSum.lean` contains the genuine proofs:
  `primRootsSum_eq_moebius` (line 101), `ramanujanSum_eq_moebius_of_coprime` (line 160),
  `farey_ramanujan_decomp` (line 207). These are substantive multi-step proofs, not stubs.
- `grep` of both files for `sorry|admit|native_decide|axiom`: **none found** (static).
- `formal-conjectures/_AxiomCheck.lean:43-45` issues `#print axioms` on
  `farey_ramanujan_decomp`, `ramanujanSum_eq_moebius_of_coprime`, `primRootsSum_eq_moebius`,
  `farey_bridge_identity_unconditional`. Its header *claims* only
  `propext, Classical.choice, Quot.sound`, but this is an UNVERIFIED static claim until re-built.

---

## KEEP-2 — The Sign law AS AN OBSERVATION (NOT a theorem)

The paper calls it "Theorem" (thm:sign / thm:sign-small). For the honest note this MUST
be demoted to an **observation / finite computation**. Verbatim statements + caveats:

**thm:sign (Sign Theorem), verbatim** `main.tex:2053-2056`:
> For every prime 11 ≤ p ≤ 100,000 with M(p) ≤ −3:  ΔW(p) < 0.

This is **a finite computation over 4,617 primes**, not a universal theorem.
- The set is "4,617 primes p ≤ 100,000 with M(p) ≤ −3" (`main.tex:89, 895, 2115`).
- Honest caveat in the paper itself: the proof "follows from item (iv) alone (direct
  computation)" `main.tex:2162`; the universal version reduces to the **open
  DiscrepancyStep lemma** `main.tex:2149-2156, 2166`.
- DiscrepancyStep (the open inequality), verbatim `main.tex:2150-2153`:
  **N(p) + B(p) + C(p) > A(p)** for all primes p ≥ 11 with M(p) ≤ −3 — "verified
  computationally … its analytic proof is an open problem" `main.tex:2154-2156`.
- Remark rem:threshold `main.tex:2195-2209`: M(p) ≤ −3 is "an *empirical threshold*
  arising from the finite computational range p ≤ 100,000 … Any finite verification …
  cannot substitute for such a proof."

**thm:sign-small (small primes), verbatim** `main.tex:2068-2072`:
> For every prime 11 ≤ p ≤ 113:  ΔW(p) < 0, regardless of the value of M(p).

Paper claims this is Lean-verified by `sign_theorem_all_le_113` via `native_decide`
(`main.tex:2074-2076`). **See Lean reality table — this is a CORRECTION item: the
named declaration does NOT exist in the canonical Lean tree, and the archived
declaration does NOT match the stated hypotheses.**

---

## KEEP-3 — The certified counterexample at p = 92,173 (REAL)

**Observation obs:counterexample, exact numbers** `main.tex:840-861`:
- M(92,173) = −2  (`main.tex:843`)
- ΔW(92,173) = +3.56 × 10⁻¹¹  (`main.tex:844`)
- Strictly negative Mertens, yet the wobble decreases → disproves conj:disproved.
- **conj:disproved (the natural conjecture, FALSE)** `main.tex:834-838`:
  "For all primes p ≥ 11: M(p) < 0 ⟹ ΔW(p) ≤ 0." — paper: "This conjecture is **false**."

**Four independent computations** `main.tex:847-856`:
  (i) naive float64; (ii) 80-bit long double; (iii) Kahan compensated summation;
  (iv) **256-bit MPFR interval arithmetic**: W(92,172) − W(92,173) = +3.5614 × 10⁻¹¹,
  interval widths < 10⁻⁵⁰, "over 39 orders of magnitude smaller than |ΔW|" (`main.tex:853-855`).
- It is the ONLY counterexample among the 9,588 primes p ≥ 11 up to 100,000
  (`main.tex:858-860`); equivalently 1 of 4,977 primes with M(p) < 0 (`main.tex:72-74, 2266-2268`).
- Cert tooling: MPFR 4.2, 256-bit precision (`main.tex:1678-1679`).

**M = −2 boundary** `main.tex:863-887`: shallowest negative M at which a counterexample
appears for p ≥ 11; M/√p = −0.0066. 183 primes p≥11 have M(p)=−1 with zero
counterexamples (`main.tex:881-882`).

---

## KEEP-4 — Four-term decomposition AS A DIAGNOSTIC (not a path to RH)

**eq:4term, verbatim** `main.tex:931-945`:
> ΔW(p) = A − B − C − N,   with n = |F_{p-1}|, n′ = |F_p| = n + (p−1), and
- **A** = Σ_old D_{F_{p-1}}(f)² · (1/n² − 1/n′²)  — dilution, always positive.
- **B** = (2/n′²) Σ D_{F_{p-1}}(f)·δ(f)  — cross term.
- **C** = (1/n′²) Σ δ(f)²  — shift-squared, always positive.
- **N** = (1/n′²) Σ_new D_{F_p}(k/p)²  — new-fraction contribution, always positive.
(Paper uses calligraphic 𝒩 for "new", to avoid clash with D(f); `main.tex:946-947`.)
Consequence: ΔW(p) ≤ 0 ⟺ N + B + C ≥ A (`main.tex:948-949`).

**Diagnostic framing (use this).** rem:franel-connection `main.tex:970-986`:
W(N) is exactly the normalized Franel–Landau sum; RH ⟺ W(N)=O(N^{−1+ε}). "We do **not**
claim to approach the Riemann Hypothesis through this decomposition. Rather, its merit is
*diagnostic*" — it isolates four contributions whose near-cancellation
(N/A ∈ [0.97, 1.12]) is the empirical phenomenon, and reduces "does ΔW(p)<0?" to the
single open DiscrepancyStep lemma.

**Near-cancellation (obs:near-cancel)** `main.tex:953-964`: N/A ∈ [0.97, 1.12];
B always positive for tested M(p) ≤ −3 primes; C gives 5–18% margin; (B+C+N)/A grows
~1.4 (M=−3) → ~3.0 (M=−14). NOTE the one exception: **B(13) = −3.72×10⁻⁴ < 0**
(M(13)=−3), but B+C > 0 there so the finite computation is unaffected
(`main.tex:1022-1025, 2168-2171`). "A direct proof that B ≥ 0 remains an open problem"
(`main.tex:966`).

---

## KEEP-5 — Displacement–Cosine Identity (REAL, supporting)

**thm:disp-cos, verbatim** `main.tex:502-508`:
> For every prime p ≥ 2:  Σ_{f ∈ F_{p-1}} D(f)·cos(2πpf) = −1 − M(p)/2.   (eq:disp-cos)

Proof `main.tex:510-513`: cos(2πpf) is symmetric under f↦1−f, so apply the Master
Involution Principle (thm:involution, `main.tex:484-492`) then the Bridge Identity.
**Lean status: UNVERIFIED** — no canonical Lean theorem for disp-cos found in
`formal-conjectures/`; treat as pen-and-paper (depends on thm:involution + thm:bridge).

---

## KEEP-6 — M ≤ −3 observation (REAL finite check)

**obs:m-leq-minus3** `main.tex:894-902`:
> Among all **4,617** primes p ≤ 100,000 with M(p) ≤ −3:  ΔW(p) ≤ 0 in every case.
> Zero counterexamples. Tightest case **p = 92,177, M = −4**, |ΔW| ≈ **7 × 10⁻¹¹**,
> still safely negative.

(M=−3 threshold also "proved" only as the finite thm:sign; `main.tex:904-911`.)

---

## Franel–Landau connection + explicit RH disclaimer

- Franel–Landau theorem stated `main.tex:162-173`: RH ⟺ Σ|f_j − j/n| = O(N^{1/2+ε})
  ⟺ W(N) = O(N^{−1+ε}). Cites `\cite{Franel1924}` (`main.tex:164`) and
  `\cite{Landau1924}` (`main.tex:164`), and Hardy–Wright Ch. XVIII (`main.tex:168`).
- **Explicit RH disclaimer** (use verbatim) rem:franel-connection `main.tex:975-977`:
  "We do not claim to approach the Riemann Hypothesis through this decomposition.
  Rather, its merit is *diagnostic*."
- Wobble W(N) defined `main.tex:133-135` (eq:wobble); ΔW(N)=W(N−1)−W(N) at `main.tex:218-220`.

---

## LEAN REALITY TABLE (static analysis; re-verify before any use)

| File (path) | Main decl (file:line) | What it proves | sorry/native_decide/axiom |
|---|---|---|---|
| `formal-conjectures/FareyBridgeIdentity.lean` | `farey_bridge_identity_unconditional` (197-205) | Bridge Identity Σ e^{2πipf} = M(p)+2, prime p, **unconditional** | none (static) |
| `formal-conjectures/FareyBridgeIdentity.lean` | `farey_bridge_identity` (134-173) | same, conditional on `h_ramanujan_decomp` | none |
| `formal-conjectures/RamanujanSum.lean` | `farey_ramanujan_decomp` (207); `ramanujanSum_eq_moebius_of_coprime` (160); `primRootsSum_eq_moebius` (101) | Ramanujan-sum engine (c_q(n)=μ(q) for gcd=1; Farey decomposition) | none (static) |
| `formal-conjectures/FareySignPattern.lean` | `farey_sign_pattern_density_one` (122-150) | **VACUOUS** — proof is `:= h_chebyshev_bias`; conclusion = hypothesis | no `sorry` token, but logically empty |
| `formal-conjectures/_AxiomCheck.lean` | (#print axioms script) | lists axiom-print commands; **not re-run** | header axiom claim UNVERIFIED |

**FareySignPattern.lean is vacuous — offending lines:**
- `farey_sign_pattern_density_one … := h_chebyshev_bias`  — the hypothesis
  `h_chebyshev_bias` (FareySignPattern.lean:129-139) is **textually identical** to the
  conclusion (lines 140-150); the proof is the single token `h_chebyshev_bias`
  (FareySignPattern.lean:150). It assumes exactly what it claims to prove.
- `DeltaW` is declared `opaque` (FareySignPattern.lean:74) — no concrete ΔW exists.
- The "falsification" theorems are likewise vacuous: `pointwise_falsification_237733`
  (193-204) proves `¬Agrees 237733` only from a hypothesis `h_witness` that *is* the
  negation; proof `exact h_witness h` (line 204). Same for `_243799` (210-214) and
  `pointwise_version_falsified` (230-237).
- The paper's "density-one" content is honest in its docstring (FareySignPattern.lean:97-119
  marks it "research-open in Lean"), but the *theorem* carries no proof content.

**CORRECTION — `sign_theorem_all_le_113`:**
- It does **NOT** exist anywhere under `formal-conjectures/` (there is **no
  `SignTheorem.lean` in the canonical dir** at all).
- It exists ONLY in `archive/` copies, e.g.
  `archive/request-projects/RequestProject_aristotle/SignTheorem.lean:411`
  and `archive/aristotle-results/.../SignTheorem.lean:411`.
- The archived declaration is **NOT what the paper states**. Paper thm:sign-small claims
  "11 ≤ p ≤ 113, **regardless of M(p)**" (`main.tex:2069-2071`). The actual archived decl
  signature is:
  `theorem sign_theorem_all_le_113 (p) (hp : Nat.Prime p) (hp13 : 13 ≤ p) (hp113 : p ≤ 113) (hM : mertens p ≤ -3) : deltaWobble p < 0`
  — i.e., it requires **13 ≤ p (excludes p=11)** AND **M(p) ≤ −3 (NOT unconditional)**.
- The archived `SignTheorem.lean` also contains real `sorry`s (lines 85, 134, 548) and
  ~42 `native_decide`/`sorry` occurrences total; it is an unmerged archive artifact, not a
  certified canonical result.
- ⇒ The note must NOT cite `sign_theorem_all_le_113` as a kept Lean result, and must not
  repeat "regardless of M(p)".

---

## "16 files / 436 results" claim — INFLATED

- The paper claims **436** Lean results across **sixteen files** (`main.tex:92, 331,
  1461, 1472-1517, 1532`). The named files (PrimeCircle.lean, BridgeIdentity.lean,
  CharacterBridge.lean, InjectionPrinciple.lean, DisplacementShift.lean,
  CrossTermPositive.lean, SignTheorem.lean, MediantMinimality.lean, etc.) **do NOT
  exist** in `formal-conjectures/` and were not found anywhere outside `archive/`.
- The only substantive, canonical, sorry-free Lean is the Bridge Identity stack:
  `FareyBridgeIdentity.lean` + `RamanujanSum.lean` (+ the empty `FareySignPattern.lean`,
  + the `_AxiomCheck.lean` script). The honest note should claim **the Bridge Identity is
  Lean-verified (pending re-compile)** and nothing more about Lean.

---

## Prior-art / citations actually present in main.tex bibliography

`\bibitem` keys found in `\begin{thebibliography}` (`main.tex:2528-2653`):
`Aristotle2025`, `BPS2015`, `ErdosTuran1948`, `Franel1924` (2549),
`Garcia2025` (Tomás García, "New analytical formulas for the rank of Farey fractions…",
*Mathematics* 13(1):140, 2025 — this is the Dedekind/rank-formula ref, `main.tex:2551-2555`,
cited at `main.tex:1011, 1740`), `ParksBurrus2020`, `Landau1924` (2563),
`RubinsteinSarnak1994`, `AkbaryNgShahabi2014` (2573, the M(p)/√p limiting-distribution
framework), `Edwards1974`, `Ramanujan1918`, `HardyWright2008`, `Niederreiter1992`,
`Kanemitsu1982`, `AthreyaCheung2014`, `Duke1988`, `Montgomery1973`, `Ingham1942`,
`Odlyzko1987`, `Walfisz1963`, `DysonMehta1963`.

**MISSING — must add to the honest note (per project prior-art memory):**
- **Cox–Ghosh–Sultanow (arXiv:2105.12352, 2021)** — the static Farey↔Mertens connection.
  It is **NOT cited** in main.tex (confirmed by grep: no cox/ghosh/sultanow). The honest
  note MUST cite it, since "evaluating the Fourier transform of the Farey sequence at
  prime frequency and recognizing the Mertens function" (`main.tex:1722-1725`) overlaps
  this prior art. Frame the static identity as known; only the per-step/ΔW framing is novel.
- Franel (`Franel1924`) and Landau (`Landau1924`) ARE present (`main.tex:2546-2549,
  2563-2566`). Garcia2025 Dedekind IS present.

---

## CUT LIST (one line each, with reason)

- **Per-step "spectroscopy framework" / C1-C2-C3 meta-theorem** (thm:meta `main.tex:270-277`;
  thm:necessity `main.tex:1935-1960`) — informal "meta-theorem", not proved; cut as inflated framing.
- **"Mertens spectroscope" RH-detection / z-scores at ζ-zeros** (`main.tex:1950, 1977, 1988,
  2309-2314`; negative cases §`main.tex:1965-2003`) — empirical signal-processing claim, no theorem.
- **Three negative cases (Gauss circle, partitions, CF quotients)** `main.tex:1927-2044` — supports
  the meta-theorem only; cut with it.
- **Character-weighted bridge + GRH equivalence** (thm:char-bridge `main.tex:449-455`; rem:grh
  `main.tex:466-480`) — restatement of classical GRH equivalence; cut as scope inflation.
- **Universal Farey exponential sum** (thm:universal `main.tex:393-400`) — true but tangential;
  optional, default cut from the minimal honest note.
- **RH/GRH "new characterization"** `main.tex:1892-1923` — just the classical Mertens⟺RH
  equivalence rewritten; cut the "new RH characterization" claim.
- **Sign-bias probability c ≈ 0.73** (conj:sign-bias `main.tex:1055-1062`; abstract `main.tex:88`)
  — conjectural, RH+distribution-conditional; cut or demote to one hedged sentence.
- **Rubinstein–Sarnak / Akbary-Ng-Shahabi sigmoid story** §`main.tex:1036-1067` — speculative; cut.
- **Applications: scheduling/LoRaWAN, mesh generation, iCZT, digital geometry, military**
  `main.tex:1832-1890` — speculative engineering; cut entirely.
- **Dyson–Mehta / RMT / GUE spectral-rigidity analogy** rem:rmt `main.tex:1106-1129` — analogy
  only; cut.
- **Compression phenomenon / GK concentration / mutual-information 0.79 bits** §`main.tex:2241-2350`
  — empirical, no CIs; cut.
- **Injection Principle, Fisher info, mediant, tensor 2D/3D, etc.** §`main.tex:1133-1452` —
  classical or tangential; cut from minimal note (mediant/gap are textbook).
- **"436 Lean results across sixteen files" + all named-but-nonexistent Lean files** — cut; only
  the Bridge Identity stack is real.

---

## BLOCKLIST — claims that must NOT appear in the honest note

1. "**441 Lean results**" (or "436 results", or "sixteen files") — inflated; only the Bridge
   Identity Lean stack is real and canonical.
2. **Named-but-nonexistent Lean files** — `SignTheorem.lean`, `PrimeCircle.lean`,
   `BridgeIdentity.lean`, `CharacterBridge.lean`, `InjectionPrinciple.lean`,
   `DisplacementShift.lean`, `CrossTermPositive.lean`, `MediantMinimality.lean`,
   `DeltaCosine.lean`, `DenominatorSum.lean`, etc. None exist in `formal-conjectures/`.
3. **`sign_theorem_all_le_113`** as a verified canonical result — it lives only in `archive/`,
   has `sorry`s, and its real hypotheses (13 ≤ p, M(p) ≤ −3) contradict the paper's
   "11 ≤ p ≤ 113 regardless of M(p)".
4. **"Mertens spectroscope" / per-step RH-detection / z-scores at ζ-zeros** — no theorem.
5. **Phase formula φ₁** — NOT present in main.tex (UNVERIFIED in source); do not introduce it.
6. **Crypto / commercial / "post-bias crypto" / military-application** narrative.
7. **Any "Theorem" that is really a finite computation** — specifically the **Sign "Theorem"**
   (thm:sign / thm:sign-small): present only as an *observation over 4,617 primes* with the
   universal version flagged as reducing to the open **DiscrepancyStep** lemma.
8. **"Approaching RH" via the four-term decomposition** — explicitly disclaimed in
   `main.tex:975-977`; keep the decomposition as a *diagnostic* only.
9. **c ≈ 0.73 sign-bias probability** as a result — it is conjectural (RH + distribution).

---

## OUTSTANDING VERIFICATION (do before submission)

- [ ] Re-compile `FareyBridgeIdentity.lean` + `RamanujanSum.lean` from a fresh checkout
      (`lake exe cache get` first — 0 oleans otherwise), confirm EXIT=0.
- [ ] `#print axioms FareyBridgeIdentity.farey_bridge_identity_unconditional` and the three
      `RamanujanSum` lemmas == `[propext, Classical.choice, Quot.sound]`, **no `sorryAx`**.
- [ ] Confirm the 256-bit MPFR p=92,173 certificate reproduces (cert tooling MPFR 4.2,
      `main.tex:1678-1679`); locate the actual cert artifact in the repo before citing.
- [ ] Add Cox–Ghosh–Sultanow (arXiv:2105.12352, 2021) citation for the static Farey↔Mertens
      identity.
