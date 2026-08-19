import Mathlib

/-!
# RATE finite cores (v30 dispatch)

This file isolates two formalizable fragments of the paper-level `(RATE)`
argument.

* `FW` is the renewal/overflow arithmetic after the first marked digit has
  been chosen. The theorem here is deliberately the finite product-gain
  implication, not the canonical-word/Ford counting theorem.
* `AM` uses explicit typed marked codes. The tags distinguish one versus two
  marks, atom kind, bridge/absorption/split/coupled status, stored cores,
  auxiliary gains, and heavy magnitudes. `encode`/`decode` are executable
  finite-list code maps. The round-trip theorem `decode_encode_target` and the
  injectivity theorem `marked_code_source_injective_target` are proved for the
  concrete serialization; the source-table coverage theorem (that every source
  marked object has an admissible code) is *not* claimed here.

The paper-level `(FW)` and `(AM)` estimates are not machine-verified here.
They remain **CONJECTURAL at the Lean level** until an Aristotle result is
harvested and independently rebuilt. This file contains no analytic
counting, canonical-section, or full operator theorem.

If Aristotle finds a target false, it must use the FALSE-statement escape
hatch: retain the original only in a `FALSE AS STATED` comment, prove a named
negation with an exact witness, and then state the weakest corrected theorem.
-/

namespace RateCoreV

/-! ## 1. `(FW)` first-overflow arithmetic core -/

/- The source theorem marks an overflow digit in
`W = P R^a V`, with scales `A = d_P-c_P` and `B = alpha_V+gamma_V`.
The exact displayed inequalities are

    c(W) = c(PV) + a A B,
    |c(PV)| < 2 |A B|,
    y(W) = 2 |c(W)| <= Y.

For `|a| >= 4`, these imply `|a| |A| |B| <= Y`. The theorem below is the
finite ordered-ring part of that implication. It is independent of the
paper's canonical-word and Ford-counting inputs.
-/

theorem fw_product_gain
    {n A B Y : ℝ}
    (hn : 4 ≤ n)
    (hA : 0 ≤ A)
    (hB : 0 ≤ B)
    (hheight : 2 * (n - 2) * A * B ≤ Y) :
    n * A * B ≤ Y := by
  have hcoef : n ≤ 2 * (n - 2) := by linarith
  have hab : 0 ≤ A * B := mul_nonneg hA hB
  have hmul : n * (A * B) ≤ (2 * (n - 2)) * (A * B) :=
    mul_le_mul_of_nonneg_right hcoef hab
  have hheight' : (2 * (n - 2)) * (A * B) ≤ Y := by
    simpa [mul_assoc] using hheight
  nlinarith [hmul, hheight']

/- The convolution step uses the positive integer product `n*r*s <= Y`.
This small theorem records the monotonic relaxation used before the harmonic
sum; it does not claim the multiplicity bounds `#P <= 4r`, `#V <= 4s`. -/
theorem fw_product_mono
    {n r s Y : ℕ}
    (hn : 1 ≤ n)
    (h : n * r * s ≤ Y) :
    r * s ≤ Y := by
  calc
    r * s = 1 * (r * s) := by simp
    _ ≤ n * (r * s) := Nat.mul_le_mul_right (r * s) hn
    _ = n * r * s := by simp [Nat.mul_assoc]
    _ ≤ Y := h

/-! ## 2. Typed marked-code data -/

/- Atom kinds are explicit rather than strings. The sign is part of the
constructor because `H_+`, `H_-`, `U`, and `L` are distinct source branches. -/
inductive AtomKind
  | heavyPos
  | heavyNeg
  | unitPos
  | unitNeg
  deriving DecidableEq, Repr

inductive MarkMode
  | one
  | two
  deriving DecidableEq, Repr

/- `split` is retained separately from `bridge`; `coupled` is the adjacent
two-mark branch. The two absorption directions are also distinct. -/
inductive BoundaryStatus
  | bridge
  | absorbLeft
  | absorbRight
  | split
  | coupled
  deriving DecidableEq, Repr

/- An endpoint-normalized core stores its actual exponent body and the two
maximal unit-run lengths removed by the normalization. -/
structure Core where
  body : List ℤ
  leftUnitRun : ℕ
  rightUnitRun : ℕ
  deriving DecidableEq, Repr

/- A `MarkedCode` is the finite data used by the one-cut/two-cut coding in
`ATOM_MOMENT_BRIDGE_SOL.md` and `TWOMARK_RENEWAL_SOL.md`. The lists are kept
as data, while their source bounds (at most three cores, four gains, and two
heavy marks) are stated by `WellFormed`. -/
structure MarkedCode where
  mode : MarkMode
  firstKind : AtomKind
  secondKind : Option AtomKind
  leftStatus : BoundaryStatus
  middleStatus : BoundaryStatus
  rightStatus : BoundaryStatus
  cores : List Core
  gains : List ℕ
  heavyMagnitudes : List ℕ
  deriving DecidableEq, Repr

def WellFormed (c : MarkedCode) : Prop :=
  c.cores.length ≤ 3 ∧
    c.gains.length ≤ 4 ∧
    c.heavyMagnitudes.length ≤ 2 ∧
    (∀ h ∈ c.heavyMagnitudes, 2 ≤ h) ∧
    (c.mode = .one → c.secondKind = none) ∧
    (c.mode = .two → ∃ k, c.secondKind = some k)

/- The code is serialized to a natural-number list with a leading format tag.
List lengths make parsing deterministic; signed core exponents use a
sign/magnitude pair `(0,n)` or `(1,n)`. The format is intentionally explicit
so the decoder can distinguish all constructor data without prose. -/
def atomTag : AtomKind → ℕ
  | .heavyPos => 0
  | .heavyNeg => 1
  | .unitPos => 2
  | .unitNeg => 3

def atomOfTag : ℕ → Option AtomKind
  | 0 => some .heavyPos
  | 1 => some .heavyNeg
  | 2 => some .unitPos
  | 3 => some .unitNeg
  | _ => none

def modeTag : MarkMode → ℕ
  | .one => 0
  | .two => 1

def modeOfTag : ℕ → Option MarkMode
  | 0 => some .one
  | 1 => some .two
  | _ => none

def statusTag : BoundaryStatus → ℕ
  | .bridge => 0
  | .absorbLeft => 1
  | .absorbRight => 2
  | .split => 3
  | .coupled => 4

def statusOfTag : ℕ → Option BoundaryStatus
  | 0 => some .bridge
  | 1 => some .absorbLeft
  | 2 => some .absorbRight
  | 3 => some .split
  | 4 => some .coupled
  | _ => none

def signedNat (z : ℤ) : List ℕ :=
  if 0 ≤ z then [0, Int.toNat z] else [1, Int.toNat (-z)]

def encodeCore (c : Core) : List ℕ :=
  [c.leftUnitRun, c.rightUnitRun, c.body.length] ++ c.body.flatMap signedNat

def encode (c : MarkedCode) : List ℕ :=
  [30, modeTag c.mode, atomTag c.firstKind,
    (c.secondKind.map atomTag).getD 4,
    statusTag c.leftStatus, statusTag c.middleStatus, statusTag c.rightStatus,
    c.cores.length] ++ c.cores.flatMap encodeCore ++
    [c.gains.length] ++ c.gains ++
    [c.heavyMagnitudes.length] ++ c.heavyMagnitudes

/- The decoder below is an executable parser for the fixed header and the
length-prefixed lists. It is intentionally conservative: malformed or
truncated input returns `none`; the fourth second-kind tag means `none`. -/
def takeNatList : ℕ → List ℕ → Option (List ℕ × List ℕ)
  | 0, xs => some ([], xs)
  | n + 1, x :: xs => do
      let (ys, rest) ← takeNatList n xs
      return (x :: ys, rest)
  | _, [] => none

def decodeSigned : List ℕ → Option (ℤ × List ℕ)
  | sign :: magnitude :: xs =>
      if sign = 0 then some (Int.ofNat magnitude, xs)
      else if sign = 1 then some (-Int.ofNat magnitude, xs)
      else none
  | _ => none

def decodeCore (xs : List ℕ) : Option (Core × List ℕ) := do
  let left :: right :: bodyLength :: rest := xs | none
  let (pairs, tail) ← takeNatList (2 * bodyLength) rest
  let rec decodeDigits : List ℕ → Option (List ℤ)
    | [] => some []
    | a :: b :: ys => do
        let (z, _) ← decodeSigned [a, b]
        let zs ← decodeDigits ys
        return z :: zs
    | _ => none
  let body ← decodeDigits pairs
  return ({ body := body, leftUnitRun := left, rightUnitRun := right }, tail)

def decode (xs : List ℕ) : Option MarkedCode := do
  let 30 :: modeTag' :: firstTag :: secondTag :: leftTag :: middleTag :: rightTag :: rest := xs | none
  let mode ← modeOfTag modeTag'
  let firstKind ← atomOfTag firstTag
  let secondKind ← if secondTag = 4 then some none else (atomOfTag secondTag).map some
  let leftStatus ← statusOfTag leftTag
  let middleStatus ← statusOfTag middleTag
  let rightStatus ← statusOfTag rightTag
  let coreCount :: coreRest := rest | none
  let rec decodeCores : ℕ → List ℕ → Option (List Core × List ℕ)
    | 0, ys => some ([], ys)
    | n + 1, ys => do
        let (core, tail) ← decodeCore ys
        let (cores, rest') ← decodeCores n tail
        return (core :: cores, rest')
  let (cores, afterCores) ← decodeCores coreCount coreRest
  let gainCount :: gainRest := afterCores | none
  let (gains, afterGains) ← takeNatList gainCount gainRest
  let heavyCount :: heavyRest := afterGains | none
  let (heavyMagnitudes, trailing) ← takeNatList heavyCount heavyRest
  if trailing = [] then
    some ({ mode := mode, firstKind := firstKind, secondKind := secondKind, leftStatus := leftStatus, middleStatus := middleStatus, rightStatus := rightStatus, cores := cores, gains := gains, heavyMagnitudes := heavyMagnitudes } : MarkedCode)
  else none

/- Small serialization lemmas are proved locally. They are the constructor
and parser scaffolding; they do not assert that every source marked object has
an admissible code or that the source code map is injective. -/
theorem atomOfTag_atomTag (k : AtomKind) : atomOfTag (atomTag k) = some k := by
  cases k <;> rfl

theorem modeOfTag_modeTag (m : MarkMode) : modeOfTag (modeTag m) = some m := by
  cases m <;> rfl

theorem statusOfTag_statusTag (s : BoundaryStatus) :
    statusOfTag (statusTag s) = some s := by
  cases s <;> rfl

theorem signedNat_decode (z : ℤ) :
    decodeSigned (signedNat z) = some (z, []) := by
  cases z with
  | ofNat n => simp [signedNat, decodeSigned]
  | negSucc n =>
    simp only [signedNat]
    simp [decodeSigned]
    omega

/-! ### Parser scaffolding for the length-prefixed lists -/

/- `takeNatList` splits off an initial segment of the announced length. -/
theorem takeNatList_append (l rest : List ℕ) :
    takeNatList l.length (l ++ rest) = some (l, rest) := by
  induction l with
  | nil => simp [takeNatList]
  | cons a l ih => simp [takeNatList, ih]

theorem takeNatList_self (l : List ℕ) : takeNatList l.length l = some (l, []) := by
  simpa using takeNatList_append l []

theorem signedNat_length (z : ℤ) : (signedNat z).length = 2 := by
  unfold signedNat; split <;> rfl

theorem flatMap_signedNat_length (body : List ℤ) :
    (body.flatMap signedNat).length = 2 * body.length := by
  induction body with
  | nil => simp
  | cons z zs ih =>
    simp [List.flatMap_cons, signedNat_length z, ih]
    omega

/- The digit parser inverts the sign/magnitude serialization of a core body. -/
theorem decodeDigits_flatMap (body : List ℤ) :
    decodeCore.decodeDigits (body.flatMap signedNat) = some body := by
  induction body with
  | nil => simp [decodeCore.decodeDigits]
  | cons z zs ih =>
    rcases le_or_gt 0 z with hz | hz
    · have hs : signedNat z = [0, z.toNat] := by simp [signedNat, hz]
      rw [List.flatMap_cons, hs]
      simp [decodeCore.decodeDigits, decodeSigned, ih, Int.toNat_of_nonneg hz]
    · have hs : signedNat z = [1, (-z).toNat] := by simp [signedNat, not_le.mpr hz]
      rw [List.flatMap_cons, hs]
      simp [decodeCore.decodeDigits, decodeSigned, ih]
      omega

theorem decodeCore_append (c : Core) (rest : List ℕ) :
    decodeCore (encodeCore c ++ rest) = some (c, rest) := by
  obtain ⟨body, l, r⟩ := c
  have h := takeNatList_append (body.flatMap signedNat) rest
  rw [flatMap_signedNat_length] at h
  simp [encodeCore, decodeCore, h, decodeDigits_flatMap]

theorem decodeCores_append (cores : List Core) (rest : List ℕ) :
    decode.decodeCores cores.length (cores.flatMap encodeCore ++ rest)
      = some (cores, rest) := by
  induction cores generalizing rest with
  | nil => simp [decode.decodeCores]
  | cons c cs ih =>
    simp only [List.length_cons, List.flatMap_cons, List.append_assoc,
      decode.decodeCores, decodeCore_append c (cs.flatMap encodeCore ++ rest)]
    simp [ih]

/- The executable round-trip target is stated for the data representation. -/
theorem decode_encode_target (c : MarkedCode) : decode (encode c) = some c := by
  obtain ⟨mode, k1, k2, ls, ms, rs, cores, gains, heavy⟩ := c
  simp only [encode, decode]
  simp [modeOfTag_modeTag, atomOfTag_atomTag, statusOfTag_statusTag,
    decodeCores_append, takeNatList_append, takeNatList_self]
  cases k2 with
  | none => simp
  | some k => cases k <;> simp [atomTag, atomOfTag]

/- The unconditional strengthening: `encode` is injective on the whole data
type, not only on `WellFormed` codes. -/
theorem encode_injective : Function.Injective encode := by
  intro x y hxy
  have h : decode (encode x) = decode (encode y) := by rw [hxy]
  rw [decode_encode_target, decode_encode_target] at h
  exact Option.some_injective _ h

/- The source coding theorem is the exact remaining dispatch target. It is
named separately so an Aristotle result cannot be mistaken for the local
serialization round trip. The `WellFormed` hypotheses are kept because the
dispatch asked for them, but the proof does not need them: the explicit
serialization is injective on all of `MarkedCode`, since `decode` inverts
`encode` unconditionally. -/
theorem marked_code_source_injective_target :
    ∀ (x y : MarkedCode), WellFormed x → WellFormed y →
      encode x = encode y → x = y := fun _ _ _ _ hxy => encode_injective hxy

/-! ### Concrete executable sanity checks for the serialization format -/

/-- A sample two-mark code with two stored cores. -/
def sampleCode : MarkedCode :=
  { mode := MarkMode.two, firstKind := AtomKind.heavyNeg,
    secondKind := some AtomKind.unitPos,
    leftStatus := BoundaryStatus.split, middleStatus := BoundaryStatus.coupled,
    rightStatus := BoundaryStatus.bridge,
    cores := [{ body := [3, -2, 0], leftUnitRun := 1, rightUnitRun := 5 },
              { body := [], leftUnitRun := 0, rightUnitRun := 0 }],
    gains := [1, 2, 3, 4], heavyMagnitudes := [7, 9] }

#guard encode sampleCode =
  [30, 1, 1, 2, 3, 4, 0, 2, 1, 5, 3, 0, 3, 1, 2, 0, 0, 0, 0, 0, 4, 1, 2, 3, 4, 2, 7, 9]

#guard decode (encode sampleCode) = some sampleCode

/- Malformed input is rejected: the header tag must be `30`. -/
#guard decode [29, 0, 0, 4, 0, 0, 0, 0, 0, 0] = none

/- The finite source-side product gain is likewise a dispatch target. Its
hypotheses mirror the typed code's recorded gains and heavy magnitudes, but
the analytic Ford/core population is deliberately excluded. -/
theorem marked_code_product_gain_target
    (c : MarkedCode) (h : WellFormed c) :
    c.gains.length ≤ 4 ∧ c.heavyMagnitudes.length ≤ 2 := by
  exact ⟨h.2.1, h.2.2.1⟩

end RateCoreV
