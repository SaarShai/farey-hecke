#!/usr/bin/env python3
"""Build the LaTeX section + appendices from the markdown source.

Pipeline:
  1. Read each markdown source.
  2. Preprocess: convert LaTeX-style `\\[ ... \\]` display-math blocks
     to `$$ ... $$`.
  3. Pipe through pandoc to LaTeX.
  4. Post-process: strip pandoc auto-labels, drop horizontal-rule
     artefacts, fix section titles, fix encoding issues, etc.

Idempotent.
"""
from __future__ import annotations
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent
PANDOC = "/Users/za/miniforge3/bin/pandoc"


def preprocess_markdown(md: str) -> str:
    md = re.sub(r"^\\\[[ \t]*\n", "$$\n", md, flags=re.MULTILINE)
    md = re.sub(r"^\\\][ \t]*\n", "$$\n\n", md, flags=re.MULTILINE)
    return md


def run_pandoc(md: str) -> str:
    return subprocess.run(
        [PANDOC, "--from", "markdown", "--to", "latex", "--wrap=preserve"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout


def _match_brace_group(s, i):
    """Given s[i] == '{', return j such that s[i:j+1] is the balanced group."""
    assert s[i] == "{"
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return -1


def _unwrap_texorpdfstring_and_strip_label(text):
    """Brace-balanced replacement of:
        \section{\texorpdfstring{A}{B}}\label{...}    →  \section{A}
        \section{\texorpdfstring{A}{B}}               →  \section{A}
        \section{A}\label{...}                         →  \section{A}
       and similarly for subsection / subsubsection / paragraph.
    """
    out = []
    i = 0
    cmds = ("section", "subsection", "subsubsection", "paragraph")
    while i < len(text):
        m = re.match(r"\\(" + "|".join(cmds) + r")\{", text[i:])
        if not m:
            out.append(text[i])
            i += 1
            continue
        cmd = m.group(1)
        arg_start = i + m.end() - 1  # index of the opening brace
        arg_end = _match_brace_group(text, arg_start)
        if arg_end < 0:
            out.append(text[i])
            i += 1
            continue
        arg = text[arg_start + 1 : arg_end]
        # If arg is \texorpdfstring{A}{B}, replace with just A.
        tps = re.match(r"\\texorpdfstring\{", arg)
        if tps:
            a_start = tps.end() - 1
            a_end = _match_brace_group(arg, a_start)
            if a_end > 0:
                # Now skip past the second argument {B}.
                rest = arg[a_end + 1 :]
                b_match = re.match(r"\{", rest)
                if b_match:
                    arg = arg[a_start + 1 : a_end]
        new_segment = f"\\{cmd}{{{arg}}}"
        # Look ahead for \label{...} immediately after, and drop it.
        after = arg_end + 1
        label_m = re.match(r"\\label\{[^}]*\}", text[after:])
        if label_m:
            after += label_m.end()
        out.append(new_segment)
        i = after
    return "".join(out)


def _three_col_table_to_description(m):
    """Convert pandoc's 3-column longtable to a `description` list.

    Cells are separated by ` & `; rows by ` \\\\` followed by newline.
    Pandoc wraps the headers in \begin{minipage}... but the body rows
    are plain `cellA & cellB & cellC \\`.
    """
    header_block, body_block = m.group(1), m.group(2)
    rows = re.split(r"\s*\\\\\n", body_block.strip())
    out = [r"\begin{description}[leftmargin=1em, style=nextline]"]
    for row in rows:
        if not row.strip():
            continue
        parts = [p.strip() for p in re.split(r"\s+&\s+", row)]
        if len(parts) != 3:
            # Cell text contains a stray ` & `? Fall back to longtable row.
            return m.group(0)
        paper_object, lean_file, status = parts
        out.append(
            r"\item[\textnormal{" + paper_object + r"} \quad "
            r"\texttt{" + lean_file + r"}] " + status
        )
    out.append(r"\end{description}")
    return "\n".join(out)


def postprocess_latex(text: str, kind: str) -> str:
    # 1. Strip pandoc auto-labels and unwrap \texorpdfstring{A}{B} -> A
    #    in section/subsection/subsubsection titles. Inner braces may
    #    occur in the math arg (e.g. K\^{}w), so we do a brace-balanced
    #    scan rather than regex-with-[^}]*.
    text = _unwrap_texorpdfstring_and_strip_label(text)

    # 2. Strip "X.N ", "X.N.M ", "A.N ", "B.N ", "A.N.M ", "B.N.M "
    #    prefixes from section/subsection/subsubsection titles so they
    #    don't duplicate amsart's auto-numbering.
    text = re.sub(r"\\section\{§X\. ", r"\\section{", text)
    text = re.sub(r"\\subsection\{X\.\d+ ", r"\\subsection{", text)
    text = re.sub(r"\\subsubsection\{X\.\d+\.\d+ ", r"\\subsubsection{", text)
    text = re.sub(r"\\subsection\{[AB]\.\d+ ", r"\\subsection{", text)
    text = re.sub(r"\\subsubsection\{[AB]\.\d+\.\d+ ", r"\\subsubsection{", text)
    text = re.sub(
        r"\\begin\{center\}\\rule\{[^}]*\}\{[^}]*\}\\end\{center\}\n*", "", text,
    )
    if kind == "appendix-A":
        text = re.sub(
            r"\\section\{Appendix A[^}]*\}",
            r"\\section{Full proof of Theorem X.4.1 ($B_\\infty$ identity)}",
            text,
        )
    elif kind == "appendix-B":
        text = re.sub(
            r"\\section\{Appendix B[^}]*\}",
            r"\\section{Full proof of Theorem X.4.2 ($c_K$ leading + subleading identity)}",
            text,
        )
    text = text.replace("\\tightlist\n", "")

    # § → \S\, : T1 fontenc maps 0xA7 to ğ; use the textcomp macro.
    text = text.replace("§", "\\S\\,")

    # Unicode safety net. The markdown sources write all *math* with
    # LaTeX commands inside $...$ (e.g. \approx, \le), so any literal
    # Unicode math glyph surviving in the pandoc output is necessarily
    # in *text* mode, where the T1/lmodern fonts have no glyph and TeX
    # emits "Missing character" (a silent rendering defect in the PDF).
    # Map the dangerous text-mode glyphs to robust LaTeX. Idempotent:
    # re-running on already-clean LaTeX is a no-op (none of these
    # glyphs occur in valid generated LaTeX).
    _uni = {
        "≈": r"$\approx$", "≤": r"$\le$", "≥": r"$\ge$",
        "≠": r"$\ne$", "∼": r"$\sim$", "×": r"$\times$",
        "∞": r"$\infty$", "→": r"$\to$", "⇒": r"$\Rightarrow$",
        "−": r"$-$", "±": r"$\pm$", "∈": r"$\in$", "∉": r"$\notin$",
        "⋅": r"$\cdot$", "∣": r"$\mid$", "∤": r"$\nmid$",
        "⩽": r"$\le$", "⩾": r"$\ge$", "≅": r"$\cong$",
        "…": r"\dots{}", "⋯": r"$\cdots$", "∅": r"$\emptyset$",
        "≪": r"$\ll$", "≫": r"$\gg$", "∘": r"$\circ$",
        "⟶": r"$\longrightarrow$", "↦": r"$\mapsto$",
    }
    for _g, _r in _uni.items():
        text = text.replace(_g, _r)

    # Pandoc emits \#\#\# Header when a level-3 heading follows display
    # math with no blank line. Recover as a \subsubsection.
    def _subsub(m):
        title = m.group(1)
        title = re.sub(r"^X\.\d+\.\d+ ", "", title)
        title = re.sub(r"^[AB]\.\d+\.\d+ ", "", title)
        return r"\subsubsection{" + title + r"}"
    text = re.sub(r"^\\#\\#\\# ([^\n]+)$", _subsub, text, flags=re.MULTILINE)

    # Broken cross-reference: eq:W2 referenced the OLS regression we
    # removed when compressing §X.5.5. Replace with textual cue.
    text = text.replace(
        r"(\ref{eq:W2})",
        r"(the rank-vs-$\log N$ regression of \S\,X.5.5)",
    )

    # Citation substitutions: convert in-text author-year mentions into
    # \cite{...} calls so the BibTeX bibliography renders.
    #
    # Order matters: longest / most specific patterns first so we don't
    # double-cite.
    cite_patterns = [
        # Aoki--Koyama 2023, eq. (1.4) p. 235
        (r"Aoki--Koyama \(2023, \\emph\{J\. Number Theory\} \\textbf\{245\}, eq\. \(1\.4\), p\.[~ ]?235\)",
         r"Aoki--Koyama~\\cite[eq.~(1.4), p.~235]{AokiKoyama2023}"),
        (r"Aoki--Koyama \(2023, Proposition 2\.1, p\.[~ ]?244\)",
         r"Aoki--Koyama~\\cite[Proposition~2.1, p.~244]{AokiKoyama2023}"),
        (r"Aoki--Koyama \(2023\)", r"Aoki--Koyama~\\cite{AokiKoyama2023}"),
        # Bare "Aoki--Koyama 2023" (no parenthesised year), e.g. in
        # table cells: "(AK) cited (Aoki--Koyama 2023)". Must run
        # after the parenthesised forms above so it doesn't pre-empt
        # them.
        (r"Aoki--Koyama 2023\b", r"Aoki--Koyama~\\cite{AokiKoyama2023}"),
        # Akatsuka (2017), Kodai Math. J. 40, 79-101 -- Lemma 2.1 / eq.(2.5).
        # (The cited paper is the 2017 Kodai paper; there is NO Akatsuka 2013
        # paper. Bibkey renamed Akatsuka2017EulerProduct 2026-05-16. Both the
        # 2017 phrasings (current .md masters) and any residual legacy "2013"
        # phrasings map to the SAME correct key, so stale prose auto-corrects
        # to the right (2017) bibliography entry.)  Order: specific -> general.
        (r"Akatsuka 2017 \(Kodai Math\. J\. \\textbf\{40\}, 79--101\) Lemma 2\.1 / eq\. \(2\.5\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"Akatsuka \(2017\) Lemma 2\.1 / eq\. \(2\.5\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"Akatsuka 2017, eqs?\. \(2\.5\)",
         r"Akatsuka~\\cite[eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"Akatsuka \(2017\)", r"Akatsuka~\\cite{Akatsuka2017EulerProduct}"),
        (r"\bAkatsuka 2017\b", r"\\cite{Akatsuka2017EulerProduct}"),
        # legacy 2013 phrasings (residual stale prose) -> correct 2017 key
        (r"Akatsuka \(2013, Lemma 2\.1 / eq\. \(2\.5\)\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"Akatsuka \(2013\) Lemma 2\.1 / eq\. \(2\.5\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"Akatsuka 2013 Lemma 2\.1 / eq\. \(2\.5\)",
         r"Akatsuka~\\cite[Lemma~2.1 \\& eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"Akatsuka 2013,? eq\. \(2\.5\)",
         r"Akatsuka~\\cite[eq.~(2.5)]{Akatsuka2017EulerProduct}"),
        (r"\(Akatsuka \(2013\),[^)]*The Euler product[^)]*Lemma 2\.1 and equation \(2\.5\)\)",
         r"(\\cite[Lemma~2.1 \\& eq.~(2.5)]{Akatsuka2017EulerProduct})"),
        (r"Akatsuka \(2013\)", r"Akatsuka~\\cite{Akatsuka2017EulerProduct}"),
        (r"\bAkatsuka 2013\b", r"\\cite{Akatsuka2017EulerProduct}"),
        # Mikolás 1949 (classical Farey--Mertens identity / prior art)
        (r"Mikol[aá]s \(1949(?:/50)?\)", r"Mikol\\'as~\\cite{Mikolas1949}"),
        (r"\bMikol[aá]s 1949\b", r"\\cite{Mikolas1949}"),
        # Inoue 2021
        (r"Inoue \(2021, Theorem 1\)", r"Inoue~\\cite[Theorem~1]{Inoue2021}"),
        (r"Inoue \(2021\) Theorem 1", r"Inoue~\\cite[Theorem~1]{Inoue2021}"),
        (r"\bInoue 2021 Theorem 1\b", r"Inoue~\\cite[Theorem~1]{Inoue2021}"),
        (r"Inoue \(2021\)", r"Inoue~\\cite{Inoue2021}"),
        (r"\bInoue 2021\b", r"\\cite{Inoue2021}"),
        # Soundararajan 2009 Theorem 1
        (r"Soundararajan \(2009\)[^,.]*Theorem 1", r"Soundararajan~\\cite[Theorem~1]{Soundararajan2009}"),
        (r"Soundararajan \(2009\) Theorem 1", r"Soundararajan~\\cite[Theorem~1]{Soundararajan2009}"),
        (r"\bSoundararajan 2009 Theorem 1\b", r"Soundararajan~\\cite[Theorem~1]{Soundararajan2009}"),
        (r"Soundararajan \(2009\)", r"Soundararajan~\\cite{Soundararajan2009}"),
        (r"\bSoundararajan 2009\b", r"\\cite{Soundararajan2009}"),
        # Hardy & Wright
        (r"Hardy(?: \\&|--| and ) ?Wright[^,.]*Theorem 304", r"Hardy--Wright~\\cite[Theorem~304]{HardyWright2008}"),
        (r"Hardy(?: \\&|--| and ) ?Wright Theorem 304", r"Hardy--Wright~\\cite[Theorem~304]{HardyWright2008}"),
        # Pólya 1913
        (r"P\\'olya \(1913\)", r"P\\'olya~\\cite{Polya1913}"),
        (r"Pólya \(1913\)", r"Pólya~\\cite{Polya1913}"),
        (r"\bPólya 1913\b", r"\\cite{Polya1913}"),
        (r"\bP\\'olya 1913\b", r"\\cite{Polya1913}"),
        # Ng 2004
        (r"\bNg 2004\b", r"Ng~\\cite{Ng2004}"),
        (r"Ng \(2004\)", r"Ng~\\cite{Ng2004}"),
        # Titchmarsh §3.11
        (r"Titchmarsh[^,.]*Theorem 3\.11", r"Titchmarsh~\\cite[Theorem~3.11]{Titchmarsh1986RZF}"),
        (r"Titchmarsh[^,.]*\\S\\,3\.11", r"Titchmarsh~\\cite[\\S\\,3.11]{Titchmarsh1986RZF}"),
        # Montgomery--Vaughan Theorem 9.4
        (r"Montgomery--Vaughan[^,.]*Theorem 9\.4(?: / Corollary 9\.5)?",
         r"Montgomery--Vaughan~\\cite[Theorem~9.4]{MontgomeryVaughan2007}"),
        (r"Montgomery--Vaughan Thm 9\.4", r"Montgomery--Vaughan~\\cite[Theorem~9.4]{MontgomeryVaughan2007}"),
        # Tenenbaum
        (r"Tenenbaum,[^,.]*Introduction to Analytic and Probabilistic Number Theory,?\s*Chapter II\.5",
         r"Tenenbaum~\\cite[Chapter~II.5]{Tenenbaum2015}"),
        # Davenport
        (r"Davenport[^,.]*MNT[^,.]*", r"Davenport~\\cite{Davenport2000MultiplicativeNumberTheory}"),
    ]
    for pat, repl in cite_patterns:
        text = re.sub(pat, repl, text)

    # Remove the §X-level "References (section)" block from the main
    # section — the BibTeX-rendered bibliography replaces it.
    if kind == "section":
        text = re.sub(
            r"\\subsection\{References \(section\)\}.*?(?=\\section|\Z)",
            "",
            text, flags=re.DOTALL,
        )

    # Add \hypertarget anchors at theorem / lemma markers so cross-
    # references at integration (or PDF readers' internal links) can
    # jump to them. We anchor the marker, not the whole statement.
    def _anchor(m):
        kind_, num = m.group(1), m.group(2)
        key = f"{kind_.lower()}:X.{num}"
        return r"\hypertarget{" + key + r"}{\textbf{" + kind_ + r" X." + num + r".}}"
    text = re.sub(
        r"\\textbf\{(Lemma|Theorem|Proposition|Corollary) X\.(\d+(?:\.\d+)?)\.\}",
        _anchor, text,
    )

    # (We considered converting the §X.6 3-column file-by-file Lean
    # inventory table to a description list to avoid overflow; the
    # \small rendering plus \sloppy is acceptable for the draft and the
    # complexity of a robust regex isn't worth it. Skip.)

    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


JOBS = [
    ("SECTION_DRAFT_2026-05-12.md", "section_X.tex", "section"),
    ("APPENDIX_A_BINFTY_PROOF.md", "appendix_A.tex", "appendix-A"),
    ("APPENDIX_B_CK_SUBLEADING_PROOF.md", "appendix_B.tex", "appendix-B"),
]

for src, dst, kind in JOBS:
    md = (SRC / src).read_text()
    md = preprocess_markdown(md)
    latex = run_pandoc(md)
    latex = postprocess_latex(latex, kind)
    (HERE / dst).write_text(latex)
    print(f"{src:>38}  →  {dst}  ({len(latex.splitlines())} lines)")
