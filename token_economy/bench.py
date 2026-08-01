from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

from .code_map import code_map
from .context import checkpoint, meter
from .delegate import classify
from .tokens import estimate_tokens
from .wiki import WikiStore


def _copy_wiki_markdown(source: Path, target: Path) -> None:
    """Copy only durable wiki markdown into an isolated benchmark workspace."""
    for path in WikiStore(source).iter_markdown():
        relative = path.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)


def run_framework_smoke(repo_root: Path, wiki_root: Path | None = None) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    wiki_root = (wiki_root or repo_root / "wiki").resolve()
    code = code_map(repo_root, query="WikiStore context", max_files=3, max_symbols=30)
    route = classify("summarize this wiki note and document the result")
    with tempfile.TemporaryDirectory(prefix="token-economy-bench-") as temp_dir:
        scratch_root = Path(temp_dir)
        scratch_wiki = scratch_root / "wiki"
        _copy_wiki_markdown(wiki_root, scratch_wiki)
        hits = WikiStore(scratch_wiki).search("context refresh", 3)
        packet = checkpoint(scratch_root, goal="framework smoke benchmark", plan="verify core paths")
    sample = "Find context refresh docs, classify delegation, create handoff."
    tasks = [
        {"name": "wiki_query", "ok": isinstance(hits, list), "tokens": estimate_tokens(str(hits))},
        {"name": "code_map", "ok": code["returned_files"] >= 1, "tokens": code["token_estimate"]},
        {"name": "context_refresh", "ok": packet["tokens"] <= 2000, "tokens": packet["tokens"]},
        {"name": "delegation_classification", "ok": route.model_class != "reasoning_top", "tokens": estimate_tokens(str(route.as_dict()))},
        {"name": "code_extraction", "ok": (repo_root / "token_economy/wiki.py").exists(), "tokens": estimate_tokens(sample)},
        {"name": "research_summary", "ok": (repo_root / "prompts/subagents/research-lite.prompt.md").exists(), "tokens": estimate_tokens(sample)},
    ]
    return {
        "suite": "framework-smoke",
        "tasks": tasks,
        "ok": all(t["ok"] for t in tasks),
        "total_estimated_tokens": sum(t["tokens"] for t in tasks),
        "quality_rubric": "smoke only: validates interfaces; does not claim savings",
        "workspace": "isolated-temporary-copy",
        "caller_repo_writes": 0,
    }
