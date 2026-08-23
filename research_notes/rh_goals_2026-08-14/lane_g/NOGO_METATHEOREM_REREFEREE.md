# NOGO METATHEOREM — COLD RE-REFEREE (promotion gate)

> Installation note (orchestrator, 2026-08-23): the re-referee seat was
> read-only and returned this report inline; installed verbatim, unedited
> except this note and HTML-entity unescaping.

**Date:** 2026-08-23. **Posture:** cold, independent; did not author or advise any file under review. **Pass type:** correction-closure + bypass-interaction check (not a re-derivation of the mathematics; NOGO-4 referee did that).

## Criterion table

| # | Criterion | Evidence I produced | Verdict |
|---|---|---|---|
| 1 | D1 addressed, referee's prescribed wording | `NOGO_METATHEOREM_SOL.md:663-703`. Entailment restated `A ∧ H_Sel90 ⊨ ¬P_naive`; hypothesis-containment paragraph reproduces the referee's `REFEREE.md:70` language verbatim ("*truth* risk … also, and more damagingly for a **metatheorem**, a *hypothesis-containment* risk"); §1.3 consequence stated as OPEN, moved to SCOPE box per referee's standing ambiguity | **PASS** (see S-1: now stale) |
| 2 | D2 | `:705-718`. A5 pole clause restated exactly as prescribed: "every pole of `φ` in `Re s > 1/2` is real and lies in `(1/2,1]`, and there are finitely many"; Kelmer Prop 4.4 receipt quoted | **PASS** |
| 3 | D3 | `:720-727`. `N ≥ 4` attached (λ≥√2 ⟺ q≥4); `q=3` routed to the direct `ϕ_Euler(n) ∈ ℕ` argument; "not a whole-family receipt" | **PASS** |
| 4 | D4 | `:729-735`. Count corrected 6→5, rows enumerated `A0,A4,A4⁺,A6,A7`; alternative reading (9) recorded. I re-counted against §2: `A1,A2,A3,A5` do carry distinct arithmetic derivations from `Λ` | **PASS** |
| 5 | D5 | `:737-748`. `d(n)=ϕ_Euler(n)`, `g_n=n`, `d(1)=1`, `Σϕ(n)n^{−s}=ζ(s−1)/ζ(s)` ⇒ `L*_3 = ζ(2s−1)/ζ(2s)`. Identity correct | **PASS** |
| 6 | D6 | `:750-760`. (a) strip confinement added to Met. I input list at the divergence step; (b) §5.3 flag 1 downgraded to "immediate corollary of A4" via `|L*−1|<1` for large `Re s`. Both halves present | **PASS** |
| 7 | D7 | `:762-766`. "unavoidable" → "unavoidable for this witness" | **PASS** |
| 8 | D8 (a)+(b), the two new rows | `:768-791`. Row 3 `A ⊨ P_line(3/4)?` = **OPEN and RH-HARD**; row 4 = `A` fails to decide in at least one direction, **PROVED UNCONDITIONALLY**. I re-derived both: `φ_3 ∈ 𝔐(A)` + Prop 4.1 gives `A ⊨ P_line(3/4) ⇒ φ_3 ⊨ P_line(3/4) ⇒ RH`; and RH ⇒ `A ⊭ ¬P_line`, ¬RH ⇒ `A ⊭ P_line`. Neither row consumes `H_Sel90` — membership `φ_3 ∈ 𝔐(A)` is Sel90-free. Correct, and correctly unconditional | **PASS** |
| 9 | D9 | `:793-804`. Gloss corrected to "no *consequence of `A`* separates them", plus the mandatory Dirichlet-data sentence (`g_n ∈ ℤ[λ_q]` encodes `q`) | **PASS** |
| 10 | D10 | `:806-819`. Canonical `P_naive` fixed to §3.1 (`Re ρ > 1/2` **and** `Im ρ ≠ 0`); the §0/§6 readings named non-derivable. §8 row 1 of the new table uses the §3.1 form | **PASS** |
| 11 | D11 | `:821-826`. `φ_5` → `φ_3`, with §5.1 remark 2 as the reason | **PASS** |
| 12 | D12 | `:828-845`. Four-item dependency set: Sel90, Iwaniec §3.4 NOT READ, Venkov via FJS only, Hejhal/FJS via `pdftotext` transcriptions | **PASS** |
| 13 | D13 | `:847-865`. Pointer moved to `.../aristotle_dispatch_v33_aristotle/LawSkeletonI.lean`; §1.3 claim-2 dispatch-file line refs correctly retained | **PASS** |
| 14 | Bypass D-1..D-6 applied (precondition of the DISPATCH relabel) | `SEL90_..._SOL.md:523-619`: D-1 Fubini reason replaced with the compact-box/fixed-`T` statement + Backlund/Titchmarsh 9.2 explanation; D-2 (a) non-negative integrand ⇒ `[T−1,T+1]→[T−1,T]` valid, (b) `H = H₀+iT` translate ⇒ `κ(R)` `T`-free; D-3 cites `LAW_..._SOL.md:172`; D-4 `σ_pole`; D-5 lines 85–86; D-6 numerics recorded as under-stated. All six, all faithful | **PASS** |
| 15 | Append-only (no existing line touched) | `git show --numstat 00c6bc8` → SOL bypass `100 0`; `git show --numstat bdab8e5` → NOGO SOL `229 0`, MAP `14 0`; grep of `^-` lines shows only the `--- a/` headers. DISPATCH `36 0`, addendum is a new §11 appended after line 344. The 5 deletions in `00c6bc8` are entirely in `SHARD_a2_l64-128.ckpt.json` (live d8 checkpoint, out of this brief's scope — see S-4) | **PASS** |
| 16 | No out-of-scope edits to lane_g / dispatch | `git diff --stat HEAD -- research_notes/.../lane_g/ projects/aristotle_dispatch_v33/` → empty (clean tree); commit file lists are exactly the declared ones | **PASS** |
| 17 | DISPATCH §11 relabel is licensed and correctly scoped | `DISPATCH.md` §11: quotes the referee gate verbatim, records D-1..D-3 applied, relabels `S5` (line 35) and `H3` (line 73) to PROVED, and holds scope: `H3` consumed form only, per-`q`, no `q`-uniformity, no effective height, no formalization; GAP-1/GAP-2 retained; `H4`/`H5` untouched. Matches the referee's licence exactly, no drift upward | **PASS** |

## Duty 2 — the substantive question: what is Metatheorem I's post-bypass conditionality?

I audited the bypass's §2 input list line by line against the corrected axiom list. Result:

| Bypass input (`SEL90_..._SOL.md:88-112`) | Derivable from corrected `A`? |
|---|---|
| **(D)/(NF)** `φ = √π(Γ(s−½)/Γ(s))d(1)g_1^{−2s}L*`, `L* = 1+Σa_nλ_n^{−s}`, real coeffs, abs. conv. | **A4** verbatim (+**A3** for reality). YES |
| **(E)** right-edge decay, `|L*−1| ≤ A e^{−cℜs} ≤ ½` for `ℜs ≥ σ₁ ≥ 3/2`; no zeros/poles there | **A4** (needs `0 < g_1 < g_2` strictly, which A4 supplies). YES |
| **(F)** `φφ(1−s)=1`; order ≤ 2; holo. in `ℜs>½` except finitely many poles, **all real**, in `(½,1]` | **A2** + **A1** + **D2-corrected A5**. YES — *and only because of D2.* Under the printed A5 this input **exceeded** `A` |
| **(U)/(G)** `|φ(½+it)|=1`, `|L*(½+it)| = κ(|t|tanh π|t|)^{1/2}`; only zero on the line is `s=½` | **A7** + the Γ-identity `|Γ(½+it)/Γ(it)|² = t tanh πt`. YES |
| **(P)** `|L*| ≤ C|t|^{1/2}` on `½ ≤ σ ≤ 3/2`, extended to all `ℜs ≥ ½` | **A6** + Stirling + **A4** (the D-3 fix's `σ ≥ 3/2` clause is A4's absolute convergence). YES |
| **(Rl)** `L*(s̄) = conj L*(s)` | **A3**. YES |
| Lemma A (Littlewood/Titchmarsh 9.9), Stirling, subharmonicity, Carathéodory, Schwarz reflection, Fubini, dominated convergence | ambient classical analysis, not hypotheses on `φ` — permissible in any `A ⊨` claim |
| `Σ(σ_j−½) = O(1)`, monotonicity of `F`, strip confinement for the divergence step | **A5** / **A4**. YES |
| `(I)` (Kelmer Lemma 4.5) | NOGO-4 referee read the proof: only `(4.15)` + Γ-algebra, positivity-free. **A7**. YES |
| banked Hejhal/FJS receipts | these justify that the `φ_q` family *satisfies* the axioms; they are membership evidence, not extra hypotheses |

**No bypass input exceeds `A` as corrected.** Therefore the correct post-bypass statement is the **upgrade**:

> `A ⊨ ¬P_naive` — unconditional on `H_Sel90`.

with three residuals that must be printed alongside it, none of which is a hypothesis on `φ`:
1. `(J)` is consumed in the `(J)-avg`/`H3` form only; `GAP-1` (`(J)-sharp`, `O_q(log T)` at every height) and `GAP-2` (`(C)`/`(DIF)`) still rest on Sel90 and are **not** in `law_right_zeros_infinite_target`'s signature (bypass referee verified against the Lean signature, verdict 2/15/16).
2. The bypass is refereed **PROMOTABLE-with-corrections**, D-1..D-3 applied — so the licence is live, not provisional.
3. **One genuine, unclosed gap in FORM (S-2 below):** the bypass is written for `L_q^*`, `q ≥ 3`, with `q`-indexed constants; it never states the transfer to an arbitrary `M ∈ 𝔐(A)`. I performed that containment audit myself (table above) and it holds — every step cites only (D),(E),(F),(G),(P),(Rl) plus ambient analysis, and §4 is a `q=3` numerical check only. But **no banked file states it**, and the `A ⊨` upgrade is exactly a genericity claim. It is a one-paragraph append, not new mathematics.

I therefore license the upgrade **conditional on that paragraph being written**; I refuse to certify an `A ⊨` sentence that rests only on this seat's unbanked audit.

## Findings (non-blocking, ordered)

**S-1 — §8 D1's bypass cross-reference is STALE and now under-strength.** `NOGO_..._SOL.md:696-703` calls the bypass "**UNREFEREED**", "discharges nothing today", "no claim in this file may be strengthened on it". True at write time — `git log --date=iso`: `bdab8e5` 22:43:50, bypass referee `0408361` 22:51:39 (8 min later). The governing correction block therefore now understates the established position, in the one place a reader looks for Metatheorem I's conditionality. *Why missed:* the two correction cycles were run in the wrong order. **Fix:** append a D1-addendum recording that the bypass was refereed at `0408361`, that `H3`/`S5` are relabelled PROVED (`DISPATCH.md` §11), and stating the upgraded entailment plus the S-2 genericity paragraph.

**S-2 — the genericity/transfer statement is nowhere banked** (detailed above). Blocks printing `A ⊨` today; does not block promotion of the file as written, which claims only `A ∧ H_Sel90 ⊨`.

**S-3 — nomenclature: "trichotomy" now has four rows.** `:781` "Corrected trichotomy table" with four rows. Cosmetic, but it is the note's headline object.

**S-4 — out of this brief's scope, flagged not adjudicated:** `00c6bc8` also carries `SHARD_a2_l64-128.ckpt.json` (`1881 +/5 −`), a live d8 checkpoint bundled into a corrections commit. The 5 deletions are entirely there, not in any reviewed file. Mixed-concern commit; no effect on this gate.

## Ruling

# PROMOTED

`NOGO_METATHEOREM_SOL.md` §8 closes all thirteen defects fully and faithfully, in the referee's prescribed language where prescribed, append-only (229+/0−), with no new over-strength and no out-of-scope edit. The bypass cycle (D-1..D-6) and the `DISPATCH.md` §11 relabel are likewise faithful and correctly scope-limited.

**Final statements, at the maximum strength the evidence licenses today:**

**Metatheorem I.** For `P_naive`: *`φ` has no zero `ρ` with `Re ρ > 1/2` and `Im ρ ≠ 0`* (§3.1 definition, D10) —
> `A ∧ H_Sel90 ⊨ ¬P_naive`, with `A5` read in its D2-corrected form (every pole in `Re s > 1/2` is real and lies in `(1/2,1]`, finitely many).
>
> **Upgrade licensed, pending the S-1/S-2 append:** `A ⊨ ¬P_naive` outright. Every input of the refereed Sel90 bypass — (D)/(NF), (E), (F), (G), (P), (Rl) — is a consequence of `A0–A7` as corrected, `(F)`'s reality-of-poles clause **only because of D2**; the rest is ambient classical analysis. Residual: `(J)` is consumed in the `(J)-avg`/`H3` form only; `GAP-1`/`GAP-2` remain on Sel90 and are absent from the conclusion chain's signature.

**Metatheorem II.** `A ⊭ ¬P_line(3/4)`, **conditional on RH**, witness `φ_3`; the conditionality is unavoidable **for this witness** (D7). Sel90-free.

**The two D8 rows.**
- **(D8a)** `A ⊨ P_line(3/4)?` is **OPEN and RH-HARD** — a positive answer proves RH in one line, via `φ_3 ∈ 𝔐(A)` and Prop 4.1.
- **(D8b)** **Unconditionally: `A` fails to decide `P_line(3/4)` in at least one direction** — RH ⇒ `A ⊭ ¬P_line(3/4)`; ¬RH ⇒ `A ⊭ P_line(3/4)`. Independent of `H_Sel90` and of the bypass.

**Not licensed:** any `q`-uniform constant, effective first height, or machine formalization of `H3`; `(J)-sharp`; `(C)`; and the §6 paper-section draft, which stays unusable until redrafted per D9/D10/D11 (the correction block records this itself at `:869-871`).
