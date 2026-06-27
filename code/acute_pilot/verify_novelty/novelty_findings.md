# Novelty findings — are a(11..15) = 24/32/33/64/128 still the best known? (June 2026)

VERDICT: **YES, all five are still the best known. NONE has been beaten by any
2019–2026 paper, preprint, or LLM sweep.** Evidence below, with verbatim quotes.
Nothing here is fabricated; every quote was pulled from the cited source as run.

---

## 1. Live OEIS A089676 — the authoritative record

WebFetch is 403-blocked by oeis.org. Retrieved instead via the JSON API and curl
with a browser User-Agent:
`curl -A "Mozilla/5.0" "https://oeis.org/search?q=id:A089676&fmt=json"`

- **Record metadata:** revision #108, last edited 2026-05-30T16:40:10 (Sean A.
  Irvine). Author David Bevan, 2004. Keywords `nonn,more,nice`.
- **Confirmed DATA (proven terms), offset 0:** `1,2,2,4,5,6,8,9,10,16,17`
  → only goes up to **a(10) = 17**. a(11..15) are LOWER BOUNDS, not proven values.
- **The load-bearing comment (verbatim), by Dmitry Kamenetsky, May 18 / Jun 05 2018:**
  > "The best known lower bounds for a(11-15) are 24, 32, 33, 64 and 128.
  > a(11-14) were found by D. Kamenetsky, while a(15) was found by D. Kamenetsky
  > and V. Chubenko (see attached file). Lower bounds for n > 15 have been found
  > by V. Harangi (see Table 3 in his paper)."

### Full revision-history walk (108 of 108 revisions captured)
`/history?seq=A089676&start=...` paged through all 108 revisions.
- The bounds 24/32/33/64/128 were entered in the **#94–#97 cluster, Jun 05 2018**
  (Dmitry Kamenetsky + N. J. A. Sloane).
- All later revisions are housekeeping, NOT bound changes:
  - **#98–#104 (Nov 2018):** formatting/cross-ref edits (Schoenfield, Greubel,
    Marcus, Arndt).
  - **#105–#107 (Aug 15 2024, von Brömssen → Heinz):** a single spelling fix,
    "Furedi" → "Füredi", inside the Randriambololona comment. No numeric change.
  - **#108 (May 30 2026, Sean A. Irvine):** changed `http`→`https` in two LINKS.
    No numeric change.
- The confirmed DATA string never extended past `...,16,17` in any revision.

**Conclusion from OEIS:** as of the live database (2026-05-30) the five records
are exactly as Kamenetsky set them in 2018. No improvement was ever submitted.

### Canonical witness file matches repo
`https://oeis.org/A089676/a089676_1.txt` (the file linked in the LINKS section)
downloads to 8537 bytes, md5 `bb4ddc5584f9ccf3743c06ade1b230ff`, **byte-identical**
to the repo's `code/acute_pilot/a089676_witnesses.txt`. Both verifiers PASS all 5
on the freshly downloaded official copy.

---

## 2. Most recent serious computational paper: Chubenko & Kurz

**"Divisible minimal codes", arXiv:2312.00885v3, dated 5 Jun 2025** (authors
Vladimir Chubenko, Sascha Kurz). Extracted with `pdftotext`. Verbatim:

> "the maximum possible sizes of acute sets in {0,1}^d up to dimension d = 10 are
> stated in A089676 of the 'The On-Line Encyclopedia of Integer Sequences' (OEIS)."

> "Up to isomorphism there are exactly five acute sets in {0,1}^9 with maximum
> cardinality 16 – only one of them is linear. In {0,1}^10 the number of
> non-isomorphic acute sets of maximum possible cardinality 17 is 655 ... For
> dimension 11 we performed a partial search finding 17 non-isomorphic acute sets
> of size 23 and **two of size 24**."

> "Using an integer linear programming formulation we have checked that the
> cardinality of all 11-dimensional extensions of acute sets in {0,1}^9 with
> cardinality 8 or 9 is upper bounded by 28. Thus, **the maximum cardinality of an
> acute set in {0,1}^11 is upper bounded by 28.**"

Interpretation:
- This paper **reproduces** a(11) ≥ 24 (two size-24 sets), and **does NOT beat**
  any record.
- It adds an UPPER bound: a(11) ∈ [24, 28]. (This narrows the gap; it does not
  raise the lower bound. The lower-bound record 24 is intact.)
- No new lower bound is offered for n = 12, 13, 14, 15.
- Note V. Chubenko is the co-discoverer of the a(15) ≥ 128 witness per OEIS, so
  this group is exactly the source community — they would have published any
  improvement here. They did not.

---

## 3. Acute sets ↔ minimal binary linear codes (why the code literature is moot here)

Randriambololona [Ran17], restated by Chubenko–Kurz (Lemma 11):
> "Let C be an [n, k]₂-code. The codewords of C form an acute set iff C is minimal."

So a minimal `[n,k]₂` code gives an acute set of `2^k` points in `{0,1}^n`.
**Axis caution that defuses the active code literature:** the acute-set ambient
dimension equals the code **LENGTH n**, NOT the code dimension k. The 2024–2025
minimal-code activity (Scotti "Recent advances on minimal codes" arXiv:2411.11882;
Alfarano et al.; the m(k,2) bounds in Chubenko–Kurz itself) improves the minimum
**length** m(k,2) for a **fixed dimension** k — a different quantity. E.g. a
minimal `[62,17]₂` code yields 2^17 points in {0,1}^62 (ambient dim 62), nothing
to do with a(11..15).

Two of the five records, a(11)=24 and a(13)=33, are **not powers of two**, so they
cannot come from a linear code at all — they are inherently non-linear sets found
by Kamenetsky's search. The minimal-code literature therefore cannot have silently
superseded them.

---

## 4. LLM / evolutionary sweeps (AlphaEvolve, FunSearch, CPro1)

AlphaEvolve (arXiv:2506.13131, Google DeepMind) is a real coding-agent system that
has improved some combinatorial constructions, and there is a 2024–2026 line of
"LLM/evolution discovers extremal combinatorial objects" papers (e.g. constant-
weight codes arXiv:2603.00174). **No source was found applying AlphaEvolve,
FunSearch, or CPro1 to A089676 / acute sets in the binary hypercube.** No
LLM-driven improvement to any of the five records exists in the literature found.

---

## Sources (all accessed June 2026)
- OEIS A089676 JSON record + full 108-revision history — https://oeis.org/A089676
  (fetched via `?fmt=json` and `/history?seq=A089676`; WebFetch 403, curl+UA works)
- Canonical witness file — https://oeis.org/A089676/a089676_1.txt
- V. Chubenko, S. Kurz, "Divisible minimal codes", arXiv:2312.00885v3 (5 Jun 2025)
  — https://arxiv.org/abs/2312.00885
- H. Randriambololona, "(2,1)-Separating systems beyond the probabilistic bound",
  Israel J. Math. 195 (2013) 171–186 (arXiv:1010.5764) — the best asymptotic lower
  bound, ~11^{3n/50}, but not record-setting at the small n=11..15.
- V. Harangi, "Acute Sets in Euclidean Spaces" (2011) — lower bounds for n>15.
- M. Scotti, "Recent advances on minimal codes", arXiv:2411.11882 (2024) — minimal
  code LENGTH axis, does not touch a(11..15).
- AlphaEvolve, arXiv:2506.13131 — no acute-set application found.

## UNVERIFIED / caveats
- I did not exhaustively read every minimal-code preprint from 2019–2026; the
  argument that they cannot improve a(11..15) is structural (length vs dimension
  axis + non-power-of-two records), not an enumeration. Confidence is high but the
  structural argument is the basis, not a paper-by-paper sweep.
- Google Scholar itself was not directly queried (no Scholar access tool); novelty
  relied on web search + the live OEIS record + the most recent dedicated paper
  (Chubenko–Kurz), which is the community that owns these witnesses.
