# Aletheia — Certified Autonomous Math Engine (GOAL + interface contract)

**Mission.** A reusable pipeline that takes a mathematics problem and runs it
through **DISCOVER → FALSIFY → CERTIFY → VERIFY → SYNTHESIZE**, emitting
machine-auditable certificates at each step. Differentiator vs proof-search AI
(AlphaProof etc.): discovery of *novel* results + adversarial falsification +
interval certification + formal (Lean) verification, end-to-end, with provenance.

This file is the SHARED CONTRACT. Every engine module is built to it.

## Stages
1. **scout** (discover) — agent-orchestrated exploration → candidate `Claim`s + scripts. (Pattern + existing Brainer skills; documented, not new code in v1.)
2. **falsify** — adversarial refutation: controls, independent methods, parameter/N sweeps, edge cases → `FalsifyReport {survives|refuted}`.
3. **certify** — interval/ball arithmetic (Arb / python-flint): rigorous enclosure → `Certificate`.
4. **verify** — Lean via Aristotle: sorry-free + axiom-check → `ProofCertificate`.
5. **synthesize** — honest write-up + provenance `RunRecord`.

## Directory layout (`engine/`)
- `engine/certify/`        — Arb certification module + certificate format
- `engine/falsify/`        — adversarial refutation harness
- `engine/formal_verify/`  — Aristotle/Lean bridge + proof certificate
- `engine/orchestrator/`   — pipeline driver + RunRecord/provenance + scout/synthesize docs
- `engine/README.md`       — architecture, stage docs, how to run a problem
- `engine/GOAL.md`         — this file

## Interface contract (JSON dicts; every artifact carries `claim_id`)
- `Claim`: `{id, statement, kind: "numerical"|"theorem", artifact, params}`
- `FalsifyReport`: `{claim_id, attempts: [{name, method, result}], verdict: "survives"|"refuted", evidence}`
- `Certificate`: `{claim_id, method, enclosure, certified: bool, certificate_path, tool}`
- `ProofCertificate`: `{claim_id, lemma, lean_file, sorry_free: bool, axioms: [str], proved: bool}`
- `RunRecord`: `{run_id, claim, falsify, certify, verify, synthesis, timestamps}`

## Module entrypoints (one clear function each)
```
certify.certify(claim: dict) -> Certificate        # engine/certify/
falsify.falsify(claim: dict) -> FalsifyReport       # engine/falsify/
formal_verify.verify(lemma: str, project_dir) -> ProofCertificate   # engine/formal_verify/
orchestrator.run(claim: dict) -> RunRecord          # engine/orchestrator/ (composes the above)
```

## v1 scope (honest)
General, problem-agnostic stage interfaces; the **Hecke transfer-operator work is
the reference PLUGIN**: `certify` wraps `code/zeta_cert_rosen.py` (Arb det/winding);
`formal_verify` wraps the `aristotle` CLI (the flow proven this session in
`projects/aristotle_minpoly_lambda`); `falsify` generalizes the patterns used this
session (q=3 control, N-stability, independent-method cross-check, parameter sweep).
v1 is demonstrated on the Hecke domain; the interfaces are domain-agnostic.

## Acceptance (each module)
Clean API per contract + a **self-contained smoke test that RUNS and PASSES**
(command + output quoted) + emits a valid artifact dict. No `sorry`/stubs left in
claimed-working code. Honest report: attempts, assumptions, limits.
