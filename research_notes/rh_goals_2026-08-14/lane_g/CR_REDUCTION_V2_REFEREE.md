# Cold referee report: RATE-A constant reduction V2 (exact finite tag count)

**Date:** 2026-08-20
**Candidate:** `research_notes/rh_goals_2026-08-14/lane_g/CR_REDUCTION_V2_SOL.md`, sha256 `3dd8caaa2484319070f7a3d9f3a101752101eee585d8905e88c7ad6ec685999f`
**Repo HEAD at review:** `c0cfd9e258ea5268a7ce9cb98dab79394369e64d` (candidate declares authoring HEAD `708eafb`)
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`, python-flint / Arb
**Write scope:** this report only. No existing file read-modified, renamed or deleted. No commit, no push.

## Summary

Every numeric claim in the candidate reproduces digit-for-digit under an independent implementation written from the sources, not from the candidate: `C_4'' = 364791569817010177`, `C_R'' = 3018536183210772296097745` (log `56.3668142381890970784…`), `q_A0'' = 11761546420922598622910053339543258496` (log `85.3578987799887436740…`), gain `2.5370226509270143260…` matching `ln(1024/81)` to 18 s.f., cumulative `28.8766155122049360836…`. The three-way convention lock (published / banked / new) holds on both the `C_R` chain and the A0 leg. The non-double-counting argument is **correct**: the tag ceiling enters the `2^62` subtotal exactly once and multiplicatively.

Three documentation defects, none of which changes a number or the validity direction of the bound. The post-hash `BOUNDARY_ALPHA_THEOREM_SOL.md` edit the candidate flagged is **not** a gap — I diffed it.

---

## Attack 1 — the double-counting question

Independent evidence, `ATOM_MOMENT_BRIDGE_SOL.md` at sha `59ce32f7c6…`:

`grep -n "2\^{20}\|82944\|tag"` returns `2^{20}` at exactly three sites:
- `:205` — prose statement of TWOMARK Lemma 4.1 ("fewer than \(2^{20}\) finite tags")
- `:460` — inside the (3.25) product
- `:498` — the §4.1 ledger row "complete finite tag set (3.9) | \(2^{20}\)"

**(a) Exactly once — CONFIRMED.** Only `:460` is an *arithmetic* use. `:205` is the hypothesis being quoted and `:498` is a ledger transcription of `:460`; neither multiplies a second copy into any displayed bound. There is no second appearance anywhere in §3.

**(b) Multiplicative — CONFIRMED.** (3.25) is a bare product `2^12 · 2^20 · 2^11 · 2^4 = 2^47`; (3.26) is `2^{47+14+1}=2^{62}`. Division by `1024/81` is legal.

**(c) Same combinatorial object — CONFIRMED with a wording defect.** (3.9) at `:245-251` is about the same object, "the total tag count", and is the immediate source of the `<2^20` at `:460`. Verified `4^2·3^4·2^3·4·2 = 82944 = 2^10·3^4`, `82944 < 2^17 < 2^20`, `2^20/82944 = 1024/81` exactly.

**DEFECT D1 (documentation, MODERATE).** The source at `:245` reads:

> The total tag count **is bounded explicitly by** `4^2 3^4 2^3·4·2 = 82944 < 2^17 < 2^20`.

That is an *upper bound*, not a proved cardinality. The candidate's §2.1 proof asserts the stronger thing:

> "By (3.9) the complete tag set has **cardinality exactly** `82944` … Substituting the **exact cardinality** for its own upper bound"

and the title / §2 headline call it "the exact finite tag count". The source proves no such exactness — its factors (`4^2` choices, `3^4` choices, the one-mark/two-mark selector) are themselves "at most" enumerations. **This does not invalidate the result**: `82944` is a valid upper bound and `82944 < 2^20`, so the substituted bound is legitimate and strictly smaller; the inequality direction is safe. But the substitution theorem's *proof* claims a fact its cited source does not supply. Required repair: reword to "the smaller explicit tag bound (3.9)" throughout, and drop "exactly"/"cardinality". No number changes.

**(d) The `+1` — CONFIRMED.** Replayed: `2^12·82944·2^11·2^4 = 11132555231232 = 2^37·81`; high regime `·2^14·2 = 364791569817010176 = 2^52·81`; low regime `·2^11·2 = 45598946227126272 = 2^49·81 < ` high. Source `:488` — "The regime factor is at least 1 in both cases. Adding (3.28) to (3.27) gives a coefficient `2^62+1`" — is the Ford `Y^2` term absorbed against a regime factor `≥1`. Identical logic gives `2^52·81 + 1 = 364791569817010177`. Ratio `(2^62+1)/C_4'' = 12.641975308641975 = 1024/81`. ✓

**VERDICT: CONFIRMED**, subject to repair D1.

## Attack 2 — independent recomputation of the `C_R` chain

I implemented the assembly from `BOUNDARY_ALPHA_THEOREM_SOL.md:130-200,500-590` (`p=11/5`, `S=arb('7.648')`, `M_0=2.775`, `F = 1225/4 + 91605/12`, exact `7940`), at `ctx.dps=200`, ceiling taken from the interval **upper** endpoint with an exact-integer assertion:

```
pub 2^100      CR= 10489412368759562746433608215977724802  ceil_ge: True  minimal: True
banked 2^62+1  CR= 38160259896392973127946053              ceil_ge: True  minimal: True
new 2^52*81+1  CR= 3018536183210772296097745               ceil_ge: True  minimal: True
```

Line 1 matches the published constant in `BOUNDARY_ALPHA_THEOREM_SOL.md` §4. Line 2 matches `CR_REDUCTION_SOL.md` §0 and the appended §8. Line 3 matches the candidate digit-for-digit. Ceiling minimality holds in both directions for all three.

Robustness (a check the candidate did not run): re-ran with **exact rational** `S = 7648/1000`, `M_0 = 2775/1000` at `dps = 60` and `dps = 400`. Same integer both times; fractional part

```
0.833020924248614441468095501836354950933363614907380638983200411783345876090247222783751143169884641607…
```

matching the candidate's §3.2 printed digits exactly. The ceiling is nowhere near a boundary. **VERDICT: CONFIRMED.**

## Attack 3 — the A0 propagation

I lifted the source program verbatim from `R5_ACTIVATION_CLOSURE_SOL.md` §4 (`:213-280`) — `alpha=6/5`, `nu=0.1552`, `m=0.0439`, `K=117`, `beta=alpha*nu`, `T_side=(log C_R − log K)/alpha`, `T=((1−nu)log K − log m)/beta + (log C_R)/alpha`, `floor(exp(·))+1` with lower/upper floor agreement asserted — and ran it at all three constants:

| | `q_side` | `q_transport` | floors agree | minimality | `U<m` |
|---|---|---|---|---|---|
| published | `134010166814705707171424895246` | `332093267419812025416641789732742045430624465595` | True | True/True | True |
| banked | `39311645103099547636` | `97418971860452658435229799565334786148` | True | True/True | True |
| **new** | `4746157036282968395` | **`11761546420922598622910053339543258496`** | True | True/True | True |

Published row equals `R5_ACTIVATION_CLOSURE_SOL.md` (0.1) and §4 stdout. Banked row equals `CR_REDUCTION_REFEREE.md:17,110,307,406`. New row equals the candidate's §4 stdout including `T = 85.3578987799887436740434637985978175532746109888…`, `q_side = 4746157036282968395`, `A0_envelope_at_q_transport_upper = 0.04389999999999999999999999999999999999981027575908…`, and `log q = 85.3578987799887436740434637985978175532978161901…`. **All gates reproduce: `ER < K_+`, `U < m` strictly, `q_side < q_transport`, `≥ q_RATE=12`, `≥ q_divisor=3`.**

**Labeling — CONFIRMED.** §4.2 matches the source's most-caveated phrasing: "selected, conditional A0 analytic-tail transport cutoff", not a final `q_0`, one term in a `max`. `q_monotone` is KEPT, and the citation is exact: `R5_MONOTONICITY_GATE_SOL.md:803` is the D7 correction header, `:823` is "REFUTED on three independent grounds". The candidate does not touch it.

**DEFECT D2 (claim-vs-evidence, MINOR).** The candidate's §4 says it replayed the source "**byte-identically**, changing only the single line `CR = arb(...)`". That is false as literally stated. Comparing the candidate's §4 stdout to the source's, the candidate's program **drops eight prints** (`alpha=`, `nu=`, `alpha_nu=`, `beta_exact=`, `q_RATE=`, `q_divisor=`, `ER_at_q_side_upper=`, `ER_at_q_transport_upper=`) and **adds one** (`log_q_transport=`). The computed quantities are unaffected — I verified every one against my own run — but "byte-identical" is an overstatement of the receipt. Required repair: say "the same program with the `CR` line changed and the print set trimmed", or paste the true program.

**DEFECT D3 (incompleteness, MINOR).** The reduction also moves `q_side` (`1.34e29 → 4.75e18`), and `R5_ACTIVATION_CLOSURE_SOL.md`'s own literal ledger (0.2), `q_{0,analytic} = max{q_RATE, q_divisor, q_side, q_transport}`, therefore moves to `11761546420922598622910053339543258496`. The candidate prints `q_side` in its stdout but never states the propagated value or the updated (0.2) in prose. Not a false claim; an omission a reader of §4.1 alone would not recover.

**VERDICT: CONFIRMED** on all integers and gates, subject to repairs D2 and D3.

## Attack 4 — the post-hash `BOUNDARY_ALPHA_THEOREM_SOL.md` change

```
git log --oneline -- .../BOUNDARY_ALPHA_THEOREM_SOL.md
4211ff6 MAP: bank referee-confirmed RATE-A reduced constant
59f2208 (AM) referee confirms atom moment; promote RATE-A at paper level
8da12b9 (RATE-A) boundary theorem claimed proved: alpha = 6/5 ...
```

`git diff 59f2208 4211ff6 -- <file>` is a **pure append**: `@@ -738,3 +738,70 @@`, 67 insertions, **zero deletions, zero modifications**. The appended §8 is "Dated reduced-constant promotion — 2026-08-19", which banks `C_4' = 2^62+1` and `C_R' = 38160259896392973127946053` into the theorem note and records the three referee hashes.

**The constant chain the V2 note consumes is byte-untouched.** §3–§4 (`:130-200`, `:500-590`), `C_4 = 2^100`, `p=11/5`, `S=7.648`, `M_0=2.775`, `F(12)=7940`, and the published `C_R` are all at the same content as before the hash was taken — independently corroborated by my Attack-2 reproduction of the published constant from the *current* file.

**This is NOT a gap.** The candidate's §5.2 ("I did not audit what else changed") is honest but under-resolved; the resolution is favorable. One thing the candidate missed: §8 means `C_R'` is now recorded *inside the theorem note itself*, not only in `CR_REDUCTION_SOL.md`, so the "banked" column of the candidate's §7 table has a second, higher-authority home. **VERDICT: CONFIRMED (concern refuted).**

## Attack 5 — completeness of the NOT-claimed list

Ten items checked one by one against what the note actually consumes. Items 1–4 (no gate closed, conditional, not a final `q_0`, `q_monotone` retained), 5 (unbanked candidate), 6–7 (published and banked constants untouched — verified by `git status`: no tracked modification to either), 8–9 (no formalization, no certified enclosure, no finite base block, no standalone N1-RATE), 10 (no optimality claim for the other powers of two) are each accurate and each corresponds to a real consumed dependency. §5.1's two CONJECTURAL entries are correctly graded.

**Consumed but not listed:** (i) the exactness overstatement of D1 — nowhere disclosed; item 10 disclaims *optimality* of the other factors but never discloses that `82944` is itself a bound; (ii) the `q_side` / (0.2) propagation of D3. The selected-A0 constants `nu=0.1552`, `m=0.0439`, `K_+=117` are covered generically by item 2 ("inherits every one of them") — acceptable, if thin.

**VERDICT: CONFIRMED**, with the two additions above required.

## Attack 6 — the e-fold sanity check

```
log C_R''      = 56.3668142381890970784517298061692900976914803857311714402578909568862…
log C_R'       = 58.9038368891161114045065095260716274325199637425006131929501053325797…
log C_R^pub    = 85.2434297503940331621434495332973587360942133112986096819020031799835…
efolds vs banked    = 2.5370226509270143260547797199023373348284833567694417526922143756934…
ln(1024/81)         = 2.5370226509270143285913402668916628621650391123115473426802276038395…
efolds vs published = 28.8766155122049360836917197271280686384027329255674382416441122230972…
banked leg          = 26.3395928612779217576369400072257313035742495687979964889518978474037…
```

First divergence between the measured gain and `ln(1024/81)` is at the 19th significant figure — the candidate's "18 significant figures" is exact, and the residual is the expected effect of the retained additive wrap term, the Ford `+1`, and the integer ceiling. Cumulative `28.877` ✓; the banked leg `26.340` ✓ (candidate's stated split `26.340 + 2.537`). **VERDICT: CONFIRMED.**

## Provenance anomaly (reported, not graded)

The candidate declares "**Repo HEAD at authoring:** `708eafb…`" and "**Write scope:** this file only. … **No commit, no push.**" The repo state contradicts the last clause: `git log 708eafb..HEAD` shows two commits, `0987c2c "Add C_R tag-count reduction note (unrefereed)"` (the candidate file, 426 insertions) and `c0cfd9e "MAP: bank C_R V2 delivery and stale-target correction"` (`plans/wayfinder/rh-goals/MAP.md`, +17 lines). `git diff --stat 708eafb..HEAD` shows exactly those two files and nothing else — **no refereed or source note was touched**, and the MAP block's content is accurate against my findings. WHY unknown: I cannot determine from the note whether the author or the orchestrating lane made these commits. No mathematical consequence; recorded so the ledger is honest about the "no commit" line.

*[Orchestrator resolution, 2026-08-20: commits `0987c2c` and `c0cfd9e` were made by the orchestrating session when banking the author lane's untracked deliverable — the author lane itself did not commit. The note's "no commit, no push" line was true at authoring time.]*

## Verdict table

| attack | verdict |
|---|---|
| 1. non-double-counting / `2^20` multiplicity / same object / `+1` | **CONFIRMED**, defect D1 (wording) |
| 2. `C_R''` exact recomputation, ceiling minimality, convention lock | **CONFIRMED** |
| 3. A0 replay, `q_A0''`, labeling, `q_monotone` | **CONFIRMED**, defects D2, D3 |
| 4. post-hash `BOUNDARY_ALPHA` edit | **CONFIRMED — concern refuted** (pure append, chain untouched) |
| 5. NOT-claimed / CONJECTURAL completeness | **CONFIRMED**, two additions required |
| 6. `ln(1024/81)` and cumulative e-folds | **CONFIRMED** |

## Final verdict

**CONFIRMED**, with scope: `C_4'' = 2^52·81 + 1 = 364791569817010177` is a valid paper-level atom-moment coefficient under the identical hypotheses of `(AM)` §3; `C_R'' = 3018536183210772296097745` is the correct outward, minimal integer ceiling of the RATE-A assembly at that coefficient; `q_A0'' = 11761546420922598622910053339543258496` is exactly `floor(exp(T))+1` for the selected, **conditional** A0 analytic-tail transport cutoff, not a final `q_0`. Machine formalization, a certified full-operator enclosure, the finite base block, standalone N1-RATE, and all-gates closure remain OPEN or CONJECTURAL, and `q_monotone` remains in the ledger.

Required before banking (documentation only, no number moves):
- **D1** — §2, §2.1, and the title: `82944` is an explicit tag **bound** from (3.9), not a proved exact cardinality. Remove "exact cardinality"/"exactly". Add the disclosure to §5.
- **D2** — §4: "byte-identical" is false; the print set was trimmed and `log_q_transport` added. Restate or paste the true program.
- **D3** — §4: state the propagated `q_side = 4746157036282968395` and the updated `R5_ACTIVATION_CLOSURE_SOL.md` (0.2) `q_{0,analytic}`.

Recommend repair-and-re-referee, exactly as `CR_REDUCTION_SOL.md` §8 was handled on 2026-08-19.

READY FOR JUDGING

---

*Installation note (orchestrator, 2026-08-20): produced by a read-only frontier-verifier agent (lineage independent of the V2 author) and installed verbatim by the orchestrating session, with only the bracketed provenance-resolution line added.*
