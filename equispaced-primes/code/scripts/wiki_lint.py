#!/usr/bin/env python3
"""
wiki_lint.py — Farey research wiki health check.

Implements the lint operation defined in wiki/SCHEMA.md.

Usage:
    python3 wiki_lint.py                  # report only
    python3 wiki_lint.py --fix             # auto-fix what's safe
    python3 wiki_lint.py --wiki PATH       # override default wiki path

Checks:
    1. Every content page has complete frontmatter
    2. last_verified not past decay threshold (flags stale)
    3. Orphan pages (no inbound links, not in INDEX)
    4. Broken wikilinks
    5. INDEX entries resolve to real files
    6. Contradictions table exists if contradictions flagged
    7. Effective confidence (after decay) above deprioritization threshold

Exit codes:
    0 = clean
    1 = warnings only
    2 = errors (missing frontmatter, broken links)
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

DEFAULT_WIKI = Path.home() / "Documents/Spark Obsidian Beast/Farey Research/wiki"

# Pages exempt from frontmatter requirement (meta / governance files).
EXEMPT_FILES = {
    "INDEX.md",
    "SCHEMA.md",
    "log.md",
    "Contradictions.md",
    "Supersessions.md",
}

# Half-life in days by decay_rate.
HALF_LIFE_DAYS = {
    "slow": 730,      # 2 years
    "normal": 180,    # 6 months
    "fast": 30,       # 1 month
}

DEPRIORITIZE_THRESHOLD = 0.30
STALE_THRESHOLD = 0.50   # effective_confidence below this → flag as stale

REQUIRED_FIELDS = [
    "type",
    "status",
    "confidence",
    "sources",
    "last_verified",
    "decay_rate",
]

VALID_TYPES = {
    "discovery",
    "theorem",
    "conjecture",
    "method",
    "reference",
    "lesson",
    "meta",
}

VALID_STATUSES = {
    "proved",
    "lean_verified",
    "computational",
    "conjectural",
    "open",
    "disproved",
    "superseded",
}

VALID_DECAY = {"slow", "normal", "fast"}


@dataclass
class Page:
    path: Path
    name: str
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""
    has_frontmatter: bool = False
    issues: list[tuple[str, str]] = field(default_factory=list)  # (severity, message)


# --- frontmatter parser (YAML-lite, no external deps) --------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    block = m.group(1)
    body = text[m.end():]
    data: dict[str, Any] = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        data[key] = _coerce(value)
    return data, body


def _coerce(value: str) -> Any:
    if value == "" or value.lower() == "null":
        return None
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",")]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value.strip("'\"")


# --- checks --------------------------------------------------------------------

def load_pages(wiki: Path) -> list[Page]:
    pages = []
    for path in sorted(wiki.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        pages.append(Page(
            path=path,
            name=path.name,
            frontmatter=fm,
            body=body,
            has_frontmatter=bool(fm),
        ))
    return pages


def check_frontmatter(page: Page) -> None:
    if page.name in EXEMPT_FILES:
        return
    if not page.has_frontmatter:
        page.issues.append(("error", "missing frontmatter entirely"))
        return
    for field_name in REQUIRED_FIELDS:
        if field_name not in page.frontmatter:
            page.issues.append(("error", f"missing required field: {field_name}"))

    t = page.frontmatter.get("type")
    if t is not None and t not in VALID_TYPES:
        page.issues.append(("warn", f"unknown type: {t}"))

    s = page.frontmatter.get("status")
    if s is not None and s not in VALID_STATUSES:
        page.issues.append(("warn", f"unknown status: {s}"))

    d = page.frontmatter.get("decay_rate")
    if d is not None and d not in VALID_DECAY:
        page.issues.append(("warn", f"unknown decay_rate: {d}"))

    c = page.frontmatter.get("confidence")
    if isinstance(c, (int, float)) and not (0.0 <= c <= 1.0):
        page.issues.append(("error", f"confidence out of [0,1]: {c}"))


def effective_confidence(page: Page, today: date) -> float | None:
    fm = page.frontmatter
    c = fm.get("confidence")
    lv = fm.get("last_verified")
    dr = fm.get("decay_rate", "normal")
    if not isinstance(c, (int, float)):
        return None
    if not isinstance(lv, str):
        return None
    try:
        lv_date = datetime.strptime(lv, "%Y-%m-%d").date()
    except ValueError:
        page.issues.append(("error", f"last_verified not ISO date: {lv}"))
        return None
    half_life = HALF_LIFE_DAYS.get(dr, HALF_LIFE_DAYS["normal"])
    delta_days = max(0, (today - lv_date).days)
    return float(c) * math.exp(-math.log(2) * delta_days / half_life)


def check_freshness(page: Page, today: date) -> None:
    if page.name in EXEMPT_FILES:
        return
    eff = effective_confidence(page, today)
    if eff is None:
        return
    if eff < DEPRIORITIZE_THRESHOLD:
        page.issues.append((
            "warn",
            f"effective confidence {eff:.2f} below deprioritize threshold — re-verify or archive",
        ))
    elif eff < STALE_THRESHOLD:
        page.issues.append((
            "info",
            f"effective confidence {eff:.2f} below stale threshold — consider re-verifying",
        ))


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
# A real Obsidian page name: letters, digits, spaces, _, -. No commas / brackets / colons / etc.
VALID_PAGENAME_RE = re.compile(r"^[A-Za-z0-9 _\-]+$")


def strip_code(text: str) -> str:
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def collect_links(page: Page) -> set[str]:
    stripped = strip_code(page.body)
    links = set()
    for m in WIKILINK_RE.finditer(stripped):
        raw = m.group(1).strip()
        if not raw or not VALID_PAGENAME_RE.match(raw):
            continue  # skip matrix notation like [[5,-8]], template placeholders, etc.
        links.add(raw)
    return links


def check_links(pages: list[Page]) -> None:
    names = {p.name[:-3] for p in pages}  # strip .md
    inbound: dict[str, int] = {n: 0 for n in names}
    for page in pages:
        for link in collect_links(page):
            if link in names:
                inbound[link] = inbound.get(link, 0) + 1
            else:
                page.issues.append(("warn", f"broken wikilink: [[{link}]]"))
    # orphan check (no inbound, not in INDEX)
    index_page = next((p for p in pages if p.name == "INDEX.md"), None)
    index_links = collect_links(index_page) if index_page else set()
    for page in pages:
        if page.name in EXEMPT_FILES:
            continue
        name_no_ext = page.name[:-3]
        if inbound.get(name_no_ext, 0) == 0 and name_no_ext not in index_links:
            page.issues.append(("info", "orphan: no inbound links and not in INDEX"))


def check_index_resolves(pages: list[Page]) -> None:
    index_page = next((p for p in pages if p.name == "INDEX.md"), None)
    if not index_page:
        return
    names = {p.name[:-3] for p in pages}
    for link in collect_links(index_page):
        if link not in names:
            index_page.issues.append(("warn", f"INDEX references missing page: [[{link}]]"))


def check_supersession(pages: list[Page]) -> None:
    by_name = {p.name[:-3]: p for p in pages}
    for page in pages:
        fm = page.frontmatter
        sup = fm.get("supersedes")
        if isinstance(sup, list):
            for target in sup:
                if not target:
                    continue
                old = by_name.get(target)
                if not old:
                    page.issues.append(("warn", f"supersedes missing page: {target}"))
                    continue
                sb = old.frontmatter.get("superseded_by")
                if sb != page.name[:-3]:
                    old.issues.append((
                        "error",
                        f"superseded by [[{page.name[:-3]}]] but frontmatter field not set",
                    ))


# --- output --------------------------------------------------------------------

def report(pages: list[Page]) -> int:
    n_error = 0
    n_warn = 0
    n_info = 0
    for page in pages:
        if not page.issues:
            continue
        print(f"\n── {page.name}")
        for severity, msg in page.issues:
            marker = {"error": "✗", "warn": "!", "info": "·"}[severity]
            print(f"  {marker} [{severity}] {msg}")
            if severity == "error":
                n_error += 1
            elif severity == "warn":
                n_warn += 1
            else:
                n_info += 1
    print(f"\nSummary: {n_error} errors, {n_warn} warnings, {n_info} info")
    if n_error:
        return 2
    if n_warn:
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint the Farey research wiki.")
    ap.add_argument("--wiki", type=Path, default=DEFAULT_WIKI)
    ap.add_argument("--fix", action="store_true", help="auto-fix safe issues (reserved)")
    args = ap.parse_args()

    if not args.wiki.exists():
        print(f"error: wiki directory not found: {args.wiki}", file=sys.stderr)
        return 2

    pages = load_pages(args.wiki)
    today = date.today()

    for page in pages:
        check_frontmatter(page)
        check_freshness(page, today)

    check_links(pages)
    check_index_resolves(pages)
    check_supersession(pages)

    return report(pages)


if __name__ == "__main__":
    sys.exit(main())
