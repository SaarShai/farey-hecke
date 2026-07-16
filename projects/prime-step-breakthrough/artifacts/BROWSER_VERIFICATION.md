# Live browser verification

Date: 2026-07-15

Surface: Codex in-app browser against
`http://127.0.0.1:8765/`, served by:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=projects/prime-step-breakthrough/src \
python3 -m coprimebatch.web --host 127.0.0.1 --port 8765
```

## Interactions exercised

1. Loaded the real page and inspected its accessibility snapshot.
2. Focused the supplied-gap textarea, used keyboard selection/typing, and
   entered `1/10, 2/10, 3/10, 4/10`.
3. Clicked **Compute two-sided certificate** and observed:
   - variance `1/80`;
   - supplied (L^1) `1/2`;
   - exact expected quadratic `1/24`;
   - rigorous lower `0.050311529493745226`;
   - finite upper `0.3527062426235599`; and
   - exported constant `0.056249999999999994`, the conservative binary64
     encoding of (9/160).
4. Switched the radio control to **Farey sequence gaps**, entered order `8`,
   and verified a 22-gap exact certificate.
5. Clicked **Certify portfolio** for `2,3,5,7`; observed 13 points, exact energy
   `1213/1260`, and worst-case error `0.07547476606008743`.
6. Clicked **Run fixed benchmark**; observed deterministic ratios
   `0.58763675219038` against the best deterministic in-class baseline and
   `0.35069905423768083` against the random median.
7. Used keyboard input on the prime field.  An intentionally malformed
   composite value rendered `Error: p must be an odd prime`; replacing it with
   `101` and clicking **Compute moments** recovered successfully.
8. The (p=101) result rendered exact canonical fraction strings for huge
   moments, including values far beyond JavaScript's safe-integer range, plus
   exact zero odd moments and triangular predictions `1/6`, `1/15`, `1/28`.
9. Entered malformed gaps `1/3, 1/3`; the UI rendered
   `Error: gaps must sum exactly to 1`.  Replacing them with a valid vector and
   clicking again recovered to the completed state.
10. Inspected a full-page render.  Labels, focus state, two-column layout,
    warning, and all four workflows were visible.  Long exact results remained
    inside scrollable 32-rem panes after the visual check triggered a CSS fix.

## Cross-surface parity

The same fixed gap vector was run live through the CLI and HTTP API.  Both
returned the exact values `1/80`, `1/2`, `17/200`, `13/1200`, `1/24`, and
`1/32`, with identical floating lower/upper bounds and permutation count 24.
The HTTP representation additionally retained canonical `fraction` strings.

Verdict: **PASS** for navigation, keyboard input, clicks, alternate source
selection, exact result rendering, malformed-input display/recovery, visual
layout, and CLI/API/browser agreement.
