from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any


CORE_SKILLS = (
    "compliance-canary",
    "context-keeper",
    "semantic-diff",
    "wiki-memory",
    "index-first",
    "output-filter",
    "eval-gate",
    "write-gate",
    "impact-of-change",
    "security-oversight",
)


def discover_active_skills(repo_root: Path) -> tuple[str, ...]:
    skills_root = repo_root / "skills"
    names: list[str] = []
    shared = skills_root / "_shared"
    if shared.is_dir():
        names.append("_shared")
    if not skills_root.is_dir():
        return tuple(names)
    for skill_root in sorted(path for path in skills_root.iterdir() if path.is_dir() and path.name != "_shared"):
        entrypoint = skill_root / "SKILL.md"
        if not entrypoint.is_file():
            continue
        header = entrypoint.read_text(encoding="utf-8", errors="replace").split("---", 2)
        frontmatter = header[1] if len(header) >= 3 else ""
        retired = any(
            line.strip().lower() == "retired: true"
            for line in frontmatter.splitlines()
        )
        if not retired:
            names.append(skill_root.name)
    return tuple(names)


def skill_entrypoints(repo_root: Path, names: tuple[str, ...] = CORE_SKILLS) -> dict[str, bool]:
    return {name: (repo_root / "skills" / name / "SKILL.md").is_file() for name in names}


def _test_files(skill_root: Path) -> list[Path]:
    return sorted(
        path
        for path in skill_root.rglob("*.py")
        if path.name.startswith("test_") or path.name.endswith("_test.py")
    )


def _interpreter(repo_root: Path, test_file: Path) -> Path:
    semantic_root = repo_root / "skills" / "semantic-diff"
    if test_file.is_relative_to(semantic_root):
        local_python = semantic_root / "tools" / ".venv" / "bin" / "python"
        if local_python.is_file():
            return local_python
    return Path(sys.executable)


def run_skill_tests(
    repo_root: Path,
    names: tuple[str, ...] = CORE_SKILLS,
    timeout: int = 120,
    fail_fast: bool = False,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for name in names:
        skill_root = repo_root / "skills" / name
        for test_file in _test_files(skill_root):
            python = _interpreter(repo_root, test_file)
            try:
                proc = subprocess.run(
                    [str(python), test_file.name],
                    cwd=test_file.parent,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False,
                    start_new_session=True,
                )
                result = {
                    "skill": name,
                    "test": test_file.relative_to(repo_root).as_posix(),
                    "ok": proc.returncode == 0,
                    "exit_code": proc.returncode,
                }
                if proc.returncode:
                    output = (proc.stderr or proc.stdout).strip()
                    result["output"] = output[-2000:]
            except subprocess.TimeoutExpired:
                result = {
                    "skill": name,
                    "test": test_file.relative_to(repo_root).as_posix(),
                    "ok": False,
                    "error": f"timeout after {timeout}s",
                }
            results.append(result)
            if fail_fast and not result["ok"]:
                break
        if fail_fast and results and not results[-1]["ok"]:
            break
    failed = [result for result in results if not result["ok"]]
    return {
        "ok": not failed,
        "skills": list(names),
        "tests": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "failures": failed,
    }
