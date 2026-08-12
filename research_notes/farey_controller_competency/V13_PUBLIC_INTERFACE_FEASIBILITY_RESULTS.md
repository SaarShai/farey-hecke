# V13 public-interface feasibility

Development-only public-interface feasibility probe. Hidden action values are evaluator diagnostics only; no sealed test or competency claim is authorized.

Status: `unverified_underpowered`; leakage audit: `True`. All four validation signal AUCs are approximately 0.50, below the preregistered 0.60 usefulness threshold; no learner or planner is authorized.

## train

Samples: `3840`; unique views: `3742`; collision rate: `0.0255`; hidden positive actions: `76`; feasible: `True`.

| signal | AUC | top-action hit | pairs |
| --- | ---: | ---: | ---: |
| coverage_gain | 0.5018 | 0.9891 | 3142 |
| spectral_gain | 0.5056 | 0.9870 | 3142 |
| defect_reduction | 0.5047 | 0.9854 | 3142 |
| active_search | 0.5064 | 0.9896 | 3142 |

## validation

Samples: `1920`; unique views: `1865`; collision rate: `0.0286`; hidden positive actions: `9`; feasible: `True`.

| signal | AUC | top-action hit | pairs |
| --- | ---: | ---: | ---: |
| coverage_gain | 0.5003 | 0.9964 | 151 |
| spectral_gain | 0.5013 | 0.9969 | 151 |
| defect_reduction | 0.5005 | 0.9958 | 151 |
| active_search | 0.5016 | 0.9974 | 151 |
