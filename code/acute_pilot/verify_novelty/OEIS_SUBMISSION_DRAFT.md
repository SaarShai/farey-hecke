# OEIS A089676 — submission template for an IMPROVED lower bound

Use this ONLY if a pilot agent finds an acute set in {0,1}^n LARGER than the
current record for some n ∈ {11,12,13,14,15}:
current records a(11)≥24, a(12)≥32, a(13)≥33, a(14)≥64, a(15)≥128.

Pre-submission gate (do not skip):
1. The witness MUST pass BOTH `code/acute_pilot/verify.py` AND
   `code/acute_pilot/verify_novelty/verify2.py` (independent checkers).
2. Re-confirm the bound is still unbeaten at submission time (re-check the live
   OEIS comment + recent literature — see novelty_findings.md).
3. Sanity: new size strictly greater than the current record at that n.

The sequence's confirmed DATA (`1,2,2,4,5,6,8,9,10,16,17`, a(0..10)) is NOT
edited for a lower-bound improvement — a(11..15) are not yet proven values, only
bounds. You update the **comment** + upload a new **witness file**. (You would
edit DATA only if you PROVE an exact value, i.e. a matching upper bound too.)

---

## A. Comment edit (replace the existing Kamenetsky lower-bounds comment)

The current comment reads (verbatim, from the live record):
> The best known lower bounds for a(11-15) are 24, 32, 33, 64 and 128. a(11-14)
> were found by D. Kamenetsky, while a(15) was found by D. Kamenetsky and
> V. Chubenko (see attached file). Lower bounds for n > 15 have been found by
> V. Harangi (see Table 3 in his paper). - _Dmitry Kamenetsky_, May 18 2018 and
> Jun 05 2018

Replace the numbers for the improved n, keep OEIS attribution style
(`- _Name_, Mon DD YYYY`). Template (fill the bracketed parts):

```
The best known lower bounds for a(11-15) are [B11], [B12], [B13], [B14] and [B15].
a(11-14) were found by D. Kamenetsky, while a(15) was found by D. Kamenetsky and
V. Chubenko. The improved bound a([N]) >= [NEWSIZE] was found by [YOUR NAME]
([METHOD, e.g. "simulated annealing local search"]); see the attached file
a089676_[K].txt. Lower bounds for n > 15 have been found by V. Harangi (see
Table 3 in his paper). - _[Your Name]_, [Mon DD YYYY]
```

Notes:
- Keep the credit to Kamenetsky / Chubenko for the bounds you did NOT improve.
- `[K]` is the next free witness-file suffix (the existing file is
  `a089676_1.txt`, so a new one is typically `a089676_2.txt`).
- If you also improve the asymptotic / multiple n, list each improved value.

### Optional: also add a one-line "improvement" comment crediting the search
```
a([N]) >= [NEWSIZE] improves the previous lower bound [OLD] (D. Kamenetsky, 2018),
found by [METHOD]. The witness is in the attached file and is acute by direct
check (no three points subtend a right angle). - _[Your Name]_, [Mon DD YYYY]
```

---

## B. Witness file (`a089676_[K].txt`) — EXACT format

Match Kamenetsky's `a089676_1.txt` byte-style: a two-line header (description +
"By NAME, D/MM/YYYY"), then one block per n. Each block is
`a(n) >= SIZE:` followed by the points as space-separated bits inside
parentheses, points separated by single spaces, on (wrapped) lines. Coordinates
are written **left-to-right = bit 0 .. bit n-1** (this matches both verifiers'
`rows_to_masks` which sets bit i from the i-th character).

Header + one-block skeleton (fill in):
```
Best known lower bounds and their corresponding solutions for n=11 to 15 in A089676.
By [Your Name], [D/MM/YYYY]

a([N]) >= [NEWSIZE]:
([bits]) ([bits]) ([bits]) ... ([bits])
```
Keep the unchanged records too if you re-upload the whole file (recommended, so
the file stays self-contained), or upload only the improved block as a new file
and reference it explicitly in the comment.

A machine-generated witness block is produced by:
`python3 emit_oeis_block.py <witness_rows_file> <n>`  (script in this directory).
It reads a plain file of 0/1 rows and prints the `a(n) >= SIZE:` block in the
exact parenthesised format. Round-trip-checked: re-parsing its output through
verify.py / verify2.py reproduces the same acute set.

---

## C. Mechanics of submitting to OEIS
- You need an OEIS account (free) and to be logged in. Edits go through the
  editorial review queue (a few days), so submit well before any deadline.
- On the A089676 page, "edit" → modify the COMMENTS field (Section A above).
- Upload the witness file via the "a-file" upload (it becomes
  `https://oeis.org/A089676/a089676_[K].txt`) and add a LINKS entry:
  `Your Name, <a href="/A089676/a089676_[K].txt">Improved lower bound and solution for a([N])</a>`
- In the edit's "comment to editors" box, state: the new size, n, that it passes
  two independent acute-set checkers, and the method. Offer the witness inline if
  asked.
- Do NOT change the `data` line unless you have a matching upper bound proving the
  exact value; with only a better lower bound, the comment + a-file is the edit.

---

## D. Ready-to-go checklist (copy into the submission PR/note)
- [ ] new acute set of size [NEWSIZE] in {0,1}^[N], strictly > current record
- [ ] passes `verify.py <file> [N]`  (paste output)
- [ ] passes `verify2.py <file> [N]` (paste output, independent checker)
- [ ] novelty re-checked at submission date (no other source beat it) — cite OEIS
      rev # and any newer paper
- [ ] witness file in `a089676_[K].txt` format (header + a(N)>=SIZE: blocks)
- [ ] comment text drafted (Section A), attribution dated
- [ ] LINKS entry drafted for the a-file
- [ ] account ready, logged in, comment-to-editors written

STATUS: template ready. No record beaten yet, so nothing to submit at this time.
