# RH goals scouting — 2026-08-14

- [x] Read anthropic.com/research/riemann-zeta (41.6%→67.2% critical-line proportion; fan-out/falsify/verify/Lean methodology)
- [x] Fan out 5 codex gpt-5.6-luna xhigh search agents over repo partitions (research_notes / wiki+facts / engine+code / equispaced-primes / projects)
- [x] Self-read core zeta-adjacent notes (G_5 resonances, prime-Farey verdicts, Koyama)
- [x] Locate + audit the zero-detection method (Mertens spectroscope / MUSIC tomography — tool killed, theory residue live)
- [x] Synthesize inventory: everything zeta/RH-related, status-tagged
- [x] Cross-check goal candidates against DO-NOT-RE-CHASE list
- [x] Define 3 goals for real (modest) RH-adjacent progress
- [x] Draft 3 goal maps (wayfinder skill absent — markdown drafts)

## Review

Output: research_notes/rh_goals_2026-08-14/ — 00_SYNTHESIS.md + GOAL{1,2,3}_MAP.md.
- Goal 1: sample-complexity theory of zero detection from prime data (unscooped residue of the killed spectroscopy tool).
- Goal 2: certified resonance atlas + arithmetic-rigidity law (absorbs Pick B; requires restoring Aletheia stack from b973d56 — not on HEAD/main).
- Goal 3: unconditional Farey–Mertens structure (DiscrepancyStep Kloosterman probe with pre-registered NO-GO gate; ζ′(ρ) zero-sum constant conflict resolution; priority note).
Key repo facts surfaced: engine/ empty on HEAD (stack on codex/declusteraudit* branches only); spectroscope README claims unaudited (artifacts missing); log.md 2/π² conjecture conflicts with mimo E5 probe.

## Lane D — fresh Lean re-verification (2026-08-14)

- [x] Inspect Lake targets, theorem names, cache configuration, and existing axiom-check files.
- [x] Sequentially build the Farey Bridge target and capture exit code, wall time, and warnings.
- [x] Build the Bridge axiom-check target and capture `#print axioms` output.
- [x] Sequentially build the Aristotle Prony target and capture exit code, wall time, and warnings.
- [x] Capture `#print axioms prony_power_sum_uniqueness` output.
- [x] Write `research_notes/rh_goals_2026-08-14/lane_d/LEAN_REVERIFY.md` with verbatim commands/output and per-item verdicts.

### Lane D review/results

Output: `research_notes/rh_goals_2026-08-14/lane_d/LEAN_REVERIFY.md`.
Both requested items are VERIFIED-FRESH. Aristotle cache cloning failed with git exit 128, then the exact local v4.28.0 package set was reused inside `.lake/packages`; the target rebuilt with exit 0 and the requested axiom list.
