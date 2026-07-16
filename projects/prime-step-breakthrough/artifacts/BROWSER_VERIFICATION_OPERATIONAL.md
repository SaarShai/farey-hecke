# Operational Prefix Balance Browser Verification

Date: 2026-07-16 (America/Los_Angeles)

Surface: Codex in-app browser against the real local server at
`http://127.0.0.1:8765/`.  The server used the live `coprimebatch.web` module;
interactions used the rendered controls, keyboard text entry, native select
changes, and button clicks.

## Verified paths

| Path | Browser observation |
|---|---|
| Generic categorical counts `A=2`, `B=3` | Complete; scope `unconstrained_categorical`; `U=L=2/5`; ratio `1`; 5 output positions; digest `27ba10d5012f31413652c224027a4f955971f43f7ec16f902bfb6594875f1572` |
| Rendering preset | Complete; 4,096 positions; `U=475/512`; progressive-prefix/final-accuracy limitation visible |
| Finance preset | Complete; 65,536 positions; `U=2047/2048`; all three server-provided model-risk/integration limitations plus the browser warning visible |
| Laboratory preset | Complete; 512 positions; `U=511/512`; protocol/clinical limitation visible |
| Exact rational-vector problem | Complete; scope `exact_constrained_v1`; exact optimum; `U=L=1/6`; additive gap zero; order `g1,g2,g3` |
| Constrained forced-suffix regression | Complete; scope `constrained_a_posteriori`; forced suffix entry state included; `U=L=1`; additive gap zero; optimum proved by closed bounds; order `a,b` |
| Compact constrained categorical flow | Complete after keyboard entry of counts plus block, prefix, suffix, and precedence JSON; all four constraint classes verified; scope `constrained_categorical_a_posteriori`; primary-`B` optimum explicitly **not** proved; `U=3/4`, `L=5/8`, gap `1/8`, ratio `6/5`; ranked order `A#1,B#1,C#1,A#2,B#2,A#3,C#2,B#3`; digest `5c350396396e30b02d818ab2f68233aba7c7a43fb2ad5d27f82f1cb7448c7704` |
| Malformed problem JSON | Rendered a concise input error without sending a request; a following valid exact request recovered successfully |
| Malformed compact block JSON | Rendered `Prefix Balance input is invalid` and an `Input error`; restoring valid JSON and clicking again recovered the same ranked order and digest |
| Original supplied-gap workflow | Complete after the new panel was added; exact fraction JSON rendered |

## Visual and runtime checks

- The wide certificate panel rendered without overlap at the active desktop
  viewport; the scope cards, bounds, digest, limitations, and raw-response
  disclosure were legible.
- A dedicated viewport screenshot of the final compact certificate confirmed
  that feasibility, comparison set, the `Primary B optimum proved` label,
  bounds, ranked preview, digest, and exactly two nonduplicated limitations fit
  inside the result panel.
- Short previews do not display a false trailing ellipsis; long responses use
  bounded head/tail previews.
- Result-specific application limitations reach the rendered list from the
  canonical server preset metadata.
- Focusable form controls, status announcements, busy state, and result focus
  were exercised through the rendered UI.
- `node --check web/app.js` passed in the full verifier, and the final click,
  malformed-input, and recovery sequence exposed no browser runtime error.

This verifies software interaction and claim display.  It is not evidence of a
renderer, finance engine, laboratory system, savings, or downstream accuracy.
