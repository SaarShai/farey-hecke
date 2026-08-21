# Referee findings — EFFECTIVE_THEOREM_ASSEMBLY_SOL.md

**Date:** 2026-08-20 · **Target:** `EFFECTIVE_THEOREM_ASSEMBLY_SOL.md` @ `162282b` · **Referee leg:** `/Users/za/.venvs/farey-rh/bin/python`, mpmath `mp.dps=80`, program written fresh (NOT the note's Arb program), at `<scratchpad>/ref.py`.

**Environment disclosure:** Bash and Read access to `/Users/za/Documents/farey-hecke` was revoked mid-session by macOS TCC. Attacks 2 and 4 completed with full independent receipts before the lockout; attacks 1 and 3 are partial; attack 5 (the adjudication) could not be performed at all. This report was returned as text and installed verbatim by the orchestrator after access was restored.

## Per-attack verdicts

| # | criterion | evidence produced | verdict |
|---|---|---|---|
| 2 | Q₀ rebuild, both pairings | independent mpmath leg, below | **PASS (reproduced digit-for-digit)** |
| 4 | e^{T₀} floor + ν_z binding | independent recomputation + elasticities | **PASS on structure, FAIL on one printed number** |
| 1 | resonance step licensed at assembled hypotheses | R3 lines 88-93 / 190-270 read; KF_WALL_REFEREE read | **PARTIAL — GAP NOT REFUTED** |
| 1b | Hejhal (7.22) within printed pp.568-600 | none obtainable | **NOT VERIFIED (lockout)** |
| 3 | hypothesis-table completeness | partial sweep only | **PARTIAL — one candidate defect found** |
| 5 | ledger adjudication | sources unreadable | **NOT PERFORMED** |
| 6 | ledger discipline of the note itself | read in full | **PASS** |

## Attack 2 — Q₀ recomputation (independent leg)

Rebuilt C_R″ from the §4 assembly rather than reading it: `C4pp = 2^52·81+1`, `S=7.648`, `F(12)=1225/4+91605/12`, `pair = 2π²(S+1)(11/5)C4″F`, `wrap = (11/5)·128(1+log2)·30`, `C_R_raw = 2.775(pair+wrap)`.

```
gamma1 = 14.134725141734693790457...   t0 = 7.0673625708673468952286...
sup|s| on Gamma_R^A = 7.646893243596647842577...  < 7.648  True
C4pp = 364791569817010177   F = 7940.0
CRraw = 3018536183210772296097744.83302092424861444146809550183635495...
CRpp  = 3018536183210772296097745
T_side = 43.0038669194927841330064599089657667363260261044378878503...
q_side = 4746157036282968395
T      = 85.3578987799887436740434637985978175532746109888166112059...
qA0    = 11761546420922598622910053339543258496
log10 Q0 = 37.07046442700542269724563939847585341190166110905856819967...
KF109  B = 74.130014427948238935276263583850430088784504319106364430549   N_mono = 6942276674823096983
routeH B = 117.0                                                          N_mono = 4746157036282968395
```

All five integers and both diagnostic pairings match the note exactly. `C_R_raw` upper endpoint agrees to 60+ digits with the note's Arb value, and the ceiling is strict (raw `…744.833` → `…745`).

**Re-derivation of the "N_monotone = q_side″ EXACTLY" phenomenon.** It is an algebraic identity, not a numerical coincidence:
- `q_side″ = ⌊exp((log C_R − log K₊)/α)⌋ + 1 = ⌊(C_R/K₊)^{1/α}⌋ + 1`
- `N_monotone ≤ ⌊(C_R/B)^{1/α}⌋ + 1` with `B = min(K₊, K_F^{1/ν}K₊^{1−1/ν})`

Under route-H the second term has `log₁₀ = 162244.74`, so `B = K₊` identically, and the two closed forms are *literally the same function*. The digit agreement is forced for **every** C_R, not evidence of anything. The note (§4.3) calls it "the same phenomenon … now reproduced at C_R″", which reads as an empirical corroboration. **Minor defect (cosmetic/epistemic):** it should say `B = K₊ ⟹ N_monotone-bound ≡ q_side″ by construction`. No number is wrong.

Under the forbidden `K_F=109` diagnostic, `B = 74.130… < K₊`, so the identity breaks and `N_mono = 6942276674823096983 > q_side″` — reproduced, and correctly excluded by (H-ROUTE).

`Q₀ = max{12, 3, 4746157036282968395, 1.176e37, 4746157036282968395} = q_A0″`. **PASS.**

## Attack 4 — the e^{T₀} floor and the binding parameter

With `T₀ = ((1−ν_z)log K₊ − log m_z)/(αν_z)`:

```
T0 = 38.38531...        e^T0 = 46841857142466893.06   (log10 = 16.6706)
C_R^(5/6) * e^T0 = 11761546420922598622910053339543258495.727  ( = q_A0'' - 0.27 )
1/(alpha*nu) = 5.369415807560137457...
```

- **`e^{T₀} ≈ 4.7×10^16` is ARITHMETICALLY RIGHT** (4.684×10^16) and its C_R-independence is exact, since `log Q₀ = T₀ + (log C_R)/α` splits additively. Setting `C_R″ → 1` leaves exactly `e^{T₀}`. **PASS.**
- **DEFECT (refuted printed number).** §5(b) line 604: "which enters as \(1/(\alpha\nu_z)\approx4.47\) in the exponent." The true value is **`1/(αν_z) = 5.36941580756…`**, not 4.47. Nor is 4.47 the neighbouring coefficient `(1−ν_z)/(αν_z) = 4.53573…`. No quantity in the assembly equals 4.47. **Repair text:** replace `\(1/(\alpha\nu_z)\approx4.47\)` with `\(1/(\alpha\nu_z)=5.3694\ldots\)` (and, if the intended object was the \(K_+\) coefficient, `\((1-\nu_z)/(\alpha\nu_z)=4.5357\ldots\)`).
- **"The binding parameter is ν_z" — TRUE ONLY FOR THE FLOOR.** Elasticities computed for `T₀`: `ν·∂T₀/∂ν = −42.4`, `α·∂T₀/∂α = −38.39`, `∂T₀/∂log K₊ = +4.536`, `∂T₀/∂log m_z = −5.369`. So ν_z is indeed the most elastic parameter **of the C_R-independent floor** — claim supported. But for the *actual* `log Q₀ = 85.358` at `C_R″`, `α·∂(log Q₀)/∂α = −85.36`, i.e. **α is more elastic than ν_z by 2×**, because α also discounts `C_R^{1/α}`. Since this sentence explicitly steers the next research target, that distinction matters. **Repair text (append to §5(b) item 3):** "*Scope of 'binding'.* ν_z is the most elastic parameter of the C_R-independent floor e^{T₀} (elasticity −42.4 vs −38.4 for α). For the full Q₀ at C_R″, α is the most elastic parameter (elasticity −85.4), because α also discounts C_R^{1/α}. A geometry change that raises α therefore dominates one that raises ν_z at the current C_R, and only ν_z (or m_z, K₊) can move the floor."

## Attack 1 — the resonance step (PARTIAL)

Verified verbatim before lockout, `R3_TRANSPORT_EXECUTION_SOL.md`:
- `:88-93` — `K_+^{1-ν₀}E_R(q)^{ν₀} < 0.0439` ⇒ Rouché zero in `D_z`, then Hejhal (7.22) ⇒ pole at `1−conj(s_q)`. **Same disc `D_z=D(3/4+it₀,1/8)`, same `m_z=0.0439`, same `ν₀=0.1552`, same `Ω`, same `Γ_R`** as the assembly's (b)/(c). ✅
- `:208-231` — (3.4) and §4 "Rouché and reflection"; §4 opens "Assume (1.2) **and the finite-family holomorphy gate**", both of which the assembly carries as (H-HOL). ✅
- The hidden side hypothesis in (R3-Z) — `0 < E_R(q) ≤ K₊` plus holomorphy of *both* functions on `Ω̄` — is discharged in the assembly by part (a) and the `E_R=0` branch. ✅
- `KF_WALL_REFEREE.md:27-31, 211-240` confirms `sup_{∂Ω∖Γ_R}|F_q| < 116.9436 < 117` **on the identical Ω and t₀** — so K₊ is the same quantity, conditional on full-width H₀ + anchor + holomorphy gates, exactly as (H-SIDE) states. ✅

**GAP (candidate defect, not refuted).** `R3_TRANSPORT_EXECUTION_SOL.md` has **no dedicated referee file**. The note's own header self-grades "CONDITIONAL TRANSPORT THEOREM PROVED; **CURRENT UNCONDITIONAL R3 REMAINS A GAP**". The assembly's §2 "Scope of (c)" says (c) "**is** licensed by a banked note" and that the note's §5 marks conjectural *only* the inputs — true — but the **application of the two-constants/harmonic-measure theorem itself, on the rectangle Ω with D_z ⊂ Ω, is a consumed, unrefereed step and is not listed as a gate in §3**, which claims "Nothing is omitted." **Repair text (new row in §3):**

> ### (H-TRANS) — the two-constants/Rouché transport implication itself
> Source `R3_TRANSPORT_EXECUTION_SOL.md:60-93,190-231` ((R3-Z), (3.4), §4). **Status: PAPER-LEVEL, UNREFEREED** — no `R3_TRANSPORT_EXECUTION_REFEREE.md` exists in lane G; the source's own header reads "CONDITIONAL TRANSPORT THEOREM PROVED; CURRENT UNCONDITIONAL R3 REMAINS A GAP". What would discharge it: a cold referee on the harmonic-measure/two-constants application (boundedness of F_q on Ω̄, the ω(s,Γ_R;Ω) interval cover, and the Rouché strictness on ∂D_z).

**Hejhal (7.22) scope — NOT VERIFIED.** The assembly cites (7.22) with no page number, and R3 §4 routes the convention through `LAW_HEJHAL_S7_EXTRACT.md:67-81`. Repair regardless: the assembly should print the page of (7.22) and assert it lies inside the in-repo excerpt pp. 568-600.

## Attack 3 — hypothesis-table completeness (PARTIAL)

Gates checked against source phrasing before lockout: (H-GEOM) `m_z ≥ 0.0439`, `ν_z ≥ 0.1552` quoted verbatim and correctly from `R3_TRANSPORT_EXECUTION_SOL.md:60-65`, both graded `PROVED, Arb interval cover` in that note's `:243-245` ledger — the assembly's grade matches. (H-SIDE): the assembly quotes the *un-superseded* `CONJECTURAL / MISSING family-uniformly` row at `:250` — confirmed present and not suppressed. Honest practice.

Unchecked (lockout): (H-RATE) sub-input table (8 rows), (H-HOL), (H-C4), (H-ROUTE), the "NOT assumed" table (6 rows), the LAW quotes in §5(c). **~2 of ~20 rows completed.** One defect found: the missing (H-TRANS) row above.

## Attack 5 — ADJUDICATION: NOT PERFORMED

The four conflict sources were all unreadable (EPERM). A ruling asserted from the assembly's own paraphrase would be exactly the "adopt the author's framing" failure this seat exists to prevent. **NOT-VERIFIABLE — must be re-run with filesystem access.** Prior (to be tested, not banked): the two readings are plausibly different scopes — `(RATE-A)` as a boundary-rate theorem on Γ_R^A vs. `(RATE-A) with α>0 as consumed by the monotonicity/DH2 activation` — zero independent evidence yet; must not be quoted as a finding.

## Attack 6 — ledger discipline of the note itself: PASS

§0 and §6 upgrade nothing; §4.5 states Q₀ as `max{…, q_monotone} ≥ 1.176e37` with the `≥` and the "I do not claim the max is closed" disclaimer; §5(c) states the LAW's logical disjointness and does not promote the LAW note's self-graded header. §3's (H-RATE) explicitly declines to adjudicate. The §1.1 hash-drift disclosure is voluntary and correctly quarantined. Unusually disciplined.

## Defect list

1. **`1/(αν_z) ≈ 4.47` is wrong** · `:604` · true value 5.36941580756…
2. **"The binding parameter is ν_z" is scope-ambiguous** · `:603-606` · true for the C_R-independent floor, false for the full Q₀ where α is 2× more elastic. High-consequence: it names the next research target.
3. **(H-TRANS) missing from a table that claims "Nothing is omitted"** · §3 · the two-constants/Rouché application is consumed from an unrefereed note.
4. **Hejhal (7.22) carries no page cite** · §2(c), §3.
5. **`N_monotone = q_side″` presented as a reproduced phenomenon rather than an identity** · §4.3 · cosmetic.
6. **(Referee-side)** attacks 1b, 3, 5 unexecuted (TCC lockout).

## House verdict

**GAPS NOT REFUTED.**

No tested claim was refuted, and the two hardest arithmetic attacks reproduce exactly on an independent mpmath leg. But the note cannot be graded CONFIRMED: defect 3 falsifies §3's completeness claim as stated, defect 1 is a refuted printed number, defect 2 is an unqualified claim that will steer research, and the adjudication plus ~18 of 20 hypothesis-table rows were never independently checked. A second referee pass with repo read access is required before any promotion, and it must run attacks 1b, 3 and 5 from scratch.

READY FOR JUDGING

---

*Installation note (orchestrator, 2026-08-20): produced by a read-only frontier-verifier agent during the TCC lockout and installed verbatim from its transcript after access was restored.*
