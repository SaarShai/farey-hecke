# NOGO metatheorem — cold referee (NOGO-4)

> Installation note (orchestrator, 2026-08-23): the referee seat was read-only
> and returned this report inline; installed verbatim by the orchestrating
> session, unedited except for this note and HTML-entity unescaping (&gt; → >).
> Scratch receipts: scratchpad k.pdf / k.txt, fresh curl of arXiv 1402.4780,
> sha256 c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030,
> byte-identical to the second audit's receipt.

**Date:** 2026-08-22. **Posture:** cold, adversarial, independent lineage. Did not read the SOL author's reasoning trace; re-derived every load-bearing step.
**Target:** `research_notes/rh_goals_2026-08-14/lane_g/NOGO_METATHEOREM_SOL.md` (642 lines, UNREFEREED).
**Sources I obtained myself:** fresh `curl` of arXiv 1402.4780 (Kelmer), sha256 as above. In-repo: `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`, `LAW_SECOND_AUDIT_REFEREE.md`, `LAW_HEJHAL_S7_EXTRACT.md`, `projects/aristotle_dispatch_v33/LawSkeletonI.lean` (dispatch **and** returned copies), `plans/wayfinder/rh-goals/MAP.md`. Numerics: `/Users/za/.venvs/farey-rh/bin/python`, mpmath at 25–40 dps.

## Per-claim verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | Axiom list `A0–A7` with double-sided receipts, no axiom failing | **CONFIRMED-with-corrections** (D3, D4, D5) |
| 2 | Prop 4.1: `P_line(3/4) ⟺ RH` unconditionally for `φ_3`; `P_naive` unconditionally false | **CONFIRMED** — re-derived and numerically verified |
| 3a | Metatheorem I: `A ⊨ ¬P_naive`, every LAW step consumes only `A0–A7` | **CONFIRMED-with-corrections** (D1, D2, D6) |
| 3b | Metatheorem II: `A ⊭ ¬P_line(3/4)` conditional on RH, witness `φ_3` | **CONFIRMED**, but the minimality gloss is over-strength (D7) and the note misses an unconditional strengthening (D8) |
| 3c | Metatheorem III: `A ⊭ P_line(3/4)` OPEN | **CONFIRMED as open**, but mis-calibrated: it is RH-hard, not merely open (D8) |
| 4 | Corollary 3.5, arithmeticity-blindness | **CONFIRMED as stated**; the §6 paper gloss is **REFUTED as written** (D9) |
| 5 | Scope §5 / §6 draft strength | **CONFIRMED-with-corrections** (D9–D13) |

## Attack A — Proposition 4.1, re-derived independently

I re-derived the divisor of `φ_3 = Λ(2s−1)/Λ(2s)` from scratch, including every cancellation the note does not spell out.

* `Λ(w) = π^{−w/2}Γ(w/2)ζ(w)`: the `Γ(w/2)` poles at `w = 0,−2,−4,…` cancel the trivial zeros of `ζ` at `w = −2,−4,…` exactly; at `w = 0` there is no trivial zero (`ζ(0) = −1/2`), so `Λ` retains a simple pole; `ζ`'s pole at `w = 1` gives the second simple pole. Zero set of `Λ` = nontrivial zeros of `ζ`, with multiplicity. **Correct as the note asserts.**
* Numerator zeros in `Re s > 1/2`: `s = (1+ρ)/2`, `Re s = (1+β)/2 ∈ (1/2,1)` since `0 < β < 1` unconditionally.
* Denominator **poles** in `Re s > 1/2` (which would create zeros of `φ_3`): need `2s ∈ {0,1}`, i.e. `s ∈ {0, 1/2}` — both outside the open region. **The note's bookkeeping here is right.**
* Denominator **zeros**: `Re s = β/2 < 1/2` — outside; they give poles, not zeros.
* Numerator **poles**: `s = 1/2` (boundary) and `s = 1` (the unique right pole `σ_1 = 1`).
* No numerator/denominator zero collision: it would need `ρ` and `ρ+1` both nontrivial zeros, impossible since `Re(ρ+1) > 1`.
* At `s = 1/2` both `Λ(2s−1)` and `Λ(2s)` have simple poles; the quotient is finite and nonzero. I computed `φ_3(1/2) = −1.0` exactly (to 40 dps), confirming **no divisor on the symmetry line**, consistent with `A7` and with the LAW's strictness step.
* Nonreality: all nontrivial `ρ` are nonreal, because `ζ(σ) < 0` for real `σ ∈ (0,1)` (eta-representation). I checked `ζ(0.3) = −0.90455926`, `ζ(0.5) = −1.4603545`, `ζ(0.7) = −2.7783884`. The note asserts this without proof; it is true and classical. Recommend stating the reason.

**Both directions of the biconditional.** (⇐) RH ⇒ all `β = 1/2` ⇒ all `Re s = 3/4`. (⇒) every zero of `φ_3` in `1/2 < Re s < 1` is of the form `(1+ρ)/2` and is nonreal, so `P_line(3/4)` forces `(1+β)/2 = 3/4` for **every** nontrivial `ρ` ⇒ RH. The quantifier is total — no nontrivial zero escapes the strip restriction `1/2 < Re s < 1`, because `(1+β)/2 ∈ (1/2,1)` unconditionally. **The biconditional is exact and unconditional. CONFIRMED.**

Numerics (mp.dps 40):

```
identity  |√π Γ(s−½)ζ(2s−1)/(Γ(s)ζ(2s)) − Λ(2s−1)/Λ(2s)| ≈ 1e−41  at s = .8+3.1i, 1.3−2i, .6+.4i
k=1   ρ = 0.5+14.1347251417347i   s = 0.75+7.06736257086735i   |φ₃(s)| = 4.18e−41   Re s = 0.75000000000000000000
k=2   ρ = 0.5+21.0220396387716i   s = 0.75+10.5110198193858i   |φ₃(s)| = 8.63e−41
k=3, k=10, k=50 likewise, Re s = 0.75 to 20 digits
|φ₃(½+it)| = 1.0 at t = 1, 3.7, 20, 137
|L*₃(½+it)| − (1/√π)|Γ(½+it)/Γ(it)| ≈ 0 to 1e−41 at t = 0.5, 1, 3, 7.5, 14.13, 50
```

## Attack B — does every LAW step consume only `A0–A7`?

I audited the chain step by step against `A`, and obtained Kelmer myself rather than trusting the transcription.

**Steps I confirm are inside `A`:**

* `(NF)` and `L*(s) = 1 + O(e^{−c·Re s})` with `c = log λ_2 > 0` — needs `0 < g_1 < g_2` strictly, which `A4` supplies. Inside `A`.
* `(P)`: `L* = O(|t|^{1/2})` on `½ ≤ σ ≤ 3/2` from `A6` + Stirling; `σ ≥ 3/2` from `A4`'s absolute convergence. Inside `A`.
* `(G)`: I derived it myself from `A2 + A3 + A4` — `|φ(½+it)| = 1` follows because `1−s = s̄` on the line and `A3` gives `φ(s̄) = conj φ(s)`, so `|φ|² = 1`; substituting `(NF)` at `s = ½+it` gives `|L*| = g_1/(√π|d(1)|)·|Γ(½+it)/Γ(it)|`, exactly `A7`'s stated form with `a = g_1/(√π|d(1)|)`. Inside `A`; `A7` is redundant-but-harmless.
* `(I)`: Kelmer's **Lemma 4.5** (k.txt:997–1064). I read its proof. It uses **only** `(4.15)` — the exact critical-line modulus — plus `Γ`-algebra. **No positivity, no group input.** Inside `A`.
* Strictness: the `ord φ(s₀) + ord φ(1−s₀) = 2m = 0` argument needs only `A2 + A3` (the note credits `A2+A3+A7`; `A7` is not needed). Inside `A`.
* Reflection: `A2`. Nonreality: `A5`. Inside `A`.
* The `c^{1−2s}` conjugation repair (§5.3 item 4): I verified it myself. `φ̃(s) = c^{1−2s}φ(s)` gives `φ̃(s)φ̃(1−s) = c^{(1−2s)+(2s−1)}·1 = 1` ✓; divisor unchanged ✓; `|φ̃(½+it)| = |c^{−2it}| = 1` for `c > 0` ✓; and in `A4` form it maps `(d(n), g_n) ↦ (c·d(n), c·g_n)`, preserving reality, discreteness, `d(1) ≠ 0`, and positivity. **Repair holds. CONFIRMED.**

**The positivity leak I hypothesised, and which does NOT land — recorded because it is the obvious attack and future readers will re-raise it.** The second audit's finding A quotes Kelmer saying Selberg's setting uses Dirichlet series *with positive coefficients*, and `A4⁺` is in the note's list marked "used only where flagged" yet flagged nowhere in §3.3. I checked the primary source. Kelmer (4.10)–(4.12) states plainly that `L(s)` is *"another Dirichlet series with **real but not necessarily positive** coefficients"* and `(4.12)` carries *"with all `a_n ∈ ℝ`"*. Positivity enters only in **Lemma 4.6** (k.txt:1065–1108, `"still given by a Dirichlet series with positive coefficients … apply Proposition 4.1"`), which produces `(0.7)` for `α ≥ α_0 = 3/4` — a result the LAW does **not** consume. `(4.20)` and Lemma 4.5, which are the LAW's whole engine, are positivity-free. **`A4⁺` is genuinely not load-bearing for Metatheorem I. The note is right, for a reason it does not give.** I recommend it state this explicitly, since the second audit's own §A wording invites the opposite conclusion.

**The leaks that DO land:**

**D1 (SEVERE — the entailment is not `A ⊨`, it is `A ∧ H_Sel90 ⊨`).** The Jensen identity `(J)` is Kelmer `(4.20)`, and Kelmer's justification is verbatim (k.txt:1157): *"By Proposition 4.4, `L*(s)` satisfies all the assumptions needed for `[Sel90, Lemma 1,2]`."* The hypothesis set of `[Sel90, Lemmas 1,2]` has been read by nobody — not the LAW author, not either LAW referee, not the SOL author, not me (MAP 2026-08-23 06:55Z confirms no legal digital copy exists). The note's LEDGER RULE treats this as a *truth* risk ("proved modulo one unread citation"). It is also, and more damagingly for a **metatheorem**, a *hypothesis-containment* risk: the claim `A ⊨ ¬P_naive` requires that every hypothesis of Sel90 Lemmas 1,2 is derivable from `A0–A7`. What is actually verified is only that Kelmer's Prop 4.4 conclusions `(4.13)–(4.15)` follow from `A` (I confirm they do, at `d=2, κ=1`), and that Kelmer *asserts* Prop 4.4 suffices for Sel90. Nobody has checked Sel90's hypothesis list against Prop 4.4's conclusions. For a theorem about `φ_q` this is a normal citation dependency; for a **no-go quantifying over all models of an explicit axiom list**, an unread hypothesis list is a direct threat to the axiom list's exhaustiveness — which is precisely what §1.3 claims. The note must say so in those words, not fold it into the generic Sel90 caveat.

**D2 (MODERATE — `A5`'s pole clause is too weak, ambiguously stated, and `(J)` needs the strong reading).** `A5` reads *"finitely many poles `σ_j ∈ (1/2,1]`"*. That parses as "the poles lying in `(1/2,1]` are finite in number", which does not exclude a **non-real** pole in `Re s > 1/2`; `A1` explicitly permits finitely many poles there without constraining them. But Kelmer's Prop 4.4 states `L*` is *"holomorphic in `Re s > (d−1)/2` except for finitely many poles in `((d−1)/2, d−1]"`* — i.e. **every** right pole is real — and `(4.20)`'s pole term `T Σ_{σ_j > α}(σ_j − α)` is a sum over real `σ_j` with no `(T − |γ_j|)` weight. A model of `A` as written, with a complex right pole, is not covered by `(J)` as transcribed. Fix: restate `A5` as *"every pole of `φ` in `Re s > 1/2` is real and lies in `(1/2,1]`, and there are finitely many."* This is what both source columns actually deliver, so the fix costs nothing.

**D6 (MINOR — a used axiom is missing from Metatheorem I's proof bullet list).** §3.3's bullets never invoke strip confinement, yet the divergence step needs `β` bounded to convert "unbounded weighted sum" into "infinitely many zeros" (the second audit names this at line 19). Separately, my reading of Kelmer shows strip confinement is not an independent assumption at all: it is a one-line consequence of `(4.12)`, since `|L* − 1| < 1` for `Re s` large, so `L*` has no zeros there. That downgrades §5.3 flag 1 from "implicit step supplied by the referee" to "immediate corollary of `A4`", which is a strengthening of the note. Recommend both edits.

## Attack C — axiom receipts, spot-checked against the cited sources

I checked **7 of the 9 rows** (not a sample), including both rows the note self-flags.

* **A0** — MMS "all the Hecke triangle groups have only one cusp"; second audit line 22 confirms. **PASS.**
* **A1** — arithmetic column: `Λ` order 1 in `w`, hence order 1 in `s` under `w = 2s`, hence ≤ 2 ✓; sole right pole `s = 1` ✓ (I confirmed numerically: `φ₃(1+1e−8) ≈ 9.5e7`, pole). Non-arith column: FJS §2.4 / Venkov Thm 3.5, second audit line 16, in orbifold generality. **PASS.**
* **A2** — `φ₃(1−s) = Λ(1−2s)/Λ(2−2s) = Λ(2s)/Λ(2s−1)` ✓, re-derived. **PASS.**
* **A4** — I verified independently that the `q=3` instance really is of Hejhal `(7.5)` shape: `ζ(2s−1)/ζ(2s) = Σ_{n≥1} ϕ_Euler(n) n^{−2s}`, so `d(n) = ϕ_Euler(n) > 0`, `g_n = n`, `d(1) = 1`, discrete, absolutely convergent for `Re s > 1`. The note asserts the closed form but never identifies `d(n)`; it should, since that is what makes the arithmetic column an independent receipt rather than a restatement. **PASS.**
* **A4⁺, flagged row** — the note cites Hejhal Lemma 7.3 which `LAW_HEJHAL_S7_EXTRACT.md:29` records as **`N ≥ 4` (uses `λ ≥ √2`)**. Since `λ_q = 2cos(π/q) ≥ √2 ⟺ q ≥ 4`, that citation does **not** cover `q = 3`. Harmless in fact (the `q=3` column argues directly from `d(n) = ϕ_Euler(n) ∈ ℕ`, and the non-arithmetic `q ≥ 5` are all inside `N ≥ 4`), but the note presents Lemma 7.3 as a whole-family receipt. **PASS with citation correction — see D3.**
* **A5, self-flagged row** — arithmetic column verified above (zero real right zeros, all zeros nonreal in `(1/2,1)`, one pole at `1`). Non-arith column: Kelmer Thm 3 preamble, which I read at source (k.txt:172–175): *"The zeroes of the scattering determinant, `ϕ(s)`, in the half plane `ℜ(s) > (d−1)/2` are all located in some vertical strip."* Confirmed verbatim. **PASS**, with D2 and D6 attached.
* **A6, the note's own attack (iii)** — I checked whether Hejhal Lemma 7.7 really covers `N = 3`. `LAW_HEJHAL_S7_EXTRACT.md:19–20` records §7 opening with `G_N`, `λ = 2cos(π/N)`, **`N ≥ 3`**, and line 34 records Lemma 7.7 as *"uniform in N"*; the second audit's page image gives the proof line *"Repeat the derivation of 155(12.2) with `B=10` when `N < ∞`"*. `N = 3` is a finite `N ≥ 3`. **PASS — attack (iii) fails, the note is right.**
* **A7** — `|φ₃(½+it)| = 1.0` to 20 digits at `t = 1, 3.7, 20, 137`; `(G)` verified to `~1e−41`. **PASS.**

I also verified **every in-repo line citation** the note makes to `LAW_SECOND_AUDIT_REFEREE.md` (lines 13,14,15,16,18,19,20,22,23,24,25,26,27,32,34,40,46). All 17 land on the claimed content. This is unusually clean and I record it as a strength.

## Attack D — Metatheorem II

The witness argument is valid: `φ_3 ∈ 𝔐(A)` by §3.2 (subject to D1/D2), and by Prop 4.1 `φ_3 ⊨ P_line(3/4) ⟺ RH`; so under RH, `φ_3` is a model of `A` satisfying `P_line(3/4)`, hence `A ⊭ ¬P_line(3/4)`. Soundness then blocks any derivation of `¬P_line(3/4)` from `A`. **CONFIRMED.** RH is exactly the minimal hypothesis *for this witness*, by the biconditional. Two problems attach — D7 and D8 below.

## Attack E — over-strength phrases (§0, §3, §5, §6)

Full defect list follows; D9–D13 are this attack.

## Numbered defect list

**D1 — `A ⊨` is not established; it is `A ∧ H_Sel90 ⊨`.** *Where:* §0 table row 1; §3.3 proof and status; §5 SCOPE first paragraph; §6 "Theorem (no-go)". *Why missed:* the author inherited the LAW's framing of Sel90 as a *truth* risk and did not notice that a metatheorem about an axiom list also carries a *hypothesis-containment* risk. **Severity: severe.** Required fix: state that `A` is exhaustive of what the LAW consumes **modulo the unread hypothesis list of `[Sel90, Lemmas 1,2]`**, and that the exhaustiveness claim of §1.3 cannot be closed until Sel90 is read.

**D2 — `A5` does not exclude non-real right poles, but `(J)` requires it.** *Where:* §1.2 `A5`, §1.3, §3.3 bullet 2. *Why missed:* FJS's printed divisor list enumerates real exceptions, and the author transcribed the enumeration rather than the exclusion. **Severity: moderate.** Fix as stated above.

**D3 — Hejhal Lemma 7.3 is printed for `N ≥ 4` and cannot receipt `A4⁺` at `q = 3`.** *Where:* §2 table, `A4⁺` row. *Why missed:* the row cites the extract's summary without carrying its `N ≥ 4` parenthetical across the column boundary. **Severity: minor** (the `q=3` case is covered by the direct integer-count argument). Fix: attach `N ≥ 4` to the citation and note that `q = 3` uses the direct argument.

**D4 — "in six of the nine rows the two columns are the same citation" is false; it is five.** *Where:* §2, closing paragraph. *Evidence:* shared-citation rows are `A0, A4, A4⁺, A6, A7` = 5; `A1, A2, A3, A5` carry distinct arithmetic-side derivations from `Λ`. Under the alternative reading ("the generic citation also covers `q=3`") the count is 9, not 6. No reading yields 6. **Severity: minor, but it is a stated count that fails.** *Why missed:* hand-count of a nine-row table.

**D5 — `d(n)` is never identified for `q = 3`.** *Where:* §2 `A4` row. Supplying `d(n) = ϕ_Euler(n)` (`Σ ϕ(n)n^{−s} = ζ(s−1)/ζ(s)`) turns the arithmetic column into a genuinely independent receipt. **Severity: minor / improvement.**

**D6 — strip confinement is used but unlisted, and is over-flagged.** *Where:* §3.3 bullets; §5.3 flag 1. It is needed for the divergence step and it is a one-line consequence of `A4`'s right-edge estimate, not a referee-supplied implicit step. **Severity: minor / improvement.**

**D7 — "The conditionality is unavoidable" is over-strength.** *Where:* §3.4 status paragraph. It is unavoidable **for the witness `φ_3`**. The note gives no argument that no other `M ∈ 𝔐(A)` has unconditionally-collinear right-strip zeros. **Severity: minor.** Fix: "unavoidable for this witness".

**D8 — the OPEN row is mis-calibrated: resolving it positively would prove RH.** *Where:* §0 table row 3; §3.4 closing; §5.1; §6 final paragraph. Since `φ_3 ∈ 𝔐(A)`, `A ⊨ P_line(3/4)` implies `φ_3 ⊨ P_line(3/4)` implies RH by Prop 4.1. So the third row is not "open" in the ordinary sense — it is **RH-hard**, and the note's own Prop 4.1 supplies the reduction in one line. Symmetrically, the note misses the cheap **unconditional** statement: `φ_3` alone shows `A` fails to decide `P_line(3/4)` in at least one direction, since if RH holds then `A ⊭ ¬P_line(3/4)` and if RH fails then `A ⊭ P_line(3/4)`. Both belong in the trichotomy table. **Severity: moderate — this is the note's best unclaimed result and its most important honesty calibration.** *Why missed:* the author reached for a countermodel construction (§5.1) and did not look for the reduction already sitting in §4.

**D9 — §6's arithmeticity gloss over-reads Corollary 3.5.** *Where:* §6 draft, *"What `A` cannot do is separate the arithmetic members of the family from the non-arithmetic ones."* Corollary 3.5 is correct as a statement about **`A`-entailments**. But the structures are pairs `M = (φ, 𝒟)`, and `𝒟 = (d(n), g_n)` is in the language. The `g_n` are the `|c|`-values, which lie in `ℤ[λ_q]` and therefore encode `q`. An argument that inspects the Dirichlet data — still "generic analytic machinery" by any ordinary reading — is not covered by the Corollary. **Severity: moderate.** Fix: say "no *consequence of `A`* separates them", and add one sentence noting that the Dirichlet data itself is not arithmeticity-blind.

**D10 — `P_naive` is defined two incompatible ways.** *Where:* §0 table row 1 ("no zeros **at all** in `Re s > 1/2`") versus §3.1 (`Im ρ ≠ 0` required) versus §6 draft ("no zeros off the line `Re s = ½` in the right half-plane"). `A5` explicitly permits finitely many real right zeros, so the §0 and §6 readings are non-derivable from `A` for a second and trivial reason, which weakens rather than strengthens the result. **Severity: minor but load-bearing for a note whose whole thesis is "say which statement you mean".** Fix: use §3.1's definition everywhere.

**D11 — "the error can be exhibited: apply the argument to `φ_5`" is not exhibitable.** *Where:* §3.3 Consequence. §5.1 remark 2 states there is no theorem-valid `φ_q` zero certifier for non-arithmetic `q`; the concrete exhibition is `φ_3`, where failure is classical. **Severity: minor.** Fix: "apply it to `φ_3`, where the failure is classical fact".

**D12 — the LEDGER RULE header understates the dependency set.** *Where:* §0, *"the residual dependency … has not been read"* naming Sel90 alone. §2 itself declares Iwaniec §3.4 NOT READ, Venkov reached only through FJS, and §5.3 flag 3 says the entire `A1`/`A6` chain rests on `pdftotext` **transcriptions**, not verbatim output. §5 DEPENDENCY is honest; the header is not, and the header is what gets quoted. **Severity: minor.** Fix: header should say "one unread *engine* citation plus the not-read/transcribed source set enumerated in §2 and §5.3".

**D13 — the machine-verification citation points at the wrong file.** *Where:* §3.3 status, *"machine-verified conditional on `H3`–`H5` (Aristotle v33, `LawSkeletonI.lean`)"*, and §7 provenance, both naming `projects/aristotle_dispatch_v33/LawSkeletonI.lean`. That is the **dispatch skeleton**: 16 `sorry` occurrences, and its own header reads *"Everything below with a `sorry` body is CONJECTURAL at the Lean level. This file machine-verifies nothing."* The proved artifact is `projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/LawSkeletonI.lean` (3 `sorry` hits, all in prose; status line: *"No `sorry` bodies remain"*), and MAP 2026-08-23 06:55Z records the independent local re-compile. **The claim is true; the pointer is to the file that refutes it.** *Why missed:* both copies share a filename. **Severity: minor but embarrassing in a paper draft.** Fix: cite the `_aristotle/` path. (The §1.3 claim-2 line references to the dispatch file at `:31-32,160-162,182-183,210-213` are correct and should stay — I verified `H1`/`H2` are definitional per `DISPATCH.md:71-72`, so "the analytic imports are `H3`–`H5`" is accurate.)

## Independent corroborations produced in the course of this review

Not defects; recorded because they raise confidence in the note's inherited ledger warnings, and because I produced them myself rather than transcribing them.

* **Kelmer's printed `B_Γ` is wrong, confirmed at source and numerically.** (4.18) evaluates the last term as `log|t tanh(πt)/π|` where `|Γ(½+it)/Γ(it)|² = t tanh(πt)` exactly, injecting a spurious `−½log π`. At `d=2, κ=1, a=1/√π`, Kelmer's formula gives `B_Γ = (−4logπ−1)/(8π) = −0.2219781556`. My direct numerical evaluation of `(1/2π)∫_{−T}^{T}(T−|t|)log|L*(½+it)|dt − (1/4π)T²log T`, divided by `T²`, gives `−0.2107732` (T=200), `−0.2105234` (T=1000), `−0.2104734` (T=5000), converging to `(−2logπ−3)/(8π) = −0.2104609172`. §5.4's "do not consume `A_q`, `B_q`, `C_q` from Kelmer" is independently vindicated, and the note correctly uses none of them.
* **Kelmer Remark 0.2 verified verbatim** (k.txt:217–221): *"for `Γ = SL₂(Z)` the scattering determinant can be computed explicitly in terms of the Riemann Zeta function and its poles are located at the zeroes of `ζ(1−2s)`, hence, a positive proportion are on the line `ℜ(s) = ¼`."* §3.3(ii) and the §6 draft's closing sentence are correctly sourced.
* **Hejhal Thm 7.11's own proof (extract §2 step 7) turns on `|φ_∞| ≢ 1` for the theta group**, which is consistent with `A7` only because `G_∞` has two cusps and is excluded by the note's "finite `q ≥ 3`". No contradiction; worth one sentence in §5.2 so a reader does not trip on it.

## Gate

**PROMOTABLE-with-corrections.**

No claim of the note is refuted. Proposition 4.1 — the note's one genuinely new piece of mathematics and the correction it was commissioned to make — is **CONFIRMED unconditionally**, re-derived and verified numerically to 20+ digits. Metatheorem I is a faithful model-theoretic re-reading of the promoted LAW and I found no step consuming a group, a surface, arithmeticity, an Euler product, or `q`; the two attacks most likely to land (positivity via Selberg's class, and the `c^{1−2s}` conjugation) both **fail** on inspection of the primary sources, and the note is right on each.

Promotion is blocked until **D1, D2, D8, D9** are repaired in the file. D1 and D2 change what the metatheorem says; D8 changes what the trichotomy is worth and is the note's best unclaimed result; D9 is a false sentence in the paper-section draft. D3–D7 and D10–D13 are mandatory before any paper-level use but do not touch the mathematics.

One standing ambiguity, graded strict: §1.3's claim that `A` is **exhaustive** of the LAW's inputs cannot be discharged by anyone while `[Sel90, Lemmas 1,2]` is unread. I graded the note against the weaker, checkable claim "no step *visible in the transcribed chain* consumes anything outside `A`", which it satisfies. The stronger claim, which is what a no-go metatheorem needs, remains **open**, and the note should say so in the SCOPE box rather than in a footnote.
