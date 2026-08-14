# Distribution options for the certified resonance stack

Owner decision required. This memo presents three neutral options; it makes
no distribution decision.

| Option | Outline | Rough effort | Primary audience | Checks before any public release |
|---|---|---:|---|---|
| **A — Public reproducibility package** | Publish a GitHub repository containing branch aletheia-stack, the receipts, and REPRODUCE.md; mint a Zenodo DOI so the package is immediately citable. | 1–3 days | Independent computational researchers, referees, and readers who need the code and receipts now. | Fresh independent re-run on a second machine; choose and add an explicit license; complete the pending winding-certification upgrade for the q=4 and q=6 pins. Also confirm that the absolute q=4/q=6 receipt path is portable or document the release procedure. |
| **B — Package plus short note** | Option A plus a short Experimental Mathematics-style note framing and testing the arithmeticity-signature law. | 1–3 weeks | The reproducibility audience plus computational-number-theory readers and journal reviewers. | All Option A checks; separately audit the note's claim scope against the receipts, state the q=4/q=6 winding-certification status, and obtain the required author/editorial approvals before public submission or release. |
| **C — Private collaboration-first share** | Share the pinned branch, receipts, and reproduction instructions privately with the Koyama collaboration before deciding on a public release. | 1–3 days for a controlled handoff, plus collaboration time | Koyama collaborators and the immediate research team. | Before a later public release, complete the same second-machine independent re-run, license choice, and pending q=4/q=6 winding-certification upgrade; also settle collaboration permissions, attribution, and any embargo or pre-publication constraints. |

The common technical gate is deliberate: the q=4 and q=6 results currently have
certified-Arb midpoint/Newton and finite-N stability evidence, but the
winding-certification upgrade is still pending. The owner can choose whether
that gate is a prerequisite for private sharing, public code/receipt release,
or both.

