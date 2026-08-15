# Open slots for `PAPER_SKELETON.md`

The skeleton contains **10** occurrences of the exact placeholder marker. All are reserved for the concurrent (N=10^5) computation. The expected source is:

`research_notes/rh_goals_2026-08-14/lane_a/a5_checkpoints/`

That directory exists but is empty at assembly time. No substitute value has been inferred from the (N=10000) receipts.

## Weighted zero-sum slots

1. `PAPER_SKELETON.md:101`, “Boundary ordinate (T_{10^5})” — insert the (N=10^5) boundary ordinate (T) from the A5 checkpoint receipt. Keep the `[RECEIPT]` tag. Expected source field: A5 boundary ordinate / `T`.

2. `PAPER_SKELETON.md:102`, “Positive partial sum” — insert the direct positive-ordinate weighted partial sum at (N=10^5). Keep the `[RECEIPT]` tag. Expected source field: A5 positive partial sum.

3. `PAPER_SKELETON.md:103`, “Two-sided partial sum” — insert the convention-audited two-sided value at (N=10^5), normally twice the positive partial sum under the existing conjugacy convention. Confirm that relation against the A5 receipt before filling. Keep the `[RECEIPT]` tag. Expected source field: A5 two-sided partial sum.

4. `PAPER_SKELETON.md:104`, “Central one-sided tail” — insert the A5 fitted central one-sided tail. Keep the `[FITTED-TAIL]` tag. Expected source field: A5 central tail estimate.

5. `PAPER_SKELETON.md:105`, “Conservative one-sided tail” — insert the A5 conservative/envelope one-sided tail. Keep the `[FITTED-TAIL]` tag. Expected source field: A5 conservative tail or envelope.

6. `PAPER_SKELETON.md:106`, “Final two-sided estimate and tail bar” — insert the A5 final two-sided estimate together with its supported tail bar, using the same notation as the V2 result. Keep the `[FITTED-TAIL]` tag. Expected source field: A5 final estimate and uncertainty/bar.

## Gonek-test slots

7. `PAPER_SKELETON.md:133`, (N=10^5) row, (T) column — insert the A5 boundary ordinate. This should agree with slot 1 if both computations use the same zero boundary. Keep the `[RECEIPT]` provenance entry. Expected source field: A5 `T`.

8. `PAPER_SKELETON.md:133`, (N=10^5) row, (J_{-1}(T)) column — insert the direct cumulative (J_{-1}) value at the A5 boundary. Keep the `[RECEIPT]` provenance entry. Expected source field: A5 cumulative `J_minus1`.

9. `PAPER_SKELETON.md:133`, (N=10^5) row, (J_{-1}(T)/T) column — insert the A5 ratio, preferably the receipt field rather than a re-rounded recomputation. Keep the `[RECEIPT]` provenance entry. Expected source field: A5 `J_minus1_over_T`.

10. `PAPER_SKELETON.md:133`, (N=10^5) row, ratio-to-(3/\pi^3) column — insert the A5 ratio against the receipt's Gonek target coefficient. Keep the `[RECEIPT]` provenance entry. Expected source field: A5 `ratio_to_3_over_pi_cubed`.

## Fill gate

After the A5 artifact arrives, replace only the marker text, add the exact A5 field provenance to the affected table/slot text, and recheck that slots 1 and 7 agree. Recompute any prose conclusion that depends on the new row; do not silently change the current **TOO EARLY** verdict or the **3 significant digits** claim without a fresh receipt/report supporting the change.
