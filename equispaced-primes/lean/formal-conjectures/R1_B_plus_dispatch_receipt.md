---
title: "R1 / B+ — Aristotle dispatch receipt: R1_B_plus.lean (4 sorry-stub identities) → full theorems"
type: dispatch-receipt
domain: research
created: 2026-05-09
sources:
  - handoff-2026-05-09-followup/R1_B_plus.lean
  - handoff-2026-05-09-followup/R1_B_plus_proof_attempt.md
  - handoff-2026-05-09-followup/R1_B_plus_proof_attempt.py
  - archive/request-projects/RequestProject/CrossTermPositive.lean
  - archive/request-projects/RequestProject/DisplacementShift.lean
  - archive/request-projects/RequestProject/PrimeCircle.lean
  - archive/request-projects/RequestProject/BridgeIdentity.lean
  - handoff-2026-05-04-theorem-B-and-C1/MertensDecomposition.lean
  - handoff-2026-05-04-theorem-B-and-C1/BridgeIdentityStatement.lean
tags: [aristotle, dispatch, lean, formalization, R1, B-plus, mth-bridge-identity, ramanujan-sum]
---

# R1 / B+ — Aristotle dispatch receipt

## Headline

**Project submitted to Aristotle.**
- **Project ID:** `8e608890-f0ba-4a89-bbb0-a63b5bcab697`
- **Status at dispatch:** `QUEUED`
- **Dispatched at (UTC):** `2026-05-09T21:07:37Z`
- **Mode:** asynchronous (no `--wait`).  Lean output is **not yet available**;
  poll for completion (instructions below).

## API contract used

| Item | Value |
|---|---|
| Service | Harmonic Aristotle (cloud Lean theorem prover) |
| Base URL | `https://aristotle.harmonic.fun/api/v2` |
| Auth | `Authorization: Bearer $ARISTOTLE_API_KEY` |
| Client | `aristotlelib` 1.0.1 (PyPI), Python 3.13 venv at `/tmp/aristotle_venv/` |
| CLI invoked | `aristotle submit "<prompt>" --project-dir /tmp/aristotle_dispatch_R1` |
| API key source | `~/.farey_api_keys` (env var `ARISTOTLE_API_KEY`); length 49, prefix `arstl_`, last 4 `CwzQ` |

## Relationship to prior dispatches

Second programmatic Aristotle dispatch from this account.  The first
(`424973ae-...-3ad`, P3b SmoothedDwfFormula, 2026-05-09T18:35Z) finished as
`COMPLETE_WITH_ERRORS` shortly before this dispatch.  This dispatch is
independent — it formalizes a different, structurally-simpler set of
identities (pure ℚ algebra + elementary Fourier on Farey sequences) and
uses a separate Lean payload.

## Payload summary (what Aristotle is working on)

**Project directory:** `/tmp/aristotle_dispatch_R1/` (uploaded, 3384 LOC total)

| File | LOC | MD5 | Role |
|---|---:|---|---|
| `lakefile.toml` | 11 | `d3ae68ec…888c` | Lake project config (Mathlib v4.28.0) |
| `lean-toolchain` | 1 | `b8b2923c…83b7` | `leanprover/lean4:v4.28.0` |
| `RequestProject/R1_B_plus.lean` | 189 | `bbbb0260…9ac9` | **Target file** — 6 `sorry`s (4 core + 2 specialization) |
| `RequestProject/PrimeCircle.lean` | 278 | `6e5f1404…0626` | Already-proved fareySet, totient sum identities |
| `RequestProject/DisplacementShift.lean` | 182 | `1aa15b70…41d2d` | Already-proved fareyRank, displacement, shiftFun |
| `RequestProject/BridgeIdentity.lean` | 363 | `6eb651fb…0328` | Already-proved mertens, classical Bridge identity (M(p)+2) |
| `RequestProject/CrossTermPositive.lean` | 356 | `f2780b6e…ee58` | Already-proved crossTerm, dispSquaredSum |
| `RequestProject/MertensDecomposition.lean` | 133 | `537dc161…058a` | Already-proved Lemma 3.1 (crossTerm = 2·B0 − 2·Spsi) |
| `RequestProject/StrictPositivity.lean` | 222 | `54f0825e…a718` | Auxiliary already-proved file (Σ δ² > 0) |
| `RequestProject/DenominatorSum.lean` | 554 | `c464b28c…6156` | Auxiliary already-proved file (Σ D = -φ(b)/2) |
| `RequestProject/MertensGrowth.lean` | 71 | `f2462e3b…cdc4` | Auxiliary already-proved file (M growth) |
| `R1_B_plus_proof_attempt.md` | 644 | `c324e168…da49` | Math reference (~33 KB; 10 V-checks; cited theorems) |
| `R1_B_plus_proof_attempt.py` | 380 | `127e3479…5ac5` | Exact-rational verifier (10 V-checks all passing on primes p ≤ 100) |

The 6 `sorry` targets in `R1_B_plus.lean`, in source order:

| # | Theorem | Type | Difficulty |
|---|---|---|---|
| 1 | `B0_closed_form` | Pure ℚ algebra (T1) | Low — Σ_f f, Σ_f rank(f) closed forms |
| 2 | `crossTerm_eq_V_NX_Q` | Pure ℚ algebra (T2) | Low — δ(f) = ⌊pf⌋ − (p−1)f substitution |
| 3 | `mth_bridge_identity` | Elementary Fourier (T3) | Medium — denominator grouping + Ramanujan sum bijection |
| 4 | `re_Tm_closed_form` | Reflection symmetry (T4) | Low — f → 1−f reflection on F_{p−1} |
| 5 | `re_T1_eq_M_plus_2_over_2` | Specialization | Low — m=1 of T4 + classical Bridge |
| 6 | `crossTerm_pos_iff_imTm_bound` | Reduction placeholder | Open — RHS uses `True` placeholder; `sorry` acceptable until SP-1 closure |

The four core theorems (T1–T4) are pure ℚ identities (T1, T2) and elementary
Fourier on the Farey set (T3, T4); none require analytic NT machinery beyond
what is already proved in `BridgeIdentity.lean`.

## Prompt sent to Aristotle (verbatim)

> Fill in all sorries in RequestProject/R1_B_plus.lean. Target: a fully-proved
> Lean 4 file (Mathlib v4.28.0) of four exact identities derived in
> R1_B_plus_proof_attempt.md (also bundled in this project dir) plus two
> specialization theorems. The four core sorries are:
>
> (T1) `B0_closed_form` — for every N, MertensDecomposition.B0 N = fareyV N
> - |F_N|·fareyX N - |F_N|/4. Pure ℚ algebraic identity. Proof outline:
> expand B0 using shift_eq_centered_minus_psi or the displacement
> definition, then use Σ_{f∈F_N} f = |F_N|/2 (Farey reflection f ↔ 1−f, with
> both 0/1 and 1/1 in F_N) and Σ_{f∈F_N} rank(f) = |F_N|·(|F_N|+1)/2 (rank
> is a permutation of 1..|F_N|).
>
> (T2) `crossTerm_eq_V_NX_Q` — for every prime p ≥ 2, crossTerm p / 2 =
> fareyV (p−1) − |F_{p−1}|·fareyX (p−1) − fareyQ p. Pure ℚ algebraic
> identity. Proof outline: substitute shiftFun p f = f − Int.fract(p·f) into
> the definition of crossTerm, then expand using the rank-displacement
> identity.
>
> (T3) `mth_bridge_identity` — for every prime p and every m ≥ 1, Re
> Σ_{f∈F_{p−1}} exp(2πimpf) = 2 + Σ_{b=2}^{p−1} c_b(m) where c_b(m) is the
> Ramanujan sum. Proof outline: group F_{p−1} by denominator b. The b=1
> contributions are f=0/1 and f=1/1, summing to 2. For 2 ≤ b ≤ p−1, since
> gcd(p,b)=1, the map a ↦ p·a mod b is a bijection on (ℤ/bℤ)^×, so the
> inner sum Σ_{a coprime to b} exp(2πi m p a / b) reduces to c_b(m) =
> Σ_{d∣gcd(m,b)} μ(b/d)·d. The classical Bridge identity (BridgeIdentity.lean,
> theorem `bridge_identity`) is the m=1 specialization (c_b(1) = μ(b)) and
> is already proved.
>
> (T4) `re_Tm_closed_form` — for every prime p and every m ≥ 1, Re T_m(p) =
> (1/2)·[2 + Σ_{b=2}^{p−1} c_b(m)] where T_m(p) := Σ_{f∈F_{p−1}} D(f)
> e^{2πimpf}. Proof outline: by f → 1−f reflection on F_{p−1}, rank(1−f) =
> |F_{p−1}|+1 − rank(f) and cos(2π m p (1−f)) = cos(2π m p f) (using m·p
> integer). Pairing gives Σ rank(f) cos(2πmpf) = (|F_{p−1}|+1)/2 · C_m(p)
> and Σ f · cos(2πmpf) = (1/2) · C_m(p), where C_m(p) is the m-th Bridge
> sum (T3). Subtracting: Re T_m = (|F_{p−1}|+1)/2 · C_m −
> |F_{p−1}|·(1/2)·C_m = (1/2)·C_m.
>
> Two specialization sorries:
> - `re_T1_eq_M_plus_2_over_2` — m=1 specialization of T4 + classical Bridge
>   identity (c_b(1) = μ(b), then Σ_{b=2}^{p−1} μ(b) = M(p−1) − 1 = M(p)
>   using μ(p) = −1 for prime p).
> - `crossTerm_pos_iff_imTm_bound` — placeholder reduction theorem
>   (currently has `True` placeholder RHS); leave the placeholder structure
>   but a `sorry` is acceptable here since SP-1 closure is open.
>
> Mathematical context bundled in this project dir:
> - R1_B_plus_proof_attempt.md (~33 KB, full mathematical context: cited
>   theorems, prior-route table, two named open sub-problems, cost
>   estimates)
> - R1_B_plus_proof_attempt.py (~12 KB, exact-rational verifier; 10
>   V-checks all passing on primes p ≤ 100)
>
> Project structure (all in RequestProject/):
> - PrimeCircle.lean — fareySet, totient sum identities (already proved)
> - DisplacementShift.lean — fareyRank, displacement, shiftFun (already
>   proved)
> - BridgeIdentity.lean — mertens, bridge_identity classical M(p)+2 result
>   (already proved); the c_b(1) = μ(b) identity is here
> - CrossTermPositive.lean — crossTerm, dispSquaredSum (already proved)
> - MertensDecomposition.lean — Lemma 3.1 already proved: crossTerm p =
>   2·B0(p−1) − 2·Spsi p, plus the pointwise (★) identity. The four target
>   sorries should be proved on top of these.
> - StrictPositivity.lean, DenominatorSum.lean, MertensGrowth.lean —
>   auxiliary already-proved files.
>
> If a sorry truly requires Mathlib infrastructure absent from v4.28.0
> (e.g. a particular Ramanujan-sum library lemma not yet in Mathlib),
> leave it as sorry and add a -- TODO(aristotle): prerequisite <name>
> comment — do NOT introduce new axioms. The four target identities are
> pure rational/elementary-Fourier algebra and should not require any
> analytic machinery beyond what already exists in `BridgeIdentity.lean`.
>
> Build target: `lake build RequestProject.R1_B_plus` returns 0 with no
> remaining sorries (apart from optional TODO-tagged ones).

## Aristotle's response

```
WARNING: Your project contains .lean files but no .lake folder.
Aristotle works better with access to your project's dependencies.
Did you forget to run `lake build`?

Project created: 8e608890-f0ba-4a89-bbb0-a63b5bcab697
```

The `.lake` warning is benign (same as P3b dispatch): the upload omits the
local Mathlib build artefacts (~5 GB).  Aristotle's worker will resolve
Mathlib v4.28.0 from its own cache.

`aristotle list --limit 5` immediately after submission confirmed:

```
ID                                   STATUS    CREATED       PROGRESS
8e608890-f0ba-4a89-bbb0-a63b5bcab697 QUEUED   5 secs ago    -
```

(P3b's `424973ae-…-3ad` is now `COMPLETE_WITH_ERRORS` — see its receipt for
follow-up.)

## How to poll / retrieve the result

**Pre-flight (every session):**

```bash
set -a; source ~/.farey_api_keys; set +a   # loads ARISTOTLE_API_KEY
source /tmp/aristotle_venv/bin/activate    # aristotlelib 1.0.1
```

**Check status of just this project (one-liner):**

```bash
/tmp/aristotle_venv/bin/aristotle list --limit 50 \
  | grep -F 8e608890-f0ba-4a89-bbb0-a63b5bcab697
# status moves QUEUED → IN_PROGRESS → COMPLETE / COMPLETE_WITH_ERRORS / FAILED / OUT_OF_BUDGET
```

**Block until done and download the result tarball:**

```bash
/tmp/aristotle_venv/bin/aristotle result 8e608890-f0ba-4a89-bbb0-a63b5bcab697 \
  --destination /Users/za/Documents/Farey\ NOW/primes-equispaced/formal-conjectures/R1_B_plus_aristotle_result.tar.gz
```

**Cancel (if needed):**

```bash
/tmp/aristotle_venv/bin/aristotle cancel 8e608890-f0ba-4a89-bbb0-a63b5bcab697
```

**Multi-project polling.** `scripts/poll_aristotle.sh` was extended to
poll a list of project IDs sourced from
`scripts/aristotle_project_ids.txt` (one ID + label per line). To poll
both P3b and this new R1 project, run:

```bash
./scripts/poll_aristotle.sh                # one-shot status of both
./scripts/poll_aristotle.sh --watch        # poll every 15 min, both projects
./scripts/poll_aristotle.sh --download R1_B_plus  # download R1 once COMPLETE
```

**Expected wall-clock.**  Per the task brief, Aristotle takes **4-8 weeks**
on full theorems of analytic-NT difficulty.  The four R1 core targets
(T1–T4) are pure ℚ algebra (T1, T2) + elementary Fourier (T3, T4) — no
analytic continuation, no contour shifts, no Stirling — so this dispatch
is at the **easy end** of the difficulty spectrum.  Comparable
sorry-fill projects in the account log have completed within minutes to
hours; the analytic outlier was P3b at "still completing after 2 hours".
Estimate: minutes to ~1 day, but capped at 4-8 weeks per Harmonic SLA.

## Once Aristotle returns COMPLETE

1. Download tarball with `aristotle result <id> --destination …`
2. Extract to obtain `R1_B_plus.lean` (the filled-in version)
3. Save to `formal-conjectures/R1_B_plus_full.lean`
4. Run `lake build RequestProject.R1_B_plus` from this repo root; capture output
5. Verify `grep -c "sorry\|axiom" R1_B_plus_full.lean` ≤ 1 (the
   `crossTerm_pos_iff_imTm_bound` placeholder is permitted to remain)
6. Append build status + sorry/axiom audit to this receipt

## Local artefacts (preserved for reproducibility)

- `/tmp/aristotle_dispatch_R1/` — full project directory submitted (do not
  rely on this surviving reboots; copy to repo if needed for audit)
- `/tmp/aristotle_submit_R1_output.txt` — verbatim CLI stdout from `aristotle submit`
- `/tmp/aristotle_R1_prompt.txt` — verbatim prompt text passed to Aristotle
- `/tmp/aristotle_venv/` — Python 3.13 venv with `aristotlelib` 1.0.1

## Constraints honoured

- **API key never written to any saved file.**  The key was sourced from
  `~/.farey_api_keys` into the env (length 49, prefix `arstl_`, last 4
  `CwzQ`); only this masked form appears in any artefact.
- **R1 deliverables read-only.**  `handoff-2026-05-09-followup/R1_B_plus.lean`,
  `R1_B_plus_proof_attempt.md`, and `R1_B_plus_proof_attempt.py` were
  copied verbatim into the dispatch payload (only the canonical-vs-bare
  Lean import paths in the dispatch copy of `R1_B_plus.lean` were
  rewritten to `import RequestProject.X`, matching the in-payload
  module layout). The handoff sources are unchanged.
- **No bundle modifications.**  `archive/request-projects/RequestProject/`
  and `handoff-2026-05-04-theorem-B-and-C1/` files were copied (read-only)
  into the dispatch payload; `MertensDecomposition.lean`'s imports were
  adjusted in the *copy* (not the source) to point at
  `RequestProject.PrimeCircle` etc.
- **No Lean proofs written by the dispatcher.**  The four core sorries
  remain as `theorem … := by sorry`; only the prose comments and import
  paths were touched in the dispatch copy of `R1_B_plus.lean`.

## Appendix — payload sanity checks

- `wc -l /tmp/aristotle_dispatch_R1/RequestProject/R1_B_plus.lean` → 189
- `grep -c "sorry" /tmp/aristotle_dispatch_R1/RequestProject/R1_B_plus.lean` → 7 (6 actual `:= by sorry`, plus 1 mention in the file-header docstring at line 11)
- `grep -c "axiom " /tmp/aristotle_dispatch_R1/RequestProject/R1_B_plus.lean` → 0
- All `import` lines in dispatch payload resolve to a sibling file in
  `RequestProject/` (no dangling imports).
