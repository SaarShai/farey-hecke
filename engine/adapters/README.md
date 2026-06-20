# Aletheia — optional accelerator adapters (`engine/adapters/`)

These are **optional** add-ons to the Aletheia engine. The core pipeline
(`engine/{certify,falsify,formal_verify,orchestrator}`) already runs entirely
locally; the adapters here only make two stages **cheaper / bigger** when the
relevant tool happens to be available, and **degrade gracefully** to the normal
local path when it isn't. Nothing in the engine *requires* them.

| Adapter | Stage it accelerates | What it does | Hard dependency |
|---------|----------------------|--------------|-----------------|
| `ollama_scout.py`   | **SCOUT** (stage 1, discover) | cheap local-LLM triage / claim proposals / summaries via `ollama` | local `ollama` + a pulled model (`llama3.1:8b`) — optional |
| `kaggle_offload.py` | **CERTIFY / scan** (stage 3, batch) | generate + push a self-contained Kaggle kernel for a heavy sweep, then poll + pull results | `~/.local/bin/kaggle` + `~/.kaggle/kaggle.json` — optional |

Both adapters are **transport / assist only** — neither re-implements any math.
Everything a SCOUT adapter proposes still passes through the unchanged
FALSIFY → CERTIFY → VERIFY gauntlet; an offloaded CERTIFY job runs the *same*
frozen engine source the local stage would, just on Kaggle's CPU instead of
yours.

---

## 1. `ollama_scout.py` — cheap SCOUT-stage assist

The SCOUT (DISCOVER) stage is agent-orchestrated and deliberately has no fixed
code in v1 (see `engine/README.md` §"Stage 1 — SCOUT"). This adapter lets the
orchestrator spend a *local* 8B model on throwaway triage instead of frontier
tokens: "is this candidate worth pursuing?", "propose 3 falsifiable claims about
X", "summarize this 40-line numeric dump in one line".

### API

```python
from engine.adapters.ollama_scout import scout, scout_detailed, propose_claims, available

available()                      # {installed, models, model_present, error}
scout("In one line, what is a Hecke triangle group?")   # -> str (never raises)
scout_detailed(prompt, model="llama3.1:8b", timeout_s=120)  # -> full dict
propose_claims("non-arith Hecke G_5 resonances", n=3)   # -> [ {statement, kind, rationale}, ... ]
```

`scout()` **never raises**. On any failure (no `ollama`, model not pulled, daemon
down, timeout, empty/garbled response) it returns a sentinel string
`"[ollama-unavailable: <why>]"`, and `scout_detailed()` returns
`{"ok": False, "error": ...}`. The orchestrator treats `ok=False` as "no scout
assist available" and falls back to the agent-driven scout pattern.

The adapter runs a tiny terminal emulator over `ollama run`'s output (it honors
the cursor-back + erase-line control codes ollama emits when soft-wrapping) so
the returned text is clean linear UTF-8, not the TTY redraw stream.

Env overrides: `OLLAMA_BIN`, `OLLAMA_MODEL`.

### How it slots into the pipeline

```
SCOUT (agent + Brainer skills)
  └─ optional: ollama_scout.propose_claims(topic) ──▶ candidate Claim stubs
        │  (candidates ONLY — no authority)
        ▼
   Claim dict  ──▶  FALSIFY ──▶ CERTIFY ──▶ VERIFY ──▶ SYNTHESIZE
```

### Smoke

```
$ python3 engine/adapters/ollama_scout.py --smoke
```

Probes `ollama list`, then runs `scout("In one line, what is a Hecke triangle
group?")` and quotes the model's answer. Passes both when ollama answers (quotes
the real text) and when ollama is unavailable (records the graceful fallback
honestly) — the adapter is correct either way.

---

## 2. `kaggle_offload.py` — heavy CERTIFY / scan offload

For *batch* work that is too slow to babysit locally — e.g. a multi-`q` spectrum
sweep or a wide Arb winding-box scan over many seeds. It mirrors the hand-built
kernels under `kaggle_kernels/`: a **self-contained** script = frozen engine body
+ a small driver that writes a JSON result to `/kaggle/working`, plus a
`kernel-metadata.json`. Kaggle gives ~9h free CPU sessions.

### API

```python
from engine.adapters.kaggle_offload import offload, fetch

job_spec = {
    "job_id":     "hecke-spectrum-sweep",        # -> kernel slug (REQUIRED)
    "title":      "Hecke spectrum sweep",
    "engine_src": open("code/_snapshots/zeta_mayer_rosen.frozen.py").read(),
    "driver_src": "...sweep driver that sets RESULT or writes RESULT_NAME...",
    "params":     {"q_list": [5, 7, 9, 11], "N_list": [20, 30]},
    "result_name":"zeta_rosen_sweep.json",
}

# (a)+(b): generate the kernel folder; push only if you opt in.
res = offload(job_spec, push=False)   # -> {kernel_id, status:"generated", folder, script_path, metadata_path, url}
res = offload(job_spec, push=True)    # -> status:"queued" on success, "push_failed" otherwise

# (c): later, poll status + pull output.
out = fetch(res["kernel_id"])                       # single status check (no wait)
out = fetch(res["kernel_id"], poll=True, timeout_s=1800)   # wait up to 30 min
# -> {kernel_id, status, results_path, output_dir, pulled_files}
results = json.load(open(out["results_path"]))      # the kernel's JSON result
```

The generated script always defines `JOB_PARAMS` (from `params`), runs the engine
body then the driver, and — as a safety net — if the driver wrote nothing, dumps
`JOB_PARAMS` + a stub note to `result_name`, so `fetch()` always finds a
parseable JSON. `engine_path` may be given instead of `engine_src` to read the
frozen body from a file.

`offload(push=False)` is pure local generation (**no network**); it is the safe
default and the smoke path. Push is always **opt-in** (`push=True`), mirroring
the engine's "don't spend remote compute unless asked" convention (cf. the VERIFY
stage's `submit=` gate).

Generated kernels land under `engine/runs/kaggle_offload/<slug>/`; pulled output
under `.../<slug>/output/`.

### How it slots into the pipeline

```
CERTIFY (local Arb)                       ── small / single-point: run locally
   │
   └─ heavy / batch ──▶ kaggle_offload.offload(job_spec, push=True)
                            │  (a) build kernel + metadata
                            │  (b) kaggle kernels push  ──▶ Kaggle queue
                            ▼
                        ...Kaggle runs ~minutes–hours...
                            │
                        kaggle_offload.fetch(kernel_id)
                            │  (c) poll status + pull *.json
                            ▼
                        results JSON  ──▶  feed back as CERTIFY enclosure
                                           / a batch of Claims to certify locally
```

The offloaded result is **not** itself a certificate — it is the *numeric
evidence batch*. Promote a candidate to a real `Certificate` by running the local
`engine/certify` Arb winding box on the specific seed the sweep surfaced, exactly
as if SCOUT had handed it over. (Offload widens the search; local CERTIFY still
issues the certificate.)

### Smoke

```
$ python3 engine/adapters/kaggle_offload.py --smoke
```

Generates a tiny stdlib-only "certify pi" kernel + `kernel-metadata.json`,
asserts the metadata **parses** and has the required keys, and asserts the
generated script **compiles**. It does **not** push (pushing is optional). To
push a clearly-named test kernel manually:

```python
offload({...,"job_id":"aletheia-test-<you>"}, push=True)   # reports the kaggle URL
```

---

## Provenance / honesty

- Neither adapter is on the critical path; absence of `ollama` or `kaggle`
  leaves the engine fully functional.
- `ollama_scout` output is **proposal-grade only** — it carries no certificate
  authority and is always re-checked by FALSIFY/CERTIFY/VERIFY.
- `kaggle_offload` output is **evidence-grade only** — a JSON sweep result, not a
  `Certificate`; the local Arb stage still issues certificates.
- Both stages should be recorded in the `RunRecord` (`stage_status`) as
  `source: "adapter"` with the tool + (for Kaggle) the kernel URL, so a run that
  used an accelerator is auditable and reproducible.
