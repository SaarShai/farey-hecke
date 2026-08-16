# Practical-value: package the AI-verified-math pipeline as a public repo

- status: ACTIVE 2026-08-16 — owner upgraded to full public-repo build ("create a new public repo, separate from this one"); deep-research lanes launched, Opus 5 builders next; frontier orchestrates
- kind: engineering/writing
- created: 2026-08-16 (owner directive: "can/should this be a github repo…")
- blocked by: flagship paper (soft; design doc can start anytime)

Scope: extract domain-agnostic core = protocol layer (claim tiers, receipt
schemas, negative-result retention, adversarial gates) + adapter interfaces
(scout/falsifier/certifier/prover/reviewer all swappable) + one-command
orchestrator + worked end-to-end example + docs/tests/contribution guide.
Design doc + interface spec = first deliverable (doubles as half the methods
paper). Honest estimate: several focused weeks for the packaging itself.
Adjudicated prior-art basis: research_notes/practical_value_2026-08-16/.
