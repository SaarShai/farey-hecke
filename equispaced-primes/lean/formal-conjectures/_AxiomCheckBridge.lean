/-
Minimal axiom audit for the Bridge Identity stack only.
Run after `lake build RamanujanSum FareyBridgeIdentity` via:
  lake env lean formal-conjectures/_AxiomCheckBridge.lean
Expect each to print exactly: [propext, Classical.choice, Quot.sound]
and NO `sorryAx`.
-/
import RamanujanSum
import FareyBridgeIdentity

#print axioms RamanujanSum.primRootsSum_eq_moebius
#print axioms RamanujanSum.ramanujanSum_eq_moebius_of_coprime
#print axioms RamanujanSum.farey_ramanujan_decomp
#print axioms FareyBridgeIdentity.farey_bridge_identity_unconditional
