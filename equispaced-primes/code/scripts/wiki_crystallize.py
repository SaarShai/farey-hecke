#!/usr/bin/env python3
"""
wiki_crystallize.py — Convert an experiment result file into a wiki digest draft.

Reads a markdown experiment result (typically from experiments/M1_*.md or
experiments/M5_*.md) and emits a draft wiki page with provisional frontmatter.

The draft goes to wiki/_drafts/ by default (user reviews, promotes, and moves
into wiki/ once curated). Human-in-the-loop by design — script is a filer,
not an autonomous writer.

Usage:
    python3 wiki_crystallize.py experiments/M1_FOO.md
    python3 wiki_crystallize.py experiments/M1_FOO.md --type conjecture --confidence 0.60
    python3 wiki_crystallize.py experiments/M1_FOO.md --out /tmp/foo.md
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from textwrap import shorten

DEFAULT_DRAFT_DIR = Path.home() / "Documents/Spark Obsidian Beast/Farey Research/wiki/_drafts"

SECTION_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)
NUMBER_RE = re.compile(r"[-+]?\d+\.\d+|[-+]?\d+")


def extract_title(text: str, fallback: str) -> str:
    """First H1 or the fallback filename stem."""
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return fallback.replace("_", " ").title()


def extract_sections(text: str) -> dict[str, str]:
    """Split body by headings, return dict of section -> content."""
    matches = list(SECTION_RE.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1).strip().lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[name] = text[start:end].strip()
    return out


def find_section(sections: dict[str, str], keywords: list[str]) -> str:
    for key, body in sections.items():
        for kw in keywords:
            if kw in key:
                return body
    return ""


def first_sentences(body: str, n: int = 3) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", body.strip())
    return " ".join(sentences[:n])


def detect_status(text: str) -> str:
    low = text.lower()
    if "cannot execute" in low or "unable to run" in low:
        return "open"
    if "disproved" in low or "counterexample" in low:
        return "disproved"
    if "rigorous" in low and "proof" in low:
        return "proved"
    if "computational" in low or "numerically verified" in low:
        return "computational"
    if "conjecture" in low:
        return "conjectural"
    return "computational"


def detect_confidence(status: str, text: str) -> float:
    # Heuristic default; human adjusts in review.
    low = text.lower()
    if status == "proved":
        return 0.75
    if status == "disproved":
        return 0.00
    if status == "open":
        return 0.20
    if "k=10" in low or "n=10" in low:
        return 0.55
    return 0.40


def pick_type(text: str, override: str | None) -> str:
    if override:
        return override
    low = text.lower()
    if "theorem" in low and "proved" in low:
        return "theorem"
    if "conjecture" in low:
        return "conjecture"
    if "method" in low or "algorithm" in low:
        return "method"
    return "discovery"


def slugify(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    return name[:60] or "untitled"


def build_draft(
    src: Path,
    out: Path,
    title: str,
    type_: str,
    status: str,
    confidence: float,
    sections: dict[str, str],
    full_text: str,
) -> str:
    today = date.today().isoformat()

    # Pull candidate content for each digest section.
    summary_src = find_section(sections, ["summary", "conclusion", "abstract"]) or full_text
    findings_src = find_section(sections, ["finding", "result", "numerical", "data"])
    method_src = find_section(sections, ["method", "approach", "computation"])
    open_src = find_section(sections, ["open", "next", "todo", "limitation"])

    summary = first_sentences(summary_src, 4)
    findings = shorten(findings_src, width=1200, placeholder=" …") if findings_src else ""
    method = shorten(method_src, width=600, placeholder=" …") if method_src else ""
    open_issues = shorten(open_src, width=600, placeholder=" …") if open_src else ""

    # Count numeric hits as a rough "evidence density" signal.
    n_numbers = len(NUMBER_RE.findall(full_text))

    frontmatter = (
        "---\n"
        f"type: {type_}\n"
        f"status: {status}\n"
        f"confidence: {confidence:.2f}\n"
        f"sources: 1\n"
        f"last_verified: {today}\n"
        "decay_rate: normal\n"
        "supersedes: []\n"
        "superseded_by: null\n"
        "depends_on: []\n"
        "novelty: our_extension\n"
        "priority: medium\n"
        f"crystallized_from: {src.name}\n"
        "draft: true\n"
        "---\n\n"
    )

    body = (
        f"# {title}\n\n"
        "> **Draft** — crystallized from experiment result. Review, adjust "
        "confidence, link to related pages, then move from `_drafts/` to `wiki/`.\n\n"
        "## Summary\n"
        f"{summary or '(fill in)'}\n\n"
        "## Method\n"
        f"{method or '(fill in)'}\n\n"
        "## Findings\n"
        f"{findings or '(fill in)'}\n\n"
        "## Open issues / next steps\n"
        f"{open_issues or '(fill in)'}\n\n"
        "## Evidence\n"
        f"- Source file: `{src}`\n"
        f"- Numeric data points detected: {n_numbers}\n"
        "- Cross-checked by: _(fill in: which other models / runs)_\n\n"
        "## Related\n"
        "- _(wikilinks to related pages)_\n"
    )

    return frontmatter + body


def main() -> int:
    ap = argparse.ArgumentParser(description="Crystallize an experiment result into a wiki draft.")
    ap.add_argument("source", type=Path, help="path to experiment result markdown")
    ap.add_argument("--out", type=Path, default=None, help="output path (default: drafts dir)")
    ap.add_argument("--type", dest="type_", default=None, help="override type")
    ap.add_argument("--status", default=None, help="override status")
    ap.add_argument("--confidence", type=float, default=None, help="override confidence")
    ap.add_argument("--title", default=None, help="override title")
    ap.add_argument("--draft-dir", type=Path, default=DEFAULT_DRAFT_DIR)
    args = ap.parse_args()

    if not args.source.exists():
        print(f"error: source not found: {args.source}", file=sys.stderr)
        return 2

    text = args.source.read_text(encoding="utf-8", errors="replace")
    sections = extract_sections(text)

    title = args.title or extract_title(text, args.source.stem)
    status = args.status or detect_status(text)
    type_ = pick_type(text, args.type_)
    confidence = args.confidence if args.confidence is not None else detect_confidence(status, text)

    out = args.out
    if out is None:
        args.draft_dir.mkdir(parents=True, exist_ok=True)
        out = args.draft_dir / f"{slugify(title)}.md"

    draft = build_draft(args.source, out, title, type_, status, confidence, sections, text)
    out.write_text(draft, encoding="utf-8")
    print(f"wrote draft: {out}")
    print(f"  title: {title}")
    print(f"  type: {type_}  status: {status}  confidence: {confidence:.2f}")
    print("review, link, then move into wiki/ when ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
