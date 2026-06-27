# Probe F — Binary Orientable Sequences OS(8): beat 92 or settle n=8

**Date:** 2026-06-27
**Status field (filled at end):** see VERDICT.

## Aim

Produce a genuine NEW math fact on binary orientable sequences of order n=8:
either a cyclic binary OS(8) of period ≥ 93 (beating the best-known 92), or a
proof that 92 is maximal (settling n=8). Independently-checkable
witness/certificate required.

## Definitions and ground truth (web-verified)

**Definition** (Gabrić–Sawada, arXiv:2401.14341, abstract, verbatim):
"An orientable sequence of order n is a cyclic binary sequence such that each
length-n substring appears at most once **in either direction**." Equivalently
(Mitchell–Wild 2507.02526, Def. 1.2): an OS_k(n) requires `s_n(i) ≠ s_n(j)^R`
for all i,j — no length-n window equals the reverse of any length-n window
(including itself ⇒ no palindromic window). The "period" is the length L of the
cyclic sequence; it has L cyclic windows.

**Ground-truth table** (Gabrić–Sawada arXiv:2401.14341, Table 2, binary k=2):

| n | longest-known L* | upper bound U |
|---|------------------|---------------|
| 5 | 6  | 6  |
| 6 | 16 | 17 |
| 7 | 36 | 40 |
| 8 | **92** | **96** |

So for n=8 the open gap is L ∈ {93,94,95,96}; L ≥ 97 is impossible by the U=96
upper bound. The best-known 92 (= L*) was found by Gabrić–Sawada via extension
techniques on top of their cycle-joining construction (a heuristic, non-exhaustive
search); the string itself is **not printed** in the papers. (Note: Mitchell–Wild
Table 1 lists an improved *cyclic* upper bound of 105 for n=8 under a different
framing, but the operative aperiodic bound for this object is U=96.)

## Tooling built (under `code/os_probe/`)

- `verify_os.py` — exact verifier built from scratch, directly from the
  2L-distinctness definition (L windows + L reversals all distinct). Reports the
  exact failure cause on rejection. CLI: `python3 verify_os.py <seq|file> -n 8 -v`.
- `sat_os.py` — SAT encoding v1 (pattern-occupancy: per-position pattern-match
  vars, at-most-one per pattern = forward-distinct, palindrome-forbidden,
  ¬(y_p ∧ y_{rev p})). Solver: CaDiCaL via python-sat.
- `sat_os2.py` — SAT encoding v2 = v1 + **rotation symmetry breaking** (lex-leader:
  the bit string must be lexicographically ≤ all L cyclic rotations of itself;
  sound for existence/UNSAT because OS(n) is rotation-invariant). ~20× faster on
  UNSAT.
- `test_validate.py` — validation harness tying verifier + SAT to known maxima.

### Verifier + SAT VALIDATED against known ground truth

`python3 test_validate.py` → ALL PASS. Specifically:
- Verifier rejects palindromic windows, reverse-collisions, repeated windows.
- Verifier ACCEPTS known maximal witnesses: OS(5) period-6 `001011`,
  OS(6) period-16 `0001010110010111`; REJECTS one-bit corruptions.
- SAT model reproduces known maxima exactly:
  - n=5: SAT@6, UNSAT@7 ⇒ max=6 ✓ (matches L*=6).
  - n=6: SAT@16, UNSAT@17 ⇒ max=16 ✓ (and PROVES 16 is the true max; lit had U=17).
  - n=7: SAT@36, UNSAT@37,38,39,40,41 ⇒ **max=36 PROVEN**.

**Side result — NOT NEW (corrected in main loop, 2026-06-27).** The agent initially read the
table's "upper bound 40" for n=7 as meaning the exact maximum was open, and called the SAT sweep
(SAT@36, UNSAT@37–40 ⇒ max=36) "a small new settled fact." **This is WRONG — OS(7)=36 is already
PROVEN.** Web-verified: per Mitchell–Wild (arXiv:2507.02526) / Gabrić–Sawada (arXiv:2401.14341),
"maximal length orientable sequences are known only for n ≤ 7, confirming 36 is the maximum length
for an order-7 orientable sequence," established by exhaustive search. The "upper bound 40" is a
theoretical/formula bound, not a statement that the exact value was unknown. So the SAT sweep
REPRODUCED a known result; n=8 is the FIRST genuinely open order. (v1 ~11s/L, v2 ~0.5s/L.)
**Independent cross-check (main loop, code/os_probe/brute_os.py):** a from-scratch exhaustive brute
force confirms OS(5)=6 (UNSAT@7) and OS(6)=16 (UNSAT@17, exhaustive over all 2^17=131072 length-17
strings) — validating that the SAT encoding's UNSAT verdicts are trustworthy on real instances.

## Task 2 — reproduce 92 from scratch (slack check)

SAT at L=92, n=8 returns **SAT in 4.6 s** (v1). The found sequence
(`code/os_probe/witness_os8_L92.txt`):

```
10000100011100101010111001101011111001000101110110001010110110010110000010100100110001111011
```

passes the independent verifier:
`python3 verify_os.py witness_os8_L92.txt -n 8 -v` →
`92 windows + 92 reversals = 184 all distinct. OK. RESULT: VALID`.

⇒ The record 92 is easily reachable from scratch; the setup is sound and the
**slack is real**. Target confirmed **SOFT** (the known 92 was a heuristic
non-exhaustive find; SAT reaches it in seconds, and the exact frontier 93–96 is
SAT-tractable as the n≤7 settles demonstrate).

## Task 3 — settle n=8 (does period ≥ 93 exist?)

Method: SAT decision for each L ∈ {93,94,95,96} (L ≥ 97 ruled out by U=96).
- Outcome A: any SAT ⇒ explicit period-≥93 sequence ⇒ NEW RECORD.
- Outcome B: all four UNSAT ⇒ 92 PROVEN MAXIMAL ⇒ n=8 SETTLED.

Both v1 (no symmetry breaking) and v2 (rotation lex-leader) were run.

**RESULTS (n=8 settle): UNRESOLVED.** The decisive instance L=93 (does a period-93 OS(8) exist?)
did NOT resolve within the compute budget — the SAT runs ground for >40 min and were
killed/timed-out with no SAT and no UNSAT (no record file, empty settle log). So n=8 is neither
beaten nor settled. The audit's "SAT-tractable quick settle" was optimistic: n≤7 settles are
seconds, but L=93 at n=8 is a genuinely hard instance at this encoding/solver/compute level.

## VERDICT

**NO new fact produced.** Honest outcome:
- Tooling (verifier + two SAT encodings) built and VALIDATED — reproduces all known maxima n≤7,
  independently cross-checked by from-scratch brute force at n=5,6.
- Target confirmed SOFT in method (92 is a heuristic find, SAT reaches it in seconds) — but the
  n=8 *settle* is NOT cheap: L=93 did not resolve.
- The "OS(7)=36 new fact" was a misread — it is already known (n≤7 settled in the literature).
- CONCRETE NEXT STEP toward a real new fact: settle n=8 by throwing a stronger SAT/CP solver or
  more compute / better symmetry-breaking at L=93..96. Either a period-≥93 sequence (new record) or
  UNSAT-through-96 (proves 92 maximal, settles the first open order) would be a genuine new fact.

## Honesty notes / anti-fooling

- Any claimed ≥93 sequence is emitted explicitly and re-checked by the standalone
  verifier (which is itself validated against known maxima and rejects
  corruptions). A "heuristic didn't find it" is NOT reported as a settle.
- A "92 maximal" claim rests ONLY on UNSAT for **all** of L=93..96 from the SAT
  encoding, which is validated to agree with brute-force ground truth on n=5,6,7.
  The encoding's UNSAT = a complete certificate (CaDiCaL is a complete solver).
- No sequence, bound, or citation fabricated. All bounds quoted from the two
  papers above with line-level extraction from the PDFs.
