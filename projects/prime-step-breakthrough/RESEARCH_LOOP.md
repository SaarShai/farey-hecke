# Prime-Step Breakthrough Research Loop

This file freezes the orchestration and verification contract. The mathematical
and product specification will be written after the blindspot survey, then
treated as the source of truth for the rest of the program.

```loop
name: prime-step-breakthrough
topology: closed · outer · fleet
generator: independent mathematics, computation, prior-art, and application workers coordinated by a single-writer research lead
verifier: fresh-context blind proof referee plus deterministic exact-arithmetic, test, benchmark, and browser-smoke gates; final cross-vendor referee is separate from the advisor
gate: python3 ./projects/prime-step-breakthrough/verify_all.py must exit_code == 0 and its evidence report must include proof, novelty, application benchmark, tests, and live UI checks
stop: done only when every RESEARCH_SPEC.md done-means criterion passes; no-op if a wave yields no candidate above the evidence floor; partial carries every failed criterion to the next wave; blocked/escalate only for missing credentials, destructive ambiguity, or conflicting requirements
budget: max_iterations=8, max_agents=24, max_wallclock=48h
quorum: two independent mathematical checks plus one cold cross-vendor referee agree on the stated claim strength; deterministic gates remain authoritative
anchor_files: AGENTS.md, start.md, projects/prime-step-breakthrough/RESEARCH_SPEC.md, projects/prime-step-breakthrough/STATE.md
state_store: projects/prime-step-breakthrough/STATE.md
recall: before each wave read STATE.md, query wiki-memory for the active hypothesis, and inspect the cited source artifacts
writeback: after each wave record attempts, exact commands, verifier verdicts, falsifications, changed facts, and the next action in STATE.md
state_concurrency: single_writer
stuck: two consecutive waves with no falsifiable candidate or the same verifier rejection twice
advisor: GPT-5.6-Sol at xhigh via Codex as requested, plus the strongest reachable other-vendor frontier advisor at commitment boundaries; advisors do not grade their own proposals
redaction: model_roster secret-shape redaction plus exclusion of keys, credentials, private correspondence, PII, .env files, and unrelated private-repo content
consent: user explicitly requested GPT and Codex advisor egress in this task; only public mathematical statements and scoped derived artifacts may leave the host
verifier_blind: true
verifier_inputs: user goal, frozen acceptance criteria, mathematical statements, source citations, code artifacts, and raw gate outputs only
on_error: transient network or rate-limit errors retry at most twice; bad output returns as an observation; auth, configuration, permission, or policy blocks interrupt and reroute; unexpected errors halt and surface
output_actions: local scoped file writes; one scoped git commit maximum after every gate passes; no push, email, publication, deployment, deletion, or external message
```
