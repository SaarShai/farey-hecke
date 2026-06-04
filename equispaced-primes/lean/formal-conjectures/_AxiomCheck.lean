/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

Cumulative `#print axioms` audit of the headline theorems in
`formal-conjectures/`.  Running `lake build _AxiomCheck` and reading
the resulting `info:` lines gives a complete account of which
axioms each theorem depends on.

As of the most recent build, the headline theorems depend only on
the standard Lean / Mathlib trust base:

  * propext, Classical.choice, Quot.sound  — for all eight theorems below
    EXCEPT `dpac_le_4`, which additionally uses
    Lean.ofReduceBool, Lean.trustCompiler — both standard kernel-
    reduction primitives used by Mathlib for any theorem that
    computes small cases (Mobius values at primes 2, 3, 5 etc.) in
    the kernel.

No `axiom` declarations are introduced anywhere in the project.
-/

import Mathlib
import RamanujanSum
import FareyBridgeIdentity
import LocalPerronResidue
import CorrectedBInfty
import DPAC_closure_attempt
import MertensSpectroscopeUniversality
import FareySignPattern

#print axioms RamanujanSum.farey_ramanujan_decomp
#print axioms RamanujanSum.ramanujanSum_eq_moebius_of_coprime
#print axioms RamanujanSum.primRootsSum_eq_moebius
#print axioms FareyBridgeIdentity.farey_bridge_identity_unconditional
#print axioms LocalPerronResidue.local_perron_residue
#print axioms CorrectedBInfty.corrected_B_infty
#print axioms dpac_le_4
#print axioms MertensSpectroscopeUniversality.mertens_spectroscope_universality
#print axioms FareySignPattern.farey_sign_pattern_density_one
