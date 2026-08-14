# Lean build re-verification — lane D

Date: 2026-08-14
Scope: read-only source inspection/build verification. No source files were edited. Build artifacts are under project .lake directories.

## Discovery

Bridge Lake root: /Users/za/Documents/farey-hecke/equispaced-primes/lean/

- lean-toolchain: leanprover/lean4:v4.28.0
- lakefile.toml registers FareyBridgeIdentity with srcDir = "formal-conjectures".
- lakefile.toml registers _AxiomCheck.
- formal-conjectures/_AxiomCheckBridge.lean is a focused, direct-run audit file.
- Main theorem: FareyBridgeIdentity.farey_bridge_identity_unconditional.

Aristotle Lake root: /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v16/result/project_aristotle/

- lean-toolchain: leanprover/lean4:v4.28.0
- lakefile.toml registers PronyPowerSums and makes it the default target.
- Main theorem: prony_power_sum_uniqueness.
- No scratch project was needed: the artifact is already a Lake project.

## Item 1 — Farey Bridge identity

### Cache

Command:

~~~text
set +e
/usr/bin/time -p lake exe cache get 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Output:

~~~text
Current branch: HEAD
Using cache (Azure) from origin: leanprover-community/mathlib4
No files to download
Already decompressed 8010 file(s)
real 16.60
user 2.47
sys 4.58
EXIT_CODE=0
~~~

### Target build

Command:

~~~text
set +e
/usr/bin/time -p lake build FareyBridgeIdentity 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Captured result/output:

~~~text
⚠ [8026/8028] Replayed RamanujanSum
warning: formal-conjectures/RamanujanSum.lean:115:29: This simp argument is unused:
  Nat.gcd_mul_left
warning: formal-conjectures/RamanujanSum.lean:115:47: This simp argument is unused:
  Nat.gcd_mul_right
warning: formal-conjectures/RamanujanSum.lean:116:42: This simp argument is unused:
  Nat.gcd_mul_left
warning: formal-conjectures/RamanujanSum.lean:121:44: This simp argument is unused:
  Nat.gcd_mul_left
warning: formal-conjectures/RamanujanSum.lean:135:110: This simp argument is unused:
  Nat.mul_div_cancel'
Build completed successfully (8028 jobs).
real 4.92
user 4.43
sys 6.61
EXIT_CODE=0
~~~

The same output also contained non-failing info suggestions for ring_nf in RamanujanSum. No warning was emitted from FareyBridgeIdentity itself.

### Registered cumulative axiom audit

Command:

~~~text
set +e
/usr/bin/time -p lake build _AxiomCheck 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Captured decisive output:

~~~text
ℹ [8033/8034] Built _AxiomCheck (40s)
info: formal-conjectures/_AxiomCheck.lean:33:0: 'RamanujanSum.farey_ramanujan_decomp' depends on axioms: [propext, Classical.choice, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:34:0: 'RamanujanSum.ramanujanSum_eq_moebius_of_coprime' depends on axioms: [propext, Classical.choice, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:35:0: 'RamanujanSum.primRootsSum_eq_moebius' depends on axioms: [propext, Classical.choice, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:36:0: 'FareyBridgeIdentity.farey_bridge_identity_unconditional' depends on axioms: [propext, Classical.choice, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:37:0: 'LocalPerronResidue.local_perron_residue' depends on axioms: [propext, Classical.choice, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:38:0: 'CorrectedBInfty.corrected_B_infty' depends on axioms: [propext, Classical.choice, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:39:0: 'dpac_le_4' depends on axioms: [propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:40:0: 'MertensSpectroscopeUniversality.mertens_spectroscope_universality' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
info: formal-conjectures/_AxiomCheck.lean:41:0: 'FareySignPattern.farey_sign_pattern_density_one' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (8034 jobs).
real 46.50
user 15.35
sys 11.93
EXIT_CODE=0
~~~

The audit build emitted the same non-failing RamanujanSum diagnostics recorded above.

### Focused Bridge axiom check

Command:

~~~text
set +e
/usr/bin/time -p lake env lean formal-conjectures/_AxiomCheckBridge.lean 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Output:

~~~text
'RamanujanSum.primRootsSum_eq_moebius' depends on axioms: [propext, Classical.choice, Quot.sound]
'RamanujanSum.ramanujanSum_eq_moebius_of_coprime' depends on axioms: [propext, Classical.choice, Quot.sound]
'RamanujanSum.farey_ramanujan_decomp' depends on axioms: [propext, Classical.choice, Quot.sound]
'FareyBridgeIdentity.farey_bridge_identity_unconditional' depends on axioms: [propext, Classical.choice, Quot.sound]
real 8.73
user 5.09
sys 3.23
EXIT_CODE=0
~~~

### Item 1 verdict

**VERIFIED-FRESH**

Evidence: FareyBridgeIdentity build exit 0; registered _AxiomCheck exit 0; focused audit exit 0; main theorem axiom list is exactly [propext, Classical.choice, Quot.sound]. The dependency warnings/info are recorded and did not cause failure.

## Item 2 — Aristotle Prony artifact

### Cache: first attempt

Command:

~~~text
set +e
/usr/bin/time -p lake exe cache get 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Output:

~~~text
info: mathlib: cloning https://github.com/leanprover-community/mathlib4.git
error: external command 'git' exited with code 128
real 0.17
user 0.08
sys 0.07
EXIT_CODE=1
~~~

The project package directory was empty. The exact matching v4.28.0 package set already downloaded for the Bridge project was reused through symlinks under the Aristotle .lake/packages directory only.

Command:

~~~text
set -e
for pkg_path in /Users/za/Documents/farey-hecke/equispaced-primes/lean/.lake/packages/*; do
  pkg_name=${pkg_path##*/}
  if test ! -e ".lake/packages/$pkg_name"; then
    ln -s "$pkg_path" ".lake/packages/$pkg_name"
  fi
done
find .lake/packages -maxdepth 1 -type l -print | sort
~~~

Output:

~~~text
.lake/packages/Cli
.lake/packages/LeanSearchClient
.lake/packages/Qq
.lake/packages/aesop
.lake/packages/batteries
.lake/packages/importGraph
.lake/packages/mathlib
.lake/packages/plausible
.lake/packages/proofwidgets
~~~

### Initial build attempt

Command:

~~~text
set +e
/usr/bin/time -p lake build PronyPowerSums 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Output:

~~~text
info: mathlib: cloning https://github.com/leanprover-community/mathlib4.git
error: external command 'git' exited with code 128
real 0.11
user 0.05
sys 0.04
EXIT_CODE=1
~~~

### Successful local rebuild

Command:

~~~text
set +e
/usr/bin/time -p lake build PronyPowerSums 2>&1
rc=$?
printf 'EXIT_CODE=%s\n' "$rc"
exit 0
~~~

Output:

~~~text
ℹ [8026/8027] Built PronyPowerSums (21s)
info: PronyPowerSums.lean:171:0: 'prony_power_sum_uniqueness' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (8027 jobs).
real 26.55
user 9.43
sys 10.14
EXIT_CODE=0
~~~

The source file's top-level #print axioms prony_power_sum_uniqueness emitted the requested axiom result during the successful build.

### Item 2 verdict

**VERIFIED-FRESH**

Evidence: after the explicitly recorded cache/clone failure, the existing Lake target rebuilt the artifact successfully using the exact local v4.28.0 dependency package set; exit 0, wall time 26.55s, and axiom list [propext, Classical.choice, Quot.sound]. No warning was emitted on the successful Prony build. No build exceeded 40 minutes.

## Source write-integrity check

Commands:

~~~text
find equispaced-primes/lean/formal-conjectures -maxdepth 1 -type f \( -name '*.olean' -o -name '*.ilean' \) -print | sort
find projects/aristotle_dispatch_v16/result/project_aristotle -maxdepth 1 -type f \( -name '*.olean' -o -name '*.ilean' \) -print | sort
~~~

Output:

~~~text
~~~

Compiled artifacts were under .lake/build:

~~~text
equispaced-primes/lean/.lake/build/lib/lean/FareyBridgeIdentity.olean
equispaced-primes/lean/.lake/build/lib/lean/_AxiomCheck.olean
projects/aristotle_dispatch_v16/result/project_aristotle/.lake/build/lib/lean/PronyPowerSums.olean
~~~

No source-side .olean/.ilean files were created.
