---
GOAL: Implement the accessible local JSON API and browser UI for the frozen CoprimeBatch core API.
ROLE: mechanical product builder
SCOPE: projects/prime-step-breakthrough/src/coprimebatch/web.py and projects/prime-step-breakthrough/web/{index.html,app.js,styles.css}
INPUTS: RESEARCH_SPEC.md and briefs/core_builder.md
NO_TOUCH: all other files
DELIVERABLE: standard-library HTTP server plus keyboard-accessible single-page interface
VERIFY: server starts on requested host/port; GET /api/health, POST /api/certificate, /api/optimize, /api/shift return JSON; static UI loads; malformed requests return 4xx JSON
DONE: exact fixed benchmark appears in UI, out-of-class uniform-grid warning is prominent, ARIA-live results work, no external CDN/dependency, no prohibited path changed
---

Use `ThreadingHTTPServer`; bind to 127.0.0.1 by default.  The UI needs three
panels: portfolio certificate, optimizer, and prime-shift moments.  It must
display input constraints, selected denominators, point count, energy, WCE,
baseline ratios, factorisation time, and limitations.  Never say "optimal"
for greedy output.  Include a visible warning: if arbitrary 1D nodes are
allowed, use a uniform or established quadrature rule instead.
