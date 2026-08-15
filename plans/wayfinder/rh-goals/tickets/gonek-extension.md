# Extend Gonek J₋₁ test to the full 100k-zero table

- Type: research
- Mode: AFK
- Status: claimed
- Claimed by: lane A5 (codex luna) — MERGED with mertens-constant-precision N=1e5 run
- Blocked by: none
- Source: frontier follow-up to A3 TOO-EARLY verdict; feeds constants paper (user greenlit pushing constants precision)

## Question
Does J₋₁(T)/T move toward 3/π³ (ratio → 1) by T ≈ 75,000 (N = 10^5 zeros),
or does the drift persist/diverge?

## Resolution
(open — at T≈10^4: ratio ≈ 0.95, drifting; lane_a/j_minus1_receipt.json.
2026-08-14 ~20:30: the N=10^5 zero refinement OFFLOADED TO KAGGLE — local
A5 died in the network outage; 5 private kernels
saarshai/mertens-zeros-n100k-part1..part5 pushed and running (18k zeros
each, indices 10k..100k; CSV: index, gamma_refined, abs_zeta_prime_sq,
residual; residual gate 1e-15). Harvest: kaggle kernels output <ref>.
Bundles + instructions: lane_k/KAGGLE_OFFLOAD.md.)
