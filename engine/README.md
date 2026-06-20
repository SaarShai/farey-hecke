# Aletheia — Certified Autonomous Math Engine

A reusable pipeline that takes a mathematics problem and runs it through five
stages, emitting **machine-auditable certificates** at each step:

```
   DISCOVER          FALSIFY           CERTIFY            VERIFY          SYNTHESIZE
   (scout)           (refute)          (enclose)          (Lean)          (write-up)
      │                 │                 │                 │                 │
  candidate   ──▶   adversarial   ──▶  interval /    ──▶  sorry-free   ──▶  honest
   Claim            refutation          ball arith         axiom-clean       paragraph
   + scripts        (controls,          (Arb /             Lean proof        + provenance
                     independent         python-flint)      via Aristotle     RunRecord
                     methods, N/         rigorous           CLI               (engine/runs/)
                     prec sweeps,        enclosure
                     null/edge)
      │                 │                 │                 │                 │
      ▼                 ▼                 ▼                 ▼                 ▼
   Claim          FalsifyReport      Certificate     ProofCertificate    RunRecord
                  {survives|          {certified}     {sorry_free,        {run_id, …,
                   refuted}                            proved}             synthesis}
```

**Differentiator vs. proof-search AI (AlphaProof etc.):** discovery of *novel*
results + adversarial falsification + interval certification + formal (Lean)
verification, end-to-end, with provenance. The Hecke transfer-operator work is
the reference plugin; the stage interfaces are domain-agnostic.

The shared interface contract lives in [`GOAL.md`](GOAL.md). This README
documents the architecture, how to run a problem end-to-end, and the two
non-code stages (SCOUT and SYNTHESIZE).

---

## The five stages

| # | Stage | Kind | Entrypoint | Artifact |
|---|-------|------|-----------|----------|
| 1 | **scout** (discover) | agent-orchestrated (no code in v1) | Brainer skills | `Claim` + scripts |
| 2 | **falsify** | code | `falsify.falsify(claim) -> FalsifyReport` | `FalsifyReport` |
| 3 | **certify** | code | `certify.certify(claim) -> Certificate` | `Certificate` |
| 4 | **verify** | code | `formal_verify.verify(lemma, project_dir) -> ProofCertificate` | `ProofCertificate` |
| 5 | **synthesize** | code (orchestrator) | `orchestrator.synthesize(run_record) -> str` | `RunRecord` + summary |

The **orchestrator** (`orchestrator.run(claim) -> RunRecord`) is the spine: it
composes stages 2→3→4 and then 5, recording everything as a provenance
`RunRecord` written to `engine/runs/<run_id>.json`.

### Stage 1 — SCOUT (discover) · *non-code, agent-orchestrated*

Scout is **discovery**, performed by the repo's agent + Brainer skills rather
than by a fixed program. It is documented as a *pattern*, not shipped as code in
v1. The pattern this project uses:

1. **Autonomous exploration** — an agent fans out over a question (e.g. "is the
   B(q) cluster ceiling a closed form?"), generates candidate mechanisms, and
   writes throwaway numerical scripts under `code/`.
2. **Memory-grounded triage** — before re-deriving, query durable memory so dead
   ends are not re-chased: `wiki-memory` (`skills/wiki-memory/tools/wiki.py
   search → timeline → fetch`), the `wiki/` store (`wiki/L1_index.md`), and the
   session `MEMORY.md`. Skills `index-first`, `plan-first-execute`, and
   `lean-execution` shape the search.
3. **Adversarial framing up front** — `loop-engineering` forces a concrete
   *gate / stop / budget* before any generate-and-check loop, and pairs every
   generator with a **separate** verifier (the downstream FALSIFY/CERTIFY stages
   are exactly that separation).
4. **Output** — a `Claim` dict per the contract plus the candidate scripts. The
   `Claim` then enters the coded pipeline at FALSIFY.

`Claim` shape: `{id, statement, kind: "numerical"|"theorem", artifact, params}`.

### Stage 2 — FALSIFY *(code: `engine/falsify/`)*

A config-driven adversarial-refutation harness. It runs a battery of probes —
**control** (a case where the claim should *not* hold), **independent** (a second
method computing the same quantity must agree), **stability** (vary truncation
N / precision / grid), **null** (a neighbouring/off point must not also satisfy
the claim) — supplied as callables in `claim["params"]`. It **defaults to
skepticism**: any probe that is missing, errors, or returns an undecided score
is scored FAILED, so a claim survives only if it *actively passes every* probe.
Returns a `FalsifyReport {claim_id, attempts, verdict: "survives"|"refuted",
evidence}`.

### Stage 3 — CERTIFY *(code: `engine/certify/`)*

Rigorous interval / ball arithmetic (Arb via `python-flint`). The reference
evaluator (`artifact="hecke_transfer_operator_zero"`) wraps the certified
argument-principle winding engine (`code/zeta_resonance_g5.py` /
`code/zeta_cert_rosen.py`) to enclose a transfer-operator zero with a verified
winding number. Returns a `Certificate {claim_id, method, enclosure, certified:
bool, certificate_path, tool}`.

### Stage 4 — VERIFY *(code: `engine/formal_verify/`)*

Lean via the `aristotle` CLI. Submits/post-processes a Lean project, checks the
proof is **sorry-free** and reports the **axiom** set. Returns a
`ProofCertificate {claim_id, lemma, lean_file, sorry_free: bool, axioms, proved:
bool}`. By design it refuses to spend Aristotle compute unless explicitly asked
(`submit=True` / `verify_project` on an existing run) — so an orchestrator call
that does not opt in is gracefully recorded as not-attempted.

### Stage 5 — SYNTHESIZE *(code: orchestrator)*

`orchestrator.synthesize(run_record) -> str` emits an **honest one-paragraph
summary**: what survived falsification, what was certified, what was formally
verified, and — explicitly — which stages were stubbed or failed, so the
summary never overstates the run. The full provenance lives in the `RunRecord`.

---

## RunRecord format

`orchestrator.run` returns and persists a `RunRecord` (JSON, schema
`aletheia.runrecord/v1`):

```jsonc
{
  "run_id":     "<claim_id_slug>--NNNN",   // deterministic: slug + counter, NO wall-clock/RNG
  "schema":     "aletheia.runrecord/v1",
  "claim":      { …the input Claim verbatim… },
  "falsify":    { …FalsifyReport,    or a {"stub": true} placeholder… },
  "certify":    { …Certificate,      or a {"stub": true} placeholder… },
  "verify":     { …ProofCertificate, or a {"stub": true} placeholder… },
  "synthesis":  "honest one-paragraph summary",
  "stage_status": {                        // provenance: real vs stub, per stage
    "falsify": {"source": "real"|"stub", "error": null|"…"},
    "certify": {"source": "real"|"stub", "error": null|"…"},
    "verify":  {"source": "real"|"stub", "error": null|"…"}
  },
  "verdict":    "survives"|"refuted"|"unknown",   // rolled up from falsify
  "timestamps": {"started": "ISO-8601", "finished": "ISO-8601"}
}
```

**Reproducibility.** `run_id` is derived from the claim id + a per-claim counter
(`make_run_id`); no wall-clock or RNG enters the id. Pass `counter=` and
`timestamp=` to `run()` for byte-for-byte reproducible records.

**Defensive composition.** The three stage modules are imported *lazily* inside
`run()`. If a module is not importable yet, the orchestrator substitutes a
clearly-labelled `{"stub": true}` placeholder and keeps going. If a real module
raises, it is downgraded to its stub with the traceback captured in
`stage_status[...].error` — a single stage failure never aborts the pipeline.

---

## How to run a problem end-to-end

```python
from engine.orchestrator.orchestrator import run

claim = {
    "id": "my-claim-001",
    "statement": "…",
    "kind": "numerical",                 # or "theorem"
    "artifact": "hecke_transfer_operator_zero",
    "params": { … domain params + falsify probe callables … },
}

record = run(claim)                      # composes FALSIFY → CERTIFY → VERIFY → SYNTHESIZE
print(record["synthesis"])               # honest one-paragraph summary
# RunRecord persisted to engine/runs/<run_id>.json
```

CLI / smoke:

```bash
python3 engine/orchestrator/orchestrator.py --smoke   # trivial claim, prints RunRecord
python3 engine/orchestrator/smoke_test.py             # self-contained test (exit 0 = pass)
```

`run()` keyword args: `counter` (pin the run_id counter), `timestamp` (pin
ISO-8601 timestamps), `project_dir` (Lean dir for VERIFY), `write` (default
True), `runs_dir` (override output dir).

---

## Contract summary

(Full text in [`GOAL.md`](GOAL.md).) Every artifact is a JSON dict carrying a
`claim_id`.

```
Claim            : {id, statement, kind, artifact, params}
FalsifyReport    : {claim_id, attempts:[{name,method,result}], verdict, evidence}
Certificate      : {claim_id, method, enclosure, certified, certificate_path, tool}
ProofCertificate : {claim_id, lemma, lean_file, sorry_free, axioms, proved}
RunRecord        : {run_id, claim, falsify, certify, verify, synthesis, timestamps}

certify.certify(claim) -> Certificate
falsify.falsify(claim) -> FalsifyReport
formal_verify.verify(lemma, project_dir) -> ProofCertificate
orchestrator.run(claim) -> RunRecord            # composes the above
```

---

## Worked example — a Hecke claim, end-to-end

**Claim.** *`s = 0.4539 + 5.7635i` is a certified even-sector resonance of the
non-arithmetic Hecke group `G_5`* (a zero of `det(1 − L⁺_s)` for the `G_5`
transfer operator, even / `mms+` sector).

```python
from engine.orchestrator.orchestrator import run

def _probe(params):                      # stand-in adversarial probe (passes)
    return {"passed": True, "method": "demo", "detail": "…"}

claim = {
    "id": "G5-even-resonance-s0.4539+5.7635i",
    "statement": "s=0.4539+5.7635i is a certified even-sector resonance of non-arith Hecke G_5",
    "kind": "numerical",
    "artifact": "hecke_transfer_operator_zero",
    "params": {
        "q": 5, "re": 0.4539, "im": 5.7635, "sign": +1, "N": 30, "n_head": 4,
        # FALSIFY probe callables (control / independent / stability / null):
        "control_fn": _probe, "independent_fn": _probe,
        "sweep_fn": _probe,  "null_fn": _probe,
    },
}

record = run(claim, counter=0, timestamp="2026-06-20T10:30:00Z")
```

**Composition that actually ran** (against the real sibling modules):

- **FALSIFY** (real) → `survives` — all four adversarial probes passed.
- **CERTIFY** (real) → `certified: true` — the Arb argument-principle engine
  enclosed the zero with **winding number 1** (ball `[0.99999…, 1.00000…]`),
  `|det|` ≈ `9.8e-16` at the Newton-refined centre `0.45389518 + 5.76353724i`,
  dimension tail certified.
- **VERIFY** (stub) → not attempted — the Lean stage refuses to spend Aristotle
  compute unless `submit=True`, so it is honestly recorded as not-attempted.

**Sample RunRecord** (the real record written to
`engine/runs/G5-even-resonance-s0.4539-5.7635i--0000.json`, with the large
certificate `enclosure` object elided as `…`):

```jsonc
{
  "run_id": "G5-even-resonance-s0.4539-5.7635i--0000",
  "schema": "aletheia.runrecord/v1",
  "claim": {
    "id": "G5-even-resonance-s0.4539+5.7635i",
    "statement": "s=0.4539+5.7635i is a certified even-sector resonance of non-arith Hecke G_5",
    "kind": "numerical",
    "artifact": "hecke_transfer_operator_zero",
    "params": { "q": 5, "re": 0.4539, "im": 5.7635, "sign": 1, "N": 30,
                "n_head": 4, "control_fn": "<function …>", "…": "…" }
  },
  "falsify": {
    "claim_id": "G5-even-resonance-s0.4539+5.7635i",
    "attempts": [ {"name": "control", …}, {"name": "independent", …},
                  {"name": "stability", …}, {"name": "null", …} ],
    "verdict": "survives",
    "evidence": { "n_attempts": 4, "n_passed": 4, "n_scored": 4, "…": "…" },
    "stub": false
  },
  "certify": {
    "claim_id": "G5-even-resonance-s0.4539+5.7635i",
    "method": "argument-principle winding (Arb interval enclosure)",
    "enclosure": { "winding_number": 1,
                   "winding_ball": [0.9999999999999669, 1.000000000000033],
                   "center_point": {"re": 0.45389518007494245, "im": 5.7635372417301065},
                   "absdet_center_mid": 9.75e-16, "dim_tail_certified": true, "…": "…" },
    "certified": true,
    "certificate_path": ".../engine/runs/G5-even-resonance-s0.4539+5.7635i__certify.json",
    "tool": "code/zeta_resonance_g5.py (Arb argument-principle winding box)",
    "stub": false
  },
  "verify": {
    "claim_id": "G5-even-resonance-s0.4539+5.7635i",
    "lemma": "s=0.4539+5.7635i is a certified even-sector resonance of non-arith Hecke G_5",
    "lean_file": null, "sorry_free": false, "axioms": [], "proved": false,
    "stub": true,
    "note": "STUB FALLBACK: real formal_verify.verify raised at run time. …",
    "error": "RuntimeError: verify(submit=False) does not spend Aristotle compute. …"
  },
  "synthesis": "Claim \"G5-even-resonance-s0.4539+5.7635i\" — … It survived 4 adversarial refutation attempt(s) (controls / independent methods / sweeps). It was rigorously certified by code/zeta_resonance_g5.py (Arb argument-principle winding box) (enclosure …). No formal (Lean) proof was attempted (verify stubbed). CAVEAT: stage(s) ['verify'] were stubbed at run time, so this run is a pipeline-composition demonstration, not a fully certified result.",
  "stage_status": {
    "falsify": {"source": "real", "error": null},
    "certify": {"source": "real", "error": null},
    "verify":  {"source": "stub", "error": "RuntimeError: verify(submit=False) does not spend Aristotle compute. …"}
  },
  "verdict": "survives",
  "timestamps": {"started": "2026-06-20T10:30:00Z", "finished": "2026-06-20T10:30:00Z"}
}
```

This is the engine working as intended: two stages ran for real and produced
rigorous artifacts, the third (Lean) was honestly recorded as not-attempted, and
the synthesis paragraph states that caveat rather than claiming a full proof.

---

## Files

```
engine/
├── GOAL.md                         shared interface contract
├── README.md                       this file
├── orchestrator/
│   ├── orchestrator.py             run() + synthesize() + RunRecord + CLI
│   └── smoke_test.py               self-contained test (real env + injected fakes)
├── falsify/                        FALSIFY stage  (sibling-owned)
├── certify/                        CERTIFY stage  (sibling-owned)
├── formal_verify/                  VERIFY stage   (sibling-owned)
└── runs/                           RunRecord JSON provenance, one per run
```
