# Feedback-learning competency probe

**Run:** deterministic seed `20260811`  
**Status:** finite preliminary result; not an agency claim  
**Code:** [`experiment.py`](experiment.py)  
**Receipt:** [`receipt.json`](receipt.json)

## Predeclared gates and checked outcomes

| Gate | Observed support | Outcome |
|---|---:|---|
| H1 goal persistence | `0.0000` | negative |
| H2 variable means | `0.0556` of tasks | negative |
| H3 feedback learning | `0.0000` | negative |
| H4 deleted-identity recovery | `0.0000` vs random | negative |
| H5 frozen unseen-`N` transfer | `0.0000` vs random | negative |
| H6 authorized switch / distractor resistance | `1.0000` | positive |

The practical thresholds were locked in `experiment.py` before execution. A
negative result is retained: this run does not claim that scalar feedback made
the contextual learner better than the matched controls. The positive switching
result is narrow: the wrapper changed the goal only when authorized and ignored
the unrequested distractor cue.

## Baselines and common result

The six conditions were random legal action, largest-gap fixed heuristic, local
denominator detector, true-feedback learner, reward-shuffled learner, and
no-feedback learner. On this small task stream all conditions had the same
transfer normalized-progress mean (`0.5556`) and deleted-label recovery mean
(`0.8889`); the action menus make this a low-separation probe. That null/negative
result is useful evidence against overstating learning from this setup.

The variable-means diagnostic found two near-best local action families on only
`5.56%` of tasks (tolerance `0.002` visible-metric units). Most episodes expose
one dominant local move, so the practical variable-means gate fails.

## Identity and agency guardrails

Identity metrics are evaluator-only. `hidden_hit_rate` is recorded but not used
as a competency win because every legal reduced candidate belongs to the intact
Farey set. Deleted-label recovery is the meaningful evaluator statistic here.
Exact labels, `N`, and the complete current legal action menu are structural
privilege; the protocol is not leak-tight and does not establish agency.

## Reproduction and validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/experiment.py
python3 -m json.tool research_notes/farey_controller_competency/receipt.json >/dev/null
python3 -m py_compile research_notes/farey_controller_competency/experiment.py
```

The checked run completed in about one second and emitted deterministic JSON.
