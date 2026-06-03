GOAL: Finish + honestly synthesize the "-1 dominance" (Chebyshev prime-race) investigation using the M1/M2/M3 compute fleet. Work autonomously until DONE; verify with results; send NOTHING outward.

FIRST ACTION - read in full (full detail, live state, constraints, DoD):
- /Users/za/Documents/Farey NOW/projects/minus1-dominance/GOAL_HANDOFF.md   (the full handoff)
- /Users/za/Documents/Farey NOW/projects/minus1-dominance/REPORT.md         (verdict synthesis - PRESENT, hand-written)
- /Users/za/Documents/Farey NOW/MACHINE_ACCESS.md                           (fleet SSH access)

VERDICT ALREADY ESTABLISHED (conditional GRH+LI; adversarially verified; do NOT re-litigate): "-1 dominance among non-residues" is FALSE/backwards - a=-1 is the LEAST-biased non-residue (RS sign-density delta-MINIMUM) because its limiting variance V(N;-1,1) is the MAXIMUM; = Fiorilli-Martin Crelle 676 (2013) Thm 1.10 for primes q==3 mod 4. NR-vs-NR head-to-head delta=1/2 (vacuous). Sanity-checked (RS delta(4;3,1)=0.99593, delta(3;2,1)=0.99907). Nothing unconditional over Q.

LIVE STATE:
- Sieve to 3e14 RUNNING on M2 (alicia@192.168.1.92:~/farey-sieve/): mr1_par -> curve_3e14.tsv, 11 threads, caffeinated, ETA ~12-18h. Check: pgrep -fl mr1_par; tail run.log; ls -la curve_3e14.tsv.
- Option 3 (analytic delta/variance-ordering sweep over many moduli) NOT yet launched -> run on M1 (new@192.168.1.22), reusing the workflow's VALIDATED code in this dir (canonical_verify.py / sharp_gap.py / gap_bound.py / compute_delta.py), generalized to large q.
- Free check: V(-1)=max corroborated for N=7,11 (asymptotic regime reached) but NOT N=8,19,23 (onset ~3e14, beyond our 1.3e13 data) - hence the sieve.

DO (in order):
1) Read REPORT.md (verdict). Minus1Core.lean NOT yet built (Lean hung on 0-olean .lake). Build: cd primes-equispaced && `lake exe cache get` FIRST, then `( ~/.elan/bin/lake env lean .../Minus1Core.lean 2>&1; echo EXIT=$? ) >/tmp/m1.out`; trust the EXIT= line. If still failing, stage an Aristotle dispatch package and ASK the user to submit.
2) Launch the option-3 sweep on M1 (caffeinate -i nohup): generalize the variance-ordering test to large q (primes q<1e5, then push); validate by reproducing the q<2000 result first; save results+plot here; report every q where -1 is NOT variance-max (FM predicts only finitely many).
3) Poll the M2 sieve. When curve_3e14.tsv passes x=1.3e13, cross-check EXACTLY vs koyama_replication_bundle/out2.tsv (must match to the integer). At 3e14, compute RS-normalized V(N;a,1) per non-residue and test whether a=-1 becomes the variance-MAX for N=19 and N=23 (the asymptotic prediction).
4) Write projects/minus1-dominance/LEDGER.md - the honest, cited, scoped summary: PROVEN(conditional GRH+LI vs unconditional) / EMPIRICAL / FORMALIZED. Verify every citation vs the primary texts here (FM Crelle 676 2013 Thm 1.10; RS Experimental Math 1994; Aoki-Koyama JNT 245 2023 arXiv:2203.12266).

DISCIPLINE: long jobs under `caffeinate -i nohup CMD > log 2>&1 &`; trust EXIT=/run.log lines, NOT task-notification summaries (they falsely report success). Wi-Fi DHCP IPs DRIFT - re-discover per MACHINE_ACCESS.md if SSH fails.

NON-NEGOTIABLE: never send outbound / contact Koyama / post / publish (all outward steps USER-driven; the math proceeds as our own work); never commit/push/change git config/skip hooks unless the user explicitly asks; adversarial honesty (separate proven/numerical/conjectural, NEVER upgrade conditional GRH/LI/DRH -> unconditional, verify EVERY citation - fabrication is this project's #1 failure mode); ~/Documents is Google-Drive-synced - no folder/.git move/rename/delete without per-action confirmation, treat ' (1)' files as conflict artifacts.

DONE = REPORT.md read + verdict/Lean confirmed (or Aristotle-staged); option-3 sweep complete + saved; sieve to 3e14 done, cross-checked <=1.3e13, N=19/23 variance test computed; LEDGER.md written. Report honestly to the user; send nothing outward.
