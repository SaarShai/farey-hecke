# Joint spectral-section insertion package

`section.tex` is the insertion-ready manuscript fragment.  It assumes the host preamble
provides `amsmath`, `amssymb`, `amsthm`, `booktabs`, and `graphicx`, defines the
`compresult` theorem environment, and defines `\spectralfigurepath` to point to the
spectral reconstruction figure.

`preview.tex` is a self-contained wrapper used only to compile and inspect the fragment.
It references the verified 1800-by-2475 PNG figure in
`projects/minus1-dominance/spectral_transients_3e14/output/` rather than copying or
altering the spectral package.  This avoids the unembedded Helvetica fonts in the current
R-generated vector PDF.  Before submission, either retain the PNG at adequate final
resolution or re-export the vector figure with all fonts embedded.

Compile from this directory with:

```sh
/Users/za/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/latex/bin/tectonic preview.tex
```

Before insertion into Koyama's manuscript:

1. reconcile theorem-environment names and equation numbering with the host preamble;
2. replace the provisional data-archive sentence with a DOI;
3. add the manuscript's bibliography citations for the standard prime-race explicit formula;
4. preserve the ordinary-count versus regularized-statistic scope distinction;
5. obtain both authors' approval of the final prose, figures, and contribution statement.

An optional disclosure paragraph, required if the reported AI assistance is retained in the
submission workflow, is provided in
`../../koyama/pre_reply_2026-08-01/11_AI_AND_COMPUTATIONAL_ASSISTANCE_DISCLOSURE.md`.
