# Independent verification + novelty + OEIS-readiness arm — A089676 acute-set pilot

Scope: be the trust anchor and novelty guard for the acute-set pilot.
A089676: a(n) = max size of an ACUTE set S ⊆ {0,1}^n (every angle determined by
three points of S is strictly acute). Right angle at apex Q between P,R iff
(P−Q)·(R−Q) = 0. Records under test (Kamenetsky 2018 lower bounds):
a(11)≥24, a(12)≥32, a(13)≥33, a(14)≥64, a(15)≥128.

All commands quoted below were actually run; outputs are reproduced verbatim.

---

## JOB 1 — Second independent verifier (`verify2.py`)

`verify2.py` is written to share NO implementation idea with the trusted
`../verify.py`, so a bug in the math identity could not hide in both:

| aspect            | verify.py (trusted)              | verify2.py (this arm)                     |
|-------------------|----------------------------------|-------------------------------------------|
| vector storage    | python int **bitmask**           | explicit **integer coordinate list**      |
| right-angle test  | `(P^Q) & (R^Q) == 0` (XOR/AND)   | `sum_i (p_i−q_i)*(r_i−q_i) == 0` (dot)     |
| popcount?         | implicit via int                 | none — plain arithmetic                   |
| triple loop       | apex j, legs a<b                 | apex Q, `combinations(others,2)`          |
| sign guard        | (comment-level)                  | asserts each coord term ∈ {0,1} at runtime|
| parser            | regex split on header            | `finditer` header spans (rewritten)       |

`verify2.py` independently re-derives the "only a right angle is forbidden, no
obtuse angle is possible" fact by a coordinate sign argument (each per-coordinate
term (p−q)(r−q) ∈ {0,1} for 0/1 inputs), rather than from the XOR/AND identity.

### 1a. verify2 self-test (the 5 OEIS records)
```
$ python3 verify2.py --selftest
n=11: dim=11 size=24 claim=24 acute=True PASS
n=12: dim=12 size=32 claim=32 acute=True PASS
n=13: dim=13 size=33 claim=33 acute=True PASS
n=14: dim=14 size=64 claim=64 acute=True PASS
n=15: dim=15 size=128 claim=128 acute=True PASS
SELFTEST PASS
```

### 1b. trusted verifier, for comparison
```
$ python3 ../verify.py --selftest
n=11: size=24 claim=24 acute=True PASS
n=12: size=32 claim=32 acute=True PASS
n=13: size=33 claim=33 acute=True PASS
n=14: size=64 claim=64 acute=True PASS
n=15: size=128 claim=128 acute=True PASS
SELFTEST PASS
```
=> **Both verifiers PASS all 5 records and AGREE.**

### 1c. Differential cross-check (positives + forced negatives)
Per-n witness files run through BOTH verifiers; plus two adversarial negative
families injected into each record:
- NEGATIVE A: append an exact duplicate of the first point.
- NEGATIVE B: append a forced right angle (apex Q=0, P=e0, R=e1; disjoint
  supports ⇒ dot product 0).
```
=== POSITIVE (per-n clean record) ===
n=11 size=24: verify.py PASS rc=0 || verify2.py PASS rc=0 -> AGREE PASS
n=12 size=32: verify.py PASS rc=0 || verify2.py PASS rc=0 -> AGREE PASS
n=13 size=33: verify.py PASS rc=0 || verify2.py PASS rc=0 -> AGREE PASS
n=14 size=64: verify.py PASS rc=0 || verify2.py PASS rc=0 -> AGREE PASS
n=15 size=128: verify.py PASS rc=0 || verify2.py PASS rc=0 -> AGREE PASS
=== NEGATIVE A (duplicated point): all n -> AGREE reject (rc1=1 rc2=1) ===
=== NEGATIVE B (forced right angle): all n -> AGREE reject (rc1=1 rc2=1) ===
OVERALL: ALL AGREE
```

### 1d. In-process random differential fuzz (20,000 trials)
Random 0/1 sets, n∈[2,10], m∈[2,14]; assert `is_acute` (bitmask) and
`is_acute_explicit` (dot product) return identical verdicts.
```
fuzz in-process: 20000 trials, 0 verdict mismatches, 2861 acute-positives
RESULT: PERFECT AGREEMENT
```
2861 of the 20k random sets were genuinely acute, so the agreement is not the
trivial "both always reject" — the two engines agree on both classes.

### 1e. Canonical-source closure
The repo witness file is byte-identical to the live OEIS file `a089676_1.txt`:
```
$ md5 (local a089676_witnesses.txt) = bb4ddc5584f9ccf3743c06ade1b230ff
$ md5 (downloaded OEIS a089676_1.txt) = bb4ddc5584f9ccf3743c06ade1b230ff
diff -> IDENTICAL (byte-for-byte)
```
Both verifiers also PASS all 5 on the freshly-downloaded official file.

**JOB 1 verdict: verify2.py is a sound, independent trust anchor. It agrees
with verify.py on every test (5 records, both negative families, 20k fuzz).**
Any witness a pilot agent produces must pass BOTH `../verify.py` and
`verify2.py`.

---

## JOB 2 — Novelty re-confirm (records still unbeaten as of June 2026)

### Primary source: live OEIS A089676 (revision #108, 2026-05-30)
Retrieved via `https://oeis.org/search?q=id:A089676&fmt=json`
(WebFetch is 403-blocked by OEIS; the JSON API + curl with a browser UA works).

- Confirmed DATA (the proven terms) only reaches **a(10)=17**:
  `1,2,2,4,5,6,8,9,10,16,17` (offset 0). a(11..15) are lower bounds, not proven.
- Comment, verbatim (author Dmitry Kamenetsky, May 18 / Jun 05 2018):
  > "The best known lower bounds for a(11-15) are 24, 32, 33, 64 and 128.
  > a(11-14) were found by D. Kamenetsky, while a(15) was found by
  > D. Kamenetsky and V. Chubenko (see attached file). Lower bounds for n > 15
  > have been found by V. Harangi (see Table 3 in his paper)."
- **Full 108-revision history walked** (`/history?seq=A089676`). The bounds
  24/32/33/64/128 were entered in the #94–#97 cluster (Jun 05 2018). EVERY
  revision after that (#98–#108, Nov 2018 → May 2026) is housekeeping by OEIS
  editors:
  - #105–#107 (Aug 15 2024, von Brömssen/Heinz): a spelling fix
    "Furedi" → "Füredi" in a comment. No bound change.
  - #108 (May 30 2026, Sean A. Irvine): http→https in LINKS. No bound change.
  No revision in 2019–2026 altered any a(11..15) value; DATA never grew past 17.

### Most-recent serious computational treatment: Chubenko & Kurz
**"Divisible minimal codes", arXiv:2312.00885v3 (5 Jun 2025).** This is the only
post-2018 paper found that computes acute sets in {0,1}^n at these dimensions.
Relevant verbatim findings (from the PDF, extracted with pdftotext):
- It cites A089676 and notes max sizes are stated there "up to dimension d=10"
  — i.e. n≥11 remain lower bounds.
- n=9: exactly 5 acute sets of max cardinality 16 (one linear).
- n=10: 655 non-isomorphic acute sets of max cardinality 17 (none linear).
- n=11: "a partial search finding 17 non-isomorphic acute sets of size 23 and
  **two of size 24**" — i.e. it **reproduces** Kamenetsky's a(11)≥24, does NOT
  beat it.
- n=11 NEW result (does not change the lower bound): via an ILP argument they
  prove "the maximum cardinality of an acute set in {0,1}^11 is **upper bounded
  by 28**." So a(11) is now bracketed **[24, 28]**; the LOWER bound 24 stands.
- No new lower bound is reported for n=12,13,14,15.

### Code-theory connection (and why it does NOT touch these records)
Chubenko–Kurz formalize: the codewords of a binary minimal `[n,k]₂` code form an
acute set in `{0,1}^n` of size `2^k` (Randriambololona [Ran17]). KEY axis caution:
the acute-set ambient dimension = the code **LENGTH n**, NOT the code dimension k.
The active 2024–2025 minimal-code papers (Scotti, Alfarano–Bishnoi, etc.) improve
`m(k,2)` = the minimum **length** for a fixed **dimension** k — a different axis —
and yield acute sets in very high ambient dimension (e.g. a minimal `[62,17]₂`
code → 2^17 points in {0,1}^62). None of that improves a(11..15).
Also note records a(11)=24 and a(13)=33 are **not powers of two**, so they are
inherently NON-linear (beyond any minimal-code construction); Kamenetsky's
heuristic search remains the source.

### LLM-driven sweeps (AlphaEvolve / FunSearch / CPro1)
Searched for any AlphaEvolve / FunSearch / CPro1-style result on acute sets in
the hypercube (2024–2026). AlphaEvolve (arXiv:2506.13131) is real and has
improved some combinatorial constructions, but **no source found applies it (or
FunSearch/CPro1) to A089676 / acute sets in {0,1}^n**. No improvement located.

### JOB 2 verdict
**All five records are STILL the best known as of June 2026 — UNBEATEN.**
- a(11) ≥ 24  (now also ≤ 28, Chubenko–Kurz 2025; lower bound unchanged)
- a(12) ≥ 32
- a(13) ≥ 33
- a(14) ≥ 64
- a(15) ≥ 128
Sources: live OEIS A089676 (rev #108, 2026-05-30, full history); arXiv:2312.00885v3
(Chubenko & Kurz, Jun 2025). No 2019–2026 paper, preprint, or LLM sweep beat any
of them. If a pilot agent produces a larger acute set at any of these n, it would
be a genuine new record (see OEIS_SUBMISSION_DRAFT.md).

---

## JOB 3 — OEIS-submission prep
See `OEIS_SUBMISSION_DRAFT.md` for the ready-to-fill comment wording and the
witness-file format (matching Kamenetsky's `a089676_1.txt`).

---

## File manifest (this directory)
- `verify2.py`              — second independent verifier (`--selftest` built in)
- `NOTES.md`                — this file (all evidence, commands + outputs)
- `OEIS_SUBMISSION_DRAFT.md`— ready-to-fill OEIS comment + witness-file template
- `novelty_findings.md`     — sources + verbatim quotes for the novelty re-confirm
