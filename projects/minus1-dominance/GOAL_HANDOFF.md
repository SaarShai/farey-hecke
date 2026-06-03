# "-1 dominance" investigation -> completion + honest synthesis - HANDOFF

Self-contained handoff for a `/goal` session. Everything needed is here. Work autonomously,
verify with results, send NOTHING outward.

## MISSION
Finish and honestly synthesize the "Dominance of -1" Chebyshev prime-race investigation, using the
M1/M2/M3 compute fleet, ending in a cited, correctly-scoped ledger of what we can stand behind.

## VERDICT ALREADY ESTABLISHED (conditional GRH+LI; adversarially verified - do NOT re-litigate)
- "-1 dominates the non-residue hierarchy" is FALSE and exactly backwards. a = -1 (mod N) is the
  **LEAST-biased** non-residue: the Rubinstein-Sarnak sign-density delta(N;-1,1) is the MINIMUM over
  non-residues, because the limiting variance **V(N;-1,1) is the MAXIMUM** (delta is strictly
  decreasing in V). For primes q == 3 (mod 4) this is **Fiorilli-Martin, Crelle 676 (2013), Thm 1.10**
  (primary-verified verbatim in FM_text.txt:325).
- NR-vs-NR head-to-head is vacuous: delta(N;a,b) = 1/2 exactly for distinct non-residues (RS symmetry).
- Mechanism = parity: a=-1 puts all its weight on ODD characters (|chi(-1)-1|^2 = 4 odd, 0 even);
  odd characters carry larger c_chi = sum_{gamma: L(1/2+i gamma,chi)=0} 1/(1/4+gamma^2). Skew = 0
  (symmetric RS law); Aoki-Koyama DRH magnitude ruled out as a discriminant (degenerate among NR
  under Chowla nonvanishing). NOTHING unconditional over Q.
- Sanity validated: reproduced RS densities delta(4;3,1)=0.99593 (RS 0.99590), delta(3;2,1)=0.99907
  (RS 0.99906); zero-violation scan q<2000.

## LIVE STATE (as of handoff, 2026-06-02)
- **Workflow** `minus1-dominance-investigation` (run wf_9ffc1616-c18) ABORTED at its Lean step (0-olean
  `.lake` hang); Theory/Compute/Prove completed. `REPORT.md` is hand-written from those phases and is
  PRESENT. `Minus1Core.lean` was NOT produced (Lean is TODO, step 1).
- **Sieve to 3e14 RUNNING on M2** (`alicia@192.168.1.92:~/farey-sieve/`): `mr1_par 300000000000000
  grid_full.txt curve_3e14.tsv 11 224` under `caffeinate -i nohup`, log `run.log`. ETA ~12-18h.
  Check with `pgrep -fl mr1_par`, `tail run.log`, `ls -la curve_3e14.tsv`. NOTE: mr1_par writes
  curve_3e14.tsv only at COMPLETION (it assembles all grid points after every chunk finishes), so an
  empty/absent output file mid-run is NORMAL - judge progress by `pgrep mr1_par` (alive) + run.log, not
  the output file.
- **Option 3 NOT yet launched**: the analytic delta/variance-ordering sweep over many moduli, to run
  on **M1** (`new@192.168.1.22`).
- **Free empirical check** (existing verified curve to 1.3e13): V(-1)=max corroborated for N=7,11
  (asymptotic regime reached) but NOT N=8,19,23 (their onset ~ e^33.4 ~ 3e14 is beyond 1.3e13 data) -
  which is exactly why the sieve to 3e14 is justified.

## RESOURCES
- Fleet SSH: see `/Users/za/Documents/Farey NOW/MACHINE_ACCESS.md`. M1 = `new@192.168.1.22` (M1 Max
  10c/32GB), M2 = `alicia@192.168.1.92` (M2 Pro 12c/16GB; busy with sieve), M3 = this host. Key
  `~/.ssh/id_ed25519`. Nodes on AC. Wi-Fi DHCP **IPs DRIFT** -> re-discover via MACHINE_ACCESS.md if
  SSH fails. Run long jobs `caffeinate -i nohup CMD > log 2>&1 &`; over SSH `python3` may be CLT 3.9
  (M2 has mpmath there); use full paths if needed.
- **Aristotle** = user-submitted Lean prover (you cannot submit). If `Minus1Core.lean` won't compile
  locally (broken submodule env), stage a clean dispatch package and ASK the user to submit.
- **Kaggle** wired (`kaggle-feeder`) if more CPU is wanted.
- Validated code already in this workspace: `compute_delta.py`, `canonical_verify.py`,
  `canonical_ordering.py`, `sharp_gap.py`, `gap_bound.py`, `empirical_rank.py`, plus the primary-source
  texts (FM_text.txt, AK_text.txt, PNR_text.txt).

## STEPS (in order)
1. **Read `REPORT.md`** (the verdict). Then BUILD `Minus1Core.lean` (not yet produced): `cd
   "/Users/za/Documents/Farey NOW/primes-equispaced" && lake exe cache get` FIRST (the `.lake` has 0
   oleans, which hung the workflow), then `( ~/.elan/bin/lake env lean ".../Minus1Core.lean" 2>&1; echo
   EXIT=$? ) >/tmp/m1lean.out 2>&1`; trust the EXIT= line. If it still fails, stage an Aristotle
   dispatch package and ask the user to submit.
2. **Launch option 3 on M1**: generalize the workflow's validated variance-ordering test (the FM
   gap-inequality / V(N;a,1) computation) to a large q-range (e.g. all primes q<10^5, then push). For
   each q, decide whether a=-1 is the variance-MAX over non-residues (=> least-biased). Validate by
   reproducing the q<2000 result first. Save results + a plot to this workspace; report every q where
   -1 is NOT variance-max (FM Thm 1.10 predicts only finitely many). Run under caffeinate+nohup.
3. **Monitor the M2 sieve**: when curve_3e14.tsv passes x=1.3e13, **cross-check exactly** vs
   `koyama_replication_bundle/out2.tsv` (must match to the integer at shared checkpoints). At 3e14,
   compute V(N;a,1) per non-residue from curve_3e14.tsv (RS-normalized variance over the x-grid) and
   test whether a=-1 becomes the variance-MAX for **N=19 and N=23** (the asymptotic prediction).
4. **Write `projects/minus1-dominance/LEDGER.md`**: the honest, cited, scoped summary -
   PROVEN(conditional GRH+LI vs unconditional) / EMPIRICAL / FORMALIZED. Include the -1 verdict, the
   option-3 sweep result, the sieve/variance result. Verify every citation against the primary texts
   here (FM Crelle 676 2013 Thm 1.10; RS Experimental Math 1994; Aoki-Koyama JNT 245 2023
   arXiv:2203.12266). Mark anything unverified.

## CONSTRAINTS (hard)
- **Never** send outbound / contact Koyama / post / publish - ALL outward steps are USER-driven
  (Koyama collaboration is gated; the math proceeds as our own work).
- Never commit / push / change git config / skip hooks unless the user explicitly asks.
- **Adversarial honesty**: separate PROVEN from NUMERICAL from CONJECTURAL; NEVER upgrade a CONDITIONAL
  (GRH/LI/DRH) result to unconditional; verify EVERY citation (fabrication is this project's #1 failure
  mode).
- Trust the `EXIT=`/`run.log` lines in redirect files, NOT task-notification summaries (they have
  falsely reported success).
- `~/Documents` is Google-Drive-synced: no folder/`.git` move/rename/delete without per-action user
  confirmation; treat `* (1)` files as Drive conflict artifacts, never authoritative.
- Compute offload to M1/M2/Kaggle is INTERNAL (not outbound) - use it freely.

## DEFINITION OF DONE
- REPORT.md read; verdict + Lean status confirmed (or Aristotle-staged).
- Option-3 sweep complete; results + plot saved; exceptions (if any) reported.
- M2 sieve to 3e14 complete, cross-checked at <=1.3e13, and the N=19/23 variance test computed.
- LEDGER.md written - honest, cited, correctly scoped.
- Final report to the user. Nothing sent outward.
