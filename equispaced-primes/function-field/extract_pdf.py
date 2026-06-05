#!/usr/bin/env python3
"""Local citation-verification helper: extract text windows from published-paper PDFs.
Scope: published math papers only (Akatsuka 2017 Kodai 40; Aoki-Koyama 2023 JNT 245).
NOT correspondence. Used only to primary-verify equation statements / conditionality.
"""
import sys, re
from pdfminer.high_level import extract_text

def show(path, page_start, page_end, patterns):
    txt = extract_text(path, page_numbers=list(range(page_start, page_end)))
    txt = re.sub(r'[ \t]+', ' ', txt)
    print(f"\n===== {path}  pages {page_start}-{page_end-1} =====")
    for pat in patterns:
        for m in re.finditer(pat, txt, re.I):
            a = max(0, m.start() - 600)
            b = min(len(txt), m.end() + 1400)
            print(f"\n--- match {pat!r} ---")
            print(txt[a:b].strip())

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "akatsuka":
        # Akatsuka 2017, Kodai Math J 40, 79-101. Theorem 1 / eq (1.5) in intro; Lemma 2.1 / eq (2.5) in section 2.
        show("/Users/za/Downloads/akatsukaDRH3.pdf", 0, 9,
             [r"\(2\.5\)", r"Lemma 2\.1", r"Theorem 1", r"\(1\.5\)", r"unconditional", r"Riemann [Hh]ypothesis", r"\bDRH\b", r"\bRH\b"])
    elif which == "aoki":
        # Aoki-Koyama 2023, JNT 245, 233-262. eq (1.4) ~ p.235 (PDF page ~3).
        show("/Users/za/Downloads/1-s2.0-S0022314X22002335-main.pdf", 0, 6,
             [r"\(1\.4\)", r"\(1\.5\)", r"DRH", r"Deep Riemann", r"e\^?\{?-?\\?gamma", r"Euler", r"unconditional"])
