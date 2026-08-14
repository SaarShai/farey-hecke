# Reproducing the certified resonance stack

Validation record date: **2026-08-14**. The source checkout is the
aletheia-stack branch at commit
4c42ca03266c9214ebbce7a7c41ccac630c2a1ac. The four validation programs
below were recorded as no-argument runs from the checkout's code/ directory.
This documentation pass did not execute them.

## Environment

Validated platform: macOS/arm64.

Create the virtual environment and install the validated package versions:

~~~sh
uv venv /Users/za/.venvs/farey-rh
uv pip install --python /Users/za/.venvs/farey-rh/bin/python \
  "mpmath==1.4.1" "python-flint==0.9.0" "numpy==2.5.2"
~~~

The unpinned package-install form is:

~~~sh
uv pip install mpmath python-flint numpy
~~~

The validated runs use the interpreter at
/Users/za/.venvs/farey-rh/bin/python. PARI/GP 2.17.3 is used by separate
lanes; it is **not required for this certified resonance stack**.

## Validated runs

All four records below were verified on 2026-08-14. Run each command exactly
as shown, with the working directory set to code/.

### (a) q=3 certified enclosures

Argument handling: code/zeta_cert_q3.py defines main() without an argument
parser and accepts no configured options.

~~~sh
cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code
/Users/za/.venvs/farey-rh/bin/python zeta_cert_q3.py
~~~

Expected runtime: **978.6 s**.

Expected verdict line:

~~~text
6/6 enclosures contain published; 6/6 proven Re sign-change; 6/6 dimension-certified; 6/6 strict-interior; max width 1.22e-05
~~~

Receipt named by the validation record: code/out/zeta_cert_q3.json
(relative to the worktree root).

### (b) q=3 versus G_5 resonance geometry

Argument handling: code/run_resonance_geometry.py has no argument parser; its
computation runs at module level and the validated invocation supplies no
arguments.

~~~sh
cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code
/Users/za/.venvs/farey-rh/bin/python run_resonance_geometry.py
~~~

Expected runtime: **1585 s**.

Expected summary:

~~~text
q3 re_std 6.475e-14 vs G5 re_std 0.029986
~~~

Receipt: code/out/resonance_geometry.json (relative to the worktree root).

### (c,d) q=4 and q=6 controls

Argument handling: code/controls_q4q6/run_q4q6_controls.py accepts the
optional --max-scan-seconds argument, whose default is 5400.0. The validated
run used no arguments, so it uses that default and runs the q=3 preflight
followed by q=4 and q=6.

~~~sh
cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code
/Users/za/.venvs/farey-rh/bin/python controls_q4q6/run_q4q6_controls.py
~~~

Expected outputs:

~~~text
q=4: 177.6 s; 3 pins; re_std 9.83e-12
q=6: 410.1 s; 2 pins; re_std 1.03e-11
~~~

Receipt:
/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_b/Q4Q6_CONTROLS_RECEIPT.json.
The wrapper currently uses this absolute project path when writing its
receipt; on another machine, account for that path before running it.

## Receipts inventory

| Receipt path | What it certifies or records | Date |
|---|---|---|
| code/out/zeta_cert_q3.json | Six q=3 published-zero enclosures; all contain the published ordinates, have proven real-part sign changes, are dimension-certified and strict-interior; maximum recorded width is 1.22e-05. | 2026-08-14 |
| code/out/resonance_geometry.json | Eight q=3 even resonances on the Re(s)=1/4 line and eight stable G_5 even resonances; records q3 re_std=6.475169e-14 and G_5 re_std=0.0299861836. | 2026-08-14 |
| /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_b/Q4Q6_CONTROLS_RECEIPT.json | q=4 control: 3 pins, re_std=9.829142e-12, 177.605 s; q=6 control: 2 pins, re_std=1.025589e-11, 410.124 s; both report LINE. | 2026-08-14 |
| code/code/out/zeta_cert_q3.json (observed duplicate, not the named inventory path) | A second q=3 receipt with the same six all-true certification fields and wall_seconds=978.649...; this is the receipt that matches the stated 978.6 s record when the script is run from code/. | 2026-08-14 |

## What the numbers mean

For the arithmetic q=3, q=4, and q=6 surfaces, the even-sector resonances
land on Re(s)=1/4 at the zero ordinates of zeta(2s), producing a near-zero
real-part standard deviation. For the non-arithmetic G_5 control, the
resonances form a scattered cloud in the real direction, with re_std around
0.03. This is the arithmeticity-signature comparison reported by these
lanes, not a standalone proof of a broader claim. The operator conventions
are extracted in
research_notes/MMS_0912.2236_EXTRACTION.txt.

## Discrepancy and portability notes

The named worktree-root receipt code/out/zeta_cert_q3.json exists, but its
current wall_seconds is 735.5440979003906, which disagrees with the validated
runtime 978.6 s. The q=3 script writes the literal relative path
code/out/zeta_cert_q3.json; therefore, running it from the checkout's code/
directory writes to code/code/out/zeta_cert_q3.json. That nested receipt has
wall_seconds=978.6493239402771 and matches the stated runtime. No receipt was
substituted or modified for this document; both paths are listed so an
independent researcher can identify the discrepancy.

