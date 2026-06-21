# How to verify `LblkWindow.lean`

The genuine chain builds ONLY inside the inner subproject
`projects/aristotle_dispatch_v15/uniform_q5to18/`.  `LblkWindow.lean` imports that chain,
so it is verified there (NOT self-contained `lake env lean`-able — it must import
`GenuineClassDischarge`, `ToplevelStitchGen`, `L1bArcCoverage`, `OnsetEquality`).

## Steps (what was run, EXIT 0, all results axiom-clean)

    cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18
    cp /Users/za/Documents/farey-hecke/projects/lblk_window_lean/LblkWindow.lean ./LblkWindow.lean
    # append a [[lean_lib]] glob to lakefile.toml:
    #   [[lean_lib]]
    #   name = "LblkWindow"
    #   globs = ["LblkWindow"]
    ~/.elan/bin/lake build LblkWindow
    # then restore lakefile.toml and remove ./LblkWindow.lean + .lake/build/lib/lean/LblkWindow.*

`#print axioms` for every result printed `[propext, Classical.choice, Quot.sound]`
(sorryAx GONE).  Build: `Build completed successfully (8052 jobs).`
