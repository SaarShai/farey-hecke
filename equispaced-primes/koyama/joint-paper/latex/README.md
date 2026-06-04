# LaTeX bundle — §X technical/computational section

This folder contains the LaTeX source for the technical/computational
section (§X) of the joint paper, converted from the markdown source
in the parent folder.

## Files

| File | Purpose |
|---|---|
| `paper.tex` | Minimal driver: preamble, theorem environments, `\input`s the three subfiles, runs the bibliography. Designed for stand-alone compilation while the host paper structure is being assembled. |
| `section_X.tex` | The §X main section (text). |
| `appendix_A.tex` | Appendix A — proof of Theorem X.4.1 ($B_\infty$ identity). |
| `appendix_B.tex` | Appendix B — proof of Theorem X.4.2 ($c_K$ leading + subleading identity). |
| `references.bib` | BibTeX bibliography (18 external references: 11 cited in §X.3–§X.7 + appendices, and 7 classical-context entries for the Introduction). |
| `clean.py` | Conversion script: regenerates `section_X.tex` / `appendix_*.tex` from the markdown source via pandoc + post-cleanup. Idempotent. |

## Build

The recommended driver is **tectonic** (a single-binary, self-contained
LaTeX engine that pulls packages on demand). Build with:

```bash
tectonic paper.tex
```

For a standard TeX Live install:

```bash
pdflatex paper && biber paper && pdflatex paper && pdflatex paper
```

(or `latexmk -pdf paper`). Note that the bibliography uses
`biblatex` with the `bibtex` backend; if your distribution has only
the older `bibtex` binary, the bibliography will still build.

## Regenerate from markdown

If the markdown source in `..` is edited, regenerate with:

```bash
pandoc --from markdown --to latex --wrap=preserve ../SECTION_DRAFT_2026-05-12.md     -o section_raw.tex
pandoc --from markdown --to latex --wrap=preserve ../APPENDIX_A_BINFTY_PROOF.md      -o appendix_A_raw.tex
pandoc --from markdown --to latex --wrap=preserve ../APPENDIX_B_CK_SUBLEADING_PROOF.md -o appendix_B_raw.tex
python3 clean.py
rm section_raw.tex appendix_A_raw.tex appendix_B_raw.tex
```

## Conventions for integration

- Section / lemma / theorem / equation tags (`X.3.1`, `X.4.1`, `eq:Binfty`,
  `eq:cK`, `(AK)`, `(SP-L)`, `(NDC)`) are placeholders; the host paper
  will renumber on integration.
- Theorem statements are currently set as bolded paragraphs
  (`\textbf{Theorem X.4.1.}` … in italic prose) rather than as proper
  `\begin{theorem}…\end{theorem}` environments. The host-paper
  structure can wrap them into the preferred environment.
- The §X-level "References" list at the end of `section_X.tex` is a
  human-readable summary with per-citation roles in the paper; the
  authoritative bibliography is `references.bib` rendered via
  `\printbibliography` in `paper.tex`. On integration these can be
  consolidated.

## Known cosmetic notes

- Pandoc renders markdown tables as `longtable`; `paper.tex` loads
  `longtable`. For final typesetting, some tables may be better as
  `tabular`/`booktabs` — easy mechanical conversion.
- Pandoc uses `\(...\)` for inline math; both `\(...\)` and `$...$`
  are valid LaTeX.
- The blockquote for the Aoki–Koyama eq.\ (1.4) verbatim quote in
  §X.4.3 is rendered as `\begin{quote}…\end{quote}`; cleaner styling
  (e.g.\ a `displayquote` or a numbered display) is a one-line tweak.
