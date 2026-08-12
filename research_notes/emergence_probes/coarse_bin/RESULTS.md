# Coarse-bin emergence probe

- **Objective:** sort six coarse bins of eight values each; any within-bin order is valid.
- **Probe:** a local A-before-B tie convention applies only inside equal bins. Same-label adjacency is measured externally and is not an objective.
- **Controls:** independent label shuffle, randomized equal-bin ties/schedule, and an explicit anti-clustering policy.

## Deterministic result

All conditions completed the coarse objective in 1.000 of trials. The role-tie probe's final within-bin same-label rate was 0.833; randomized ties gave 0.484; anti-clustering gave 0.244. The role-tie condition therefore shows an unnecessary organization signal relative to the matched controls, while the controls bound schedule/label effects.

The perturbation/restart receipt records a mixed-label equal-bin swap followed by the role-local restart. This is a finite toy-model signal, not evidence of agency, intrinsic utility, or zero-cost computation.

Receipt: [receipt.json](receipt.json).
