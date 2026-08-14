# A4 zero-sum extension plan

- [x] Audit the prior receipt, source checksum, backend, and A3 checkpoint schema.
- [x] Run the resumable weighted extension for missing chunks 3001--10000.
- [x] Combine A3 500-zero derivative means with the A4 weighted checkpoints.
- [x] Fit the Gonek-scaled block means and calculate central/envelope tails.
- [x] Quantify first-order seed, backend, and tail-model budgets.
- [x] Recheck candidate forms and write the v2 report and receipt.

All files created by A4 belong under `lane_a/`; computation checkpoints belong in
this directory. A3's `j_minus1_checkpoints/` is read-only input.
