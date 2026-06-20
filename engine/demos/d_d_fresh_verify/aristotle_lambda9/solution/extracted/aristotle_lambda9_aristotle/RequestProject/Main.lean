import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat
open scoped Classical
open scoped Pointwise

set_option maxHeartbeats 8000000
set_option maxRecDepth 4000
set_option synthInstance.maxHeartbeats 20000
set_option synthInstance.maxSize 128

set_option relaxedAutoImplicit false
set_option autoImplicit false

set_option pp.fullNames true
set_option pp.structureInstances true
set_option pp.coercions.types true
set_option pp.funBinderTypes true
set_option pp.letVarTypes true
set_option pp.piBinderTypes true

set_option grind.warning false

lemma lambda_9_min_poly :
    let x : Real := 2 * Real.cos (Real.pi / 9)
    x ^ 3 - 3 * x - 1 = 0 := by
  have := Real.cos_three_mul ( Real.pi / 9 ) ; rw [ ( by ring : 3 * ( Real.pi / 9 ) = Real.pi / 3 ) ] at this ; rw [ Real.cos_pi_div_three ] at this; nlinarith;