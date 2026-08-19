import Mathlib

/-!
# Bounded one/two-mark source data (v31 dispatch)

This file is a standalone, executable data model for the bounded record in
Lemma 4.1 of `TWOMARK_RENEWAL_SOL.md`.  It separates the paper source object
from its code: a source carries a word and its validity checks, a mark choice,
four boundary-status fields, the three empty-core flags, the coupled-case
selector, and the normalized cores; a `PaperCode` has only a finite tag, three
core slots, four auxiliary integers, and two heavy-magnitude slots.

The source-table targets below are deliberately CONJECTURAL until an
independent Aristotle result and a cold source-coverage audit exist.  The
executable definitions do not assert the matrix inequality (4.1), Ford
counting, `(AM)`, RATE-A, or the LAW.  Those are paper inputs/exclusions, not
hidden hypotheses in this source.
-/

namespace RateCoreVI

/-! ## Normalized source atoms and validity checks -/

inductive AtomKind
  | heavyPos
  | heavyNeg
  | unitPos
  | unitNeg
  deriving DecidableEq, Repr, Fintype

/- A heavy atom is `H_{+n}` or `H_{-n}`; a light atom is `U^t` or `L^t`.
The numerical side conditions (`n >= 2`, `t >= 1`, and the balanced range)
are checked by `SourceAtom.rangeOK` rather than hidden in the constructors. -/
inductive SourceAtom
  | heavyPos (magnitude : ℕ)
  | heavyNeg (magnitude : ℕ)
  | unitPos (runLength : ℕ)
  | unitNeg (runLength : ℕ)
  deriving DecidableEq, Repr

def SourceAtom.kind : SourceAtom → AtomKind
  | .heavyPos _ => .heavyPos
  | .heavyNeg _ => .heavyNeg
  | .unitPos _ => .unitPos
  | .unitNeg _ => .unitNeg

def SourceAtom.magnitude : SourceAtom → ℕ
  | .heavyPos n => n
  | .heavyNeg n => n
  | .unitPos t => t
  | .unitNeg t => t

def SourceAtom.isHeavy : SourceAtom → Bool
  | .heavyPos _ | .heavyNeg _ => true
  | .unitPos _ | .unitNeg _ => false

def SourceAtom.isUnit : SourceAtom → Bool
  | .heavyPos _ | .heavyNeg _ => false
  | .unitPos _ | .unitNeg _ => true

def SourceAtom.rangeOK (q : ℕ) : SourceAtom → Bool
  | .heavyPos n | .heavyNeg n => 2 ≤ n && 2 * n ≤ q
  | .unitPos t | .unitNeg t => 1 ≤ t && 3 ≤ q

def SourceAtom.heavyMagnitude? : SourceAtom → Option ℕ
  | .heavyPos n | .heavyNeg n => some n
  | .unitPos _ | .unitNeg _ => none

def sameUnitSign : SourceAtom → SourceAtom → Bool
  | .unitPos _, .unitPos _ => true
  | .unitNeg _, .unitNeg _ => true
  | _, _ => false

/- Adjacent equal-sign light atoms would be one maximal run. -/
def maximalRunOK : List SourceAtom → Bool
  | [] => true
  | [_] => true
  | a :: b :: rest => !(sameUnitSign a b) && maximalRunOK (b :: rest)

structure BalancedRangeData (q : ℕ) where
  rangeOK : Bool
  maximalRunsOK : Bool
  deriving DecidableEq, Repr

def balancedRangeData (q : ℕ) (atoms : List SourceAtom) : BalancedRangeData q :=
  { rangeOK := atoms.all (SourceAtom.rangeOK q)
    maximalRunsOK := maximalRunOK atoms }

structure BalancedWord (q : ℕ) where
  atoms : List SourceAtom
  checks : BalancedRangeData q
  deriving DecidableEq, Repr

def BalancedWord.Valid (w : BalancedWord q) : Prop :=
  w.checks = balancedRangeData q w.atoms ∧
    w.checks.rangeOK = true ∧
    w.checks.maximalRunsOK = true

/-! ## Mark choices and every source-table branch selector -/

inductive MarkChoice
  | one (index : ℕ)
  | two (leftIndex rightIndex : ℕ)
  deriving DecidableEq, Repr

def MarkChoice.Valid (choice : MarkChoice) (atoms : List SourceAtom) : Prop :=
  match choice with
  | .one i => i < atoms.length
  | .two i j => i < j ∧ j < atoms.length

/- Each of the four boundary fields has one of these three statuses.  The
paper's factor is `3^4`; the four coupled alternatives are represented by the
separate `CoupledCase` type below. -/
inductive CutAction
  | bridge
  | absorb
  | split
  deriving DecidableEq, Repr, Fintype

inductive CoupledCase
  | unitHeavy
  | heavyUnit
  | unitUnit
  | reverseUnitUnit
  deriving DecidableEq, Repr, Fintype

structure EmptyCoreFlags where
  left : Bool
  middle : Bool
  right : Bool
  deriving DecidableEq, Repr

structure Core where
  body : List SourceAtom
  leftUnitRun : ℕ
  rightUnitRun : ℕ
  deriving DecidableEq, Repr

def Core.Valid (q : ℕ) (c : Core) : Prop :=
  c.body.all (SourceAtom.rangeOK q) = true ∧
    maximalRunOK c.body = true

/- Four gain-bearing integer positions correspond to `p,r,s,v` (or the two
light bridge lengths) in the paper tables.  The four status fields are the
four factors in the paper's `3^4` ceiling. -/
structure CutData where
  leftAction : CutAction
  middleAction : CutAction
  rightAction : CutAction
  outerAction : CutAction
  empty : EmptyCoreFlags
  coupled : CoupledCase
  auxiliaries : Fin 4 → ℕ
  deriving DecidableEq, Repr

/- The source carries the full normalized word and decomposition metadata.
The code below retains only its bounded core slots and marked magnitudes. -/
structure MarkedSource (q : ℕ) where
  word : BalancedWord q
  mark : MarkChoice
  cuts : CutData
  cores : List Core
  deriving DecidableEq, Repr

def MarkedSource.Valid (s : MarkedSource q) : Prop :=
  BalancedWord.Valid s.word ∧
    MarkChoice.Valid s.mark s.word.atoms ∧
    (∀ c ∈ s.cores, Core.Valid q c)

/-! ## The bounded paper record and executable source maps -/

/- The exact paper overcount is
`4^2 * 3^4 * 2^3 * 4 * 2 = 82944`.  `sourceEncode` is the only constructor
used to choose an admissible tag from source data; arbitrary tags remain
representable so that the decoder is total and executable. -/
abbrev PaperTag := Fin 82944

structure PaperCode (q : ℕ) where
  tag : PaperTag
  cores : Fin 3 → Option Core
  auxiliaries : Fin 4 → ℕ
  heavyMagnitudes : Fin 2 → Option ℕ
  deriving DecidableEq, Repr

def PaperCode.Valid (q : ℕ) (c : PaperCode q) : Prop :=
  (∀ i a, c.cores i = some a → Core.Valid q a) ∧
    (∀ i n, c.heavyMagnitudes i = some n → 2 ≤ n)

def listAtNat? {α : Type} : List α → ℕ → Option α
  | [], _ => none
  | x :: _, 0 => some x
  | _ :: xs, n + 1 => listAtNat? xs n

def listAt? {α : Type} {n : ℕ} (xs : List α) (i : Fin n) : Option α :=
  listAtNat? xs i.val

def optionToList {α : Type} : Option α → List α
  | none => []
  | some x => [x]

def actionTag : CutAction → ℕ
  | .bridge => 0
  | .absorb => 1
  | .split => 2

def actionOfTag : ℕ → CutAction
  | 0 => .bridge
  | 1 => .absorb
  | _ => .split

def coupledTag : CoupledCase → ℕ
  | .unitHeavy => 0
  | .heavyUnit => 1
  | .unitUnit => 2
  | .reverseUnitUnit => 3

def coupledOfTag : ℕ → CoupledCase
  | 0 => .unitHeavy
  | 1 => .heavyUnit
  | 2 => .unitUnit
  | _ => .reverseUnitUnit

def atomKindTag : AtomKind → ℕ
  | .heavyPos => 0
  | .heavyNeg => 1
  | .unitPos => 2
  | .unitNeg => 3

def atomKindOfTag : ℕ → AtomKind
  | 0 => .heavyPos
  | 1 => .heavyNeg
  | 2 => .unitPos
  | _ => .unitNeg

def markedKind? (atoms : List SourceAtom) (index : ℕ) : Option AtomKind :=
  (listAtNat? atoms index).map SourceAtom.kind

def markedKindTag (atoms : List SourceAtom) (index : ℕ) : ℕ :=
  (markedKind? atoms index).map atomKindTag |>.getD 2

def markedHeavyMagnitudes (s : MarkedSource q) : List ℕ :=
  let atoms := s.word.atoms
  let one (i : ℕ) :=
    match listAtNat? atoms i with
    | some a => optionToList (SourceAtom.heavyMagnitude? a)
    | none => []
  match s.mark with
  | .one i => one i
  | .two i j => one i ++ one j

def sourceTagIndex (s : MarkedSource q) : ℕ :=
  let atoms := s.word.atoms
  let modeCode := match s.mark with | .one _ => 0 | .two _ _ => 1
  let firstIndex := match s.mark with | .one i => i | .two i _ => i
  let secondIndex := match s.mark with | .one _ => 0 | .two _ j => j
  let kindCode := markedKindTag atoms firstIndex + 4 * markedKindTag atoms secondIndex
  let cutCode := actionTag s.cuts.leftAction +
    3 * (actionTag s.cuts.middleAction +
      3 * (actionTag s.cuts.rightAction + 3 * actionTag s.cuts.outerAction))
  let emptyCode := (if s.cuts.empty.left then 1 else 0) +
    2 * (if s.cuts.empty.middle then 1 else 0) +
    4 * (if s.cuts.empty.right then 1 else 0)
  let coupledCode := coupledTag s.cuts.coupled
  modeCode + 2 * (kindCode + 16 * (cutCode + 81 * (emptyCode + 8 * coupledCode)))

def paperTagOfSource (s : MarkedSource q) : PaperTag :=
  ⟨sourceTagIndex s % 82944, Nat.mod_lt _ (by norm_num)⟩

def sourceEncode {q : ℕ} (s : MarkedSource q) : PaperCode q :=
  { tag := paperTagOfSource s
    cores := listAt? s.cores
    auxiliaries := s.cuts.auxiliaries
    heavyMagnitudes := listAt? (markedHeavyMagnitudes s) }

def collect3 {α : Type} (f : Fin 3 → Option α) : List α :=
  optionToList (f ⟨0, by omega⟩) ++
    optionToList (f ⟨1, by omega⟩) ++
    optionToList (f ⟨2, by omega⟩)

def collect2 {α : Type} (f : Fin 2 → Option α) : List α :=
  optionToList (f ⟨0, by omega⟩) ++ optionToList (f ⟨1, by omega⟩)

def sourceDecode {q : ℕ} (c : PaperCode q) : Option (MarkedSource q) :=
  let cores := collect3 c.cores
  let atoms := cores.flatMap Core.body
  let checks := balancedRangeData q atoms
  let modeIsTwo := c.tag.val % 2 = 1
  let mark := if modeIsTwo then MarkChoice.two 0 1 else MarkChoice.one 0
  let cutDigit := c.tag.val / 2
  let emptyDigit := cutDigit / 81
  let cuts : CutData :=
    { leftAction := actionOfTag (cutDigit % 3)
      middleAction := actionOfTag ((cutDigit / 3) % 3)
      rightAction := actionOfTag ((cutDigit / 9) % 3)
      outerAction := actionOfTag ((cutDigit / 27) % 3)
      empty :=
        { left := emptyDigit % 2 = 1
          middle := (emptyDigit / 2) % 2 = 1
          right := (emptyDigit / 4) % 2 = 1 }
      coupled := coupledOfTag ((emptyDigit / 8) % 4)
      auxiliaries := c.auxiliaries }
  some
    { word := { atoms := atoms, checks := checks }
      mark := mark
      cuts := cuts
      cores := cores }

def codeGain {q : ℕ} (c : PaperCode q) : ℕ :=
  1 + (Finset.univ.sum fun i => c.auxiliaries i) +
    (Finset.univ.sum fun i => (c.heavyMagnitudes i).getD 0)

/-! ## Local FALSE-AS-STATED witnesses -/

def zeroEmptyFlags : EmptyCoreFlags :=
  { left := false, middle := false, right := false }

def zeroCutData : CutData :=
  { leftAction := .bridge
    middleAction := .bridge
    rightAction := .bridge
    outerAction := .bridge
    empty := zeroEmptyFlags
    coupled := .unitUnit
    auxiliaries := fun _ => 0 }

def collisionAtoms : List SourceAtom :=
  [.unitPos 1, .unitNeg 1, .unitPos 1]

def collisionLeft : MarkedSource 3 :=
  { word :=
      { atoms := collisionAtoms
        checks := balancedRangeData 3 collisionAtoms }
    mark := .one 0
    cuts := zeroCutData
    cores := [] }

def collisionRight : MarkedSource 3 :=
  { word :=
      { atoms := collisionAtoms
        checks := balancedRangeData 3 collisionAtoms }
    mark := .one 2
    cuts := zeroCutData
    cores := [] }

theorem balanced_word_valid_rejects_nonmaximal :
    ¬ BalancedWord.Valid
      ({ atoms := [.unitPos 1, .unitPos 1]
         checks := { rangeOK := true, maximalRunsOK := true } } : BalancedWord 3) := by
  norm_num [BalancedWord.Valid, balancedRangeData, maximalRunOK, sameUnitSign]

theorem source_encode_collision :
    sourceEncode collisionLeft = sourceEncode collisionRight := by
  rfl

theorem collision_sources_valid :
    MarkedSource.Valid collisionLeft ∧ MarkedSource.Valid collisionRight := by
  norm_num [MarkedSource.Valid, BalancedWord.Valid, balancedRangeData,
    maximalRunOK, sameUnitSign, SourceAtom.rangeOK, MarkChoice.Valid,
    collisionLeft, collisionRight,
    collisionAtoms, zeroCutData, zeroEmptyFlags, Core.Valid]

theorem source_decode_mark_counterexample :
    sourceDecode (sourceEncode collisionRight) ≠ some collisionRight := by
  native_decide

theorem source_collision_sources_ne : collisionLeft ≠ collisionRight := by
  decide

/- The requested injectivity target is FALSE AS STATED: equal-kind marks at
distinct indices receive the same finite tag and the same bounded payload. -/
theorem source_encode_injective_false :
    ¬ Function.Injective (@sourceEncode 3) := by
  intro h
  exact source_collision_sources_ne (h source_encode_collision)

def invalidCore : Core :=
  { body := [.heavyPos 1], leftUnitRun := 0, rightUnitRun := 0 }

def invalidSource : MarkedSource 3 :=
  { word :=
      { atoms := [.unitPos 1]
        checks := balancedRangeData 3 [.unitPos 1] }
    mark := .one 0
    cuts := zeroCutData
    cores := [invalidCore] }

/- The requested validity target is FALSE AS STATED because it quantifies over
raw sources: this source contains a heavy core magnitude outside the range. -/
theorem source_encode_valid_false :
    ∃ s : MarkedSource 3, ¬ PaperCode.Valid 3 (sourceEncode s) := by
  refine ⟨invalidSource, ?_⟩
  intro h
  have hcore : Core.Valid 3 invalidCore :=
    h.1 ⟨0, by omega⟩ invalidCore (by rfl)
  norm_num [Core.Valid, invalidCore, SourceAtom.rangeOK] at hcore

/- The decoder is total on the executable format, which is the weakest
machine-checked replacement available before the paper branch map is extracted.
It is not a source round-trip theorem. -/
theorem source_decode_total {q : ℕ} (s : MarkedSource q) :
    ∃ t, sourceDecode (sourceEncode s) = some t := by
  simp [sourceDecode]

theorem source_codeGain_pos {q : ℕ} (s : MarkedSource q) :
    1 ≤ codeGain (sourceEncode s) := by
  unfold codeGain
  omega

theorem paperTag_card :
    Fintype.card PaperTag = 82944 := by
  simp [PaperTag]

theorem paperTag_card_lt :
    Fintype.card PaperTag < 2^20 := by
  norm_num [PaperTag]

end RateCoreVI
