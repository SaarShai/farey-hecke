# Frontier repo-spec decisions — 2026-08-16

Based on REPO_DESIGN_PIPELINE.md + REPO_DESIGN_SPECTRAL.md (both adjudicated
sound). Owner authorized public repo creation 2026-08-16.

## Repo 1: lemma-ledger (name per report rank 1 "LemmaLedger")
Positioning: "A claim ledger with mechanically enforced evidence promotion
for AI-assisted mathematics."
- v1 = PRIMARY GAP 1 only: versioned claim graph (JSON schema), promotion
  validator (statistical → numerical → certified → machine-proved, distinct
  validators per tier, no silent inheritance), negative-result retention,
  receipt envelope (hashes, versions, rounded-down margins).
- Form: documentation-first standard + pip-installable validator
  (`lemma-ledger` CLI) + template repo layout + ONE pinned replayable
  worked example (small conjecture through all tiers).
- Deferred to v2 (recorded in ROADMAP.md): sandboxed replay/CI gate (GAP 2),
  adapter protocol (GAP 3).
- License: Apache-2.0. Python 3.11+. No LLM calls in v1 (the ledger is
  model-agnostic by design — that IS the swappability).

## Repo 2: contourcert (name per report rank 1 "ContourCert")
Positioning: "Proof-carrying winding certificates for spectral determinants."
- v1 per report §4: (1) versioned certificate format (all binding fields
  listed in the report, margins serialized rounded-down as decimal strings);
  (2) SMALL independent checker (single command `contourcert check CERT`,
  no plotting/search/adaptivity, pinned python-flint, strict on unknown
  fields, conformance fixtures incl. salted NEGATIVE certificates, verdict
  string "VALID NUMERICAL WINDING CERTIFICATE FOR ADAPTER X" — never
  "THEOREM PROVED"); (3) generic contour engine (producer, callback-based);
  (4) tail-adapter interface with our proven Hecke/Rosen families as worked
  examples labeled bring-your-own-tail-bound for new families.
- Two-layer trust split per report §3 (DRAT analogy with its stated limit).
- G_5 flagship example certificate included so paper reviewers can re-verify.
- License: MIT (max uptake for a checker). Python 3.11+, python-flint pinned.

## Shared build rules (binding on builders)
- Build at /Users/za/Documents/lemma-ledger and /Users/za/Documents/contourcert
  (git init, local only; publish AFTER frontier review + secret scan).
- NEVER copy: anything from ~/.farey_api_keys, ~/.kaggle, .env, tokens, or
  absolute local paths into repo content. Sanitize provenance to repo-relative.
- No fabricated benchmarks/stars/users; README claims only what v1 does.
- Honest limitation sections are mandatory (from the two reports' caveats).
